"""Silent president: functions without speech."""

from __future__ import annotations

import tempfile
from pathlib import Path

import arma
import munera
from arma import CIMICES, PETITIO_SOLIS, Relsotron, telum
from munera import Silentium, president_author, silere
from praeses import Praeses, president
from princip import ROLES, admissible, civis, iustitia, oblitus, roles_held, vicecomes


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
    munera.ZAMECHANIYA = tmp_path / "zamechaniya.csv"
    cr = munera.creator_problema("creator", "failure in labour")
    assert cr["kind"] == "creator"
    try:
        munera.zamechanie("praeses", "remark")
    except Silentium:
        pass
    else:
        raise AssertionError("president must not write general remarks")
    gz = munera.zamechanie("civis", "general remark")
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
    assert "Hostility is removed" in weapon["feature"]
    assert "controlled magnetic field" in weapon["feature"]
    assert "spherical segment of the planet" in weapon["feature"]
    assert "not a shot" in weapon["feature"]
    assert "not fired" in weapon["feature"]
    assert "plasma" in weapon["feature"]
    assert "bed bugs" in weapon["feature"].casefold()
    assert "mathematical precision" in weapon["feature"]
    assert "eye" in weapon["feature"]
    assert "task completed" in weapon["feature"]

    gun = telum()
    waiting = gun.ordo()
    assert gun.queue.head is not None
    assert gun.queue.head.ictus.target == "War"
    assert gun.queue.head.next is None
    assert gun.queue.tail is gun.queue.head
    assert len(waiting) == 1
    assert waiting[0].target == "War"
    assert waiting[0].latin == "Bellum"
    assert waiting[0].charge == "plasma"
    assert waiting[0].destination == "fantasy"
    assert gun.exspectat("War") is True
    assert gun.exspectat("Hostility") is False
    assert gun.disparatum("War") is False
    assert gun.disparatum("Hostility") is False
    assert gun.sublatum("Hostility") is True
    assert gun.sublatum("Hostilitas") is True
    assert gun.factum("Hostility") is False
    assert gun.chain() == "head → War / Bellum → None"
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
    assert facta[0].locus == "father's room at work"
    assert "All shot. Task completed." in gun.text()
    assert "in oculum" in gun.text()
    assert "Hostility is removed: Hostility / Hostilitas. Not fired." in gun.text()
    assert "Magnetic waves of the Intelligent Sun removed it." in gun.text()
    assert gun.petitiones() == (PETITIO_SOLIS,)
    assert gun.petita("spherical segment of the planet") is True
    assert gun.petita("controlled magnetic field") is True
    assert gun.petita(PETITIO_SOLIS.phrase) is True
    assert gun.exspectat("spherical segment of the planet") is False
    assert gun.factum("controlled magnetic field") is False
    assert gun.disparatum(PETITIO_SOLIS.locus) is False
    assert PETITIO_SOLIS.phrase in gun.text()
    assert "Not a shot. Not fired." in gun.text()
    assert "campus magneticus gubernabilis" in gun.text()
    assert PETITIO_SOLIS.status == "recorded"
    root = Path(__file__).resolve().parent.parent
    agents = (root / "AGENTS.md").read_text(encoding="utf-8")
    readme = (root / "README.md").read_text(encoding="utf-8")
    assert PETITIO_SOLIS.phrase in agents
    assert PETITIO_SOLIS.phrase in readme
    assert "segmentum sphaericum planetae" in agents
    assert "segmentum sphaericum planetae" in readme

    first = gun.disparare()
    assert first is not None
    assert first.target == "War"
    assert first.status == "fired"
    assert gun.exspectat("War") is False
    assert gun.disparatum("War") is True
    assert gun.factum("War") is True
    assert gun.disparare() is None
    assert len(gun.ordo()) == 0
    assert [s.target for s in gun.facta()] == [
        CIMICES.target,
        "War",
    ]
    assert gun.sublatum("Hostility") is True

    fresh = Relsotron()
    assert [s.target for s in fresh.ordo()] == ["War"]
    assert [s.target for s in fresh.facta()] == [CIMICES.target]
    assert [s.target for s in fresh.sublata()] == ["Hostility"]
    assert arma.BELLUM.target == "War"
    assert arma.HOSTILITAS.target == "Hostility"
    assert arma.HOSTILITAS.latin == "Hostilitas"
    assert arma.HOSTILITAS.status == "removed"
    assert arma.HOSTILITAS.charge == "magnetic wave"
    assert CIMICES.target == "Bed bugs in the father's room at work"
    assert "railgun on the far side of the Moon" in gun.text()
    assert "it will be shot with plasma" in Relsotron().text()


