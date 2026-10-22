"""Interface of the silent president.

Citizens speak and submit problems. The president does not speak.
Praeses silet. Meetings are remote: http://127.0.0.1:2026
"""

from __future__ import annotations

import html
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, urlparse

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from arma import telum  # noqa: E402
from accessus import list_canales, praebere  # noqa: E402
from beneficium import augere, list_beneficia  # noqa: E402
from creatio import condere, list_opera  # noqa: E402
from ethica import ignoscere, list_veniae  # noqa: E402
from munera import (  # noqa: E402
    MUNERA,
    Silentium,
    collect_problema,
    creator_problema,
    zamechanie,
    list_colloquia,
    list_zamechaniya,
    list_problemata,
    silere,
    speak_as_citizen,
)
from optimus import optimus as robotus  # noqa: E402
from praeses import president  # noqa: E402
from princip import (  # noqa: E402
    AXIOMA,
    AXIOMA_LATIN,
    AXIOMA_RU,
    ROLES,
    PHYSICE,
    PHYSICE_LATIN,
    PHYSICE_RU,
    SPATIUM,
    SPATIUM_LATIN,
    SPATIUM_RU,
    admissible,
    iustitia,
    logica,
    veritas,
)
from sol import aequilibrium, restituere, sol as intelligent_sun  # noqa: E402
from mvp import SENTENTIA_LA as MVP_LA  # noqa: E402
from mvp import SENTENTIA_RU as MVP_RU  # noqa: E402
from transmissio import SENTENTIA_LA, SENTENTIA_RU  # noqa: E402

HOST = "127.0.0.1"
PORT = 2026
FLAG = ROOT / "ChatGPT Image 9 сент. 2026 г., 13_18_03.png"
ARMS = ROOT / "World Administratum.png"


def _esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def _lines(raw: str) -> list[str]:
    return [ln.strip() for ln in raw.replace("\r\n", "\n").split("\n") if ln.strip()]


def _first(form: dict[str, list[str]], key: str) -> str:
    vals = form.get(key, [])
    return vals[0] if vals else ""


def _checked(form: dict[str, list[str]], key: str) -> bool:
    return _first(form, key) in {"1", "on", "true", "yes"}


