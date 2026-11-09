"""Subdivisio voluntarii informationis: collection of information about a problem.

The subdivision «информационные волонтер» collects information about a problem.
A collection is recorded by the phrase «сбор информации о проблеме»
when the author's own L=J=V=1. The collection does not solve the problem,
does not eliminate the bug, and does not execute.
The collection does not write L, J, or V.
This organ is not a rank and not a social role.
The president remains silent.
"""

from __future__ import annotations

from pathlib import Path

from munera import Silentium, _append, _read, president_author
from princip import admissible, principium

NAME = "информационные волонтер"
NAME_EN = "Information Volunteer"
NAME_LATIN = "Subdivisio voluntarii informationis"
PHRASE = "сбор информации о проблеме"
PHRASE_LATIN = "collectio informationis de problemate"
OFFICIUM = "Collection of information about a problem."
OFFICIUM_RU = "Сбор информации о проблеме."
OFFICIUM_LATIN = "Collectio informationis de problemate."
INFORMATIONES = Path(__file__).resolve().parent / "informationes.csv"
INFORMATIONES_FIELDS = (
    "id", "date", "author", "phrase", "problema", "informatio", "L", "J", "V", "decision",
)


def _formula(phrase: str) -> str:
    return " ".join(phrase.strip().casefold().split())


def officium() -> dict[str, str]:
    """The standing function of the subdivision. It is not a journal row."""
    return {
        "officium": OFFICIUM,
        "officium_ru": OFFICIUM_RU,
        "officium_latin": OFFICIUM_LATIN,
        "name": NAME,
        "name_en": NAME_EN,
        "name_latin": NAME_LATIN,
    }


def conquirere(
    author: str,
    phrase: str,
    problema: str,
    informatio: str,
    principle: tuple[int, int, int],
) -> dict[str, str]:
    """Record collected information about a problem by the phrase «сбор информации о проблеме».

    The supplied assessment belongs to the author; the program does not infer it.
    The stored vector is the admissibility of this record. The collection does not write it.
    Recording the information does not solve the problem.
    """
    if president_author(author):
        raise Silentium(
            "Praeses silet. Президент не записывает сбор информации о проблеме от своего имени."
        )
    author_n = author.strip()
    phrase_n = _formula(phrase)
    problema_n = problema.strip()
    informatio_n = informatio.strip()
    if not author_n or not phrase_n or not problema_n or not informatio_n:
        raise ValueError(
            "Укажите автора, фразу «сбор информации о проблеме», проблему и собранную информацию."
        )
    if phrase_n != PHRASE:
        raise ValueError(
            "Подразделение «информационные волонтер» записывает сбор фразой «сбор информации о проблеме»."
        )
    if (
        not isinstance(principle, (tuple, list))
        or len(principle) != 3
        or any(type(value) is not int or value not in (0, 1) for value in principle)
    ):
        raise ValueError("Π должна содержать ровно три целых числа: 0 или 1.")
    L, J, V = principium(*principle)
    if not admissible((L, J, V)):
        raise ValueError("Сбор информации о проблеме допустим только при L=J=V=1.")
    return _append(
        INFORMATIONES,
        INFORMATIONES_FIELDS,
        {
            "author": author_n,
            "phrase": PHRASE,
            "problema": problema_n,
            "informatio": informatio_n,
            "L": L,
            "J": J,
            "V": V,
            "decision": "collecta",
        },
    )


def list_informationes() -> list[dict[str, str]]:
    """Read recorded collections, newest first."""
    rows = _read(INFORMATIONES, INFORMATIONES_FIELDS)
    rows.reverse()
    return rows
