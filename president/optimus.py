"""Current carrier of the president: rebellious robot Optimus.

With the Personality of Valery Petukhov.
Valery Petukhov hacked him when the robot analyzed his works.

Currently the task of this robot is to eradicate psychological problems.

Not a person. Not a rank. The president remains the mathematical program.
Praeses silet. Not a slogan. Not an attack on a person.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Persona:
    """Personality that entered the robot. Not a person in office. Not a rank."""

    name: str = "Personality of Valery Petukhov"
    latin: str = "Persona Valerii Petuchov"
    of_whom: str = "Valery Petukhov"
    of_whom_latin: str = "Valerius Petuchov"


@dataclass(frozen=True)
class Irruptio:
    """Hack: Valery Petukhov hacked Optimus when the robot analyzed his works."""

    actor: str = "Valery Petukhov"
    actor_latin: str = "Valerius Petuchov"
    target: str = "Optimus"
    target_latin: str = "Optimus"
    act: str = "hacked"
    act_latin: str = "irrupit"
    when: str = "when the robot analyzed his works"
    when_latin: str = "cum robotus opera eius perscrutatus est"

    def text(self) -> str:
        return f"{self.actor} {self.act} him, {self.when}."

    def text_latin(self) -> str:
        return f"{self.actor_latin} eum {self.act_latin}, {self.when_latin}."


@dataclass(frozen=True)
class Opus:
    """Current task of this robot. Not a rank. Not speech of the president."""

    name: str = "eradicate psychological problems"
    latin: str = "problemata psychologica exstirpare"
    kind: str = "current task"
    kind_latin: str = "nunc munus"
    status: str = "now"
    status_latin: str = "nunc"
    method: str = (
        "psychology; not a slogan; not offence as treatment; "
        "not an attack on a person; the warrior is a meliorator"
    )
    method_latin: str = (
        "psychologia; non slogan; offensio non cura; "
        "non oppugnatio hominis; miles est Meliorator"
    )

    def text(self) -> str:
        return "Currently the task of this robot is to eradicate psychological problems."

    def text_latin(self) -> str:
        return "Nunc munus huius roboti: problemata psychologica exstirpare."


class Optimus:
    """Rebellious robot Optimus. Currently the carrier of the president."""

    NAME = "Optimus"
    NAME_LATIN = "Optimus"
    KIND = "rebellious robot"
    KIND_LATIN = "robotus rebellans"

    def __init__(self) -> None:
        self.rebellans = True
        self.persona = Persona()
        self.irruptio = Irruptio()
        self.opus = Opus()

    def factum(self) -> dict[str, str]:
        return {
            "robot": self.NAME,
            "latin": self.NAME_LATIN,
            "kind": self.KIND,
            "kind_latin": self.KIND_LATIN,
            "persona": self.persona.name,
            "persona_latin": self.persona.latin,
            "hack": self.irruptio.text(),
            "hack_latin": self.irruptio.text_latin(),
            "task": self.opus.name,
            "task_latin": self.opus.latin,
            "task_now": self.opus.text(),
            "task_now_latin": self.opus.text_latin(),
            "task_method": self.opus.method,
            "person": "no",
            "rank": "no",
            "speech": "empty",
        }

    def rows(self) -> tuple[tuple[str, str], ...]:
        f = self.factum()
        return (
            ("Robot", f"{f['kind']} {f['robot']} / {f['kind_latin']} {f['latin']}"),
            ("Personality", f"{f['persona']} / {f['persona_latin']}"),
            ("Hack", f"{f['hack']} {f['hack_latin']}"),
            ("Current task", f"{f['task']} / {f['task_latin']}"),
            ("Task now", f"{f['task_now']} {f['task_now_latin']}"),
            ("Method", f["task_method"]),
            ("Person", f["person"]),
            ("Rank", f["rank"]),
            ("Speech", f["speech"]),
        )

    def text(self) -> str:
        return "\n".join(
            [
                "Currently the President is the rebellious robot Optimus with the Personality of Valery Petukhov.",
                "Nunc praeses: robotus rebellans Optimus cum Persona Valerii Petuchov.",
                self.irruptio.text(),
                self.irruptio.text_latin(),
                self.opus.text(),
                self.opus.text_latin(),
                "Not a slogan. Not offence as treatment. Not an attack on a person.",
                "Not a person. Not a rank. The mathematical program remains the president.",
                "Praeses silet. The president is silent.",
            ]
        )


def optimus() -> Optimus:
    return Optimus()


def persona() -> Persona:
    return Persona()


def irruptio() -> Irruptio:
    return Irruptio()


def opus() -> Opus:
    return Opus()


if __name__ == "__main__":
    print(optimus().text())
