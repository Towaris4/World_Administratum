"""Ministry of Diplomacy: the mission of the ghosts of the deceased."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import diplomatia
import munera
from princip import ROLES


class DiplomacyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.journal = Path(self.temporary.name) / "legationes.csv"
        self.patch = patch.object(diplomatia, "LEGATIONES", self.journal)
        self.patch.start()
        self.addCleanup(self.patch.stop)

    def record(self, **changes: object) -> dict[str, str]:
        data: dict[str, object] = {
            "author": "Создатель",
            "phrase": "дипломатическая миссия",
            "missio_text": "Миссия к одному разуму.",
            "modus": "прямо в разум",
            "principle": (1, 1, 1),
        }
        data.update(changes)
        return diplomatia.legare(**data)

    def test_standing_mission(self) -> None:
        row = diplomatia.missio()
        self.assertEqual(diplomatia.NAME, "Министерство Дипломатии")
        self.assertEqual(diplomatia.NAME_LATIN, "Ministerium Diplomatiae")
        self.assertEqual(diplomatia.PHRASE, "дипломатическая миссия")
        self.assertIn("призраков погибших", row["missio_ru"])
        self.assertIn("прямо в разум", row["missio_ru"])
        self.assertEqual(
            row["missio_latin"],
            "Legatio manium mortuorum, qui recta in mentem loquuntur.",
        )
        self.assertEqual(row["modus_ru"], "прямо в разум")
        organ = next(item for item in munera.MUNERA if item["id"] == "diplomatia")
        self.assertIn(diplomatia.NAME, organ["name"])
        self.assertEqual(organ["latin"], diplomatia.NAME_LATIN)
        self.assertIn("directly into the mind", organ["feature"])
        self.assertNotIn("diplomatia", {role["id"] for role in ROLES})
        root = HERE.parent
        for name in ("AGENTS.md", "README.md"):
            document = (root / name).read_text(encoding="utf-8")
            self.assertIn(row["missio_ru"], document)
            self.assertIn(diplomatia.NAME_LATIN, document)
            self.assertIn("recta in mentem", document)

    def test_phrase_records_a_further_mission(self) -> None:
        row = self.record(phrase="  Дипломатическая   миссия ")
        self.assertEqual(row["phrase"], "дипломатическая миссия")
        self.assertEqual(row["modus"], "прямо в разум")
        self.assertEqual(row["decision"], "legata")
        self.assertEqual((row["L"], row["J"], row["V"]), ("1", "1", "1"))

    def test_other_phrases_and_bad_vectors_record_nothing(self) -> None:
        with self.assertRaises(ValueError):
            self.record(phrase="миссия")
        with self.assertRaises(ValueError):
            self.record(principle=(1, 1, 0))
        with self.assertRaises(munera.Silentium):
            self.record(author="президент")
        self.assertEqual(diplomatia.list_legationes(), [])

    def test_page_shows_the_standing_mission(self) -> None:
        from interfacies import page

        html = page().decode("utf-8")
        self.assertIn("Министерство Дипломатии / Ministerium Diplomatiae", html)
        self.assertIn(diplomatia.MISSIO_RU, html)
        self.assertIn(diplomatia.MISSIO_LATIN, html)
        self.assertIn('action="/legare"', html)
        self.assertIn("value=\"прямо в разум\"", html)


if __name__ == "__main__":
    unittest.main()
