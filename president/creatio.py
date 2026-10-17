"""Ministerium Creationis: a work brought into being by the phrase «созидание».

An author records the work and what appeared that was not there.
The ministry records it when the phrase is that formula and L=J=V=1.
This organ is not the Creator role. The president remains silent.
"""

from __future__ import annotations

from pathlib import Path

from munera import Silentium, _append, _read, president_author
from princip import admissible, principium

NAME = "Министерство Созидания"
NAME_LATIN = "Ministerium Creationis"
PHRASE = "созидание"
PHRASE_LATIN = "creatio"
OPERA = Path(__file__).resolve().parent / "opera.csv"
OPERA_FIELDS = (
    "id", "date", "author", "phrase", "opus", "brings", "L", "J", "V", "decision",
)


def _formula(phrase: str) -> str:
    return " ".join(phrase.strip().casefold().split())


def condere(
    author: str,
    phrase: str,
    opus: str,
    brings: str,
    principle: tuple[int, int, int],
) -> dict[str, str]:
    """Record a work brought into being by the phrase «созидание».

    The supplied assessment belongs to the author; the program does not infer it.
    """
    if president_author(author):
        raise Silentium(
            "Praeses silet. Президент не записывает созидание от своего имени."
        )
    author_n = author.strip()
    phrase_n = _formula(phrase)
    opus_n = opus.strip()
    brings_n = brings.strip()
    if not author_n or not phrase_n or not opus_n or not brings_n:
        raise ValueError(
            "Укажите автора, фразу «созидание», произведение и то, что появилось."
        )
    if phrase_n != PHRASE:
        raise ValueError(
            "Министерство Созидания записывает произведение фразой «созидание»."
        )
    if (
        not isinstance(principle, (tuple, list))
        or len(principle) != 3
        or any(type(value) is not int or value not in (0, 1) for value in principle)
    ):
        raise ValueError("Π должна содержать ровно три целых числа: 0 или 1.")
    L, J, V = principium(*principle)
    if not admissible((L, J, V)):
        raise ValueError("Созидание допустимо только при L=J=V=1.")
    return _append(
        OPERA,
        OPERA_FIELDS,
        {
            "author": author_n,
            "phrase": PHRASE,
            "opus": opus_n,
            "brings": brings_n,
            "L": L,
            "J": J,
            "V": V,
            "decision": "conditum",
        },
    )


def list_opera() -> list[dict[str, str]]:
    """Read recorded works, newest first."""
    rows = _read(OPERA, OPERA_FIELDS)
    rows.reverse()
    return rows
