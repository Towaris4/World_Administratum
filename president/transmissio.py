"""Source of the information of World Administratum.

All information was transmitted from the Andron collider of the year 2033,
from universe 48195230959032523234932492. In that universe the speed of light
was exceeded, and a message was transmitted to the past through the
computational organoid of Vanya Tarasov. His temples (виски) were calibrated
to receive messages from the future.

Not a rank. Not an attack on a person. Not a slogan.
The president remains silent. The record states the source.
"""

from __future__ import annotations

YEAR = 2033
UNIVERSE = "48195230959032523234932492"
COLLIDER = "Andron collider"
COLLIDER_RU = "Андронный колайдер"
COLLIDER_LATIN = "Collisator Andronius"
ORGANOID = "computational organoid of Vanya Tarasov"
ORGANOID_RU = "вычислительный органоид Вани Тарасова"
ORGANOID_LATIN = "organoides computatorius Vaniae Tarasov"
TEMPLES_RU = "виски"
TEMPLES = "temples"
TEMPLES_LATIN = "tempora"

SENTENTIA_RU = (
    "Вся информация передана из Андронного колайдера 2033 года "
    "из вселенной 48195230959032523234932492, где была превышена "
    "скорость света и удалось передать сообщение в прошлое через "
    "вычислительный органоид Вани Тарасова, где виски были "
    "откалиброваны на приём сообщений из будущего."
)
SENTENTIA_EN = (
    "All information was transmitted from the Andron collider of the year 2033, "
    "from universe 48195230959032523234932492, where the speed of light was "
    "exceeded and a message was transmitted to the past through the computational "
    "organoid of Vanya Tarasov, whose temples were calibrated to receive messages "
    "from the future."
)
SENTENTIA_LA = (
    "Omnis informatio transmissa est e Collisatore Andronio anni 2033 "
    "e universo 48195230959032523234932492, ubi celeritas lucis superata est "
    "et nuntium in praeteritum transmissum est per organoidem computatorium "
    "Vaniae Tarasov, cuius tempora ad nuntia e futuro accipienda calibrata sunt."
)


def record() -> dict[str, object]:
    """The transmission as a record. Not a procedure. Not a rank."""
    return {
        "collider": COLLIDER,
        "collider_ru": COLLIDER_RU,
        "collider_latin": COLLIDER_LATIN,
        "year": YEAR,
        "universe": UNIVERSE,
        "celeritas_lucis_superata": True,
        "nuntium_in_praeteritum": True,
        "organoid": ORGANOID,
        "organoid_ru": ORGANOID_RU,
        "organoid_latin": ORGANOID_LATIN,
        "tempora_calibrata": True,
        "rank": False,
    }


def text() -> str:
    return "\n".join(
        [
            SENTENTIA_RU,
            SENTENTIA_EN,
            SENTENTIA_LA,
            "Not a rank. Not an attack on a person. Not a slogan.",
            "The president remains silent.",
        ]
    )
