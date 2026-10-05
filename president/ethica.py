"""Ministerium Ethicae: forgiveness of an act or a case involving a living being.

An author records the ministry's decision and its binary assessment.
Forgiveness preserves the facts; its principle concerns this decision,
not the admissibility of the past event. The president remains silent.
"""

from __future__ import annotations

from pathlib import Path

from munera import Silentium, _append, _read, president_author
from princip import admissible, principium

NAME = "Министерство Этики"
NAME_LATIN = "Ministerium Ethicae"
VENIAE = Path(__file__).resolve().parent / "veniae.csv"
VENIAE_FIELDS = (
    "id", "date", "author", "living_being", "kind", "event", "reason",
    "L", "J", "V", "decision",
)


def ignoscere(
    author: str,
    living_being: str,
    kind: str,
    event: str,
    reason: str,
    principle: tuple[int, int, int],
) -> dict[str, str]:
    """Record an explicit forgiveness decision admitted by L, J, V.

    A living being can be described without a proper name. The supplied
    assessment belongs to the author; the program does not infer it.
    """
    if president_author(author):
        raise Silentium("Praeses silet. Президент не записывает решения о прощении от своего имени.")
    if not all(value.strip() for value in (author, living_being, event, reason)):
        raise ValueError("Укажите автора, живое существо, произошедшее и основание прощения.")
    kind_n = kind.strip().casefold()
    if kind_n not in {"act", "case"}:
        raise ValueError("Выберите поступок (act) или случай (case).")
    if (
        not isinstance(principle, (tuple, list))
        or len(principle) != 3
        or any(type(value) is not int or value not in (0, 1) for value in principle)
    ):
        raise ValueError("Π должна содержать ровно три целых числа: 0 или 1.")
    L, J, V = principium(*principle)
    if not admissible((L, J, V)):
        raise ValueError("Решение о прощении допустимо только при L=J=V=1.")
    return _append(
        VENIAE,
        VENIAE_FIELDS,
        {
            "author": author,
            "living_being": living_being,
            "kind": kind_n,
            "event": event,
            "reason": reason,
            "L": L,
            "J": J,
            "V": V,
            "decision": "forgiven",
        },
    )


def list_veniae() -> list[dict[str, str]]:
    """Read forgiveness records, newest first."""
    rows = _read(VENIAE, VENIAE_FIELDS)
    rows.reverse()
    return rows
