#!/usr/bin/env python3
"""Telur efnisorð Ísmús með auðkennum — hráefni í þýðingartöfluna."""
import json, re, collections, sys
telja = collections.Counter(); audk = {}; lang = {}
for line in open('raw.jsonl', encoding='utf-8'):
    d = json.loads(line)
    for m in re.finditer(r'<isebel:keyword\s+id="([^"]*)"([^>]*)>([^<]*)</isebel:keyword>', d['xml']):
        i, at, t = m.group(1), m.group(2), m.group(3).strip()
        if not t:
            continue
        l = re.search(r'xml:lang="([^"]*)"', at)
        telja[t] += 1
        audk[t] = i
        lang[t] = l.group(1) if l else '—'
print('ólík efnisorð:', len(telja), '| tilvik:', sum(telja.values()))
kum = 0; alls = sum(telja.values())
with open('efnisord-hrat.tsv', 'w', encoding='utf-8') as f:
    f.write('#id\tlang\tfjoldi\thlutfall_uppsafnad\tordid\n')
    for t, c in telja.most_common():
        kum += c
        f.write('%s\t%s\t%d\t%.1f\t%s\n' % (audk[t], lang[t], c, 100*kum/alls, t))
for n in (50, 100, 150, 200, 300, 400):
    k = sum(c for _, c in telja.most_common(n))
    print('  efstu %3d orð þekja %.1f %% tilvika' % (n, 100*k/alls))
