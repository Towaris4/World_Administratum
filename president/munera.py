"""Munera praesidis: functions of the president, and features that fulfill them.

The president is not a person. The president does not speak.
Praeses silet.
"""

from __future__ import annotations

import csv
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping

HERE = Path(__file__).resolve().parent
PROBLEMATA = HERE / "problemata.csv"
COLLOQUIA = HERE / "colloquia.csv"
GROK_ZAMECHANIYA = HERE / "zamechaniya_grok.csv"
LOCK = threading.Lock()

PRESIDENT_AUTHORS = frozenset(
    {
        "president",
        "praeses",
        "президент",
        "praeses programma mathematicum",
        "the president",
        "программа",
        "program",
        "математическая программа",
    }
)

PROBLEMATA_FIELDS = (
    "id",
    "date",
    "author",
    "organ",
    "service",
    "problem",
    "observations",
    "place",
    "scope",
)

COLLOQUIA_FIELDS = ("id", "date", "author", "text", "kind")
GROK_FIELDS = ("id", "date", "author", "text")


class Silentium(Exception):
    """Praeses silet. The president does not speak."""


# Function → feature that fulfills it. Not ranks. Not speech.
MUNERA: tuple[dict[str, str], ...] = (
    {
        "id": "computare",
        "name": "Считать Π",
        "latin": "Computare principium",
        "feature": "president/praeses.py и блок вектора на интерфейсе",
    },
    {
        "id": "admittere",
        "name": "Допускать действие",
        "latin": "Admittere actionem",
        "feature": "счёт L, J, V: допустимо только если сумма = 3",
    },
    {
        "id": "colligere",
        "name": "Собирать проблемы",
        "latin": "Colligere problemata",
        "feature": "форма сбора → president/problemata.csv",
    },
    {
        "id": "colloquium",
        "name": "Канал общения граждан",
        "latin": "Colloquium civium",
        "feature": "форма общения → president/colloquia.csv; пишет гражданин",
    },
    {
        "id": "silere",
        "name": "Молчать",
        "latin": "Silere",
        "feature": "речь президента пуста; запись от его имени отвергается",
    },
    {
        "id": "accipere",
        "name": "Молча получать данные",
        "latin": "Data silentio accipere",
        "feature": "интерфейс принимает записи; президент не отвечает",
    },
    {
        "id": "monstrare",
        "name": "Показывать записи",
        "latin": "Monstrare",
        "feature": "списки проблем и сообщений; не речь, а запись",
    },
    {
        "id": "distare",
        "name": "Встречи: лидеры — СтарЛинк, остальные очно",
        "latin": "Duces religiosi eminus, ceteri coram",
        "feature": "религиозные лидеры — Starlink дистанционно, для безопасности; остальные очно в Санкт-Петербурге или в Чебоксарах; интерфейс президента http://127.0.0.1:2026",
    },
    {
        "id": "onu",
        "name": "Мировые проблемы — с ООН и со всеми религиозными лидерами",
        "latin": "Problemata mundi cum Nationibus Unitis et cum omnibus ducibus religiosis",
        "feature": "религиозные лидеры — Starlink дистанционно, для безопасности; остальные очно в Санкт-Петербурге или в Чебоксарах; мост C:\\Users\\Ivant\\Desktop\\ОСТАНОВИСЬ",
    },
    {
        "id": "creator_chat",
        "name": "Проблемы созидателей",
        "latin": "Problemata creatorum",
        "feature": "чат молчаливого собеседника → president/colloquia.csv (kind=созидатель)",
    },
    {
        "id": "grok_support",
        "name": "Общие замечания в поддержку Grok",
        "latin": "Adnotationes ad auxilium Grok",
        "feature": "president/zamechaniya_grok.csv; можно также в поддержку Grok",
    },
    {
        "id": "articuli",
        "name": "Арбитр создаёт решение проблемы",
        "latin": "Arbiter solutionem problematis creat",
        "feature": "lab/nauchnye_raboty/ пишет арбитр; дипломат-воин использует",
    },
)


