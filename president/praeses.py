"""Praeses programma mathematicum.

The president of World Administratum / Mundus Administratum is not a person.
The president is this mathematical program.
Where is the president? Here: the program, and the vector it computes.
"""

from __future__ import annotations

import math
from pathlib import Path

NAME = "World Administratum"
NAME_LATIN = "Mundus Administratum"
OFFICE = "Praeses programma mathematicum"
AXES = ("iustitia", "veritas")


class Praeses:
    """Presidential office: a vector computed by this program."""

    def __init__(self, iustitia: float, veritas: float) -> None:
        self.P = (float(iustitia), float(veritas))

    @property
    def magnitude(self) -> float:
        return math.sqrt(sum(x * x for x in self.P))

    def direction(self) -> tuple[float, float]:
        m = self.magnitude
        if m == 0:
            return (0.0, 0.0)
        return (self.P[0] / m, self.P[1] / m)

    def where(self) -> str:
        d = self.direction()
        here = Path(__file__).resolve()
        return "\n".join(
            [
                f"{NAME} / {NAME_LATIN}",
                f"{OFFICE}",
                "Где президент: эта математическая программа.",
                f"program = {here}",
                f"P = ({AXES[0]} = {self.P[0]}, {AXES[1]} = {self.P[1]})",
                f"|P| = {self.magnitude}",
                f"direction = ({AXES[0]} = {d[0]}, {AXES[1]} = {d[1]})",
            ]
        )


def president() -> Praeses:
    return Praeses(1.0, 1.0)


if __name__ == "__main__":
    print(president().where())
