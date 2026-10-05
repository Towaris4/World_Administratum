"""Ethics ministry: isolated journal, principle, and HTTP integration checks."""

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

import ethica
import interfacies
import munera


class FormParser(HTMLParser):
    """Find fields inside their actual form, independent of page whitespace."""

    def __init__(self) -> None:
        super().__init__()
        self.forms: list[dict[str, object]] = []
        self.current: dict[str, object] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "form":
            self.current = {"action": attributes.get("action"), "method": attributes.get("method"), "fields": set()}
            self.forms.append(self.current)
        elif self.current is not None and tag in {"input", "textarea", "select"}:
            fields = self.current["fields"]
            assert isinstance(fields, set)
            if attributes.get("name"):
                fields.add(attributes["name"])

    def handle_endtag(self, tag: str) -> None:
        if tag == "form":
            self.current = None


class IsolatedEthicsTest(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.patches = ExitStack()
        self.addCleanup(self.patches.close)
        for attribute in ("PROBLEMATA", "COLLOQUIA", "ZAMECHANIYA"):
            self.patches.enter_context(patch.object(munera, attribute, self.directory / (attribute.lower() + ".csv")))
        self.patches.enter_context(patch.object(ethica, "VENIAE", self.directory / "veniae.csv"))

    def forgive(self, **changes: object) -> dict[str, str]:
        data: dict[str, object] = {
            "author": "Арбитр-создатель",
            "living_being": "Живое существо без известного имени",
            "kind": "case",
            "event": "Произошёл случай, требующий рассмотрения",
            "reason": "После рассмотрения принято решение простить",
            "principle": (1, 1, 1),
        }
        data.update(changes)
        return ethica.ignoscere(**data)


class EthicsJournalTests(IsolatedEthicsTest):
    def test_ministry_is_registered_as_function(self) -> None:
        self.assertEqual(ethica.NAME, "Министерство Этики")
        self.assertEqual(ethica.NAME_LATIN, "Ministerium Ethicae")
        ministries = [item for item in munera.MUNERA if item["id"] == "ethica"]
        self.assertEqual(len(ministries), 1)
        self.assertIn(ethica.NAME, ministries[0]["name"])
        self.assertEqual(ministries[0]["latin"], ethica.NAME_LATIN)

    def test_only_all_one_vector_is_admitted(self) -> None:
        for vector in itertools.product((0, 1), repeat=3):
            with self.subTest(vector=vector):
                previous = ethica.list_veniae()
                if vector == (1, 1, 1):
                    row = self.forgive(principle=vector)
                    self.assertEqual(row["decision"], "forgiven")
                    self.assertEqual((row["L"], row["J"], row["V"]), ("1", "1", "1"))
                else:
                    with self.assertRaises(ValueError):
                        self.forgive(principle=vector)
                    self.assertEqual(ethica.list_veniae(), previous)
        self.assertEqual(len(ethica.list_veniae()), 1)

    def test_invalid_vectors_never_create_decisions(self) -> None:
        invalid = ((), (1,), (1, 1), (1, 1, 1, 1), (-1, 1, 1), (1, 2, 1), (1, 1, 2), (1.0, 1, 1), (True, 1, 1), ("1", 1, 1), "111", None)
        for vector in invalid:
            with self.subTest(vector=vector), self.assertRaises(ValueError):
                self.forgive(principle=vector)
        self.assertEqual(ethica.list_veniae(), [])

    def test_required_fields_cannot_be_empty(self) -> None:
        for field in ("author", "living_being", "event", "reason"):
            for value in ("", " \t\n "):
                with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                    self.forgive(**{field: value})
        self.assertEqual(ethica.list_veniae(), [])

    def test_kind_is_explicit_and_normalized(self) -> None:
        self.assertEqual(self.forgive(kind=" ACT ")["kind"], "act")
        self.assertEqual(self.forgive(kind=" CaSe ")["kind"], "case")
        existing = ethica.list_veniae()
        for kind in ("", " ", "problem", "поступок", "incident"):
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                self.forgive(kind=kind)
        self.assertEqual(ethica.list_veniae(), existing)

    def test_president_cannot_author_a_decision(self) -> None:
        for author in munera.PRESIDENT_AUTHORS:
            with self.subTest(author=author), self.assertRaises(munera.Silentium):
                self.forgive(author="  " + author.upper() + "  ")
        self.assertEqual(ethica.list_veniae(), [])

    def test_living_being_needs_description_but_no_proper_name(self) -> None:
        beings = ("Человек, имя неизвестно", "Безымянное животное", "Растение во дворе")
        for being in beings:
            with self.subTest(being=being):
                row = self.forgive(living_being=being)
                self.assertEqual(row["living_being"], being)
                self.assertEqual(row["decision"], "forgiven")
        self.assertEqual(len(ethica.list_veniae()), len(beings))

    def test_csv_roundtrip_preserves_unicode_quotes_newlines_and_order(self) -> None:
        event = 'Случай с котом, "Рыжим"\nВторая строка §'
        reason = 'Решение после наблюдения\nПроверены L, J, V; прощение'
        first = self.forgive(author="  Создатель  ", living_being="  Кот  ", event=event, reason=reason)
        second = self.forgive(kind="act", event="Второй поступок")
        self.assertEqual((first["id"], second["id"]), ("1", "2"))
        self.assertEqual(first["author"], "Создатель")
        self.assertEqual(first["living_being"], "Кот")
        datetime.fromisoformat(first["date"])
        with ethica.VENIAE.open(encoding="utf-8", newline="") as stream:
            reader = csv.DictReader(stream)
            self.assertEqual(reader.fieldnames, ["id", "date", "author", "living_being", "kind", "event", "reason", "L", "J", "V", "decision"])
            stored = list(reader)
        self.assertEqual(stored, [first, second])
        self.assertEqual(stored[0]["event"], event)
        self.assertEqual(stored[0]["reason"], reason)
        self.assertEqual(ethica.list_veniae(), [second, first])
        self.assertEqual(ethica.list_veniae(), [second, first])

    def test_decision_does_not_change_existing_problem_message_or_remark(self) -> None:
        problem = munera.collect_problema("Создатель", "орган", "служба", "исходный случай")
        message = munera.speak_as_citizen("Создатель", "исходная запись")
        remark = munera.zamechanie("Создатель", "исходное замечание")
        paths = (munera.PROBLEMATA, munera.COLLOQUIA, munera.ZAMECHANIYA)
        originals = {path: path.read_bytes() for path in paths}
        self.forgive(event=problem["problem"])
        self.assertEqual({path: path.read_bytes() for path in paths}, originals)
        self.assertEqual(munera.list_problemata(), [problem])
        self.assertEqual(munera.list_colloquia(), [message])
        self.assertEqual(munera.list_zamechaniya(), [remark])

    def test_page_contains_ministry_form_and_escapes_decisions(self) -> None:
        payloads = {
            "author": '<author onclick="bad()">Создатель</author>',
            "living_being": '<being data-x="1">Живое существо</being>',
            "event": '<script>alert("event")</script>',
            "reason": '<img src=x onerror="bad()"> Причина & наблюдения',
        }
        self.forgive(**payloads)
        document = interfacies.page().decode("utf-8")
        self.assertIn(ethica.NAME, document)
        self.assertIn(ethica.NAME_LATIN, document)
        parser = FormParser()
        parser.feed(document)
        forms = [form for form in parser.forms if form["action"] == "/ignoscere"]
        self.assertEqual(len(forms), 1)
        self.assertEqual(forms[0]["method"], "post")
        self.assertTrue({"author", "living_being", "kind", "event", "reason", "L", "J", "V"}.issubset(forms[0]["fields"]))
        for value in payloads.values():
            with self.subTest(value=value):
                self.assertIn(html.escape(value, quote=True), document)
                self.assertNotIn(value, document)


class EthicsHTTPTests(IsolatedEthicsTest):
    def setUp(self) -> None:
        super().setUp()
        self.patches.enter_context(patch.object(interfacies.Handler, "log_message", return_value=None))
        self.server = interfacies.ThreadingHTTPServer(("127.0.0.1", 0), interfacies.Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True)
        self.thread.start()
        self.addCleanup(self.stop_server)

    def stop_server(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def post(self, **changes: object) -> tuple[int, str]:
        form = {"author": "Создатель", "living_being": "Безымянное животное", "kind": "case", "event": "Случай", "reason": "Решение простить", "L": "1", "J": "1", "V": "1"}
        for key, value in changes.items():
            if value is None:
                form.pop(key, None)
            else:
                form[key] = value
        body = urlencode(form).encode("utf-8")
        connection = http.client.HTTPConnection(*self.server.server_address, timeout=3)
        try:
            connection.request("POST", "/ignoscere", body, {"Content-Type": "application/x-www-form-urlencoded"})
            response = connection.getresponse()
            status, location = response.status, response.getheader("Location", "")
            response.read()
            return status, location
        finally:
            connection.close()

    def assert_error_redirect(self, **changes: object) -> None:
        existing = ethica.list_veniae()
        status, location = self.post(**changes)
        self.assertEqual(status, 303)
        query = parse_qs(urlparse(location).query)
        self.assertTrue(query.get("err"))
        self.assertNotIn("ok", query)
        self.assertEqual(ethica.list_veniae(), existing)

    def test_successful_post_persists_one_decision_and_redirects_to_page(self) -> None:
        status, location = self.post(event="Случай & наблюдение\nВторая строка")
        self.assertEqual(status, 303)
        self.assertEqual(urlparse(location).path, "/")
        self.assertTrue(parse_qs(urlparse(location).query).get("ok"))
        rows = ethica.list_veniae()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["event"], "Случай & наблюдение\nВторая строка")
        self.assertEqual(rows[0]["decision"], "forgiven")
        connection = http.client.HTTPConnection(*self.server.server_address, timeout=3)
        try:
            connection.request("GET", location)
            response = connection.getresponse()
            self.assertEqual(response.status, 200)
            document = response.read().decode("utf-8")
            self.assertIn(ethica.NAME, document)
            self.assertIn("Случай &amp; наблюдение", document)
        finally:
            connection.close()

    def test_missing_fields_fail_without_writing(self) -> None:
        for field in ("author", "living_being", "kind", "event", "reason", "L", "J", "V"):
            with self.subTest(field=field):
                self.assert_error_redirect(**{field: None})

    def test_rejected_or_invalid_principle_fails_without_writing(self) -> None:
        for key, value in (("L", "0"), ("J", "0"), ("V", "0"), ("L", "2"), ("J", "true"), ("V", "1.0"), ("V", "")):
            with self.subTest(key=key, value=value):
                self.assert_error_redirect(**{key: value})

    def test_president_and_invalid_kind_fail_without_writing(self) -> None:
        self.assert_error_redirect(author="Оптимус")
        self.assert_error_redirect(kind="problem")


if __name__ == "__main__":
    unittest.main()
