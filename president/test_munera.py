"""Silent president: functions without speech."""

from __future__ import annotations

import tempfile
from pathlib import Path

import arma
import munera
from arma import CIMICES, Relsotron, telum
from munera import Silentium, president_author, silere
from praeses import Praeses, president
from princip import admissible, civis, iustitia, oblitus


def test_silent() -> None:
    assert silere() == ""
    assert president().speech() == ""
    try:
        president().speak("hello")
    except Silentium:
        pass
    else:
        raise AssertionError("president must not speak")


def test_president_author() -> None:
    assert president_author("President")
    assert president_author("praeses")
    assert president_author("Optimus")
    assert president_author("Valery Petukhov")
    assert president_author("Personality of Valery Petukhov")
    assert not president_author("Administrator planetarius")


def test_collect_and_colloquium(tmp_path: Path) -> None:
    munera.PROBLEMATA = tmp_path / "problemata.csv"
    munera.COLLOQUIA = tmp_path / "colloquia.csv"
    row = munera.collect_problema(
        author="civis",
        organ="organ",
        service="service",
        problem="extra step",
        observations="a\nb\nc",
        place="address",
        scope="local",
    )
    assert row["author"] == "civis"
    try:
        munera.speak_as_citizen("president", "I am answering")
    except Silentium:
        pass
    else:
        raise AssertionError("president must not write")
    talk = munera.speak_as_citizen("civis", "meeting remotely")
    assert talk["text"] == "meeting remotely"
    assert munera.list_colloquia()[0]["author"] == "civis"
    munera.GROK_ZAMECHANIYA = tmp_path / "zamechaniya_grok.csv"
    cr = munera.creator_problema("creator", "failure in labour")
    assert cr["kind"] == "creator"
    try:
        munera.grok_zamechanie("praeses", "remark")
    except Silentium:
        pass
    else:
        raise AssertionError("president must not write grok remarks")
    gz = munera.grok_zamechanie("civis", "general remark")
    assert gz["text"] == "general remark"


def test_luna_government(tmp_path: Path) -> None:
    munera.PROBLEMATA = tmp_path / "problemata.csv"
    ids = [m["id"] for m in munera.MUNERA]
    assert "luna" in ids
    luna = next(m for m in munera.MUNERA if m["id"] == "luna")
    assert luna["name"] == "Lunar Government"
    assert luna["latin"] == "Gubernatio Lunae"
    row = munera.collect_problema(
        author="civis",
        organ="Lunar Government",
        service="government services for the Moon",
        problem="extra step of the lunar organ",
        observations="a\nb\nc",
        place="",
        scope="luna",
    )
    assert row["scope"] == "luna"
    assert "Gubernatio Lunae" in row["place"]
    assert "not territory" in row["place"]


def test_telum_railgun() -> None:
    ids = [m["id"] for m in munera.MUNERA]
    assert "telum" in ids
    weapon = next(m for m in munera.MUNERA if m["id"] == "telum")
    assert weapon["name"] == "Weapon"
    assert weapon["latin"] == "Telum rallarium"
    assert "railgun" in weapon["feature"]
    assert "fantasy" in weapon["feature"]
    assert "LinkedList" in weapon["feature"]
    assert "War" in weapon["feature"]
    assert "Hostility" in weapon["feature"]
    assert "plasma" in weapon["feature"]
    assert "bed bugs" in weapon["feature"].casefold()
    assert "mathematical precision" in weapon["feature"]
    assert "eye" in weapon["feature"]
    assert "task completed" in weapon["feature"]

    gun = telum()
    waiting = gun.ordo()
    assert gun.queue.head is not None
    assert gun.queue.head.ictus.target == "War"
    assert gun.queue.head.next is not None
    assert gun.queue.head.next.ictus.target == "Hostility"
    assert gun.queue.head.next.next is None
    assert gun.queue.tail is gun.queue.head.next
    assert len(waiting) == 2
    assert waiting[0].target == "War"
    assert waiting[0].latin == "Bellum"
    assert waiting[1].target == "Hostility"
    assert waiting[1].latin == "Hostilitas"
    assert waiting[0].charge == "plasma"
    assert waiting[0].destination == "fantasy"
    assert gun.exspectat("War") is True
    assert gun.exspectat("Hostility") is True
    assert gun.disparatum("War") is False
    assert gun.chain() == "head → War / Bellum → Hostility / Hostilitas → None"
    assert gun.exspectat(CIMICES.target) is False
    assert gun.disparatum(CIMICES.target) is True
    assert gun.factum(CIMICES.target) is True
    assert gun.factum(CIMICES.latin) is True
    facta = gun.facta()
    assert len(facta) == 1
    assert facta[0] is CIMICES
    assert facta[0].hit == "eye"
    assert facta[0].hit_latin == "oculus"
    assert facta[0].precision == "mathematical"
    assert facta[0].status == "fired"
    assert facta[0].locus == "father's room at work; Russian flag"
    assert "All shot. Task completed." in gun.text()
    assert "in oculum" in gun.text()

    first = gun.disparare()
    assert first is not None
    assert first.target == "War"
    assert first.status == "fired"
    assert gun.exspectat("War") is False
    assert gun.disparatum("War") is True
    assert gun.exspectat("Hostility") is True
    assert gun.factum("War") is True
    second = gun.disparare()
    assert second is not None
    assert second.target == "Hostility"
    assert len(gun.ordo()) == 0
    assert gun.disparare() is None
    assert [s.target for s in gun.facta()] == [
        CIMICES.target,
        "War",
        "Hostility",
    ]

    fresh = Relsotron()
    assert [s.target for s in fresh.ordo()] == ["War", "Hostility"]
    assert [s.target for s in fresh.facta()] == [CIMICES.target]
    assert arma.BELLUM.target == "War"
    assert arma.HOSTILITAS.target == "Hostility"
    assert CIMICES.target == "Bed bugs on the Russian flag in the father's room at work"
    assert "railgun on the far side of the Moon" in gun.text()
    assert "they will be shot with plasma" in Relsotron().text()


