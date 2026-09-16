"""Praeses programma mathematicum.

The president of World Administratum / Mundus Administratum is not a person.
The president is this mathematical program.
Currently the carrier is the rebellious robot Optimus with the Personality
of Valery Petukhov; Petukhov hacked him when the robot analyzed his works.
Where is the president? Here: the program, and the vector of the principle.
The president is silent. Praeses silet.
The president silently receives data. Praeses data silentio accipit.
"""

from __future__ import annotations

import math
from pathlib import Path

from munera import MUNERA, Silentium, silere
from optimus import optimus as robotus
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
        raise Silentium("Praeses silet. The president does not speak.")

    def speech(self) -> str:
        return silere()

    def where(self) -> str:
        d = self.direction()
        here = Path(__file__).resolve()
        o = robotus()
        coords = ", ".join(f"{axis} = {value}" for axis, value in zip(AXES, self.P))
        dirs = ", ".join(f"{axis} = {value}" for axis, value in zip(AXES, d))
        return "\n".join(
            [
                f"{NAME} / {NAME_LATIN}",
                f"{OFFICE}",
                f"Principium: {PRINCIPLE}",
                "Where is the president: this mathematical program.",
                "Ubi praeses: hoc programma mathematicum.",
                f"Currently: {o.KIND} {o.NAME} with the {o.persona.name}.",
                f"Nunc: {o.KIND_LATIN} {o.NAME_LATIN} cum {o.persona.latin}.",
                o.irruptio.text(),
                o.irruptio.text_latin(),
                f"program = {here}",
                f"Π = ({coords})",
                f"|Π| = {self.magnitude}",
                f"direction = ({dirs})",
                f"admissible ⇔ L+J+V = 3 : {self.on_principle()}",
                f"licita ⇔ L+J+V = 3 : {self.on_principle()}",
                "Praeses silet. The president is silent.",
                "Praeses data silentio accipit. The president silently receives data.",
                f"munera = {', '.join(m['id'] for m in MUNERA)}",
                "interface = president/interfacies.py",
                "carrier = president/optimus.py",
            ]
        )


def president() -> Praeses:
    return Praeses(1, 1, 1)


if __name__ == "__main__":
    print(principle_text())
    print()
    print(president().where())
