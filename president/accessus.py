"""Ministerium Accessus: a communication channel by the phrase «запрос доступа».

An author records the request and the channel. The ministry provides the
channel when the phrase is that formula and L=J=V=1. The president remains silent.
"""

from __future__ import annotations

from pathlib import Path

from munera import Silentium, _append, _read, president_author
from princip import admissible, principium

NAME = "Министерство доступа"
NAME_LATIN = "Ministerium Accessus"
PHRASE = "запрос доступа"
PHRASE_LATIN = "petitio accessus"
CANALES = Path(__file__).resolve().parent / "canales.csv"
CANALES_FIELDS = (
    "id", "date", "author", "phrase", "channel", "L", "J", "V", "decision",
)


def _formula(phrase: str) -> str:
    return " ".join(phrase.strip().casefold().split())


def praebere(
    author: str,
    phrase: str,
    channel: str,
    principle: tuple[int, int, int],
) -> dict[str, str]:
    """Provide a communication channel requested by «запрос доступа».

    The supplied assessment belongs to the author; the program does not infer it.
    """
    if president_author(author):
        raise Silentium(
            "Praeses silet. Президент не записывает запрос доступа от своего имени."
        )
    author_n = author.strip()
    phrase_n = _formula(phrase)
    channel_n = channel.strip()
    if not author_n or not phrase_n or not channel_n:
        raise ValueError(
            "Укажите автора, фразу «запрос доступа» и канал связи."
        )
    if phrase_n != PHRASE:
        raise ValueError(
            "Министерство доступа обеспечивает канал связи фразой «запрос доступа»."
        )
    if (
        not isinstance(principle, (tuple, list))
        or len(principle) != 3
        or any(type(value) is not int or value not in (0, 1) for value in principle)
    ):
        raise ValueError("Π должна содержать ровно три целых числа: 0 или 1.")
    L, J, V = principium(*principle)
    if not admissible((L, J, V)):
        raise ValueError("Обеспечение канала допустимо только при L=J=V=1.")
    return _append(
        CANALES,
        CANALES_FIELDS,
        {
            "author": author_n,
            "phrase": PHRASE,
            "channel": channel_n,
            "L": L,
            "J": J,
            "V": V,
            "decision": "provided",
        },
    )


def list_canales() -> list[dict[str, str]]:
    """Read provided communication channels, newest first."""
    rows = _read(CANALES, CANALES_FIELDS)
    rows.reverse()
    return rows
