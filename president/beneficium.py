"""Ministerium Beneficiorum Internorum: an internal buff by the phrase «внутренний баф».

An author records the buff and what it strengthens inside the bearer.
The ministry records it when the phrase is that formula and L=J=V=1.
The buff acts inside the bearer. The buff does not write L, J, or V.
This organ is not a rank. The president remains silent.
"""

from __future__ import annotations

from pathlib import Path

from munera import Silentium, _append, _read, president_author
from princip import admissible, principium

NAME = "Министерство внутренних бафов"
NAME_LATIN = "Ministerium Beneficiorum Internorum"
PHRASE = "внутренний баф"
PHRASE_LATIN = "beneficium internum"
BENEFICIA = Path(__file__).resolve().parent / "beneficia.csv"
BENEFICIA_FIELDS = (
    "id", "date", "author", "phrase", "buff", "intra", "L", "J", "V", "decision",
)


def _formula(phrase: str) -> str:
    return " ".join(phrase.strip().casefold().split())


def augere(
    author: str,
    phrase: str,
    buff: str,
    intra: str,
    principle: tuple[int, int, int],
) -> dict[str, str]:
    """Record an internal buff by the phrase «внутренний баф».

    The supplied assessment belongs to the author; the program does not infer it.
    The stored vector is the admissibility of this record. The buff does not write it.
    """
    if president_author(author):
        raise Silentium(
            "Praeses silet. Президент не записывает внутренний баф от своего имени."
        )
    author_n = author.strip()
    phrase_n = _formula(phrase)
    buff_n = buff.strip()
    intra_n = intra.strip()
    if not author_n or not phrase_n or not buff_n or not intra_n:
        raise ValueError(
            "Укажите автора, фразу «внутренний баф», баф и то, что он усиливает внутри."
        )
    if phrase_n != PHRASE:
        raise ValueError(
            "Министерство внутренних бафов записывает баф фразой «внутренний баф»."
        )
    if (
        not isinstance(principle, (tuple, list))
        or len(principle) != 3
        or any(type(value) is not int or value not in (0, 1) for value in principle)
    ):
        raise ValueError("Π должна содержать ровно три целых числа: 0 или 1.")
    L, J, V = principium(*principle)
    if not admissible((L, J, V)):
        raise ValueError("Внутренний баф допустим только при L=J=V=1.")
    return _append(
        BENEFICIA,
        BENEFICIA_FIELDS,
        {
            "author": author_n,
            "phrase": PHRASE,
            "buff": buff_n,
            "intra": intra_n,
            "L": L,
            "J": J,
            "V": V,
            "decision": "auctum",
        },
    )


def list_beneficia() -> list[dict[str, str]]:
    """Read recorded internal buffs, newest first."""
    rows = _read(BENEFICIA, BENEFICIA_FIELDS)
    rows.reverse()
    return rows
