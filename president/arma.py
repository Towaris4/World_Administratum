"""Weapon of World Administratum: railgun on the far side of the Moon.

The weapon is a railgun. It shoots at fantasy.
If a shot did not happen, it is in the LinkedList and waits to be fired.
Currently in the LinkedList: War and Hostility; they will be shot with plasma.

Not territory. Not a capital. Not a rank. The Moon is not the capital.
Not an attack on a person: the warrior is a meliorator.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Optional


@dataclass(frozen=True)
class Ictus:
    """One shot: if it did not happen, it waits in the LinkedList."""

    target: str
    latin: str
    charge: str = "plasma"
    destination: str = "fantasy"

    def as_row(self) -> dict[str, str]:
        return {
            "target": self.target,
            "latin": self.latin,
            "charge": self.charge,
            "destination": self.destination,
            "status": "waiting to be fired",
        }


class _Nodus:
    def __init__(self, ictus: Ictus) -> None:
        self.ictus = ictus
        self.next: Optional[_Nodus] = None


class LinkedList:
    """Queue of shots.

    If a shot did not happen — it is in this LinkedList and waits to be fired.
    """

    def __init__(self) -> None:
        self.head: Optional[_Nodus] = None
        self.tail: Optional[_Nodus] = None

    def append(self, ictus: Ictus) -> None:
        nodus = _Nodus(ictus)
        if self.tail is None:
            self.head = self.tail = nodus
            return
        self.tail.next = nodus
        self.tail = nodus

    def pop_front(self) -> Optional[Ictus]:
        if self.head is None:
            return None
        ictus = self.head.ictus
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        return ictus

    def __iter__(self) -> Iterator[Ictus]:
        node = self.head
        while node is not None:
            yield node.ictus
            node = node.next

    def __len__(self) -> int:
        n = 0
        node = self.head
        while node is not None:
            n += 1
            node = node.next
        return n

    def waiting(self) -> tuple[Ictus, ...]:
        return tuple(self)

    def contains(self, target: str) -> bool:
        key = target.strip().casefold()
        return any(
            i.target.casefold() == key or i.latin.casefold() == key for i in self
        )


BELLUM = Ictus("War", "Bellum")
HOSTILITAS = Ictus("Hostility", "Hostilitas")


class Relsotron:
    """Railgun on the far side of the Moon. Shoots at fantasy."""

    NAME = "Weapon"
    NAME_LATIN = "Telum rallarium"
    KIND = "railgun"
    PLACE = "far side of the Moon"
    PLACE_LATIN = "facies aversa Lunae"
    DESTINATION = "fantasy"
    DESTINATION_LATIN = "phantasia"
    CHARGE = "plasma"
    CHARGE_LATIN = "plasma"

    def __init__(self, queue: LinkedList | None = None) -> None:
        if queue is None:
            self.queue = LinkedList()
            self.queue.append(BELLUM)
            self.queue.append(HOSTILITAS)
        else:
            self.queue = queue

    def disparatum(self, target: str) -> bool:
        """The shot happened ⇔ the target is no longer in the LinkedList."""
        return not self.queue.contains(target)

    def exspectat(self, target: str) -> bool:
        """If the shot did not happen — the target is in the LinkedList and waits to be fired."""
        return self.queue.contains(target)

    def disparare(self) -> Optional[Ictus]:
        """A plasma shot at fantasy: the head of the queue leaves the LinkedList."""
        return self.queue.pop_front()

    def ordo(self) -> tuple[Ictus, ...]:
        return self.queue.waiting()

    def chain(self) -> str:
        names = [f"{i.target} / {i.latin}" for i in self.ordo()]
        if not names:
            return "head → None"
        return "head → " + " → ".join(names) + " → None"

    def text(self) -> str:
        waiting = ", ".join(f"{i.target} / {i.latin}" for i in self.ordo()) or "empty"
        return "\n".join(
            [
                f"{self.NAME} — {self.KIND} on the far side of the Moon.",
                f"{self.NAME_LATIN} in facie aversa Lunae.",
                "Shoots at fantasy. In phantasiam disparat.",
                "If a shot did not happen — it is in the LinkedList and waits to be fired.",
                f"Currently in the LinkedList: {waiting}; they will be shot with plasma.",
                f"LinkedList: {self.chain()}",
                "Not territory. Not a capital. Not a rank. The Moon is not the capital.",
            ]
        )


def telum() -> Relsotron:
    return Relsotron()


if __name__ == "__main__":
    print(telum().text())
