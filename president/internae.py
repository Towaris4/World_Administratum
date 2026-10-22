"""Ministerium Rerum Internarum: a request by the phrase «запрос».

An author records the request. The ministry records it when the phrase is
that formula and L=J=V=1. The request does not transfer the named things.
The request does not write L, J, or V. This organ is not a rank.
The president remains silent.

The journal stores the words of the petition. It does not store a quantity,
a form, or a method.
"""

from __future__ import annotations

from pathlib import Path

from munera import Silentium, _append, _read, president_author
from princip import admissible, principium

NAME = "Министерство внутренних дел"
NAME_LATIN = "Ministerium Rerum Internarum"
PHRASE = "запрос"
PHRASE_LATIN = "petitio"
PETITIONES = Path(__file__).resolve().parent / "internae.csv"
PETITIONES_FIELDS = (
    "id", "date", "author", "phrase", "petitio", "L", "J", "V", "decision",
)


def _formula(phrase: str) -> str:
    return " ".join(phrase.strip().casefold().split())


def scribere(
    author: str,
    phrase: str,
    petitio: str,
    principle: tuple[int, int, int],
) -> dict[str, str]:
    """Record a request by the phrase «запрос».

    The supplied assessment belongs to the author; the program does not infer it.
    The stored vector is the admissibility of this record. The request does not write it.
    Recording the petition does not transfer what it names.
    """
    if president_author(author):
        raise Silentium(
            "Praeses silet. Президент не записывает запрос от своего имени."
        )
    author_n = author.strip()
    phrase_n = _formula(phrase)
    petitio_n = petitio.strip()
    if not author_n or not phrase_n or not petitio_n:
        raise ValueError(
            "Укажите автора, фразу «запрос» и текст запроса."
        )
    if phrase_n != PHRASE:
        raise ValueError(
            "Министерство внутренних дел записывает запрос фразой «запрос»."
        )
    if (
        not isinstance(principle, (tuple, list))
        or len(principle) != 3
        or any(type(value) is not int or value not in (0, 1) for value in principle)
    ):
        raise ValueError("Π должна содержать ровно три целых числа: 0 или 1.")
    L, J, V = principium(*principle)
    if not admissible((L, J, V)):
        raise ValueError("Запрос допустим только при L=J=V=1.")
    return _append(
        PETITIONES,
        PETITIONES_FIELDS,
        {
            "author": author_n,
            "phrase": PHRASE,
            "petitio": petitio_n,
            "L": L,
            "J": J,
            "V": V,
            "decision": "scripta",
        },
    )


def list_petitiones() -> list[dict[str, str]]:
    """Read recorded requests, newest first."""
    rows = _read(PETITIONES, PETITIONES_FIELDS)
    rows.reverse()
    return rows