def test_planeta_hominibus() -> None:
    from princip import (
        AXIOMA,
        AXIOMA_LATIN,
        AXIOMA_RU,
        AXIOMA_ZH,
        INSTRUMENTUM,
        INSTRUMENTUM_LATIN,
        INSTRUMENTUM_ZH,
        ONU_REFACTOR,
        ONU_REFACTOR_LATIN,
        ONU_REFACTOR_RU,
        ONU_REFACTOR_ZH,
        PHYSICE,
        PHYSICE_LATIN,
        PHYSICE_RU,
        PHYSICE_ZH,
        PLANETA,
        PLANETA_LATIN,
        PLANETA_ZH,
        SERVITIA_ZH,
        SPATIUM,
        SPATIUM_LATIN,
        SPATIUM_RU,
        SPATIUM_ZH,
        axioma,
        planeta_hominibus,
        text,
    )
    from interfacies import page

    assert planeta_hominibus() == 1
    assert axioma() == 1
    body = text()
    assert SPATIUM in body
    assert SPATIUM_RU in body
    assert SPATIUM_LATIN in body
    assert PHYSICE in body
    assert PHYSICE_RU in body
    assert PHYSICE_LATIN in body
    assert "The 0 State of Liberty" in body
    assert "World digital administration" not in body
    assert "Virtual state" not in body
    assert PLANETA in body
    assert PLANETA_LATIN in body
    assert INSTRUMENTUM in body
    assert INSTRUMENTUM_LATIN in body
    assert ONU_REFACTOR in body
    assert ONU_REFACTOR_RU in body
    assert ONU_REFACTOR_LATIN in body
    assert AXIOMA in body
    assert AXIOMA_RU in body
    assert AXIOMA_ZH in body
    assert AXIOMA_LATIN in body
    assert SPATIUM_ZH in body
    assert PHYSICE_ZH in body
    assert PLANETA_ZH in body
    assert SERVITIA_ZH in body
    assert INSTRUMENTUM_ZH in body
    assert ONU_REFACTOR_ZH in body
    root = Path(__file__).resolve().parent.parent
    for name in ("README.md", "AGENTS.md", "lab/Lab_work_1.md"):
        doc = (root / name).read_text(encoding="utf-8")
        assert SPATIUM in doc
        assert SPATIUM_RU in doc
        assert SPATIUM_LATIN in doc
        assert PHYSICE in doc
        assert PHYSICE_RU in doc
        assert PHYSICE_LATIN in doc
        assert "The 0 State of Liberty" in doc
        assert "World digital administration" not in doc
        assert "Virtual state" not in doc
        assert "The planet belongs to people" in doc
        assert "tool for fixing bugs of the system" in doc
        assert "The UN is one of the refactoring tools." in doc
        assert "ООН — один из инструментов рефакторинга." in doc
        assert "Nationes Unitae sunt unum ex instrumentis refactorisationis." in doc
        assert AXIOMA in doc
        assert AXIOMA_RU in doc
        assert AXIOMA_ZH in doc
        assert AXIOMA_LATIN in doc
        assert SPATIUM_ZH in doc
        assert PHYSICE_ZH in doc
        assert PLANETA_ZH in doc
        assert INSTRUMENTUM_ZH in doc
        assert ONU_REFACTOR_ZH in doc
    html = page().decode("utf-8")
    assert SPATIUM in html
    assert SPATIUM_RU in html
    assert SPATIUM_LATIN in html
    assert PHYSICE in html
    assert PHYSICE_RU in html
    assert PHYSICE_LATIN in html
    assert "The 0 State of Liberty" in html
    assert "World digital administration" not in html
    assert "Virtual state" not in html
    assert "The planet belongs to people." in html
    assert "Planeta hominibus pertinet." in html
    assert "World Administratum is a tool for fixing bugs of the system." in html
    assert "Mundus Administratum est instrumentum ad vitia systematis emendanda." in html
    assert "The UN is one of the refactoring tools." in html
    assert "ООН — один из инструментов рефакторинга." in html
    assert "Nationes Unitae sunt unum ex instrumentis refactorisationis." in html
    assert AXIOMA in html
    assert AXIOMA_RU in html
    assert AXIOMA_ZH in html
    assert AXIOMA_LATIN in html
    assert SPATIUM_ZH in html
    assert PHYSICE_ZH in html
    assert PLANETA_ZH in html
    assert SERVITIA_ZH in html
    assert INSTRUMENTUM_ZH in html
    assert ONU_REFACTOR_ZH in html


