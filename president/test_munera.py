"""Silent president: functions without speech."""

from __future__ import annotations

import tempfile
from pathlib import Path

import munera
from munera import Silentium, president_author, silere
from praeses import Praeses, president
from princip import admissible


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
    assert president_author("Президент")
    assert president_author("praeses")
    assert not president_author("Administrator planetarius")


def test_collect_and_colloquium(tmp_path: Path) -> None:
    munera.PROBLEMATA = tmp_path / "problemata.csv"
    munera.COLLOQUIA = tmp_path / "colloquia.csv"
    row = munera.collect_problema(
        author="civis",
        organ="орган",
        service="услуга",
        problem="лишний шаг",
        observations="a\nb\nc",
        place="адрес",
        scope="local",
    )
    assert row["author"] == "civis"
    try:
        munera.speak_as_citizen("президент", "я отвечаю")
    except Silentium:
        pass
    else:
        raise AssertionError("president must not write")
    talk = munera.speak_as_citizen("civis", "встреча дистанционно")
    assert talk["text"] == "встреча дистанционно"
    assert munera.list_colloquia()[0]["author"] == "civis"
    munera.GROK_ZAMECHANIYA = tmp_path / "zamechaniya_grok.csv"
    cr = munera.creator_problema("созидатель", "сбой в труде")
    assert cr["kind"] == "созидатель"
    try:
        munera.grok_zamechanie("praeses", "замечание")
    except Silentium:
        pass
    else:
        raise AssertionError("president must not write grok remarks")
    gz = munera.grok_zamechanie("civis", "общее замечание")
    assert gz["text"] == "общее замечание"


def test_vector() -> None:
    p = Praeses(1, 1, 1)
    assert p.on_principle() is True
    assert admissible((1, 1, 0)) is False


if __name__ == "__main__":
    test_silent()
    test_president_author()
    with tempfile.TemporaryDirectory() as d:
        test_collect_and_colloquium(Path(d))
    test_vector()
    print("ok")
