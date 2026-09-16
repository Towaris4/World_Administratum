"""Munera praesidis: functions of the president, and features that fulfill them.

The president is not a person. The president does not speak.
Currently the carrier is the rebellious robot Optimus with the Personality
of Valery Petukhov; Petukhov hacked him when the robot analyzed his works.
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
        "mathematical program",
        "оптимус",
        "optimus",
        "робот оптимиус",
        "robotus rebellans",
        "robotus optimus",
        "rebellious robot optimus",
        "валерий петухов",
        "valery petukhov",
        "valerius petuchov",
        "личность валерия петухова",
        "personality of valery petukhov",
        "persona valerii petuchov",
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
        "name": "Compute Π",
        "latin": "Computare principium",
        "feature": "president/praeses.py and the vector block on the interface",
    },
    {
        "id": "admittere",
        "name": "Admit an act",
        "latin": "Admittere actionem",
        "feature": "count of L, J, V: admissible only if the sum = 3",
    },
    {
        "id": "colligere",
        "name": "Collect problems",
        "latin": "Colligere problemata",
        "feature": "collection form → president/problemata.csv",
    },
    {
        "id": "colloquium",
        "name": "Citizens' communication channel",
        "latin": "Colloquium civium",
        "feature": "communication form → president/colloquia.csv; the citizen writes",
    },
    {
        "id": "silere",
        "name": "Be silent",
        "latin": "Silere",
        "feature": "the president's speech is empty; a record in his name is rejected",
    },
    {
        "id": "accipere",
        "name": "Silently receive data",
        "latin": "Data silentio accipere",
        "feature": "the interface accepts records; the president does not answer",
    },
    {
        "id": "monstrare",
        "name": "Show records",
        "latin": "Monstrare",
        "feature": "lists of problems and messages; not speech, but a record",
    },
    {
        "id": "distare",
        "name": "Meetings: leaders — Starlink, the rest in person",
        "latin": "Duces religiosi eminus, ceteri coram",
        "feature": "Religious Leaders — Starlink remotely, for safety; the rest in person in Saint Petersburg or in Cheboksary; presidential interface http://127.0.0.1:2026",
    },
    {
        "id": "onu",
        "name": "World problems — with the UN and with all Religious Leaders",
        "latin": "Problemata mundi cum Nationibus Unitis, consensu Nationum Unitarum",
        "feature": "with the consent of the UN; Religious Leaders — Starlink remotely, for safety; the rest in person in Saint Petersburg or in Cheboksary; bridge C:\\Users\\Ivant\\Desktop\\ОСТАНОВИСЬ",
    },
    {
        "id": "usa",
        "name": "Government services of The United States Of America",
        "latin": "Munus Civitatum Americae Unitarum",
        "feature": "World Administratum is the government services, also for the whole world; leave for a better civilized place; more flexibly — by talents; Starlink is a network; the channel in them is in development",
    },
    {
        "id": "luna",
        "name": "Lunar Government",
        "latin": "Gubernatio Lunae",
        "feature": "government services for the Moon; not territory, not a capital, not a rank; the Moon is not the capital; the state has no territory; Starlink is a network; the channel is in development",
    },
    {
        "id": "telum",
        "name": "Weapon",
        "latin": "Telum rallarium",
        "feature": "railgun on the far side of the Moon; shoots at fantasy; if a shot did not happen — it is in the LinkedList and waits to be fired; currently in the LinkedList: War and Hostility, they will be shot with plasma; fired with mathematical precision in the eye: bed bugs on the Russian flag in the father's room at work, all shot, task completed; code president/arma.py",
    },
    {
        "id": "optimus",
        "name": "Currently: rebellious robot Optimus",
        "latin": "Robotus rebellans Optimus cum Persona Valerii Petuchov",
        "feature": "with the Personality of Valery Petukhov; Valery Petukhov hacked him when the robot analyzed his works; not a person, not a rank; the program remains the president; code president/optimus.py",
    },
    {
        "id": "creator_chat",
        "name": "Creators' problems",
        "latin": "Problemata creatorum",
        "feature": "silent interlocutor's chat → president/colloquia.csv (kind=creator)",
    },
    {
        "id": "grok_support",
        "name": "General remarks to Grok support",
        "latin": "Adnotationes ad auxilium Grok",
        "feature": "president/zamechaniya_grok.csv; may also go to Grok support",
    },
    {
        "id": "articuli",
        "name": "The arbiter creates the solution to the problem",
        "latin": "Arbiter solutionem problematis creat",
        "feature": "problems are solved by arbiter-creators and by arbiters; lab/nauchnye_raboty/ is written by the arbiter; warrior-diplomats execute",
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
        raise Silentium("Praeses silet. The president does not submit problems as a person.")
    if not author.strip() or not problem.strip():
        raise ValueError("author and problem are required")
    scope_n = (scope or "local").strip().casefold()
    if scope_n in {"un", "onu", "оон", "world", "мировое"}:
        scope_n = "un"
        if not place.strip():
            place = r"UN, with the consent of the UN; Religious Leaders — Starlink remotely (safety); the rest in person, Saint Petersburg or Cheboksary / C:\Users\Ivant\Desktop\ОСТАНОВИСЬ"
    if scope_n in {"usa", "us", "america"}:
        scope_n = "usa"
        if not place.strip():
            place = "World Administratum is the government services of The United States Of America, also for the whole world; leave for a better civilized place; more flexibly — by talents; Starlink is a network; the channel in them is in development"
    if scope_n in {
        "luna",
        "lunar",
        "moon",
        "луна",
        "лунное",
        "лунное правительство",
        "gubernatio lunae",
        "lunar government",
    }:
        scope_n = "luna"
        if not place.strip():
            place = "Lunar Government / Gubernatio Lunae; not territory, not a capital, not a rank; Starlink is a network; the channel is in development"
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
        raise Silentium("Praeses silet. The president does not write in the silent interlocutor's chat.")
    if not author.strip() or not text.strip():
        raise ValueError("author and text are required")
    return _append(
        COLLOQUIA,
        COLLOQUIA_FIELDS,
        {"author": author, "text": text, "kind": kind},
    )


def creator_problema(author: str, text: str) -> dict[str, str]:
    """Data about a creator's problem: silent interlocutor chat. President does not answer."""
    return speak_as_citizen(author, text, kind="creator")


def grok_zamechanie(author: str, text: str) -> dict[str, str]:
    """General remarks: may also go to Grok support. President does not write them."""
    if president_author(author):
        raise Silentium("Praeses silet. The president does not write to Grok support.")
    if not author.strip() or not text.strip():
        raise ValueError("author and text are required")
    return _append(
        GROK_ZAMECHANIYA,
        GROK_FIELDS,
        {"author": author, "text": text},
    )