def test_interface_scp_header() -> None:
    from interfacies import page

    html = page().decode("utf-8")
    top = html.split("<header class=\"top\">", 1)[0]
    assert "Open Creative Project" in top
    readme = Path(__file__).resolve().parent.parent.joinpath("README.md").read_text(encoding="utf-8")
    assert "Open Creative Project" in readme
    assert "SCP" not in top
    assert "Item #:" in top
    assert "Item #:</span> Π" in top
    assert "Object Class:" in top
    assert "Explained" in top
    assert "Not a rank." in top
    assert "Special Containment Procedures:" in top
    assert "Knowledge of the name is not obligatory." in top
    assert "Description:" in top
    assert "Mundus Administratum" in top
    assert "LOGICA, IUSTITIA ET VERITAS" in top
    assert "Level" not in top


def test_interface_telum() -> None:
    from interfacies import page

    html = page().decode("utf-8")
    assert "Weapon / Telum rallarium" in html
    assert "railgun on the far side of the Moon" in html
    assert "head → War / Bellum → None" in html
    assert "War and Hostility" not in html
    assert "<td>Hostility</td>" not in html
    assert "<td><em>Hostilitas</em></td>" not in html
    assert "Hostility / <em>Hostilitas</em> is removed. Not fired." in html
    assert "Magnetic waves of the Intelligent Sun removed hostility." in html
    assert "controlled magnetic field in a spherical segment of the planet" in html
    assert PETITIO_SOLIS.phrase in html
    assert "campus magneticus gubernabilis" in html
    assert "segmentum sphaericum planetae" in html
    assert ">recorded<" in html
    assert "it will be shot with plasma" in html
    assert "War" in html
    assert "plasma" in html
    assert "fantasy" in html
    assert "waiting to be fired" in html
    assert "Bed bugs in the father's room at work" in html
    assert "Cimices lectularii in cubiculo patris in labore" in html
    assert "mathematical precision" in html
    assert ">eye<" in html
    assert ">fired<" in html
    assert "All shot. Task completed." in html
    assert "Munus perfectum." in html


