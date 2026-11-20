import unittest

from report import CHAPTER


class ReportTests(unittest.TestCase):
    def test_redaction_keeps_surrounding_text(self):
        round_ = CHAPTER.rounds[0]
        assert round_.check(r"\bWK-[0-9]{4}\b")[0]
        assert round_.check(r"(?<!\w)WK-[0-9]{4}(?!\w)")[0]
        success, message = round_.check(r"\bWK-\d{4}\b")
        assert not success and "скрытый" in message and "[СКРЫТО]" in message
        assert not round_.check(r".+")[0]

    def test_log_keeps_empty_entries_and_non_delimiters(self):
        round_ = CHAPTER.rounds[1]
        assert round_.check(r"[ \t]*(?:[|;]|>>)[ \t]*")[0]
        assert round_.check(r"[ \t]*(?:\||;|>>)[ \t]*")[0]
        success, message = round_.check(r"\s*(?:[|;]|>>)\s*")
        assert not success and "скрытый" in message and r"A\n" in message
        assert not round_.check(r"[ \t]*([|;]|>>)[ \t]*")[0]
