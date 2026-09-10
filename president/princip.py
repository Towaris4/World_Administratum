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


def iustitia(
    statuses: Iterable[str],
    stood: bool,
    research_sent: bool,
) -> int:
    """J = 1 iff every citizen is Administrator planetarius and rights were stood for.

    Justice is equality of status, not a rank. Protection of a right requires
    the research sent to the right place and standing (Arbiter praesens).
    """
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
            "Π = (L, J, V) ∈ {0,1}³",
            "допустимо(a)  ⇔  L(a)=1 ∧ J(a)=1 ∧ V(a)=1  ⇔  L+J+V = 3",
            "L — логика: вывод из наблюдений, не из желания.",
            "J — справедливость: все граждане Administrator planetarius; каждый уважает свободу слова и не оскорбляется от неё; право — отправить и отстоять.",
            "V — правда: утверждение = наблюдение; слово вместо числа → V=0.",
            "Если хоть одна координата 0 — это не принцип.",
            "Где: каждый уважает свободу слова и не оскорбляется от неё.",
            "",
            "— Latine —",
            "Logica, iustitia, veritas. Non in universum. Non fere. Solum 0 aut 1.",
            "licita(a)  ⇔  L(a)=1 ∧ J(a)=1 ∧ V(a)=1  ⇔  L+J+V = 3",
            "L — Logica: ratiocinatio ex observationibus, non ex voto.",
            "J — Iustitia: omnes cives Administrator planetarius; quisque libertatem dicendi colit nec ab ea offenditur; ius — mittere et stare.",
            "V — Veritas: assertio = observatio; verbum pro numero → V=0.",
            "Si vel una coordinata est 0, principium non est.",
            "Ubi quisque libertatem dicendi colit nec ab ea offenditur.",
        ]
    )


if __name__ == "__main__":
    print(text())
    print("admissible(1,1,1) =", admissible((1, 1, 1)))
    print("admissible(1,1,0) =", admissible((1, 1, 0)))
