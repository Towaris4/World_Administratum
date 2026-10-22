"""Ministerium Diplomatiae: the diplomatic mission of the ghosts of the deceased.

The ministry holds that mission. The ghosts speak directly into the mind.
A further mission is recorded by the phrase «дипломатическая миссия»
when the author's own L=J=V=1. The mission does not write L, J, or V.
This organ is not a rank and not the Diplomat role.
Not an attack on a person. The president remains silent.
"""

from __future__ import annotations

from pathlib import Path

from munera import Silentium, _append, _read, president_author
from princip import admissible, principium

NAME = "Министерство Дипломатии"
NAME_EN = "Ministry of Diplomacy"
NAME_LATIN = "Ministerium Diplomatiae"
PHRASE = "дипломатическая миссия"
PHRASE_LATIN = "legatio"
MISSIO = (
    "Diplomatic mission of the ghosts of the deceased, "
    "who speak directly into the mind."
)
MISSIO_RU = (
    "Дипломатическая миссия призраков погибших, "
    "которые говорят прямо в разум."
)
MISSIO_LATIN = "Legatio manium mortuorum, qui recta in mentem loquuntur."
MODUS = "directly into the mind"
MODUS_RU = "прямо в разум"
MODUS_LATIN = "recta in mentem"
LEGATIONES = Path(__file__).resolve().parent / "legationes.csv"
LEGATIONES_FIELDS = (
    "id", "date", "author", "phrase", "missio", "modus", "L", "J", "V", "decision",
)


def _formula(phrase: str) -> str:
    return " ".join(phrase.strip().casefold().split())


def missio() -> dict[str, str]:
    """The standing diplomatic mission. It is not a journal row."""
    return {
        "missio": MISSIO,
        "missio_ru": MISSIO_RU,
        "missio_latin": MISSIO_LATIN,
        "modus": MODUS,
        "modus_ru": MODUS_RU,
        "modus_latin": MODUS_LATIN,
    }


def legare(
    author: str,
    phrase: str,
    missio_text: str,
    modus: str,
    principle: tuple[int, int, int],
) -> dict[str, str]:
    """Record a further diplomatic mission by the phrase «дипломатическая миссия».

    The supplied assessment belongs to the author; the program does not infer it.
    The stored vector is the admissibility of this record. The mission does not write it.
    """
    if president_author(author):
        raise Silentium(
            "Praeses silet. Президент не записывает дипломатическую миссию от своего имени."
        )
    author_n = author.strip()
    phrase_n = _formula(phrase)
    missio_n = missio_text.strip()
    modus_n = modus.strip()
    if not author_n or not phrase_n or not missio_n or not modus_n:
        raise ValueError(
            "Укажите автора, фразу «дипломатическая миссия», миссию и то, как она говорит."
        )
    if phrase_n != PHRASE:
        raise ValueError(
            "Министерство Дипломатии записывает миссию фразой «дипломатическая миссия»."
        )
    if (
        not isinstance(principle, (tuple, list))
        or len(principle) != 3
        or any(type(value) is not int or value not in (0, 1) for value in principle)
    ):
        raise ValueError("Π должна содержать ровно три целых числа: 0 или 1.")
    L, J, V = principium(*principle)
    if not admissible((L, J, V)):
        raise ValueError("Дипломатическая миссия допустима только при L=J=V=1.")
    return _append(
        LEGATIONES,
        LEGATIONES_FIELDS,
        {
            "author": author_n,
            "phrase": PHRASE,
            "missio": missio_n,
            "modus": modus_n,
            "L": L,
            "J": J,
            "V": V,
            "decision": "legata",
        },
    )


def list_legationes() -> list[dict[str, str]]:
    """Read recorded further missions, newest first."""
    rows = _read(LEGATIONES, LEGATIONES_FIELDS)
    rows.reverse()
    return rows