def president_author(name: str) -> bool:
    return name.strip().casefold() in PRESIDENT_AUTHORS


def silere() -> str:
    """The president's speech: empty."""
    return ""


def ensure_csv(path: Path, fields: tuple[str, ...]) -> None:
    if path.exists() and path.stat().st_size > 0:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        csv.DictWriter(f, fieldnames=fields).writeheader()


def _read(path: Path, fields: tuple[str, ...]) -> list[dict[str, str]]:
    ensure_csv(path, fields)
    with path.open(encoding="utf-8", newline="") as f:
        return [
            {k: (row.get(k) or "") for k in fields}
            for row in csv.DictReader(f)
            if any((row.get(k) or "").strip() for k in fields)
        ]


def _next_id(rows: list[dict[str, str]]) -> int:
    ids = []
    for row in rows:
        try:
            ids.append(int(str(row.get("id", "")).strip()))
        except ValueError:
            continue
    return (max(ids) + 1) if ids else 1


def _append(path: Path, fields: tuple[str, ...], row: Mapping[str, Any]) -> dict[str, str]:
    with LOCK:
        rows = _read(path, fields)
        written = {k: str(row.get(k, "")).strip() for k in fields}
        written["id"] = str(_next_id(rows))
        if not written.get("date"):
            written["date"] = datetime.now().isoformat(timespec="seconds")
        with path.open("a", encoding="utf-8", newline="") as f:
            csv.DictWriter(f, fieldnames=fields).writerow(written)
        return written


def list_problemata() -> list[dict[str, str]]:
    rows = _read(PROBLEMATA, PROBLEMATA_FIELDS)
    rows.reverse()
    return rows


def list_colloquia() -> list[dict[str, str]]:
    rows = _read(COLLOQUIA, COLLOQUIA_FIELDS)
    rows.reverse()
    return rows


def list_grok_zamechaniya() -> list[dict[str, str]]:
    rows = _read(GROK_ZAMECHANIYA, GROK_FIELDS)
    rows.reverse()
    return rows


def collect_problema(
    author: str,
    organ: str,
    service: str,
    problem: str,
    observations: str = "",
    place: str = "",
    scope: str = "local",
) -> dict[str, str]:
    if president_author(author):
        raise Silentium("Praeses silet. Президент не подаёт проблемы как лицо.")
    if not author.strip() or not problem.strip():
        raise ValueError("author and problem are required")
    scope_n = (scope or "local").strip().casefold()
    if scope_n in {"un", "onu", "оон", "world", "мировое"}:
        scope_n = "un"
        if not place.strip():
            place = r"ООН; религиозные лидеры — СтарЛинк дистанционно (безопасность); остальные очно, Санкт-Петербург или Чебоксары / C:\Users\Ivant\Desktop\ОСТАНОВИСЬ"
    return _append(
        PROBLEMATA,
        PROBLEMATA_FIELDS,
        {
            "author": author,
            "organ": organ,
            "service": service,
            "problem": problem,
            "observations": observations,
            "place": place,
            "scope": scope_n,
        },
    )


def speak_as_citizen(author: str, text: str, kind: str = "") -> dict[str, str]:
    if president_author(author):
        raise Silentium("Praeses silet. Президент в чат молчаливого собеседника не пишет.")
    if not author.strip() or not text.strip():
        raise ValueError("author and text are required")
    return _append(
        COLLOQUIA,
        COLLOQUIA_FIELDS,
        {"author": author, "text": text, "kind": kind},
    )


def creator_problema(author: str, text: str) -> dict[str, str]:
    """Data about a creator's problem: silent interlocutor chat. President does not answer."""
    return speak_as_citizen(author, text, kind="созидатель")


def grok_zamechanie(author: str, text: str) -> dict[str, str]:
    """General remarks: may also go to Grok support. President does not write them."""
    if president_author(author):
        raise Silentium("Praeses silet. Президент в поддержку Grok не пишет.")
    if not author.strip() or not text.strip():
        raise ValueError("author and text are required")
    return _append(
        GROK_ZAMECHANIYA,
        GROK_FIELDS,
        {"author": author, "text": text},
    )