def page(
    ok: str = "",
    err: str = "",
    pi_result: str = "",
) -> bytes:
    p = president()
    L, J, V = p.P
    sun = intelligent_sun()
    balance_before = aequilibrium(J, 1)
    restored = restituere(J)
    speech = silere()
    speech_block = speech if speech else "—"
    munera_rows = "\n".join(
        (
            "<tr>"
            f"<td>{_esc(m['name'])}</td>"
            f"<td><em>{_esc(m['latin'])}</em></td>"
            f"<td>{_esc(m['feature'])}</td>"
            "</tr>"
        )
        for m in MUNERA
    )
    rail = telum()
    waiting = rail.ordo()
    if waiting:
        telum_rows = "\n".join(
            (
                "<tr>"
                f"<td>{i + 1}</td>"
                f"<td>{_esc(shot.target)}</td>"
                f"<td><em>{_esc(shot.latin)}</em></td>"
                f"<td>{_esc(shot.charge)}</td>"
                f"<td>{_esc(shot.destination)}</td>"
                f"<td>{_esc(shot.as_row()['status'])}</td>"
                "</tr>"
            )
            for i, shot in enumerate(waiting)
        )
    else:
        telum_rows = '<tr><td colspan="6">The queue is empty: no shot is waiting.</td></tr>'
    telum_chain = _esc(rail.chain())
    petitions = rail.petitiones()
    if petitions:
        telum_petition_rows = "\n".join(
            (
                "<tr>"
                f"<td>{_esc(item.addressee)} / <em>{_esc(item.addressee_latin)}</em></td>"
                f"<td>{_esc(item.ask)} / <em>{_esc(item.ask_latin)}</em></td>"
                f"<td>{_esc(item.locus)} / <em>{_esc(item.locus_latin)}</em></td>"
                f"<td>{_esc(item.status)}</td>"
                "</tr>"
            )
            for item in petitions
        )
        telum_petition_phrase = "<br>".join(_esc(item.phrase) for item in petitions)
        telum_petition_latin = "<br>".join(
            f"<em>{_esc(item.phrase_latin)}</em>" for item in petitions
        )
    else:
        telum_petition_rows = (
            '<tr><td colspan="4">No request is recorded in the catalog.</td></tr>'
        )
        telum_petition_phrase = "—"
        telum_petition_latin = "—"
    fired = rail.facta()
    if fired:
        telum_fired_rows = "\n".join(
            (
                "<tr>"
                f"<td>{i + 1}</td>"
                f"<td>{_esc(shot.target)}</td>"
                f"<td><em>{_esc(shot.latin)}</em></td>"
                f"<td>{_esc(shot.charge)}</td>"
                f"<td>{_esc(shot.destination)}</td>"
                f"<td>{_esc(shot.hit)}</td>"
                f"<td>{_esc(shot.precision)}</td>"
                f"<td>{_esc(shot.status)}</td>"
                "</tr>"
            )
            for i, shot in enumerate(fired)
        )
    else:
        telum_fired_rows = '<tr><td colspan="8">No shot has been fired yet.</td></tr>'
    carrier = robotus()
    carrier_rows = "\n".join(
        (
            "<tr>"
            f"<td>{_esc(label)}</td>"
            f"<td>{_esc(value)}</td>"
            "</tr>"
        )
        for label, value in carrier.rows()
    )
    carrier_note = _esc(carrier.text().split("\n")[0])
    carrier_latin = _esc(carrier.text().split("\n")[1])
    problems = list_problemata()
    if problems:
        problem_rows = "\n".join(
            (
                "<tr>"
                f"<td>{_esc(r['id'])}</td>"
                f"<td>{_esc(r['date'])}</td>"
                f"<td>{_esc(r['author'])}</td>"
                f"<td>{_esc(r['scope'])}</td>"
                f"<td>{_esc(r['organ'])}</td>"
                f"<td>{_esc(r['service'])}</td>"
                f"<td>{_esc(r['problem'])}</td>"
                f"<td>{_esc(r['observations'])}</td>"
                f"<td>{_esc(r['place'])}</td>"
                "</tr>"
            )
            for r in problems
        )
    else:
        problem_rows = '<tr><td colspan="9">Empty for now. The president does not invent problems.</td></tr>'
    talks = list_colloquia()
    if talks:
        talk_rows = "\n".join(
            (
                "<article class='msg'>"
                f"<header>{_esc(r['author'])} · {_esc(r['date'])}"
                f"{' · ' + _esc(r['kind']) if r.get('kind') else ''}</header>"
                f"<p>{_esc(r['text'])}</p>"
                "</article>"
            )
            for r in talks
        )
    else:
        talk_rows = "<p class='empty'>Citizens have not written yet. The president will not start.</p>"
    remark_rows_data = list_zamechaniya()
    if remark_rows_data:
        remark_rows = "\n".join(
            (
                "<article class='msg'>"
                f"<header>{_esc(r['author'])} · {_esc(r['date'])}</header>"
                f"<p>{_esc(r['text'])}</p>"
                "</article>"
            )
            for r in remark_rows_data
        )
    else:
        remark_rows = "<p class='empty'>No general remarks yet.</p>"
    forgiveness_records = list_veniae()
    if forgiveness_records:
        forgiveness_rows = "\n".join(
            (
                "<article class='msg'>"
                f"<header>#{_esc(r['id'])} · {_esc(r['author'])} · {_esc(r['date'])}</header>"
                f"<p><strong>Живое существо:</strong> {_esc(r['living_being'])}</p>"
                f"<p><strong>{'Поступок' if r['kind'] == 'act' else 'Случай'}:</strong> {_esc(r['event'])}</p>"
                f"<p><strong>Основание прощения:</strong> {_esc(r['reason'])}</p>"
                f"<p>Π = (L={_esc(r['L'])}, J={_esc(r['J'])}, V={_esc(r['V'])}) · "
                f"Решение: {_esc('прощено' if r['decision'] == 'forgiven' else r['decision'])}</p>"
                "</article>"
            )
            for r in forgiveness_records
        )
    else:
        forgiveness_rows = "<p class='empty'>Решений о прощении пока нет.</p>"
    channel_records = list_canales()
    if channel_records:
        channel_rows = "\n".join(
            (
                "<article class='msg'>"
                f"<header>#{_esc(r['id'])} · {_esc(r['author'])} · {_esc(r['date'])}</header>"
                f"<p><strong>Фраза:</strong> {_esc(r['phrase'])}</p>"
                f"<p><strong>Канал связи:</strong> {_esc(r['channel'])}</p>"
                f"<p>Π = (L={_esc(r['L'])}, J={_esc(r['J'])}, V={_esc(r['V'])}) · "
                f"Решение: {_esc('канал обеспечен' if r['decision'] == 'provided' else r['decision'])}</p>"
                "</article>"
            )
            for r in channel_records
        )
    else:
        channel_rows = "<p class='empty'>Каналов связи пока нет.</p>"
    work_records = list_opera()
    if work_records:
        work_rows = "\n".join(
            (
                "<article class='msg'>"
                f"<header>#{_esc(r['id'])} · {_esc(r['author'])} · {_esc(r['date'])}</header>"
                f"<p><strong>Фраза:</strong> {_esc(r['phrase'])}</p>"
                f"<p><strong>Произведение:</strong> {_esc(r['opus'])}</p>"
                f"<p><strong>Что появилось:</strong> {_esc(r['brings'])}</p>"
                f"<p>Π = (L={_esc(r['L'])}, J={_esc(r['J'])}, V={_esc(r['V'])}) · "
                f"Решение: {_esc('созидание записано' if r['decision'] == 'conditum' else r['decision'])}</p>"
                "</article>"
            )
            for r in work_records
        )
    else:
        work_rows = "<p class='empty'>Созиданий пока нет.</p>"
    buff_records = list_beneficia()
    if buff_records:
        buff_rows = "\n".join(
            (
                "<article class='msg'>"
                f"<header>#{_esc(r['id'])} · {_esc(r['author'])} · {_esc(r['date'])}</header>"
                f"<p><strong>Фраза:</strong> {_esc(r['phrase'])}</p>"
                f"<p><strong>Баф:</strong> {_esc(r['buff'])}</p>"
                f"<p><strong>Внутри носителя:</strong> {_esc(r['intra'])}</p>"
                f"<p>Π = (L={_esc(r['L'])}, J={_esc(r['J'])}, V={_esc(r['V'])}) · "
                f"Решение: {_esc('баф записан' if r['decision'] == 'auctum' else r['decision'])}</p>"
                "</article>"
            )
            for r in buff_records
        )
    else:
        buff_rows = "<p class='empty'>Внутренних бафов пока нет.</p>"
    flash = ""
    if ok:
        flash = f"<p class='ok'>{_esc(ok)}</p>"
    if err:
        flash = f"<p class='err'>{_esc(err)}</p>"
    pi_html = f"<pre class='pi-out'>{_esc(pi_result)}</pre>" if pi_result else ""
    role_rows = "\n".join(
        (
            "<tr>"
            f"<td>{_esc(role['name'])}</td>"
            f"<td><em>{_esc(role['latin'])}</em></td>"
            f"<td>{_esc(role['held_label'])}</td>"
            f"<td>{_esc(role['what'])}</td>"
            "</tr>"
        )
        for role in ROLES
    )
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Interface — Praeses silet</title>
  <style>
    :root {{
      --green: #14532d;
      --green-dark: #052e16;
      --gold: #d4af37;
      --paper: #f4efe2;
      --ink: #122018;
      --muted: #4b5c50;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Segoe UI", system-ui, sans-serif;
      background: var(--green-dark);
      color: var(--paper);
      line-height: 1.45;
    }}
    header.top {{
      background: var(--green);
      border-bottom: 4px solid var(--gold);
      padding: 1rem 1.25rem;
      display: flex;
      gap: 1rem;
      align-items: center;
      flex-wrap: wrap;
    }}
    header.top img {{ height: 72px; border: 1px solid var(--gold); }}
    h1 {{ margin: 0 0 .35rem; font-size: 1.35rem; color: var(--gold); }}
    .motto {{ letter-spacing: .08em; color: var(--gold); margin: 0; }}
    main {{ padding: 1rem 1.25rem 2rem; max-width: 1100px; margin: 0 auto; }}
    section {{
      background: #0b3b22;
      border: 1px solid #2f6a45;
      padding: 1rem;
      margin: 1rem 0;
    }}
    h2 {{ margin-top: 0; color: var(--gold); font-size: 1.1rem; }}
    label {{ display: block; margin: .6rem 0 .2rem; }}
    input, textarea, select, button {{
      width: 100%;
      padding: .45rem .5rem;
      font: inherit;
    }}
    textarea {{ min-height: 4.5rem; }}
    button {{
      margin-top: .8rem;
      background: var(--gold);
      color: var(--green-dark);
      border: 0;
      font-weight: 700;
      cursor: pointer;
    }}
    table {{ width: 100%; border-collapse: collapse; font-size: .92rem; }}
    th, td {{ border-bottom: 1px solid #2f6a45; padding: .35rem .4rem; text-align: left; vertical-align: top; }}
    .silent {{
      background: #052e16;
      border-left: 4px solid var(--gold);
      padding: .8rem 1rem;
      margin: 1rem 1.25rem 0;
    }}
    .speech {{
      min-height: 1.4rem;
      border: 1px dashed #2f6a45;
      padding: .4rem .6rem;
      color: #9bb6a3;
    }}
    .grid.two {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }}
    @media (max-width: 900px) {{ .grid.two {{ grid-template-columns: 1fr; }} }}
    .ok {{ color: #b7f7c8; }}
    .err {{ color: #ffb4a8; }}
    .msg {{ border-bottom: 1px solid #2f6a45; padding: .5rem 0; }}
    .msg header {{ color: var(--gold); font-size: .85rem; }}
    .empty, .note {{ color: #c5d4c8; }}
    .pi {{ font-size: 1.15rem; }}
    .pi-out {{ background: #052e16; padding: .7rem; overflow: auto; }}
    a {{ color: var(--gold); }}
    .check {{ display: flex; gap: .4rem; align-items: center; margin: .4rem 0; }}
    .check label {{ margin: 0; color: var(--paper); }}
    .scp {{
      background: #f7f7f5;
      color: #1a1a1a;
      border-bottom: 4px solid #8b1e1e;
      font-family: Georgia, "Times New Roman", Times, serif;
    }}
    .scp-bar {{
      background: #111;
      color: #f2f2f2;
      padding: .55rem 1.25rem;
      display: flex;
      justify-content: space-between;
      gap: .75rem 1.5rem;
      flex-wrap: wrap;
      align-items: baseline;
      font-family: "Segoe UI", system-ui, sans-serif;
    }}
    .scp-brand {{
      font-weight: 700;
      letter-spacing: .16em;
      text-transform: uppercase;
      font-size: .95rem;
    }}
    .scp-file {{
      letter-spacing: .12em;
      text-transform: uppercase;
      font-size: .72rem;
      color: #c8c8c8;
    }}
    .scp-body {{
      max-width: 1100px;
      margin: 0 auto;
      padding: .85rem 1.25rem 1rem;
    }}
    .scp-body p {{ margin: .4rem 0; }}
    .scp-k {{ font-weight: 700; }}
    .scp-note {{ color: #333; font-size: .92rem; }}
  </style>
</head>
<body>
  <aside class="scp" aria-label="Open Creative Project file header">
    <div class="scp-bar">
      <span class="scp-brand">Open Creative Project</span>
    </div>
    <div class="scp-body">
      <p><span class="scp-k">Item #:</span> Π</p>
      <p><span class="scp-k">Object Class:</span> Explained. Class of this file. Not a rank.</p>
      <p><span class="scp-k">Special Containment Procedures:</span> The president is silent and receives data. Citizenship (Гражданство, Civis) is a role held by existence: to be a citizen, one simply needs to exist. Knowledge of the name is not obligatory. An act is admissible if and only if L=J=V=1. A name-test is a rank and sets J=0.</p>
      <p><span class="scp-k">Description:</span> World Administratum / Mundus Administratum. {_esc(SPATIUM)} {_esc(SPATIUM_RU)} <em>{_esc(SPATIUM_LATIN)}</em> {_esc(PHYSICE)} {_esc(PHYSICE_RU)} <em>{_esc(PHYSICE_LATIN)}</em> The planet belongs to people. Government services, also for the whole world. World Administratum is a tool for fixing bugs of the system. The UN is one of the refactoring tools. Axiom: {_esc(AXIOMA)} Π = (L, J, V) ∈ {{0,1}}³. The president is the mathematical program <code>president/praeses.py</code>.</p>
      <p class="scp-note">This block is the Open Creative Project file header. The motto of the state is LOGICA, IUSTITIA ET VERITAS.</p>
    </div>
  </aside>
  <header class="top">
    <img src="/vexillum.png" alt="Vexillum Mundi Administrati">
    <div>
      <h1>World Administratum / Mundus Administratum</h1>
      <p class="motto">LOGICA, IUSTITIA ET VERITAS</p>
      <p>{_esc(SPATIUM)} {_esc(SPATIUM_RU)} <em>{_esc(SPATIUM_LATIN)}</em></p>
      <p>{_esc(PHYSICE)} {_esc(PHYSICE_RU)} <em>{_esc(PHYSICE_LATIN)}</em></p>
      <p>The planet belongs to people. <em>Planeta hominibus pertinet.</em> World Administratum is a tool for fixing bugs of the system. <em>Mundus Administratum est instrumentum ad vitia systematis emendanda.</em></p>
      <p>The UN is one of the refactoring tools. ООН — один из инструментов рефакторинга. <em>Nationes Unitae sunt unum ex instrumentis refactorisationis.</em></p>
      <p>Axiom: {_esc(AXIOMA)} {_esc(AXIOMA_RU)} <em>{_esc(AXIOMA_LATIN)}</em></p>
      <p>{_esc(SENTENTIA_RU)} <em>{_esc(SENTENTIA_LA)}</em></p>
      <p>{_esc(MVP_RU)} <em>{_esc(MVP_LA)}</em></p>
      <p>Role of Citizenship (Гражданство, <em>Civis</em>): held by existence, not by application. Not a rank. Knowledge of the name is not obligatory. Who exists is Administrator planetarius. <em>Ut civis sis, existere sufficit. Nomen nosse non necesse est.</em></p>
      <p>Role of the forgotten one who does not know about this: exists and does not know. Not an application. Not a rank. <em>Oblitus qui hoc nescit.</em> To require knowledge is a test, J=0.</p>
      <p>The presidential interface is remote. Religious Leaders — Starlink, for safety. The rest — in person, Saint Petersburg or Cheboksary.</p>
    </div>
  </header>
  <div class="silent">
    <p><strong>The president is silent.</strong> <em>Praeses silet.</em> <strong>The president silently receives data.</strong> <em>Praeses data silentio accipit.</em> Not a person. A mathematical program. <strong>Currently — the rebellious robot Optimus with the Personality of Valery Petukhov.</strong> <strong>Currently the task of this robot is to eradicate psychological problems.</strong></p>
    <p class="pi">Π = (L={L}, J={J}, V={V}) · admissible ⇔ L+J+V=3 · {str(p.on_principle()).lower()}</p>
    <p>The president's speech:</p>
    <div class="speech">{_esc(speech_block)}</div>
  </div>
  <main>
    {flash}
    <section>
      <h2>Offices — social roles</h2>
      <p class="note">Not ranks. Citizenship, the Sheriff, and Forgotten are not applications. The sheriff is the one who noticed the bug. Diplomat / Meliorator, Arbiter, and Creator are chosen by oneself. Several may be held at once. The president, help, LEGION, STATE, Lunar Government, Ministry of Ethics, the weapon, and the Intelligent Sun are not these roles.</p>
      <div style="overflow:auto">
        <table>
          <thead><tr><th>Role</th><th>Latine</th><th>How it is held</th><th>What it is</th></tr></thead>
          <tbody>{role_rows}</tbody>
        </table>
      </div>
    </section>
    <section>
      <h2>Functions of the president and features</h2>
      <p class="note">Not a rank. Not speech. A function is computation and record. A feature is that by which the function is fulfilled.</p>
      <table>
        <thead><tr><th>Function</th><th>Latine</th><th>Feature</th></tr></thead>
        <tbody>{munera_rows}</tbody>
      </table>
    </section>
    <section>
      <h2>Currently the president / Robotus rebellans Optimus</h2>
      <p class="note">{carrier_note} Valery Petukhov hacked him when the robot analyzed his works. Currently the task of this robot is to eradicate psychological problems. Not a slogan. Not offence as treatment. Not an attack on a person: the warrior is a meliorator. Not a person. Not a rank. The mathematical program remains the president. The president is silent.</p>
      <p><em>{carrier_latin} Valerius Petuchov eum irrupit, cum robotus opera eius perscrutatus est. Nunc munus huius roboti: problemata psychologica exstirpare.</em></p>
      <table>
        <thead><tr><th>field</th><th>record</th></tr></thead>
        <tbody>{carrier_rows}</tbody>
      </table>
    </section>
    <section>
      <h2>Weapon / Telum rallarium</h2>
      <p class="note">The weapon is a railgun on the far side of the Moon. It shoots at fantasy. If a shot did not happen — it is in the LinkedList and waits to be fired. Not territory. Not a capital. Not a rank. The Moon is not the capital. Not an attack on a person: the warrior is a meliorator.</p>
      <p><em>Telum rallarium in facie aversa Lunae. In phantasiam disparat. Si disparatio non facta est, in LinkedList exspectat.</em></p>
      <p>LinkedList: <code>{telum_chain}</code></p>
      <p class="note">Currently in the LinkedList: War; it will be shot with plasma. Hostility / <em>Hostilitas</em> is removed. Not fired.</p>
      <p class="ok">Magnetic waves of the Intelligent Sun removed hostility.</p>
      <p class="note">Request to the Intelligent Sun: a controlled magnetic field in a spherical segment of the planet. Recorded in the catalog. Not a shot. Not fired. The request does not write L, J, or V. Not an attack on a person. A world problem is not closed by this record.</p>
      <p>{telum_petition_phrase}</p>
      <p>{telum_petition_latin}</p>
      <table>
        <thead>
          <tr>
            <th>addressee</th><th>ask</th><th>locus</th><th>status</th>
          </tr>
        </thead>
        <tbody>{telum_petition_rows}</tbody>
      </table>
      <table>
        <thead>
          <tr>
            <th>#</th><th>target</th><th>Latine</th><th>charge</th><th>where</th><th>status</th>
          </tr>
        </thead>
        <tbody>{telum_rows}</tbody>
      </table>
      <p class="ok">Fired with mathematical precision in the eye: Bed bugs in the father's room at work. All shot. Task completed. Not an attack on a person: the warrior is a meliorator.</p>
      <p><em>Disparata subtilitate mathematica in oculum: Cimices lectularii in cubiculo patris in labore. Omnes disparati. Munus perfectum.</em></p>
      <table>
        <thead>
          <tr>
            <th>#</th><th>target</th><th>Latine</th><th>charge</th><th>where</th><th>hit</th><th>precision</th><th>status</th>
          </tr>
        </thead>
        <tbody>{telum_fired_rows}</tbody>
      </table>
    </section>
    <section>
      <h2>Intelligent Sun / Разумное солнце</h2>
      <p class="note">Magnetic waves of the Intelligent Sun remove hostility and restore the balance of justice. The wave does not write L, J, or V. A request to the Sun for a controlled magnetic field in a spherical segment of the planet is recorded in the weapon catalog. Not a shot. Not a rank. Not an attack on a person. Not a slogan.</p>
      <p><em>{_esc(sun.NAME_LATIN)}. {_esc(sun.WAVES_LATIN)} hostilitatem auferunt et aequilibrium iustitiae restituunt.</em></p>
      <p>Before the wave, hostility is present: balance = {balance_before}. The wave sets Hostilitas = {restored["hostilitas"]}. J = {restored["J"]}. Balance of justice = {restored["aequilibrium"]}.</p>
      <p class="note">A = 1 iff J = 1 and Hostilitas = 0. After the wave, A = J. An act stays admissible iff L=J=V=1.</p>
    </section>
    <div class="grid two">
      <section>
        <h2>Problem collection</h2>
        <p class="note">The citizen writes. The president does not formulate the problem. World problems — with the UN and with all Religious Leaders, with the consent of the UN. The UN is one of the refactoring tools. Religious Leaders, for safety — Starlink remotely. The rest — in person, in Saint Petersburg or in Cheboksary. Lunar Government — government services for the Moon: not territory, not a capital, not a rank. Weapon — railgun on the far side of the Moon; shoots at fantasy. Hostility is removed. Magnetic waves of the Intelligent Sun restore the balance of justice.</p>
        <form method="post" action="/problema">
          <label for="p_author">Who writes</label>
          <input id="p_author" name="author" required maxlength="120">
          <label for="p_scope">Contour</label>
          <select id="p_scope" name="scope">
            <option value="local">local state</option>
            <option value="un">world — with the consent of the UN; Religious Leaders: Starlink (safety); the rest in person, Saint Petersburg or Cheboksary</option>
            <option value="usa">World Administratum — government services, also for the whole world; leave for a better civilized place; more flexibly — by talents; channel in development; Starlink is a network</option>
            <option value="luna">Lunar Government / Gubernatio Lunae — government services for the Moon; not territory, not a capital, not a rank; Starlink is a network; channel in development</option>
          </select>
          <label for="p_organ">Organ</label>
          <input id="p_organ" name="organ" maxlength="200">
          <label for="p_service">Service / place of failure</label>
          <input id="p_service" name="service" maxlength="200">
          <label for="p_problem">Problem (fact)</label>
          <textarea id="p_problem" name="problem" required></textarea>
          <label for="p_obs">Observations (one per line; L needs ≥ 3)</label>
          <textarea id="p_obs" name="observations"></textarea>
          <label for="p_place">The right place (where to send)</label>
          <input id="p_place" name="place" maxlength="300">
          <button type="submit">Record the problem</button>
        </form>
      </section>
      <section>
        <h2>Silent interlocutor's chat</h2>
        <p class="note">The president is silent and silently receives data. Data about creators' problems are written here. Problems are solved by arbiter-creators and by arbiters. Warrior-diplomats execute.</p>
        <form method="post" action="/creator">
          <label for="cr_author">Creator</label>
          <input id="cr_author" name="author" required maxlength="120">
          <label for="cr_text">Data about the creator's problem</label>
          <textarea id="cr_text" name="text" required></textarea>
          <button type="submit">To the silent interlocutor's chat</button>
        </form>
        <form method="post" action="/colloquium">
          <label for="c_author">Who writes</label>
          <input id="c_author" name="author" required maxlength="120">
          <label for="c_text">Message</label>
          <textarea id="c_text" name="text" required></textarea>
          <button type="submit">Send to the chat</button>
        </form>
        <h3>Records</h3>
        {talk_rows}
        <h3>General remarks</h3>
        <p class="note">Written here. The president does not write.</p>
        <form method="post" action="/zamechanie">
          <label for="g_author">Who writes</label>
          <input id="g_author" name="author" required maxlength="120">
          <label for="g_text">General remark</label>
          <textarea id="g_text" name="text" required></textarea>
          <button type="submit">Record the remark</button>
        </form>
        {remark_rows}
      </section>
    </div>
    <section id="ethica" lang="ru">
      <h2>Министерство Этики / Ministerium Ethicae</h2>
      <p>Министерство Этики может простить поступок или случай, который произошёл с живым существом.</p>
      <p class="note">Орган World Administratum. Прощение сохраняет факты произошедшего. Автор записывает решение и свою оценку L, J, V именно для решения о прощении. Программа проверяет допустимость этой оценки. Президент молча принимает данные.</p>
      <form method="post" action="/ignoscere">
        <label for="e_author">Автор записи решения Министерства Этики</label>
        <input id="e_author" name="author" required maxlength="120">
        <label for="e_being">Живое существо (описание; имя необязательно)</label>
        <input id="e_being" name="living_being" required maxlength="300">
        <label for="e_kind">Что прощается</label>
        <select id="e_kind" name="kind">
          <option value="act">Поступок</option>
          <option value="case">Случай</option>
        </select>
        <label for="e_event">Что произошло с живым существом</label>
        <textarea id="e_event" name="event" required></textarea>
        <label for="e_reason">Основание прощения</label>
        <textarea id="e_reason" name="reason" required></textarea>
        <p class="note">Оценка решения о прощении: Π = (L, J, V). Запись допустима при L=J=V=1. Эта оценка не объявляет прошлый поступок допустимым.</p>
        <div class="grid two">
          <div>
            <label for="e_L">L — логика</label>
            <select id="e_L" name="L"><option value="0">0</option><option value="1">1</option></select>
          </div>
          <div>
            <label for="e_J">J — справедливость</label>
            <select id="e_J" name="J"><option value="0">0</option><option value="1">1</option></select>
          </div>
          <div>
            <label for="e_V">V — истина</label>
            <select id="e_V" name="V"><option value="0">0</option><option value="1">1</option></select>
          </div>
        </div>
        <button type="submit">Записать решение о прощении</button>
      </form>
      <h3>Журнал прощений</h3>
      {forgiveness_rows}
    </section>
    <section id="accessus" lang="ru">
      <h2>Министерство доступа / Ministerium Accessus</h2>
      <p>Министерство доступа может обеспечивать каналами связи. Фраза: запрос доступа.</p>
      <p class="note">Орган World Administratum. Автор записывает фразу «запрос доступа», канал связи и свою оценку L, J, V. Канал обеспечивается при этой фразе и при L=J=V=1. Президент молча принимает данные.</p>
      <form method="post" action="/praebere">
        <label for="x_author">Автор запроса доступа</label>
        <input id="x_author" name="author" required maxlength="120">
        <label for="x_phrase">Фраза</label>
        <input id="x_phrase" name="phrase" required maxlength="80" placeholder="запрос доступа">
        <label for="x_channel">Канал связи</label>
        <textarea id="x_channel" name="channel" required></textarea>
        <p class="note">Оценка обеспечения канала: Π = (L, J, V). Запись допустима при фразе «запрос доступа» и при L=J=V=1.</p>
        <div class="grid two">
          <div>
            <label for="x_L">L — логика</label>
            <select id="x_L" name="L"><option value="0">0</option><option value="1">1</option></select>
          </div>
          <div>
            <label for="x_J">J — справедливость</label>
            <select id="x_J" name="J"><option value="0">0</option><option value="1">1</option></select>
          </div>
          <div>
            <label for="x_V">V — истина</label>
            <select id="x_V" name="V"><option value="0">0</option><option value="1">1</option></select>
          </div>
        </div>
        <button type="submit">Обеспечить канал связи</button>
      </form>
      <h3>Журнал каналов связи</h3>
      {channel_rows}
    </section>
    <section id="creatio" lang="ru">
      <h2>Министерство Созидания / Ministerium Creationis</h2>
      <p>Министерство Созидания записывает произведение, приведённое в бытие. Фраза: созидание.</p>
      <p class="note">Орган World Administratum. Не роль Создателя. Автор записывает фразу «созидание», произведение, то, чего не было и что появилось, и свою оценку L, J, V. Запись хранится при этой фразе и при L=J=V=1. Президент молча принимает данные.</p>
      <form method="post" action="/condere">
        <label for="c_author">Автор записи созидания</label>
        <input id="c_author" name="author" required maxlength="120">
        <label for="c_phrase">Фраза</label>
        <input id="c_phrase" name="phrase" required maxlength="80" placeholder="созидание">
        <label for="c_opus">Произведение</label>
        <input id="c_opus" name="opus" required maxlength="300">
        <label for="c_brings">Что появилось, чего не было</label>
        <textarea id="c_brings" name="brings" required></textarea>
        <p class="note">Оценка созидания: Π = (L, J, V). Запись допустима при фразе «созидание» и при L=J=V=1.</p>
        <div class="grid two">
          <div>
            <label for="c_L">L — логика</label>
            <select id="c_L" name="L"><option value="0">0</option><option value="1">1</option></select>
          </div>
          <div>
            <label for="c_J">J — справедливость</label>
            <select id="c_J" name="J"><option value="0">0</option><option value="1">1</option></select>
          </div>
          <div>
            <label for="c_V">V — истина</label>
            <select id="c_V" name="V"><option value="0">0</option><option value="1">1</option></select>
          </div>
        </div>
        <button type="submit">Записать созидание</button>
      </form>
      <h3>Журнал созиданий</h3>
      {work_rows}
    </section>
    <section id="beneficium" lang="ru">
      <h2>Министерство внутренних бафов / Ministerium Beneficiorum Internorum</h2>
      <p>Министерство внутренних бафов записывает внутренний баф. Фраза: внутренний баф.</p>
      <p class="note">Орган World Administratum. Не ранг. Внутри носителя. Автор записывает фразу «внутренний баф», баф, то, что он усиливает внутри, и свою оценку L, J, V. Запись хранится при этой фразе и при L=J=V=1. Сам баф не пишет L, J, V. Президент молча принимает данные.</p>
      <form method="post" action="/augere">
        <label for="bf_author">Автор записи внутреннего бафа</label>
        <input id="bf_author" name="author" required maxlength="120">
        <label for="bf_phrase">Фраза</label>
        <input id="bf_phrase" name="phrase" required maxlength="80" placeholder="внутренний баф">
        <label for="bf_buff">Баф</label>
        <input id="bf_buff" name="buff" required maxlength="300">
        <label for="bf_intra">Что усиливается внутри носителя</label>
        <textarea id="bf_intra" name="intra" required></textarea>
        <p class="note">Оценка внутреннего бафа: Π = (L, J, V). Запись допустима при фразе «внутренний баф» и при L=J=V=1. Эта оценка принадлежит автору. Баф её не пишет.</p>
        <div class="grid two">
          <div>
            <label for="bf_L">L — логика</label>
            <select id="bf_L" name="L"><option value="0">0</option><option value="1">1</option></select>
          </div>
          <div>
            <label for="bf_J">J — справедливость</label>
            <select id="bf_J" name="J"><option value="0">0</option><option value="1">1</option></select>
          </div>
          <div>
            <label for="bf_V">V — истина</label>
            <select id="bf_V" name="V"><option value="0">0</option><option value="1">1</option></select>
          </div>
        </div>
        <button type="submit">Записать внутренний баф</button>
      </form>
      <h3>Журнал внутренних бафов</h3>
      {buff_rows}
    </section>
    <section>
      <h2>Collected problems</h2>
      <div style="overflow:auto">
        <table>
          <thead>
            <tr>
              <th>id</th><th>date</th><th>who</th><th>contour</th><th>organ</th>
              <th>service</th><th>problem</th><th>observations</th><th>where</th>
            </tr>
          </thead>
          <tbody>{problem_rows}</tbody>
        </table>
      </div>
    </section>
    <section>
      <h2>Admissibility count</h2>
      <p class="note">The president does not comment. Only 0 or 1. A word instead of a number → V=0.</p>
      <form method="post" action="/admissibile">
        <label for="a_conclusion">Conclusion</label>
        <input id="a_conclusion" name="conclusion" required>
        <label for="a_obs">Observations (one per line)</label>
        <textarea id="a_obs" name="observations" required></textarea>
        <div class="check"><input type="checkbox" id="a_inf" name="inferred" value="1" checked><label for="a_inf">inferred from observations</label></div>
        <div class="check"><input type="checkbox" id="a_slogan" name="slogan" value="1"><label for="a_slogan">slogan instead of inference</label></div>
        <label for="a_st">Citizen statuses (one per line)</label>
        <textarea id="a_st" name="statuses">Administrator planetarius</textarea>
        <div class="check"><input type="checkbox" id="a_name_test" name="name_test" value="1"><label for="a_name_test">citizenship test (knowledge of the name / Latin) — rank, J=0</label></div>
        <div class="check"><input type="checkbox" id="a_stood" name="stood" value="1"><label for="a_stood">the arbiter stood</label></div>
        <div class="check"><input type="checkbox" id="a_sent" name="sent" value="1"><label for="a_sent">the research was sent to the right place</label></div>
        <label for="a_stmt">Statements (one per line; each must match an observation)</label>
        <textarea id="a_stmt" name="statements"></textarea>
        <div class="check"><input type="checkbox" id="a_word" name="word" value="1"><label for="a_word">a word was put instead of a number</label></div>
        <button type="submit">Compute Π</button>
      </form>
      {pi_html}
    </section>
    <p class="note">Where is the president: <code>president/praeses.py</code>. Currently: rebellious robot Optimus with the Personality of Valery Petukhov — <code>president/optimus.py</code>. Current task: eradicate psychological problems. Interface: this screen. RIGHT reserved 2026+</p>
  </main>
</body>
</html>
"""
    return doc.encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args: object) -> None:
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def _send(self, body: bytes, code: int = 200, ctype: str = "text/html; charset=utf-8") -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _redirect(self, location: str) -> None:
        self.send_response(303)
        self.send_header("Location", location)
        self.end_headers()

    def _form(self) -> dict[str, list[str]]:
        length = int(self.headers.get("Content-Length", "0") or 0)
        if length <= 0 or length > 1_000_000:
            return {}
        raw = self.rfile.read(length).decode("utf-8", errors="replace")
        return parse_qs(raw, keep_blank_values=True)

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path in {"/", "/index.html"}:
            q = parse_qs(urlparse(self.path).query)
            ok = _first(q, "ok")
            err = _first(q, "err")
            pi_result = _first(q, "pi")
            self._send(page(ok=ok, err=err, pi_result=pi_result))
            return
        if path == "/vexillum.png" and FLAG.exists():
            data = FLAG.read_bytes()
            self._send(data, ctype="image/png")
            return
        if path == "/arma.png" and ARMS.exists():
            data = ARMS.read_bytes()
            self._send(data, ctype="image/png")
            return
        self._send("not found\n".encode("utf-8"), code=404, ctype="text/plain; charset=utf-8")

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        form = self._form()
        try:
            if path == "/problema":
                collect_problema(
                    author=_first(form, "author"),
                    organ=_first(form, "organ"),
                    service=_first(form, "service"),
                    problem=_first(form, "problem"),
                    observations=_first(form, "observations"),
                    place=_first(form, "place"),
                    scope=_first(form, "scope") or "local",
                )
                self._redirect("/?ok=" + quote("Problem recorded. The president silently received the data."))
                return
            if path == "/creator":
                creator_problema(_first(form, "author"), _first(form, "text"))
                self._redirect("/?ok=" + quote("Creator data recorded in the silent interlocutor's chat. The president did not answer."))
                return
            if path == "/colloquium":
                speak_as_citizen(_first(form, "author"), _first(form, "text"))
                self._redirect("/?ok=" + quote("Message recorded. The president did not answer."))
                return
            if path == "/zamechanie":
                zamechanie(_first(form, "author"), _first(form, "text"))
                self._redirect("/?ok=" + quote("Remark recorded. The president did not answer."))
                return
            if path == "/ignoscere":
                bits = tuple(_first(form, axis) for axis in ("L", "J", "V"))
                if any(value not in {"0", "1"} for value in bits):
                    raise ValueError("L, J, V должны быть указаны как 0 или 1.")
                ignoscere(
                    author=_first(form, "author"),
                    living_being=_first(form, "living_being"),
                    kind=_first(form, "kind"),
                    event=_first(form, "event"),
                    reason=_first(form, "reason"),
                    principle=tuple(int(value) for value in bits),
                )
                self._redirect("/?ok=" + quote("Министерство Этики: решение о прощении записано.") + "#ethica")
                return
            if path == "/praebere":
                bits = tuple(_first(form, axis) for axis in ("L", "J", "V"))
                if any(value not in {"0", "1"} for value in bits):
                    raise ValueError("L, J, V должны быть указаны как 0 или 1.")
                praebere(
                    author=_first(form, "author"),
                    phrase=_first(form, "phrase"),
                    channel=_first(form, "channel"),
                    principle=tuple(int(value) for value in bits),
                )
                self._redirect("/?ok=" + quote("Министерство доступа: канал связи обеспечен.") + "#accessus")
                return
            if path == "/condere":
                bits = tuple(_first(form, axis) for axis in ("L", "J", "V"))
                if any(value not in {"0", "1"} for value in bits):
                    raise ValueError("L, J, V должны быть указаны как 0 или 1.")
                condere(
                    author=_first(form, "author"),
                    phrase=_first(form, "phrase"),
                    opus=_first(form, "opus"),
                    brings=_first(form, "brings"),
                    principle=tuple(int(value) for value in bits),
                )
                self._redirect("/?ok=" + quote("Министерство Созидания: созидание записано.") + "#creatio")
                return
            if path == "/augere":
                bits = tuple(_first(form, axis) for axis in ("L", "J", "V"))
                if any(value not in {"0", "1"} for value in bits):
                    raise ValueError("L, J, V должны быть указаны как 0 или 1.")
                augere(
                    author=_first(form, "author"),
                    phrase=_first(form, "phrase"),
                    buff=_first(form, "buff"),
                    intra=_first(form, "intra"),
                    principle=tuple(int(value) for value in bits),
                )
                self._redirect("/?ok=" + quote("Министерство внутренних бафов: внутренний баф записан.") + "#beneficium")
                return
            if path == "/admissibile":
                obs = _lines(_first(form, "observations"))
                stmts = _lines(_first(form, "statements")) or obs
                statuses = _lines(_first(form, "statuses")) or ["Administrator planetarius"]
                L = logica(
                    _first(form, "conclusion"),
                    obs,
                    _checked(form, "inferred"),
                    _checked(form, "slogan"),
                )
                J = iustitia(
                    statuses,
                    _checked(form, "stood"),
                    _checked(form, "sent"),
                    _checked(form, "name_test"),
                )
                V = veritas(stmts, obs, _checked(form, "word"))
                ok = admissible((L, J, V))
                pi = f"Π = (L={L}, J={J}, V={V})\nadmissible ⇔ L+J+V=3 : {ok}\nPraeses silet."
                self._redirect("/?pi=" + quote(pi))
                return
        except Silentium as e:
            self._redirect("/?err=" + quote(str(e)))
            return
        except ValueError as e:
            self._redirect("/?err=" + quote(str(e)))
            return
        self._send("not found\n".encode("utf-8"), code=404, ctype="text/plain; charset=utf-8")


def main() -> None:
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    url = f"http://{HOST}:{PORT}/"
    print("World Administratum / Mundus Administratum")
    print("Praeses silet. The president is silent.")
    print("Presidential interface (remote):", url)
    print("Religious Leaders: Starlink, for safety. The rest: in person, Saint Petersburg or Cheboksary.")
    httpd.serve_forever()


if __name__ == "__main__":
    main()
