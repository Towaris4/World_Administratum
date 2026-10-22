"""Ministry of Internal Affairs: a request by the phrase «запрос»."""

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

import interfacies
import internae
import munera
from princip import ROLES

FILED = "Прошу предоставить Уран и 1 робота для перепрошивки с руками как у Ювелира."


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


class IsolatedRequestTest(unittest.TestCase):
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
        self.patches.enter_context(
            patch.object(internae, "PETITIONES", self.directory / "internae.csv")
        )

    def record(self, **changes: object) -> dict[str, str]:
        data: dict[str, object] = {
            "author": "Арбитр-создатель",
            "phrase": "запрос",
            "petitio": "Прошу записать обращение.",
            "principle": (1, 1, 1),
        }
        data.update(changes)
        return internae.scribere(**data)


class RequestJournalTests(IsolatedRequestTest):
    def test_ministry_is_registered_as_function(self) -> None:
        self.assertEqual(internae.NAME, "Министерство внутренних дел")
        self.assertEqual(internae.NAME_LATIN, "Ministerium Rerum Internarum")
        self.assertEqual(internae.PHRASE, "запрос")
        ministries = [item for item in munera.MUNERA if item["id"] == "internae"]
        self.assertEqual(len(ministries), 1)
        self.assertIn(internae.NAME, ministries[0]["name"])
        self.assertEqual(ministries[0]["latin"], internae.NAME_LATIN)
        self.assertNotIn("internae", {role["id"] for role in ROLES})
        root = Path(__file__).resolve().parent.parent
        for name in ("AGENTS.md", "README.md"):
            document = (root / name).read_text(encoding="utf-8")
            self.assertIn(internae.NAME, document)
            self.assertIn(internae.NAME_LATIN, document)
            self.assertIn(internae.PHRASE, document)
            self.assertIn("does not transfer the named things", document)

    def test_phrase_records_the_request(self) -> None:
        for phrase in ("запрос", "  ЗАПРОС  ", "Запрос"):
            with self.subTest(phrase=phrase):
                row = self.record(phrase=phrase, petitio=f"текст {phrase}")
                self.assertEqual(row["phrase"], "запрос")
                self.assertEqual(row["decision"], "scripta")
                self.assertEqual((row["L"], row["J"], row["V"]), ("1", "1", "1"))

    def test_other_phrases_record_nothing(self) -> None:
        for phrase in ("", " ", "запросы", "запрос доступа", "запрос."):
            with self.subTest(phrase=phrase), self.assertRaises(ValueError):
                self.record(phrase=phrase)
        self.assertEqual(internae.list_petitiones(), [])

    def test_only_all_one_vector_is_admitted(self) -> None:
        for vector in itertools.product((0, 1), repeat=3):
            with self.subTest(vector=vector):
                previous = internae.list_petitiones()
                if vector == (1, 1, 1):
                    row = self.record(principle=vector)
                    self.assertEqual(row["decision"], "scripta")
                else:
                    with self.assertRaises(ValueError):
                        self.record(principle=vector)
                    self.assertEqual(internae.list_petitiones(), previous)
        self.assertEqual(len(internae.list_petitiones()), 1)

    def test_invalid_vectors_never_create_requests(self) -> None:
        invalid = (
            (), (1,), (1, 1), (1, 1, 1, 1), (-1, 1, 1), (1, 2, 1),
            (1.0, 1, 1), (True, 1, 1), ("1", 1, 1), "111", None,
        )
        for vector in invalid:
            with self.subTest(vector=vector), self.assertRaises(ValueError):
                self.record(principle=vector)
        self.assertEqual(internae.list_petitiones(), [])

    def test_required_fields_cannot_be_empty(self) -> None:
        for field in ("author", "petitio"):
            for value in ("", " \t\n "):
                with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                    self.record(**{field: value})
        self.assertEqual(internae.list_petitiones(), [])

    def test_president_cannot_author_a_request(self) -> None:
        for author in munera.PRESIDENT_AUTHORS:
            with self.subTest(author=author), self.assertRaises(munera.Silentium):
                self.record(author="  " + author.upper() + "  ")
        self.assertEqual(internae.list_petitiones(), [])

    def test_csv_roundtrip_preserves_unicode_and_order(self) -> None:
        petitio = "Прошу «Уран» и робота\nВторая строка §"
        first = self.record(author="  Создатель  ", petitio=petitio)
        second = self.record(petitio="Второй запрос")
        self.assertEqual((first["id"], second["id"]), ("1", "2"))
        self.assertEqual(first["author"], "Создатель")
        self.assertEqual(first["phrase"], "запрос")
        datetime.fromisoformat(first["date"])
        with internae.PETITIONES.open(encoding="utf-8", newline="") as stream:
            reader = csv.DictReader(stream)
            self.assertEqual(
                reader.fieldnames,
                ["id", "date", "author", "phrase", "petitio", "L", "J", "V", "decision"],
            )
            stored = list(reader)
        self.assertEqual(stored[0]["petitio"], petitio)
        self.assertEqual(internae.list_petitiones(), [second, first])

    def test_request_does_not_change_other_records(self) -> None:
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

    def test_page_contains_ministry_form_and_escapes_requests(self) -> None:
        payloads = {
            "author": '<author onclick="bad()">Создатель</author>',
            "petitio": '<script>alert("uran")</script>',
        }
        self.record(**payloads)
        document = interfacies.page().decode("utf-8")
        self.assertIn(internae.NAME, document)
        self.assertIn(internae.NAME_LATIN, document)
        self.assertIn(internae.PHRASE, document)
        parser = FormParser()
        parser.feed(document)
        forms = [form for form in parser.forms if form["action"] == "/scribere"]
        self.assertEqual(len(forms), 1)
        self.assertEqual(forms[0]["method"], "post")
        self.assertTrue(
            {"author", "phrase", "petitio", "L", "J", "V"}.issubset(forms[0]["fields"])
        )
        for value in payloads.values():
            self.assertIn(html.escape(value, quote=True), document)
            self.assertNotIn(value, document)
        self.assertIn("запрос записан", document)
        self.assertIn("Запрос:", document)


