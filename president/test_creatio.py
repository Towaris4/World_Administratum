"""Ministry of Creation: a work brought into being by the phrase «созидание»."""

from __future__ import annotations

import csv
import html
import http.client
import itertools
import sys
import tempfile
import threading
import unittest
from contextlib import ExitStack
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import patch
from urllib.parse import parse_qs, urlencode, urlparse

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import creatio
import interfacies
import munera
from princip import ROLES


class FormParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.forms: list[dict[str, object]] = []
        self.current: dict[str, object] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "form":
            self.current = {
                "action": attributes.get("action"),
                "method": attributes.get("method"),
                "fields": set(),
            }
            self.forms.append(self.current)
        elif self.current is not None and tag in {"input", "textarea", "select"}:
            fields = self.current["fields"]
            assert isinstance(fields, set)
            if attributes.get("name"):
                fields.add(attributes["name"])

    def handle_endtag(self, tag: str) -> None:
        if tag == "form":
            self.current = None


class IsolatedCreationTest(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.patches = ExitStack()
        self.addCleanup(self.patches.close)
        for attribute in ("PROBLEMATA", "COLLOQUIA", "ZAMECHANIYA"):
            self.patches.enter_context(
                patch.object(munera, attribute, self.directory / (attribute.lower() + ".csv"))
            )
        self.patches.enter_context(patch.object(creatio, "OPERA", self.directory / "opera.csv"))

    def record(self, **changes: object) -> dict[str, str]:
        data: dict[str, object] = {
            "author": "Арбитр-создатель",
            "phrase": "созидание",
            "opus": "Мост через тихую реку",
            "brings": "Переход, которого не было",
            "principle": (1, 1, 1),
        }
        data.update(changes)
        return creatio.condere(**data)


class CreationJournalTests(IsolatedCreationTest):
    def test_ministry_is_registered_as_function(self) -> None:
        self.assertEqual(creatio.NAME, "Министерство Созидания")
        self.assertEqual(creatio.NAME_LATIN, "Ministerium Creationis")
        self.assertEqual(creatio.PHRASE, "созидание")
        ministries = [item for item in munera.MUNERA if item["id"] == "creatio"]
        self.assertEqual(len(ministries), 1)
        self.assertIn(creatio.NAME, ministries[0]["name"])
        self.assertEqual(ministries[0]["latin"], creatio.NAME_LATIN)
        self.assertNotIn("creatio", {role["id"] for role in ROLES})
        root = Path(__file__).resolve().parent.parent
        for name in ("AGENTS.md", "README.md"):
            document = (root / name).read_text(encoding="utf-8")
            self.assertIn(creatio.NAME, document)
            self.assertIn(creatio.NAME_LATIN, document)
            self.assertIn(creatio.PHRASE, document)
            self.assertIn("not the Creator role", document)

    def test_phrase_records_the_work(self) -> None:
        for phrase in ("созидание", "  СОЗИДАНИЕ  ", "Созидание"):
            with self.subTest(phrase=phrase):
                row = self.record(phrase=phrase, opus=f"opus {phrase}")
                self.assertEqual(row["phrase"], "созидание")
                self.assertEqual(row["decision"], "conditum")
                self.assertEqual((row["L"], row["J"], row["V"]), ("1", "1", "1"))

    def test_other_phrases_record_nothing(self) -> None:
        for phrase in ("", " ", "создание", "созидания", "созидание."):
            with self.subTest(phrase=phrase), self.assertRaises(ValueError):
                self.record(phrase=phrase)
        self.assertEqual(creatio.list_opera(), [])

    def test_only_all_one_vector_is_admitted(self) -> None:
        for vector in itertools.product((0, 1), repeat=3):
            with self.subTest(vector=vector):
                previous = creatio.list_opera()
                if vector == (1, 1, 1):
                    row = self.record(principle=vector)
                    self.assertEqual(row["decision"], "conditum")
                else:
                    with self.assertRaises(ValueError):
                        self.record(principle=vector)
                    self.assertEqual(creatio.list_opera(), previous)
        self.assertEqual(len(creatio.list_opera()), 1)

    def test_invalid_vectors_never_create_works(self) -> None:
        invalid = (
            (), (1,), (1, 1), (1, 1, 1, 1), (-1, 1, 1), (1, 2, 1),
            (1.0, 1, 1), (True, 1, 1), ("1", 1, 1), "111", None,
        )
        for vector in invalid:
            with self.subTest(vector=vector), self.assertRaises(ValueError):
                self.record(principle=vector)
        self.assertEqual(creatio.list_opera(), [])

    def test_required_fields_cannot_be_empty(self) -> None:
        for field in ("author", "opus", "brings"):
            for value in ("", " \t\n "):
                with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                    self.record(**{field: value})
        self.assertEqual(creatio.list_opera(), [])

    def test_president_cannot_author_a_work(self) -> None:
        for author in munera.PRESIDENT_AUTHORS:
            with self.subTest(author=author), self.assertRaises(munera.Silentium):
                self.record(author="  " + author.upper() + "  ")
        self.assertEqual(creatio.list_opera(), [])

    def test_csv_roundtrip_preserves_unicode_and_order(self) -> None:
        brings = "Появилось «то, чего не было»\nВторая строка §"
        first = self.record(author="  Создатель  ", brings=brings)
        second = self.record(opus="Второе произведение")
        self.assertEqual((first["id"], second["id"]), ("1", "2"))
        self.assertEqual(first["author"], "Создатель")
        self.assertEqual(first["phrase"], "созидание")
        datetime.fromisoformat(first["date"])
        with creatio.OPERA.open(encoding="utf-8", newline="") as stream:
            reader = csv.DictReader(stream)
            self.assertEqual(
                reader.fieldnames,
                ["id", "date", "author", "phrase", "opus", "brings", "L", "J", "V", "decision"],
            )
            stored = list(reader)
        self.assertEqual(stored[0]["brings"], brings)
        self.assertEqual(creatio.list_opera(), [second, first])

    def test_work_does_not_change_other_records(self) -> None:
        problem = munera.collect_problema("Создатель", "орган", "служба", "исходный случай")
        message = munera.speak_as_citizen("Создатель", "исходная запись")
        remark = munera.zamechanie("Создатель", "исходное замечание")
        paths = (munera.PROBLEMATA, munera.COLLOQUIA, munera.ZAMECHANIYA)
        originals = {path: path.read_bytes() for path in paths}
        self.record()
        self.assertEqual({path: path.read_bytes() for path in paths}, originals)
        self.assertEqual(munera.list_problemata(), [problem])
        self.assertEqual(munera.list_colloquia(), [message])
        self.assertEqual(munera.list_zamechaniya(), [remark])

    def test_page_contains_ministry_form_and_escapes_works(self) -> None:
        payloads = {
            "author": '<author onclick="bad()">Создатель</author>',
            "opus": '<script>alert("opus")</script>',
            "brings": '<em>появилось</em>',
        }
        self.record(**payloads)
        document = interfacies.page().decode("utf-8")
        self.assertIn(creatio.NAME, document)
        self.assertIn(creatio.NAME_LATIN, document)
        self.assertIn(creatio.PHRASE, document)
        parser = FormParser()
        parser.feed(document)
        forms = [form for form in parser.forms if form["action"] == "/condere"]
        self.assertEqual(len(forms), 1)
        self.assertEqual(forms[0]["method"], "post")
        self.assertTrue(
            {"author", "phrase", "opus", "brings", "L", "J", "V"}.issubset(forms[0]["fields"])
        )
        for value in payloads.values():
            self.assertIn(html.escape(value, quote=True), document)
            self.assertNotIn(value, document)
        self.assertIn("созидание записано", document)
        self.assertIn("Не роль Создателя", document)


class CreationHTTPTests(IsolatedCreationTest):
    def setUp(self) -> None:
        super().setUp()
        self.patches.enter_context(patch.object(interfacies.Handler, "log_message", return_value=None))
        self.server = interfacies.ThreadingHTTPServer(("127.0.0.1", 0), interfacies.Handler)
        self.thread = threading.Thread(
            target=self.server.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True
        )
        self.thread.start()
        self.addCleanup(self.stop_server)

    def stop_server(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def post(self, **changes: object) -> tuple[int, str]:
        form = {
            "author": "Создатель",
            "phrase": "созидание",
            "opus": "Произведение",
            "brings": "То, чего не было",
            "L": "1",
            "J": "1",
            "V": "1",
        }
        for key, value in changes.items():
            if value is None:
                form.pop(key, None)
            else:
                form[key] = value
        body = urlencode(form).encode("utf-8")
        connection = http.client.HTTPConnection(*self.server.server_address, timeout=3)
        try:
            connection.request(
                "POST", "/condere", body, {"Content-Type": "application/x-www-form-urlencoded"}
            )
            response = connection.getresponse()
            status, location = response.status, response.getheader("Location", "")
            response.read()
            return status, location
        finally:
            connection.close()

    def assert_error_redirect(self, **changes: object) -> None:
        existing = creatio.list_opera()
        status, location = self.post(**changes)
        self.assertEqual(status, 303)
        query = parse_qs(urlparse(location).query)
        self.assertTrue(query.get("err"))
        self.assertNotIn("ok", query)
        self.assertEqual(creatio.list_opera(), existing)

    def test_successful_post_persists_one_work_and_redirects_to_page(self) -> None:
        status, location = self.post(brings="Появилось & наблюдение\nВторая строка")
        self.assertEqual(status, 303)
        self.assertEqual(urlparse(location).path, "/")
        self.assertEqual(urlparse(location).fragment, "creatio")
        self.assertTrue(parse_qs(urlparse(location).query).get("ok"))
        rows = creatio.list_opera()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["phrase"], "созидание")
        self.assertEqual(rows[0]["brings"], "Появилось & наблюдение\nВторая строка")
        self.assertEqual(rows[0]["decision"], "conditum")
        connection = http.client.HTTPConnection(*self.server.server_address, timeout=3)
        try:
            connection.request("GET", location)
            response = connection.getresponse()
            self.assertEqual(response.status, 200)
            document = response.read().decode("utf-8")
            self.assertIn(creatio.NAME, document)
            self.assertIn("Появилось &amp; наблюдение", document)
            self.assertIn("созидание записано", document)
        finally:
            connection.close()

    def test_missing_fields_and_wrong_phrase_fail_without_writing(self) -> None:
        for field in ("author", "phrase", "opus", "brings", "L", "J", "V"):
            with self.subTest(field=field):
                self.assert_error_redirect(**{field: None})
        self.assert_error_redirect(phrase="создание")
        self.assert_error_redirect(author="Оптимус")
        self.assert_error_redirect(L="0")


if __name__ == "__main__":
    unittest.main()