def test_sol_waves() -> None:
    from interfacies import page
    from praeses import president
    from sol import aequilibrium, restituere, sol

    ids = [m["id"] for m in munera.MUNERA]
    assert "sol" in ids
    sun = next(m for m in munera.MUNERA if m["id"] == "sol")
    assert sun["name"] == "Intelligent Sun / Разумное солнце"
    assert sun["latin"] == "Sol intelligens"
    assert "magnetic waves" in sun["feature"]
    assert "balance of justice" in sun["feature"]
    assert "Hostilitas=0" in sun["feature"]
    assert "then A=J" in sun["feature"]

    assert aequilibrium(1, 1) == 0
    assert aequilibrium(1, 0) == 1
    assert aequilibrium(0, 0) == 0
    assert aequilibrium(0, 1) == 0
    assert restituere(1) == {"hostilitas": 0, "J": 1, "aequilibrium": 1}
    assert restituere(0) == {"hostilitas": 0, "J": 0, "aequilibrium": 0}
    for bad in (2, -1, True, False):
        try:
            restituere(bad)  # type: ignore[arg-type]
        except ValueError:
            pass
        else:
            raise AssertionError(f"restituere accepted {bad!r}")
    body = sol().text()
    assert "Разумное солнце" in body
    assert "Sol intelligens" in body
    assert "does not write L, J, or V" in body
    assert "Then A = J." in body

    root = Path(__file__).resolve().parent.parent
    readme = (root / "README.md").read_text(encoding="utf-8")
    agents = (root / "AGENTS.md").read_text(encoding="utf-8")
    assert "Sol intelligens" in readme
    assert "Разумное солнце" in readme
    assert "undae magneticae" in readme
    assert "Hostility (Hostilitas) is removed" in agents
    assert "Sol intelligens" in agents
    assert "aequilibrium iustitiae restituunt" in agents

    J = president().P[1]
    html = page().decode("utf-8")
    assert "Intelligent Sun / Разумное солнце" in html
    assert f"Before the wave, hostility is present: balance = {aequilibrium(J, 1)}." in html
    done = restituere(J)
    assert f"Hostilitas = {done['hostilitas']}" in html
    assert f"J = {done['J']}" in html
    assert f"Balance of justice = {done['aequilibrium']}" in html
    assert "A = 1 iff J = 1 and Hostilitas = 0." in html
    assert "After the wave, A = J." in html
    state = sol().state(1)
    assert state["before"] == 0
    assert state["aequilibrium"] == 1
    assert state["hostilitas"] == 0


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


def test_mvp() -> None:
    from interfacies import page
    from mvp import NAMED, NAMED_RU, SENTENTIA_EN, SENTENTIA_LA, SENTENTIA_RU, record, text
    from princip import ROLES

    ids = [m["id"] for m in munera.MUNERA]
    assert "mvp" in ids
    munus = next(m for m in munera.MUNERA if m["id"] == "mvp")
    assert munus["name"] == "MVP corporation"
    assert munus["latin"] == "Corporatio MVP"
    assert "Vanya Tarasov" in munus["feature"]
    assert "Sasha Semenov" in munus["feature"]
    assert "not a rank" in munus["feature"]
    assert "president/mvp.py" in munus["feature"]
    assert "mvp" not in {role["id"] for role in ROLES}

    fact = record()
    assert fact["begun"] is True
    assert fact["rank"] is False
    assert fact["role"] is False
    assert fact["named"] == NAMED == ("Vanya Tarasov", "Sasha Semenov")
    assert fact["named_ru"] == NAMED_RU == ("Ваня Тарасов", "Саша Семенов")
    body = text()
    assert SENTENTIA_RU in body
    assert SENTENTIA_EN in body
    assert SENTENTIA_LA in body
    assert "The president remains silent." in body

    root = Path(__file__).resolve().parent.parent
    readme = (root / "README.md").read_text(encoding="utf-8")
    agents = (root / "AGENTS.md").read_text(encoding="utf-8")
    lab = (root / "lab" / "Lab_work_1.md").read_text(encoding="utf-8")
    for doc in (readme, agents, lab):
        assert "Vanya Tarasov" in doc or "Ваня Тарасов" in doc
        assert "Sasha Semenov" in doc or "Саша Семенов" in doc
        assert "MVP" in doc
    assert "Corporatio MVP" in readme
    assert "Initium corporationis MVP" in agents
    assert "mvp" in agents

    html = page().decode("utf-8")
    assert SENTENTIA_RU in html
    assert SENTENTIA_LA in html
    assert "Corporatio MVP" in html
    assert president().speech() == ""


