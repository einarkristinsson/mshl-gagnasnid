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
      esc(a.heiti) + " <small>(" + esc(a.kenni) + ")</small></div>" +
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
    metalina.textContent =
      (idf.repositoryName ? idf.repositoryName + " · " : "") +
      "n = " + y.faerslur + " færslur · " + y.beidnir + " beiðnir" +
      (y.completeListSize ? " · completeListSize " + y.completeListSize : "") +
      " · " + (sk.lokid || "");
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
