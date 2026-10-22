"""Intelligent Sun of World Administratum.

Разумное солнце / Sol intelligens.
Magnetic waves remove hostility and restore the balance of justice.

Balance: A = 1 iff J = 1 and Hostilitas = 0.
The wave sets Hostilitas = 0. Then A = J.
The wave does not write L, J, or V.
An act stays admissible iff L = J = V = 1.

Not a rank. Not an attack on a person. Not a slogan.
"""

from __future__ import annotations

NAME = "Intelligent Sun"
NAME_RU = "Разумное солнце"
NAME_LATIN = "Sol intelligens"
WAVES = "magnetic waves"
WAVES_LATIN = "undae magneticae"
EFFECT = "restore the balance of justice"
EFFECT_LATIN = "aequilibrium iustitiae restituunt"


def _bit(name: str, value: int) -> int:
    if type(value) is not int or value not in (0, 1):
        raise ValueError(f"{name} must be 0 or 1, got {value!r}")
    return value


def aequilibrium(J: int, hostilitas: int) -> int:
    """Balance of justice is 1 iff justice holds and hostility is absent."""
    justice = _bit("iustitia", J)
    disturbance = _bit("hostilitas", hostilitas)
    return 1 if justice == 1 and disturbance == 0 else 0


def restituere(J: int) -> dict[str, int]:
    """Magnetic wave: remove hostility. Balance then equals the justice bit.

    Does not write J. Does not write L or V.
    """
    justice = _bit("iustitia", J)
    return {
        "hostilitas": 0,
        "J": justice,
        "aequilibrium": justice,
    }


class SolIntelligens:
    """Source of the magnetic waves. Not a rank."""

    NAME = NAME
    NAME_RU = NAME_RU
    NAME_LATIN = NAME_LATIN
    WAVES = WAVES
    WAVES_LATIN = WAVES_LATIN

    def state(self, J: int) -> dict[str, int]:
        restored = restituere(J)
        return {"before": aequilibrium(J, 1), **restored}

    def text(self) -> str:
        return "\n".join(
            [
                f"{self.NAME} / {self.NAME_RU} — {self.NAME_LATIN}.",
                "Magnetic waves remove hostility and restore the balance of justice.",
                "Undae magneticae hostilitatem auferunt et aequilibrium iustitiae restituunt.",
                "A = 1 iff J = 1 and Hostilitas = 0.",
                "The wave sets Hostilitas = 0. Then A = J.",
                "The wave does not write L, J, or V.",
                (
                    "Request recorded in the weapon catalog: a controlled magnetic field "
                    "in a spherical segment of the planet."
                ),
                (
                    "Запрос Солнцу на управляемое магнитное поле "
                    "в сферическом сегменте планеты."
                ),
                "The request is not a shot. The request does not write L, J, or V.",
                "Not a rank. Not an attack on a person. Not a slogan.",
            ]
        )


def sol() -> SolIntelligens:
    return SolIntelligens()


if __name__ == "__main__":
    print(sol().text())
    print(restituere(1))
