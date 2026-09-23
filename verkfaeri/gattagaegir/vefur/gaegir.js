"use strict";
(function () {
  const $ = (s) => document.querySelector(s);
  const form = $("#form");
  const keyra = $("#keyra");
  const haetta = $("#haetta");
  const stada = $("#stada");
  const statustexti = $("#statustexti");
  const banner = $("#banner");
  const samantekt = $("#samantekt");
  const badges = $("#badges");
  const metalina = $("#metalina");
  const nidurstodur = $("#nidurstodur");
  const faerslukafli = $("#faerslukafli");
  const faerslulikami = $("#faerslulikami");
  const faersluspjald = $("#faersluspjald");
  const samantektarkafli = $("#samantektarkafli");
  const samantektartexti = $("#samantektartexti");

  const HOPHEITI = { endapunktur: "Endapunkturinn", faerslur: "Færslurnar",
    hreinlaeti: "Hreinlæti", gildi: "Gildin sjálf" };
  const STADATXT = { stodst: "Stóðst", sleppt: "Sleppt" };
  const ALVTXT = { villa: "Villa", advorun: "Aðvörun", abending: "Ábending" };

  let stjornandi = null;
  let faerslur = [];

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  }

  function hophylki(kenni) {
    let h = document.getElementById("hopur-" + kenni);
    if (!h) {
      h = document.createElement("div");
      h.className = "hopur";
      h.id = "hopur-" + kenni;
      h.innerHTML = "<h2>" + esc(HOPHEITI[kenni] || kenni) + "</h2>";
      nidurstodur.appendChild(h);
    }
    return h;
  }

  function merkitexti(a) {
    if (a.stada === "fell") return ALVTXT[a.alvarleiki] || "Villa";
    return STADATXT[a.stada] || a.stada;
  }
  function merkiklassi(a) {
    if (a.stada === "fell") return "merki fell " + a.alvarleiki;
    return "merki " + a.stada;
  }

  function radaAthugun(a) {
    const h = hophylki(a.hopur);
    const d = document.createElement("details");
    d.className = "rada";
    const gildra = a.gildra && a.stada === "fell"
      ? '<span class="gildra-takn">🔴</span>' : "";
    let smatt = "";
    if (a.tilvik && a.tilvik.length) {
      smatt += '<table><thead><tr><th>Auðkenni</th><th>Reitur</th>' +
        '<th>Gildi</th><th>Skýring</th></tr></thead><tbody>';
      a.tilvik.forEach((t) => {
        smatt += "<tr><td>" + esc(t.audkenni) + "</td><td>" +
          esc(t.reitur) + "</td><td>" + esc(t.gildi) + "</td><td>" +
          esc(t.skyring) + "</td></tr>";
      });
      smatt += "</tbody></table>";
    }
    if (a.lagfaering) {
      smatt += '<div class="lagfaering"><strong>Lagfæring:</strong> ' +
        esc(a.lagfaering) + "</div>";
    }
    if (a.tilvisun) {
      smatt += '<div class="tilvisun"><a href="https://github.com/' +
        'einarkristinsson/mshl-gagnasnid/blob/main/' + esc(a.tilvisun) +
        '" target="_blank" rel="noopener">' + esc(a.tilvisun) + "</a></div>";
    }
    d.innerHTML =
      '<summary><span class="' + merkiklassi(a) + '">' + esc(merkitexti(a)) +
      '</span><span class="radatexti"><div class="radaheiti">' + gildra +
      esc(a.heiti) + ' <small class="radakodi">(' + esc(a.kenni) +
      ")</small></div>" +
      '<div class="radaskilabod">' + esc(a.skilabod) + "</div></span></summary>" +
      (smatt ? '<div class="radasmatt">' + smatt + "</div>" : "");
    h.appendChild(d);
  }

  function synaSamantekt(sk) {
    const s = sk.samantekt || {};
    badges.innerHTML =
      badge("villa", s.villur, "villur") + badge("advorun", s.advaranir,
        "aðvaranir") + badge("abending", s.abendingar, "ábendingar") +
      badge("stodst", s.stodst, "stóðust") + badge("sleppt", s.sleppt,
        "sleppt");
    const y = sk.syni || {};
    const idf = sk.identify || {};
    metalina.innerHTML =
      (idf.repositoryName ? esc(idf.repositoryName) + " · " : "") +
      "n = " + esc(y.faerslur) + " færslur" +
      (y.completeListSize ? " · alls " + esc(y.completeListSize) +
        " í safni" : "") +
      '<span class="beidnimeta"> · ' + esc(y.beidnir) + " beiðnir</span>" +
      " · " + esc(sk.lokid || "");
    samantekt.hidden = false;
  }
  function badge(kl, tala, heiti) {
    return '<span class="badge ' + kl + '">' + (tala || 0) + " " + heiti +
      "</span>";
  }

  function synaFaerslur() {
    if (!faerslur.length) return;
    faerslulikami.innerHTML = "";
    faerslur.forEach((f, i) => {
      const tr = document.createElement("tr");
      const titill = (f.reitir.find((r) => r.nafn === "dc:title") || {}).gildi
        || "—";
      const merkt = f.athugasemdir.length
        ? '<span class="merkitala">' + f.athugasemdir.length + "</span>" : "";
      tr.innerHTML = "<td>" + esc(f.audkenni) + "</td><td>" + esc(titill) +
        "</td><td>" + esc(f.eydd ? "eydd" : "sýni") + "</td><td>" + merkt +
        "</td>";
      tr.addEventListener("click", () => synaSpjald(i));
      faerslulikami.appendChild(tr);
    });
    faerslukafli.hidden = false;
  }

  function synaSpjald(i) {
    const f = faerslur[i];
    const vandi = {};
    f.athugasemdir.forEach((a) => { vandi[a.reitur] = a; });
    let h = "<h3>" + esc(f.audkenni) + "</h3>";
    if (f.athugasemdir.length) {
      h += "<p><strong>Athugasemdir:</strong></p><ul>";
      f.athugasemdir.forEach((a) => {
        h += "<li>" + esc(a.athugun) + " (" + esc(a.alvarleiki) + "): " +
          esc(a.reitur || "") + " — " + esc(a.skilabod || "") + "</li>";
      });
      h += "</ul>";
    }
    h += "<table><thead><tr><th>Reitur</th><th>@lang</th><th>xsi:type</th>" +
      "<th>Gildi</th></tr></thead><tbody>";
    f.reitir.forEach((r) => {
      const kl = vandi[r.nafn] ? ' class="reitur-vandi"' : "";
      h += "<tr" + kl + "><td>" + esc(r.nafn) + "</td><td>" + esc(r.lang) +
        "</td><td>" + esc(r.xsi_type) + "</td><td>" + esc(r.gildi) +
        "</td></tr>";
    });
    h += "</tbody></table>";
    if (f.hratt_xml) {
      h += '<details class="hratt"><summary>Sýna hrátt XML (oai_dc)</summary>' +
        '<p class="smatt">Berðu saman við gullna sniðið hér að ofan.</p>' +
        '<pre class="xmlblokk">' + esc(f.hratt_xml) + "</pre></details>";
    }
    faersluspjald.innerHTML = h;
    faersluspjald.hidden = false;
    faersluspjald.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  let sidastaSkyrsla = null;
  function synaLok(sk) {
    sidastaSkyrsla = sk;
    synaSamantekt(sk);
    synaFaerslur();
    samantektartexti.textContent = sk.texti || "";
    samantektarkafli.hidden = false;
  }

  function hreinsa() {
    nidurstodur.innerHTML = "";
    faerslulikami.innerHTML = "";
    faersluspjald.hidden = true;
    faerslukafli.hidden = true;
    samantekt.hidden = true;
    samantektarkafli.hidden = true;
    banner.hidden = true;
    faerslur = [];
  }

  function medhondla(atburd, taldir) {
    if (atburd.tegund === "beidni") {
      taldir.n++;
      statustexti.textContent = "Í gangi… beiðnir: " + taldir.n +
        (atburd.nafn ? " · " + atburd.nafn : "");
    } else if (atburd.tegund === "athugun") {
      radaAthugun(atburd);
    } else if (atburd.tegund === "faersla") {
      faerslur.push(atburd);
    } else if (atburd.tegund === "villa") {
      banner.textContent = atburd.skilabod;
      banner.hidden = false;
    } else if (atburd.tegund === "lok") {
      synaLok(atburd.skyrsla);
    }
  }

  async function keyraProfun(slod, stillingar) {
    hreinsa();
    keyra.disabled = true;
    haetta.hidden = false;
    stada.hidden = false;
    statustexti.textContent = "Tengist…";
    stjornandi = new AbortController();
    const taldir = { n: 0 };
    try {
      const svar = await fetch("/api/profa", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ slod, stillingar }),
        signal: stjornandi.signal,
      });
      if (!svar.ok) {
        const j = await svar.json().catch(() => ({ villa: "villa" }));
        banner.textContent = "Villa: " + (j.villa || svar.status);
        banner.hidden = false;
        return;
      }
      const lesari = svar.body.getReader();
      const afkodari = new TextDecoder();
      let bidminni = "";
      while (true) {
        const { value, done } = await lesari.read();
        if (done) break;
        bidminni += afkodari.decode(value, { stream: true });
        let skil;
        while ((skil = bidminni.indexOf("\n")) >= 0) {
          const lina = bidminni.slice(0, skil).trim();
          bidminni = bidminni.slice(skil + 1);
          if (lina) medhondla(JSON.parse(lina), taldir);
        }
      }
    } catch (e) {
      if (e.name !== "AbortError") {
        banner.textContent = "Villa: " + e.message;
        banner.hidden = false;
      }
    } finally {
      keyra.disabled = false;
      haetta.hidden = true;
      stada.hidden = true;
      stjornandi = null;
    }
  }

  // ---- Endapunktastjóri: innbyggðir + „Mínar veitur" (localStorage) ----
  // Innbyggði listinn er eina uppspretta þekktra veitna. Slóðir eru teknar
  // orðrétt úr gagnaveitur/*/README.md og verkfaeri/README.md — ekkert er
  // fundið upp. Handrit.is og Ævir skila ekki OAI-PMH og eru óvirk.
  const INNBYGGDIR = [
    { hopur: "Gagnaveitur", nafn: "Sarpur",
      slod: "https://rosetta-icelandsarpur.ciim.zetcom.group/oai",
      sidur: 3, syni: 10, sett: 5, slodaprof: true },
    { hopur: "Gagnaveitur", nafn: "Sögulegt mann- og bæjatal (SMB)",
      slod: "https://smb.mshl.is/oai/",
      sidur: 3, syni: 10, sett: 5, slodaprof: true },
    { hopur: "Gagnaveitur", nafn: "Jarðir og fasteignir",
      slod: "https://jardir.skjalasafn.is/oai/",
      sidur: 3, syni: 10, sett: 5, slodaprof: true },
    { hopur: "Gagnaveitur", nafn: "Ísmús og Sagnagrunnur",
      slod: "https://ismus.is/oai_pmh/",
      sidur: 3, syni: 10, sett: 0, slodaprof: true,
      athugasemd: "Stórt safn og aðeins isebel-snið (engin sett, " +
        "noSetHierarchy). ListRecords fellur á brotnum færslum uppruna " +
        "megin; GetRecord-leiðin er notuð við uppskeru." },
    { hopur: "Gagnaveitur",
      nafn: "Handrit.is — skilar ekki OAI-PMH", ovirkt: true },
    { hopur: "Gagnaveitur",
      nafn: "Ævir lærðra manna — skilar ekki OAI-PMH", ovirkt: true },
    { hopur: "Prófun (hermir)", nafn: "Hermir — heill (prófun)",
      slod: "http://127.0.0.1:8766/god/oai",
      sidur: 3, syni: 10, sett: 5, slodaprof: true },
    { hopur: "Prófun (hermir)", nafn: "Hermir — brotinn (prófun)",
      slod: "http://127.0.0.1:8766/brotin/oai",
      sidur: 3, syni: 10, sett: 5, slodaprof: true },
  ];
  const HOPRAD = ["Gagnaveitur", "Mínar veitur", "Prófun (hermir)"];
  const GEYMSLULYKILL = "gattagaegir.veitur";
  // Opin útgáfa (skýið): hermirinn er á 127.0.0.1 og nær aldrei þangað —
  // /api/heilsa segir til um það og þá er hópurinn ekki sýndur.
  let opin = false;

  const endapunktar = $("#endapunktar");
  const veituath = $("#veituath");
  const fjarlaegjaHnappur = $("#fjarlaegja");
  const stillingaSvid = ["sidur", "syni", "sett"];

  let veitur = [];        // samsettur listi með lykli á hverri veitu
  let valinLykill = "";

  function gildSlod(s) {
    try {
      const u = new URL(String(s || "").trim());
      return u.protocol === "http:" || u.protocol === "https:";
    } catch (e) {
      return false;
    }
  }

  function lesaMinar() {
    try {
      const g = JSON.parse(localStorage.getItem(GEYMSLULYKILL) || "[]");
      return Array.isArray(g) ? g : [];
    } catch (e) {
      return [];
    }
  }
  function vistaMinar(listi) {
    try {
      localStorage.setItem(GEYMSLULYKILL, JSON.stringify(listi));
    } catch (e) { /* localStorage getur verið lokað — hunsa */ }
  }

  function byggjaVeitur() {
    veitur = [];
    INNBYGGDIR.forEach((v, i) => {
      if (opin && v.hopur === "Prófun (hermir)") return;
      veitur.push(Object.assign({ lykill: "innb-" + i, minn: false }, v));
    });
    lesaMinar().forEach((v) => {
      veitur.push(Object.assign({}, v, {
        lykill: "minn-" + v.id, hopur: "Mínar veitur", minn: true,
      }));
    });
  }

  function byggjaVal(velja) {
    byggjaVeitur();
    endapunktar.innerHTML = "";
    const tomt = document.createElement("option");
    tomt.value = "";
    tomt.textContent = "— veldu gagnaveitu —";
    endapunktar.appendChild(tomt);
    HOPRAD.forEach((hopur) => {
      const iHop = veitur.filter((v) => v.hopur === hopur);
      if (!iHop.length) return;
      const grp = document.createElement("optgroup");
      grp.label = hopur;
      iHop.forEach((v) => {
        const o = document.createElement("option");
        o.value = v.ovirkt ? "" : v.lykill;
        o.textContent = v.nafn;
        if (v.ovirkt) o.disabled = true;
        grp.appendChild(o);
      });
      endapunktar.appendChild(grp);
    });
    endapunktar.value = velja || "";
    synaValda();
  }

  function finnaVeitu(lykill) {
    return veitur.find((v) => v.lykill === lykill) || null;
  }

  function setjaStillingar(v) {
    $("#sidur").value = v.sidur != null ? v.sidur : 3;
    $("#syni").value = v.syni != null ? v.syni : 10;
    $("#sett").value = v.sett != null ? v.sett : 5;
    $("#slodaprof").checked = v.slodaprof != null ? !!v.slodaprof : true;
  }

  function synaValda() {
    valinLykill = endapunktar.value;
    const v = finnaVeitu(valinLykill);
    if (v && v.athugasemd) {
      veituath.textContent = v.athugasemd;
      veituath.hidden = false;
    } else {
      veituath.hidden = true;
    }
    fjarlaegjaHnappur.hidden = !(v && v.minn);
  }

  if (endapunktar) {
    endapunktar.addEventListener("change", () => {
      const v = finnaVeitu(endapunktar.value);
      if (v && !v.ovirkt) {
        $("#slod").value = v.slod || "";
        setjaStillingar(v);
        $("#slod").focus();
      }
      synaValda();
    });

    // Breytingar á stillingum meðan „mín" veita er valin -> vista þær.
    function vistaStillingarValinnar() {
      const v = finnaVeitu(valinLykill);
      if (!v || !v.minn) return;
      const minar = lesaMinar();
      const m = minar.find((x) => ("minn-" + x.id) === valinLykill);
      if (!m) return;
      m.sidur = +$("#sidur").value;
      m.syni = +$("#syni").value;
      m.sett = +$("#sett").value;
      m.slodaprof = $("#slodaprof").checked;
      vistaMinar(minar);
    }
    stillingaSvid.forEach((s) =>
      $("#" + s).addEventListener("change", vistaStillingarValinnar));
    $("#slodaprof").addEventListener("change", vistaStillingarValinnar);

    // Bæta við nýrri veitu.
    $("#baeta-vid").addEventListener("click", () => {
      const villa = $("#baeta-villa");
      const nafn = $("#ny-nafn").value.trim();
      const slod = $("#ny-slod").value.trim();
      if (!nafn) {
        villa.textContent = "Nafn vantar.";
        villa.hidden = false;
        return;
      }
      if (!gildSlod(slod)) {
        villa.textContent = "Ógild slóð — verður að byrja á http:// eða https://";
        villa.hidden = false;
        return;
      }
      villa.hidden = true;
      const minar = lesaMinar();
      const id = String(Date.now()) + "-" +
        Math.random().toString(36).slice(2, 7);
      minar.push({
        id: id, nafn: nafn, slod: slod,
        sidur: +$("#ny-sidur").value, syni: +$("#ny-syni").value,
        sett: +$("#ny-sett").value, slodaprof: $("#ny-slodaprof").checked,
        athugasemd: $("#ny-ath").value.trim() || undefined,
      });
      vistaMinar(minar);
      byggjaVal("minn-" + id);
      // beina inn í formið strax
      const v = finnaVeitu("minn-" + id);
      if (v) { $("#slod").value = v.slod; setjaStillingar(v); }
      $("#ny-nafn").value = "";
      $("#ny-slod").value = "";
      $("#ny-ath").value = "";
    });

    // Fjarlægja valda „mína" veitu.
    fjarlaegjaHnappur.addEventListener("click", () => {
      const v = finnaVeitu(valinLykill);
      if (!v || !v.minn) return;
      const minar = lesaMinar().filter((x) => ("minn-" + x.id) !== valinLykill);
      vistaMinar(minar);
      byggjaVal("");
    });

    byggjaVal("");
    fetch("/api/heilsa").then((r) => r.json()).then((h) => {
      if (h && h.opin) { opin = true; byggjaVal(valinLykill); }
    }).catch(() => { /* heilsan er valkvæm */ });
  }

  // ---- Tæknilegar upplýsingar: fela bakvinnslu-atriði sjálfgefið ----
  // Sjálfgefna sýnin er fyrir gagnagjafa: engir innri kóðar, engar
  // beiðnatölur, engar tilvísanaslóðir. Kveikt = fyrir okkur/villuleit.
  const taeknihnappur = $("#taeknistillingar");
  if (taeknihnappur) {
    taeknihnappur.addEventListener("change", () => {
      document.body.classList.toggle("syna-taekni", taeknihnappur.checked);
    });
  }

  // ---- Snið og dæmi: sótt úr /api/snid þegar spjaldið er opnað ----
  const snidbox = $("#snidbox");
  let snidSott = false;
  async function saekjaSnid() {
    const holf = $("#snidgogn");
    holf.innerHTML = '<p class="smatt">Sæki…</p>';
    try {
      const svar = await fetch("/api/snid");
      if (!svar.ok) throw new Error("stada " + svar.status);
      const d = await svar.json();
      let h = "";
      if (d.gullna) {
        h += "<h3>Gullna sniðið — oai_dc <small>(" +
          esc(d.gullna_heimild) + ")</small></h3>";
        h += '<pre class="xmlblokk">' + esc(d.gullna) + "</pre>";
      }
      if (d.daemi && d.daemi.length) {
        h += "<h3>Dæmi um gullnar færslur</h3>";
        d.daemi.forEach((x) => {
          h += "<h4>" + esc(x.titill) + " <small>(" + esc(x.heimild) +
            ")</small></h4>";
          h += '<pre class="xmlblokk">' + esc(x.xml) + "</pre>";
        });
      } else {
        h += '<p class="smatt">Engin sérdæmi enn í snidmat/daemi/.</p>';
      }
      holf.innerHTML = h || '<p class="smatt">Ekkert snið fannst.</p>';
    } catch (e) {
      holf.innerHTML = '<div class="banner">Villa við að sækja snið: ' +
        esc(e.message) + "</div>";
    }
  }
  if (snidbox) {
    snidbox.addEventListener("toggle", () => {
      if (snidbox.open && !snidSott) { snidSott = true; saekjaSnid(); }
    });
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const slod = $("#slod").value.trim();
    if (!slod) return;
    keyraProfun(slod, {
      sidur: +$("#sidur").value, syni: +$("#syni").value,
      sett: +$("#sett").value, slodaprof: $("#slodaprof").checked,
    });
  });

  haetta.addEventListener("click", () => {
    if (stjornandi) stjornandi.abort();
  });

  $("#afrita").addEventListener("click", async () => {
    const t = samantektartexti.textContent;
    try {
      await navigator.clipboard.writeText(t);
      $("#afrita").textContent = "Afritað ✓";
      setTimeout(() => ($("#afrita").textContent = "Afrita samantekt"), 1500);
    } catch (e) {
      const r = document.createRange();
      r.selectNode(samantektartexti);
      window.getSelection().removeAllRanges();
      window.getSelection().addRange(r);
      document.execCommand("copy");
    }
  });

  $("#saekjajson").addEventListener("click", () => {
    if (!sidastaSkyrsla) return;
    const blob = new Blob([JSON.stringify(sidastaSkyrsla, null, 2)],
      { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "gattagaegir-" + (sidastaSkyrsla.kenni || "skyrsla") + ".json";
    a.click();
    URL.revokeObjectURL(a.href);
  });
})();
