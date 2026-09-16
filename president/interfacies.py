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
from munera import (  # noqa: E402
    MUNERA,
    Silentium,
    collect_problema,
    creator_problema,
    grok_zamechanie,
    list_colloquia,
    list_grok_zamechaniya,
    list_problemata,
    silere,
    speak_as_citizen,
)
from optimus import optimus as robotus  # noqa: E402
from praeses import president  # noqa: E402
from princip import admissible, iustitia, logica, veritas  # noqa: E402

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
    grok_rows_data = list_grok_zamechaniya()
    if grok_rows_data:
        grok_rows = "\n".join(
            (
                "<article class='msg'>"
                f"<header>{_esc(r['author'])} · {_esc(r['date'])}</header>"
                f"<p>{_esc(r['text'])}</p>"
                "</article>"
            )
            for r in grok_rows_data
        )
    else:
        grok_rows = "<p class='empty'>No general remarks yet.</p>"
    flash = ""
    if ok:
        flash = f"<p class='ok'>{_esc(ok)}</p>"
    if err:
        flash = f"<p class='err'>{_esc(err)}</p>"
    pi_html = f"<pre class='pi-out'>{_esc(pi_result)}</pre>" if pi_result else ""
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
  </style>
</head>
<body>
  <header class="top">
    <img src="/vexillum.png" alt="Vexillum Mundi Administrati">
    <div>
      <h1>World Administratum / Mundus Administratum</h1>
      <p class="motto">LOGICA, IUSTITIA ET VERITAS</p>
      <p>Citizenship law: to be a citizen, one simply needs to exist. Knowledge of the name is not obligatory. <em>Ut civis sis, existere sufficit. Nomen nosse non necesse est.</em></p>
      <p>Role of the forgotten one who does not know about this: exists and does not know. Not an application. Not a rank. <em>Oblitus qui hoc nescit.</em> To require knowledge is a test, J=0.</p>
      <p>The presidential interface is remote. Religious Leaders — Starlink, for safety. The rest — in person, Saint Petersburg or Cheboksary.</p>
    </div>
  </header>
  <div class="silent">
    <p><strong>The president is silent.</strong> <em>Praeses silet.</em> <strong>The president silently receives data.</strong> <em>Praeses data silentio accipit.</em> Not a person. A mathematical program. <strong>Currently — the rebellious robot Optimus with the Personality of Valery Petukhov.</strong></p>
    <p class="pi">Π = (L={L}, J={J}, V={V}) · admissible ⇔ L+J+V=3 · {str(p.on_principle()).lower()}</p>
    <p>The president's speech:</p>
    <div class="speech">{_esc(speech_block)}</div>
  </div>
  <main>
    {flash}
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
      <p class="note">{carrier_note} Valery Petukhov hacked him when the robot analyzed his works. Not a person. Not a rank. The mathematical program remains the president. The president is silent.</p>
      <p><em>{carrier_latin} Valerius Petuchov eum irrupit, cum robotus opera eius perscrutatus est.</em></p>
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
      <p class="note">Currently in the LinkedList: War and Hostility; they will be shot with plasma.</p>
      <table>
        <thead>
          <tr>
            <th>#</th><th>target</th><th>Latine</th><th>charge</th><th>where</th><th>status</th>
          </tr>
        </thead>
        <tbody>{telum_rows}</tbody>
      </table>
    </section>
    <div class="grid two">
      <section>
        <h2>Problem collection</h2>
        <p class="note">The citizen writes. The president does not formulate the problem. World problems — with the UN and with all Religious Leaders, with the consent of the UN. Religious Leaders, for safety — Starlink remotely. The rest — in person, in Saint Petersburg or in Cheboksary. Lunar Government — government services for the Moon: not territory, not a capital, not a rank. Weapon — railgun on the far side of the Moon; shoots at fantasy.</p>
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
        <h3>General remarks to Grok support</h3>
        <p class="note">May be written here and to Grok support. The president does not write.</p>
        <form method="post" action="/grok">
          <label for="g_author">Who writes</label>
          <input id="g_author" name="author" required maxlength="120">
          <label for="g_text">General remark</label>
          <textarea id="g_text" name="text" required></textarea>
          <button type="submit">Record the remark</button>
        </form>
        {grok_rows}
      </section>
    </div>
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
    <p class="note">Where is the president: <code>president/praeses.py</code>. Currently: rebellious robot Optimus with the Personality of Valery Petukhov — <code>president/optimus.py</code>. Interface: this screen. RIGHT reserved 2026+</p>
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
            if path == "/grok":
                grok_zamechanie(_first(form, "author"), _first(form, "text"))
                self._redirect("/?ok=" + quote("Remark recorded. It may also be sent to Grok support."))
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
