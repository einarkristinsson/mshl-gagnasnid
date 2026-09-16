#!/usr/bin/env python3
"""saekja_allt.py — sækir ALLAR Sagnagrunns/Ísmús-færslur með GetRecord.

ListRecords hrynur á síðu 2 (PHP fatal, ólokað CDATA), svo við förum
ListIdentifiers -> GetRecord per færslu. Skrifar JSONL: {"id":..,"xml":..}
Endurræsanlegt: sleppir auðkennum sem þegar eru í skránni.
"""
import json, os, queue, re, sys, threading, time, urllib.parse, urllib.request

B = 'https://ismus.is/oai_pmh/'
UA = {'User-Agent': 'MSHL-Sagnatrog harvest (einar@kann.is)'}
HER = os.path.dirname(os.path.abspath(__file__))
UT = os.path.join(HER, 'raw.jsonl')
VILLUR = os.path.join(HER, 'villur.json')
THREADS = 6

def get(p):
    u = B + '?' + urllib.parse.urlencode(p)
    for a in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=90) as r:
                return r.read().decode('utf-8', 'replace')
        except Exception as e:
            if a == 3:
                return 'VILLA: %s' % e
            time.sleep(1.5 * (a + 1))

ids = json.load(open(os.path.join(HER, 'ids.json')))
buid = set()
if os.path.exists(UT):
    for line in open(UT, encoding='utf-8'):
        try:
            buid.add(json.loads(line)['id'])
        except Exception:
            pass
eftir = [i for i in ids if i not in buid]
print('alls %d | þegar sótt %d | eftir %d' % (len(ids), len(buid), len(eftir)), flush=True)

q = queue.Queue()
for i in eftir:
    q.put(i)
las = threading.Lock()
f = open(UT, 'a', encoding='utf-8')
villur = []
n = [0]

def vinna():
    while True:
        try:
            rid = q.get_nowait()
        except queue.Empty:
            return
        d = get({'verb': 'GetRecord', 'metadataPrefix': 'isebel', 'identifier': rid})
        ok = d.lstrip().startswith('<?xml') and '<record>' in d and '<isebel:story' in d
        with las:
            if ok:
                f.write(json.dumps({'id': rid, 'xml': d}, ensure_ascii=False) + '\n')
            else:
                villur.append({'id': rid, 'svar': d[:300]})
            n[0] += 1
            if n[0] % 500 == 0:
                f.flush()
                print('  %d/%d  villur: %d' % (n[0], len(eftir), len(villur)), flush=True)
        time.sleep(0.05)

ths = [threading.Thread(target=vinna) for _ in range(THREADS)]
[t.start() for t in ths]
[t.join() for t in ths]
f.close()
json.dump(villur, open(VILLUR, 'w'), ensure_ascii=False, indent=1)
print('LOKIÐ: sótt %d, villur %d -> %s' % (n[0] - len(villur), len(villur), VILLUR), flush=True)