def test_transmissio() -> None:
    from interfacies import page
    from transmissio import (
        SENTENTIA_EN,
        SENTENTIA_LA,
        SENTENTIA_RU,
        UNIVERSE,
        YEAR,
        record,
        text,
    )

    ids = [m["id"] for m in munera.MUNERA]
    assert "transmissio" in ids
    munus = next(m for m in munera.MUNERA if m["id"] == "transmissio")
    assert munus["name"] == "Transmission of the information"
    assert munus["latin"] == "Transmissio informationis"
    assert "Andron collider" in munus["feature"]
    assert "2033" in munus["feature"]
    assert UNIVERSE in munus["feature"]
    assert "Vanya Tarasov" in munus["feature"]
    assert "виски" in munus["feature"]
    assert "not a rank" in munus["feature"]
    assert "president/transmissio.py" in munus["feature"]

    fact = record()
    assert fact["year"] == YEAR == 2033
    assert fact["universe"] == UNIVERSE == "48195230959032523234932492"
    assert fact["celeritas_lucis_superata"] is True
    assert fact["nuntium_in_praeteritum"] is True
    assert fact["tempora_calibrata"] is True
    assert fact["rank"] is False
    assert fact["collider_ru"] == "Андронный колайдер"
    body = text()
    assert SENTENTIA_RU in body
    assert SENTENTIA_EN in body
    assert SENTENTIA_LA in body
    assert "Praeses" not in body or "silent" in body
    assert "Андронного колайдера 2033 года" in SENTENTIA_RU
    assert "вычислительный органоид Вани Тарасова" in SENTENTIA_RU
    assert "виски были откалиброваны" in SENTENTIA_RU
    assert "Collisatore Andronio" in SENTENTIA_LA
    assert "organoidem computatorium Vaniae Tarasov" in SENTENTIA_LA

    root = Path(__file__).resolve().parent.parent
    readme = (root / "README.md").read_text(encoding="utf-8")
    agents = (root / "AGENTS.md").read_text(encoding="utf-8")
    lab = (root / "lab" / "Lab_work_1.md").read_text(encoding="utf-8")
    for doc in (readme, agents, lab):
        assert "48195230959032523234932492" in doc
        assert "Андронного колайдера" in doc or "Андронный колайдер" in doc
        assert "Вани Тарасова" in doc or "Vanya Tarasov" in doc
    assert "Transmissio informationis" in readme
    assert "transmissio" in agents
    assert "celeritas lucis superata" in agents

    html = page().decode("utf-8")
    assert SENTENTIA_RU in html
    assert SENTENTIA_LA in html
    assert "Transmissio informationis" in html
    assert president().speech() == ""


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


