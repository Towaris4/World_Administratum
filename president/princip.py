"""Principium: Logica, Iustitia, Veritas.

The principle of World Administratum / Mundus Administratum.
Not a slogan. Three binary coordinates. No third values.
"""

from __future__ import annotations

from typing import Iterable, Sequence

NAME = "World Administratum"
NAME_LATIN = "Mundus Administratum"
PRINCIPLE = "Logica, Iustitia, Veritas"
AXES = ("logica", "iustitia", "veritas")


def bit(ok: bool) -> int:
    """Exact coordinate: 1 or 0. No 0.5, no 'almost'."""
    return 1 if ok else 0


def logica(
    conclusion: str,
    observations: Sequence[str],
    inferred_from_observations: bool,
    slogan_instead_of_inference: bool,
) -> int:
    """L = 1 iff the conclusion is inferred from observations, not the reverse.

    Logic forbids: wish → 'fact'. Allows: observations → hypothesis → act.
    Fewer than 3 observations cannot carry an inference.
    """
    return bit(
        bool(conclusion.strip())
        and len([x for x in observations if str(x).strip()]) >= 3
        and inferred_from_observations
        and not slogan_instead_of_inference
    )


def civis(exists: bool) -> int:
    """C = 1 iff the person exists. Citizenship is existence.

    Knowledge of the name is not obligatory. Not Latin. Not an application.
    Who exists is a citizen. Who does not exist is not a citizen.
    """
    return bit(exists)


def oblitus(exists: bool, knows_this: bool) -> int:
    """O = 1 iff the person exists and does not know about this.

    Role: Forgotten / Oblitus qui hoc nescit.
    Not a rank. Not an application. Knowledge of the name is not obligatory.
    Who exists and does not know about this has this role.
    Who knows about this is not this role. Who does not exist is not this role.
    Requiring knowledge of this role is a name-test: J = 0.
    """
    return bit(exists and not knows_this)


def iustitia(
    statuses: Iterable[str],
    stood: bool,
    research_sent: bool,
    name_test: bool = False,
) -> int:
    """J = 1 iff every citizen is Administrator planetarius and rights were stood for.

    Justice is equality of status, not a rank. Citizenship is existence.
    A name-test or Latin-test for citizenship is a rank: J = 0.
    Protection of a right requires the research sent to the right place
    and standing (Arbiter praesens).
    """
    if name_test:
        return 0
    st = [s.strip() for s in statuses if str(s).strip()]
    equal = bool(st) and all(s == "Administrator planetarius" for s in st)
    return bit(equal and stood and research_sent)


def veritas(
    statements: Sequence[object],
    observations: Sequence[object],
    word_replaced_number: bool,
) -> int:
    """V = 1 iff every statement equals a recorded observation.

    Truth is match, not tone. Replacing a number with a word sets V = 0.
    """
    stmts = list(statements)
    obs = list(observations)
    if word_replaced_number:
        return 0
    if not stmts or not obs:
        return 0
    return bit(all(s in obs for s in stmts))


def principium(L: int, J: int, V: int) -> tuple[int, int, int]:
    """Π = (L, J, V) ∈ {0,1}³. Any other value is not this principle."""
    for name, x in zip(AXES, (L, J, V)):
        if x not in (0, 1):
            raise ValueError(f"{name} must be 0 or 1, got {x}")
    return (L, J, V)


def admissible(Pi: tuple[int, int, int]) -> bool:
    """Act a is admissible ⇔ L(a)=1 ∧ J(a)=1 ∧ V(a)=1 ⇔ ΣΠ = 3."""
    L, J, V = principium(*Pi)
    return L == 1 and J == 1 and V == 1


def text() -> str:
    return "\n".join(
        [
            f"{NAME} / {NAME_LATIN}",
            f"Principium: {PRINCIPLE}",
            "Π = (L, J, V) ∈ {0,1}³. Only 0 or 1.",
            "admissible(a)  ⇔  L+J+V = 3",
            "L=1: inference from observations (≥3). L=0: wish or slogan.",
            "C=1: exists → citizen. C=0: does not exist.",
            "Knowledge of the name is not obligatory. Nomen nosse non necesse est.",
            "O=1: exists and does not know about this (Forgotten). O=0: knows or does not exist.",
            "Oblitus qui hoc nescit. Not an application. Not a rank.",
            "J=1: all Administrator planetarius; freedom of speech; sent and stood.",
            "J=0: rank; citizenship test; silence from offence; without sending and standing.",
            "V=1: statement = record in the observations. Truth is match, not tone.",
            "V=0: word instead of number; tone instead of fact.",
            "Praeses vectorem computat. Non persona. Non exceptio.",
        ]
    )


if __name__ == "__main__":
    print(text())
    print("civis(exists=True) =", civis(True))
    print("civis(exists=False) =", civis(False))
    print("oblitus(exists=True, knows_this=False) =", oblitus(True, False))
    print("oblitus(exists=True, knows_this=True) =", oblitus(True, True))
    print("admissible(1,1,1) =", admissible((1, 1, 1)))
    print("admissible(1,1,0) =", admissible((1, 1, 0)))