class RequestHTTPTests(IsolatedRequestTest):
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
            "phrase": "запрос",
            "petitio": "Прошу записать обращение.",
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
                "POST", "/scribere", body, {"Content-Type": "application/x-www-form-urlencoded"}
            )
            response = connection.getresponse()
            status, location = response.status, response.getheader("Location", "")
            response.read()
            return status, location
        finally:
            connection.close()

    def assert_error_redirect(self, **changes: object) -> None:
        existing = internae.list_petitiones()
        status, location = self.post(**changes)
        self.assertEqual(status, 303)
        query = parse_qs(urlparse(location).query)
        self.assertTrue(query.get("err"))
        self.assertNotIn("ok", query)
        self.assertEqual(internae.list_petitiones(), existing)

    def test_successful_post_persists_one_request_and_redirects_to_page(self) -> None:
        status, location = self.post(petitio="Уран & робот\nВторая строка")
        self.assertEqual(status, 303)
        self.assertEqual(urlparse(location).path, "/")
        self.assertEqual(urlparse(location).fragment, "internae")
        self.assertTrue(parse_qs(urlparse(location).query).get("ok"))
        rows = internae.list_petitiones()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["phrase"], "запрос")
        self.assertEqual(rows[0]["petitio"], "Уран & робот\nВторая строка")
        self.assertEqual(rows[0]["decision"], "scripta")
        connection = http.client.HTTPConnection(*self.server.server_address, timeout=3)
        try:
            connection.request("GET", location)
            response = connection.getresponse()
            self.assertEqual(response.status, 200)
            document = response.read().decode("utf-8")
            self.assertIn(internae.NAME, document)
            self.assertIn("Уран &amp; робот", document)
            self.assertIn("запрос записан", document)
        finally:
            connection.close()

    def test_missing_fields_and_wrong_phrase_fail_without_writing(self) -> None:
        for field in ("author", "phrase", "petitio", "L", "J", "V"):
            with self.subTest(field=field):
                self.assert_error_redirect(**{field: None})
        self.assert_error_redirect(phrase="запрос доступа")
        self.assert_error_redirect(author="Оптимус")
        self.assert_error_redirect(L="0")


class FiledRequestTests(unittest.TestCase):
    def test_uranium_and_robot_request_is_on_record(self) -> None:
        rows = internae.list_petitiones()
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["author"], "Создатель")
        self.assertEqual(row["phrase"], "запрос")
        self.assertEqual(row["petitio"], FILED)
        self.assertEqual(row["decision"], "scripta")
        self.assertEqual((row["L"], row["J"], row["V"]), ("1", "1", "1"))