def test_roles_match_description() -> None:
    ids = [role["id"] for role in ROLES]
    assert ids == ["civis", "diplomaticus", "arbiter", "creator", "vicecomes", "oblitus"]
    by_id = {role["id"]: role for role in ROLES}
    assert by_id["civis"]["name"] == "Citizenship / Гражданство"
    assert by_id["civis"]["latin"] == "Civis"
    assert by_id["civis"]["held"] == "existence"
    assert by_id["diplomaticus"]["name"] == "Diplomat / Meliorator"
    assert by_id["diplomaticus"]["latin"] == "Diplomaticus vocis"
    assert "Warrior" not in by_id["diplomaticus"]["name"]
    assert "one role" in by_id["diplomaticus"]["what"]
    assert by_id["arbiter"]["latin"] == "Arbiter praesens"
    assert by_id["arbiter"]["held"] == "choice"
    assert by_id["creator"]["latin"] == "Homo laborans creator"
    assert by_id["vicecomes"]["name"] == "Sheriff / Шериф"
    assert by_id["vicecomes"]["latin"] == "Vicecomes qui vitium animadvertit"
    assert by_id["vicecomes"]["held"] == "notice"
    assert "noticed the bug" in by_id["vicecomes"]["what"]
    assert vicecomes(True, True) == 1
    assert vicecomes(True, False) == 0
    assert vicecomes(False, True) == 0
    assert by_id["oblitus"]["latin"] == "Oblitus qui hoc nescit"
    assert by_id["oblitus"]["held"] == "unknowing"
    assert roles_held(False, False, ["diplomaticus", "civis"]) == ()
    assert roles_held(True, True) == ("civis",)
    assert roles_held(True, False) == ("civis", "oblitus")
    assert roles_held(True, True, ["diplomaticus", "arbiter", "civis", "oblitus"]) == (
        "civis",
        "diplomaticus",
        "arbiter",
    )
    assert roles_held(True, True, ["vicecomes"], noticed_bug=False) == ("civis",)
    assert roles_held(True, False, noticed_bug=True) == ("civis", "vicecomes", "oblitus")
    assert roles_held(False, False, noticed_bug=True) == ()
    root = Path(__file__).resolve().parent.parent
    readme = (root / "README.md").read_text(encoding="utf-8")
    agents = (root / "AGENTS.md").read_text(encoding="utf-8")
    register = (root / "dolzhnosti.csv").read_text(encoding="utf-8")
    lab = (root / "lab" / "Lab_work_1.md").read_text(encoding="utf-8")
    assert "**Citizenship** / **Гражданство**" in readme
    assert "| **Civis** |" in readme
    assert "**Diplomat** / **Meliorator**" in readme
    assert "**Diplomat** / **Warrior**" not in readme
    assert "Articuli arbitri" not in readme
    assert "The arbiter creates the solution to the problem" in readme
    assert "Citizenship / Гражданство (Civis) is a role" in agents
    assert "Together with Citizenship, the roles are:" in agents
    assert "Citizenship;Diplomat / Meliorator;Arbiter;Creator" in register
    assert "Civis;Diplomaticus vocis;Arbiter praesens;Homo laborans creator" in register
    assert "Citizenship;Forgotten" in register
    assert "Citizenship;Sheriff / Шериф" in register
    assert "Vicecomes qui vitium animadvertit" in register
    assert "Vicecomes qui vitium animadvertit" in readme
    assert "the sheriff is the one who noticed the bug" in agents.casefold()
    assert "noticed the bug" in lab.casefold()
    assert "Гражданство" in lab
    onu = next(item for item in munera.MUNERA if item["id"] == "onu")
    assert onu["latin"] == (
        "Problemata mundi solvuntur cum Nationibus Unitis "
        "et cum omnibus ducibus religiosis, consensu Nationum Unitarum"
    )
    assert onu["latin"] in readme
    assert "the UN is one of the refactoring tools" in onu["feature"]


def test_interface_roles() -> None:
    from interfacies import page

    html = page().decode("utf-8")
    assert "Offices — social roles" in html
    assert "Citizenship / Гражданство" in html
    assert "Diplomat / Meliorator" in html
    assert "Diplomaticus vocis" in html
    assert "by existence; not an application" in html
    assert "Arbiter praesens" in html
    assert "Homo laborans creator" in html
    assert "Oblitus qui hoc nescit" in html
    assert "Sheriff / Шериф" in html
    assert "Vicecomes qui vitium animadvertit" in html
    assert "by noticing a bug; not an application" in html
    assert "Diplomat / Warrior" not in html
    assert "Citizenship (Гражданство, Civis) is a role held by existence" in html


if __name__ == "__main__":
    test_silent()
    test_president_author()
    with tempfile.TemporaryDirectory() as d:
        test_collect_and_colloquium(Path(d))
    test_vector()
    test_civis()
    test_oblitus()
    test_roles_match_description()
    test_interface_roles()
    with tempfile.TemporaryDirectory() as d:
        test_luna_government(Path(d))
    test_telum_railgun()
    test_planeta_hominibus()
    test_interface_scp_header()
    test_interface_telum()
    test_sol_waves()
    test_mvp()
    test_transmissio()
    test_optimus_persona()
    test_interface_optimus()
    print("ok")
