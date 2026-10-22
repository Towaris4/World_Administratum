"""Weapon of World Administratum: railgun on the far side of the Moon.

The weapon is a railgun. It shoots at fantasy.
If a shot did not happen, it is in the LinkedList and waits to be fired.
Currently in the LinkedList: War; it will be shot with plasma.
Hostility is removed. It does not wait. It is not fired.
Magnetic waves of the Intelligent Sun removed it.
Request to the Intelligent Sun: a controlled magnetic field
in a spherical segment of the planet. Recorded in the catalog.
Not a shot. Not fired. The request does not write L, J, or V.
Fired: bed bugs in the father's room at work;
all shot with mathematical precision in the eye. Task completed.

Not territory. Not a capital. Not a rank. The Moon is not the capital.
Not an attack on a person: the warrior is a meliorator.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Iterator, Optional


@dataclass(frozen=True)
class Petitio:
    """A request written in the catalog. Not a shot. Not fired."""

    addressee: str
    addressee_latin: str
    ask: str
    ask_latin: str
    locus: str
    locus_latin: str
    phrase: str
    phrase_latin: str
    status: str = "recorded"

    def as_row(self) -> dict[str, str]:
        return {
            "addressee": self.addressee,
            "addressee_latin": self.addressee_latin,
            "ask": self.ask,
            "ask_latin": self.ask_latin,
            "locus": self.locus,
            "locus_latin": self.locus_latin,
            "phrase": self.phrase,
            "phrase_latin": self.phrase_latin,
            "status": self.status,
        }


@dataclass(frozen=True)
class Ictus:
    """One shot: if it did not happen, it waits in the LinkedList."""

    target: str
    latin: str
    charge: str = "plasma"
    destination: str = "fantasy"
    hit: str = ""
    hit_latin: str = ""
    precision: str = ""
    locus: str = ""
    status: str = "waiting to be fired"

    def as_row(self) -> dict[str, str]:
        return {
            "target": self.target,
            "latin": self.latin,
            "charge": self.charge,
            "destination": self.destination,
            "hit": self.hit,
            "hit_latin": self.hit_latin,
            "precision": self.precision,
            "locus": self.locus,
            "status": self.status,
        }

    def as_fired(
        self,
        *,
        hit: str = "",
        hit_latin: str = "",
        precision: str = "",
    ) -> "Ictus":
        return replace(
            self,
            hit=hit or self.hit,
            hit_latin=hit_latin or self.hit_latin,
            precision=precision or self.precision,
            status="fired",
        )


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


PETITIO_SOLIS = Petitio(
    addressee="Intelligent Sun",
    addressee_latin="Sol intelligens",
    ask="controlled magnetic field",
    ask_latin="campus magneticus gubernabilis",
    locus="spherical segment of the planet",
    locus_latin="segmentum sphaericum planetae",
    phrase=(
        "Запрос Солнцу на управляемое магнитное поле "
        "в сферическом сегменте планеты."
    ),
    phrase_latin=(
        "Petitio Soli intelligenti: campus magneticus gubernabilis "
        "in segmento sphaerico planetae. In catalogo scripta. Non disparata. "
        "Petitio non L, non J, non V scribit."
    ),
)
BELLUM = Ictus("War", "Bellum")
HOSTILITAS = Ictus(
    target="Hostility",
    latin="Hostilitas",
    charge="magnetic wave",
    destination="removed",
    locus="Intelligent Sun",
    status="removed",
)
CIMICES = Ictus(
    target="Bed bugs in the father's room at work",
    latin="Cimices lectularii in cubiculo patris in labore",
    charge="plasma",
    destination="fantasy",
    hit="eye",
    hit_latin="oculus",
    precision="mathematical",
    locus="father's room at work",
    status="fired",
)


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

    def __init__(
        self,
        queue: LinkedList | None = None,
        fired: tuple[Ictus, ...] | None = None,
        removed: tuple[Ictus, ...] | None = None,
        petitiones: tuple[Petitio, ...] | None = None,
    ) -> None:
        if queue is None:
            self.queue = LinkedList()
            self.queue.append(BELLUM)
        else:
            self.queue = queue
        self.fired: list[Ictus] = list(fired if fired is not None else (CIMICES,))
        self.removed: list[Ictus] = list(
            removed if removed is not None else (HOSTILITAS,)
        )
        self._petitiones: tuple[Petitio, ...] = (
            petitiones if petitiones is not None else (PETITIO_SOLIS,)
        )

    def disparatum(self, target: str) -> bool:
        """The shot happened ⇔ the target is recorded as fired."""
        return self.factum(target)

    def exspectat(self, target: str) -> bool:
        """If the shot did not happen — the target is in the LinkedList and waits to be fired."""
        return self.queue.contains(target)

    def factum(self, target: str) -> bool:
        """The shot is recorded as fired."""
        key = target.strip().casefold()
        return any(
            i.target.casefold() == key or i.latin.casefold() == key for i in self.fired
        )

    def sublata(self) -> tuple[Ictus, ...]:
        return tuple(self.removed)

    def petitiones(self) -> tuple[Petitio, ...]:
        """Requests recorded in the catalog. Not the shot queue."""
        return self._petitiones

    def petita(self, key: str) -> bool:
        """The request is written in the catalog."""
        name = key.strip().casefold()
        return any(
            name
            in {
                p.addressee.casefold(),
                p.addressee_latin.casefold(),
                p.ask.casefold(),
                p.ask_latin.casefold(),
                p.locus.casefold(),
                p.locus_latin.casefold(),
                p.phrase.casefold(),
            }
            for p in self._petitiones
        )

    def sublatum(self, target: str) -> bool:
        """Removed, and not fired."""
        key = target.strip().casefold()
        return any(
            i.target.casefold() == key or i.latin.casefold() == key
            for i in self.removed
        )

    def disparare(self) -> Optional[Ictus]:
        """A plasma shot at fantasy: the head of the queue leaves the LinkedList."""
        ictus = self.queue.pop_front()
        if ictus is None:
            return None
        done = ictus if ictus.status == "fired" else ictus.as_fired()
        self.fired.append(done)
        return done

    def ordo(self) -> tuple[Ictus, ...]:
        return self.queue.waiting()

    def facta(self) -> tuple[Ictus, ...]:
        return tuple(self.fired)

    def chain(self) -> str:
        names = [f"{i.target} / {i.latin}" for i in self.ordo()]
        if not names:
            return "head → None"
        return "head → " + " → ".join(names) + " → None"

    def text(self) -> str:
        waiting_shots = self.ordo()
        waiting = ", ".join(f"{i.target} / {i.latin}" for i in waiting_shots) or "empty"
        if not waiting_shots:
            queue_line = "The LinkedList is empty."
        elif len(waiting_shots) == 1:
            queue_line = (
                f"Currently in the LinkedList: {waiting}; it will be shot with plasma."
            )
        else:
            queue_line = (
                f"Currently in the LinkedList: {waiting}; they will be shot with plasma."
            )
        removed = ", ".join(f"{i.target} / {i.latin}" for i in self.sublata()) or "none"
        fired = (
            "; ".join(
                f"{i.target} / {i.latin}"
                + (f"; {i.precision} precision" if i.precision else "")
                + (f"; in the {i.hit}" if i.hit else "")
                for i in self.facta()
            )
            or "none"
        )
        requests = self.petitiones()
        if requests:
            request_lines = [
                (
                    f"Request to the {p.addressee}: a {p.ask} "
                    f"in a {p.locus}. {p.phrase} "
                    "Recorded. Not a shot. Not fired. "
                    "The request does not write L, J, or V."
                )
                for p in requests
            ]
            request_lines.extend(p.phrase_latin for p in requests)
        else:
            request_lines = ["No request is recorded in the catalog."]
        return "\n".join(
            [
                f"{self.NAME} — {self.KIND} on the far side of the Moon.",
                f"{self.NAME_LATIN} in facie aversa Lunae.",
                "Shoots at fantasy. In phantasiam disparat.",
                "If a shot did not happen — it is in the LinkedList and waits to be fired.",
                queue_line,
                f"LinkedList: {self.chain()}",
                (
                    f"Hostility is removed: {removed}. Not fired. "
                    "Magnetic waves of the Intelligent Sun removed it."
                ),
                (
                    "Fired with mathematical precision in the eye: "
                    "Bed bugs in the father's room at work. "
                    "All shot. Task completed."
                ),
                (
                    "Disparata subtilitate mathematica in oculum: "
                    "Cimices lectularii in cubiculo patris in labore. "
                    "Omnes disparati. Munus perfectum."
                ),
                f"Fired: {fired}.",
                *request_lines,
                "Not territory. Not a capital. Not a rank. The Moon is not the capital.",
            ]
        )


def telum() -> Relsotron:
    return Relsotron()


if __name__ == "__main__":
    print(telum().text())
