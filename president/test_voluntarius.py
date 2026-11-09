"""Subdivision «информационные волонтер»: collection of information about a problem."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import munera
import voluntarius
from princip import ROLES


class VolunteerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.journal = Path(self.temporary.name) / "informationes.csv"
        self.patch = patch.object(voluntarius, "INFORMATIONES", self.journal)
        self.patch.start()
        self.addCleanup(self.patch.stop)

    def record(self, **changes: object) -> dict[str, str]:
        data: dict[str, object] = {
            "author": "Создатель",
            "phrase": "сбор информации о проблеме",
            "problema": "Местный дефект органа.",
            "informatio": "Наблюдение о дефекте.",
            "principle": (1, 1, 1),
        }
        data.update(changes)
        return voluntarius.conquirere(**data)

    def test_standing_function(self) -> None:
        row = voluntarius.officium()
        self.assertEqual(voluntarius.NAME, "информационные волонтер")
        self.assertEqual(voluntarius.NAME_EN, "Information Volunteer")
        self.assertEqual(voluntarius.NAME_LATIN, "Subdivisio voluntarii informationis")
        self.assertEqual(voluntarius.PHRASE, "сбор информации о проблеме")
        self.assertEqual(row["officium_ru"], "Сбор информации о проблеме.")
        self.assertEqual(row["officium_latin"], "Collectio informationis de problemate.")
        organ = next(item for item in munera.MUNERA if item["id"] == "voluntarius")
        self.assertIn(voluntarius.NAME, organ["name"])
        self.assertEqual(organ["latin"], voluntarius.NAME_LATIN)
        self.assertIn("сбор информации о проблеме", organ["feature"])
        self.assertNotIn("voluntarius", {role["id"] for role in ROLES})
        root = HERE.parent
        for name in ("AGENTS.md", "README.md"):
            document = (root / name).read_text(encoding="utf-8")
            self.assertIn(voluntarius.NAME, document)
            self.assertIn(voluntarius.NAME_LATIN, document)
            self.assertIn(voluntarius.OFFICIUM_RU, document)
            self.assertIn(voluntarius.PHRASE, document)
            self.assertIn("Collectio informationis de problemate", document)

    def test_phrase_records_the_collection(self) -> None:
        row = self.record(phrase="  Сбор   информации   о   проблеме ")
        self.assertEqual(row["phrase"], "сбор информации о проблеме")
        self.assertEqual(row["problema"], "Местный дефект органа.")
        self.assertEqual(row["informatio"], "Наблюдение о дефекте.")
        self.assertEqual(row["decision"], "collecta")
        self.assertEqual((row["L"], row["J"], row["V"]), ("1", "1", "1"))

    def test_other_phrases_and_bad_vectors_record_nothing(self) -> None:
        with self.assertRaises(ValueError):
            self.record(phrase="информация")
        with self.assertRaises(ValueError):
            self.record(principle=(1, 1, 0))
        with self.assertRaises(munera.Silentium):
            self.record(author="президент")
        self.assertEqual(voluntarius.list_informationes(), [])

    def test_page_shows_the_subdivision(self) -> None:
        from interfacies import page

        self.record(problema="Дефект канала.", informatio="Сведения о канале.")
        html = page().decode("utf-8")
        self.assertIn("Подразделение «информационные волонтер»", html)
        self.assertIn(voluntarius.NAME_LATIN, html)
        self.assertIn(voluntarius.OFFICIUM_RU, html)
        self.assertIn(voluntarius.OFFICIUM_LATIN, html)
        self.assertIn('action="/conquirere"', html)
        self.assertIn('id="voluntarius"', html)
        self.assertIn("Дефект канала.", html)
        self.assertIn("Сведения о канале.", html)
        self.assertIn("информация собрана", html)


if __name__ == "__main__":
    unittest.main()
