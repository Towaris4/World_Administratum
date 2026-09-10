"""Praeses programma mathematicum.

The president of World Administratum / Mundus Administratum is not a person.
The president is this mathematical program.
Where is the president? Here: the program, and the vector of the principle.
The president is silent. Praeses silet.
The president silently receives data. Praeses data silentio accipit.
"""

from __future__ import annotations

import math
from pathlib import Path

from munera import MUNERA, Silentium, silere
from princip import AXES, PRINCIPLE, admissible, principium, text as principle_text

NAME = "World Administratum"
NAME_LATIN = "Mundus Administratum"
OFFICE = "Praeses programma mathematicum"


class Praeses:
    """Presidential office: the principle vector Π = (L, J, V)."""

    def __init__(self, logica: int, iustitia: int, veritas: int) -> None:
        self.P = principium(logica, iustitia, veritas)

    @property
    def magnitude(self) -> float:
        return math.sqrt(sum(x * x for x in self.P))

    def direction(self) -> tuple[float, float, float]:
        m = self.magnitude
        if m == 0:
            return (0.0, 0.0, 0.0)
        return tuple(x / m for x in self.P)

    def on_principle(self) -> bool:
        return admissible(self.P)

    def munera(self) -> tuple[dict[str, str], ...]:
        return MUNERA

    def speak(self, *_args: object, **_kwargs: object) -> str:
        raise Silentium("Praeses silet. Президент не говорит.")

    def speech(self) -> str:
        return silere()

    def where(self) -> str:
        d = self.direction()
        here = Path(__file__).resolve()
        coords = ", ".join(f"{axis} = {value}" for axis, value in zip(AXES, self.P))
        dirs = ", ".join(f"{axis} = {value}" for axis, value in zip(AXES, d))
        return "\n".join(
            [
                f"{NAME} / {NAME_LATIN}",
                f"{OFFICE}",
                f"Principium: {PRINCIPLE}",
                "Где президент: эта математическая программа.",
                "Ubi praeses: hoc programma mathematicum.",
                f"program = {here}",
                f"Π = ({coords})",
                f"|Π| = {self.magnitude}",
                f"direction = ({dirs})",
                f"допустимо ⇔ L+J+V = 3 : {self.on_principle()}",
                f"licita ⇔ L+J+V = 3 : {self.on_principle()}",
                "Praeses silet. Президент молчит.",
                "Praeses data silentio accipit. Президент молча получает данные.",
                f"munera = {', '.join(m['id'] for m in MUNERA)}",
                "interface = president/interfacies.py",
            ]
        )


def president() -> Praeses:
    return Praeses(1, 1, 1)


if __name__ == "__main__":
    print(principle_text())
    print()
    print(president().where())