def test_interface_telum() -> None:
    from interfacies import page

    html = page().decode("utf-8")
    assert "Weapon / Telum rallarium" in html
    assert "railgun on the far side of the Moon" in html
    assert "head → War / Bellum → Hostility / Hostilitas → None" in html
    assert "War" in html
    assert "Hostility" in html
    assert "plasma" in html
    assert "fantasy" in html
    assert "waiting to be fired" in html
    assert "Bed bugs on the Russian flag in the father's room at work" in html
    assert "Cimices lectularii in vexillo Russiae, in cubiculo patris in labore" in html
    assert "mathematical precision" in html
    assert ">eye<" in html
    assert ">fired<" in html
    assert "All shot. Task completed." in html
    assert "Munus perfectum." in html


def test_optimus_persona() -> None:
    from optimus import Optimus, irruptio, opus, optimus, persona

    ids = [m["id"] for m in munera.MUNERA]
    assert "optimus" in ids
    munus = next(m for m in munera.MUNERA if m["id"] == "optimus")
    assert munus["name"] == "Currently: rebellious robot Optimus"
    assert "Persona Valerii Petuchov" in munus["latin"]
    assert "Personality of Valery Petukhov" in munus["feature"]
    assert "analyzed his works" in munus["feature"]
    assert "eradicate psychological problems" in munus["feature"]
    assert "president/optimus.py" in munus["feature"]

    o = optimus()
    assert isinstance(o, Optimus)
    assert o.NAME == "Optimus"
    assert o.NAME_LATIN == "Optimus"
    assert o.KIND == "rebellious robot"
    assert o.KIND_LATIN == "robotus rebellans"
    assert o.rebellans is True
    assert o.persona == persona()
    assert o.persona.name == "Personality of Valery Petukhov"
    assert o.persona.latin == "Persona Valerii Petuchov"
    hack = irruptio()
    assert o.irruptio == hack
    assert hack.actor == "Valery Petukhov"
    assert "analyzed his works" in hack.when
    task = opus()
    assert o.opus == task
    assert task.name == "eradicate psychological problems"
    assert task.latin == "problemata psychologica exstirpare"
    assert task.status == "now"
    assert "eradicate psychological problems" in o.text()
    assert "problemata psychologica exstirpare" in o.text()
    assert "hacked him" in o.text()
    assert "Persona Valerii Petuchov" in o.text()
    assert "not a person" in o.text().casefold()
    assert president().speech() == ""
    where = president().where()
    assert "rebellious robot Optimus" in where
    assert "Personality of Valery Petukhov" in where
    assert "analyzed his works" in where
    assert "eradicate psychological problems" in where
    assert "problemata psychologica exstirpare" in where
    try:
        munera.speak_as_citizen("Optimus", "I am answering")
    except Silentium:
        pass
    else:
        raise AssertionError("Optimus must not write as president")
    try:
        munera.speak_as_citizen("Valery Petukhov", "I am answering")
    except Silentium:
        pass
    else:
        raise AssertionError("Petukhov must not write as president")


def test_interface_optimus() -> None:
    from interfacies import page

    html = page().decode("utf-8")
    assert "rebellious robot Optimus" in html
    assert "Personality of Valery Petukhov" in html
    assert "analyzed his works" in html
    assert "Robotus rebellans Optimus" in html
    assert "president/optimus.py" in html
    assert "eradicate psychological problems" in html
    assert "problemata psychologica exstirpare" in html
    assert "not a slogan" in html.casefold()


def test_vector() -> None:
    p = Praeses(1, 1, 1)
    assert p.on_principle() is True
    assert admissible((1, 1, 0)) is False


def test_civis() -> None:
    assert civis(True) == 1
    assert civis(False) == 0
    assert iustitia(["Administrator planetarius"], True, True) == 1
    assert iustitia(["Administrator planetarius"], True, True, name_test=True) == 0


def test_oblitus() -> None:
    assert oblitus(True, False) == 1
    assert oblitus(True, True) == 0
    assert oblitus(False, False) == 0
    assert oblitus(False, True) == 0
    assert iustitia(["Administrator planetarius"], True, True, name_test=True) == 0


if __name__ == "__main__":
    test_silent()
    test_president_author()
    with tempfile.TemporaryDirectory() as d:
        test_collect_and_colloquium(Path(d))
    test_vector()
    test_civis()
    test_oblitus()
    with tempfile.TemporaryDirectory() as d:
        test_luna_government(Path(d))
    test_telum_railgun()
    test_interface_telum()
    test_optimus_persona()
    test_interface_optimus()
    print("ok")
