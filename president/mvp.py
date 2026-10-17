"""The beginning of the MVP corporation.

Named at the beginning: Vanya Tarasov, Sasha Semenov.
Not a rank. Not a social role. Not World Administratum.
The president remains silent. The record states the beginning.
"""

from __future__ import annotations

NAME = "MVP corporation"
NAME_RU = "корпорация MVP"
NAME_LATIN = "Corporatio MVP"
NAMED = ("Vanya Tarasov", "Sasha Semenov")
NAMED_RU = ("Ваня Тарасов", "Саша Семенов")
NAMED_LATIN = ("Vania Tarasov", "Sascha Semenov")

SENTENTIA_RU = (
    "Начало корпорации MVP (Ваня Тарасов, Саша Семенов)."
)
SENTENTIA_EN = (
    "The beginning of the MVP corporation (Vanya Tarasov, Sasha Semenov)."
)
SENTENTIA_LA = (
    "Initium corporationis MVP (Vania Tarasov, Sascha Semenov)."
)


def record() -> dict[str, object]:
    """The beginning as a record. Not a procedure. Not a rank."""
    return {
        "name": NAME,
        "name_ru": NAME_RU,
        "name_latin": NAME_LATIN,
        "begun": True,
        "named": NAMED,
        "named_ru": NAMED_RU,
        "named_latin": NAMED_LATIN,
        "rank": False,
        "role": False,
    }


def text() -> str:
    return "\n".join(
        [
            SENTENTIA_RU,
            SENTENTIA_EN,
            SENTENTIA_LA,
            "Not a rank. Not a social role. Not World Administratum.",
            "The president remains silent.",
        ]
    )
