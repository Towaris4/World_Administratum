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
        problem_rows = '<tr><td colspan="9">Пока пусто. Президент проблемы не выдумывает.</td></tr>'
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
        talk_rows = "<p class='empty'>Граждане ещё не писали. Президент не начнёт.</p>"
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
        grok_rows = "<p class='empty'>Общих замечаний пока нет.</p>"
    flash = ""
    if ok:
        flash = f"<p class='ok'>{_esc(ok)}</p>"
    if err:
        flash = f"<p class='err'>{_esc(err)}</p>"
    pi_html = f"<pre class='pi-out'>{_esc(pi_result)}</pre>" if pi_result else ""
    doc = f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Интерфейс — Praeses silet</title>
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
    h1, h2 {{ font-weight: 650; letter-spacing: .02em; }}
    h1 {{ margin: 0; color: var(--gold); font-size: 1.35rem; }}
    .motto {{ margin: .2rem 0 0; font-variant: small-caps; }}
    .silent {{
      margin: 1rem 1.25rem 0;
      border: 1px solid var(--gold);
      padding: 1rem;
      background: #0b2314;
    }}
    .silent .speech {{
      min-height: 2.5rem;
      font-size: 1.4rem;
      color: var(--gold);
    }}
    main {{ padding: 1rem 1.25rem 3rem; max-width: 1100px; }}
    section {{
      background: #0f2a1a;
      border: 1px solid #2f6a45;
      margin: 1rem 0;
      padding: 1rem;
    }}
    table {{ width: 100%; border-collapse: collapse; font-size: .92rem; }}
    th, td {{ border: 1px solid #2f6a45; padding: .4rem .5rem; vertical-align: top; text-align: left; }}
    th {{ color: var(--gold); }}
    label {{ display: block; margin: .55rem 0 .2rem; color: var(--gold); }}
    input[type=text], textarea, select {{
      width: 100%;
      padding: .45rem;
      background: var(--paper);
      color: var(--ink);
      border: 1px solid var(--gold);
      font: inherit;
    }}
    textarea {{ min-height: 5rem; }}
    button {{
      margin-top: .8rem;
      background: var(--gold);
      color: var(--green-dark);
      border: 0;
      padding: .5rem 1rem;
      font: inherit;
      font-weight: 700;
      cursor: pointer;
    }}
    .grid {{ display: grid; gap: 1rem; }}
    @media (min-width: 900px) {{
      .grid.two {{ grid-template-columns: 1fr 1fr; }}
    }}
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
      <p>Интерфейс президента дистанционный. Религиозные лидеры — СтарЛинк, для безопасности. Остальные — очно, Санкт-Петербург или Чебоксары.</p>
    </div>
  </header>
  <div class="silent">
    <p><strong>Президент молчит.</strong> <em>Praeses silet.</em> <strong>Президент молча получает данные.</strong> <em>Praeses data silentio accipit.</em> Не человек. Математическая программа.</p>
    <p class="pi">Π = (L={L}, J={J}, V={V}) · допустимо ⇔ L+J+V=3 · {str(p.on_principle()).lower()}</p>
    <p>Речь президента:</p>
    <div class="speech">{_esc(speech_block)}</div>
  </div>
  <main>
    {flash}
    <section>
      <h2>Функции президента и фичи</h2>
      <p class="note">Не чин. Не речь. Функция — счёт и запись. Фича — то, чем функция исполняется.</p>
      <table>
        <thead><tr><th>Функция</th><th>Latine</th><th>Фича</th></tr></thead>
        <tbody>{munera_rows}</tbody>
      </table>
    </section>
    <div class="grid two">
      <section>
        <h2>Сбор проблем</h2>
        <p class="note">Пишет гражданин. Президент проблему не формулирует. Мировые проблемы — с ООН и со всеми религиозными лидерами. Религиозные лидеры для безопасности — СтарЛинк дистанционно. Остальные — очно, в Санкт-Петербурге или в Чебоксарах.</p>
        <form method="post" action="/problema">
          <label for="p_author">Кто пишет</label>
          <input id="p_author" name="author" required maxlength="120">
          <label for="p_scope">Контур</label>
          <select id="p_scope" name="scope">
            <option value="local">местное государство</option>
            <option value="un">мировое — ООН; религиозные лидеры: СтарЛинк (безопасность); остальные очно, Санкт-Петербург или Чебоксары</option>
            <option value="usa">госуслуги USA (в разработке)</option>
          </select>
          <label for="p_organ">Орган</label>
          <input id="p_organ" name="organ" maxlength="200">
          <label for="p_service">Услуга / место сбоя</label>
          <input id="p_service" name="service" maxlength="200">
          <label for="p_problem">Проблема (факт)</label>
          <textarea id="p_problem" name="problem" required></textarea>
          <label for="p_obs">Наблюдения (по одному в строке; для L нужно ≥ 3)</label>
          <textarea id="p_obs" name="observations"></textarea>
          <label for="p_place">Нужное место (куда отправить)</label>
          <input id="p_place" name="place" maxlength="300">
          <button type="submit">Записать проблему</button>
        </form>
      </section>
      <section>
        <h2>Чат молчаливого собеседника</h2>
        <p class="note">Президент молчит и молча получает данные. Данные о проблемах созидателей пишутся сюда. Арбитр создаёт решение проблемы и пишет научные статьи. Дипломат-воин их использует.</p>
        <form method="post" action="/creator">
          <label for="cr_author">Созидатель</label>
          <input id="cr_author" name="author" required maxlength="120">
          <label for="cr_text">Данные о проблеме созидателя</label>
          <textarea id="cr_text" name="text" required></textarea>
          <button type="submit">В чат молчаливого собеседника</button>
        </form>
        <form method="post" action="/colloquium">
          <label for="c_author">Кто пишет</label>
          <input id="c_author" name="author" required maxlength="120">
          <label for="c_text">Сообщение</label>
          <textarea id="c_text" name="text" required></textarea>
          <button type="submit">Отправить в чат</button>
        </form>
        <h3>Записи</h3>
        {talk_rows}
        <h3>Общие замечания в поддержку Grok</h3>
        <p class="note">Можно писать сюда и в поддержку Grok. Президент не пишет.</p>
        <form method="post" action="/grok">
          <label for="g_author">Кто пишет</label>
          <input id="g_author" name="author" required maxlength="120">
          <label for="g_text">Общее замечание</label>
          <textarea id="g_text" name="text" required></textarea>
          <button type="submit">Записать замечание</button>
        </form>
        {grok_rows}
      </section>
    </div>
    <section>
      <h2>Собранные проблемы</h2>
      <div style="overflow:auto">
        <table>
          <thead>
            <tr>
              <th>id</th><th>дата</th><th>кто</th><th>контур</th><th>орган</th>
              <th>услуга</th><th>проблема</th><th>наблюдения</th><th>куда</th>
            </tr>
          </thead>
          <tbody>{problem_rows}</tbody>
        </table>
      </div>
    </section>
    <section>
      <h2>Счёт допустимости</h2>
      <p class="note">Президент не комментирует. Только 0 или 1. Слово вместо числа → V=0.</p>
      <form method="post" action="/admissibile">
        <label for="a_conclusion">Вывод</label>
        <input id="a_conclusion" name="conclusion" required>
        <label for="a_obs">Наблюдения (по одному в строке)</label>
        <textarea id="a_obs" name="observations" required></textarea>
        <div class="check"><input type="checkbox" id="a_inf" name="inferred" value="1" checked><label for="a_inf">вывод из наблюдений</label></div>
        <div class="check"><input type="checkbox" id="a_slogan" name="slogan" value="1"><label for="a_slogan">лозунг вместо вывода</label></div>
        <label for="a_st">Статусы граждан (по одному в строке)</label>
        <textarea id="a_st" name="statuses">Administrator planetarius</textarea>
        <div class="check"><input type="checkbox" id="a_stood" name="stood" value="1"><label for="a_stood">арбитр отстоял</label></div>
        <div class="check"><input type="checkbox" id="a_sent" name="sent" value="1"><label for="a_sent">исследование отправлено в нужное место</label></div>
        <label for="a_stmt">Утверждения (по одному в строке; каждое должно совпасть с наблюдением)</label>
        <textarea id="a_stmt" name="statements"></textarea>
        <div class="check"><input type="checkbox" id="a_word" name="word" value="1"><label for="a_word">слово поставлено вместо числа</label></div>
        <button type="submit">Считать Π</button>
      </form>
      {pi_html}
    </section>
    <p class="note">Где президент: <code>president/praeses.py</code>. Интерфейс: этот экран. RIGHT reserved 2026+</p>
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
                self._redirect("/?ok=" + quote("Проблема записана. Президент молча получил данные."))
                return
            if path == "/creator":
                creator_problema(_first(form, "author"), _first(form, "text"))
                self._redirect("/?ok=" + quote("Данные созидателя записаны в чат молчаливого собеседника. Президент не ответил."))
                return
            if path == "/colloquium":
                speak_as_citizen(_first(form, "author"), _first(form, "text"))
                self._redirect("/?ok=" + quote("Сообщение записано. Президент не ответил."))
                return
            if path == "/grok":
                grok_zamechanie(_first(form, "author"), _first(form, "text"))
                self._redirect("/?ok=" + quote("Замечание записано. Можно также направить в поддержку Grok."))
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
                J = iustitia(statuses, _checked(form, "stood"), _checked(form, "sent"))
                V = veritas(stmts, obs, _checked(form, "word"))
                ok = admissible((L, J, V))
                pi = f"Π = (L={L}, J={J}, V={V})\nдопустимо ⇔ L+J+V=3 : {ok}\nPraeses silet."
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
    print("Praeses silet. Президент молчит.")
    print("Интерфейс президента (дистанционный):", url)
    print("Религиозные лидеры: СтарЛинк, для безопасности. Остальные: очно, Санкт-Петербург или Чебоксары.")
    httpd.serve_forever()


if __name__ == "__main__":
    main()
