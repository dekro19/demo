import unittest

from passes import CHAPTER


class PassesTests(unittest.TestCase):
    def test_pass_validation(self):
        round_ = CHAPTER.rounds[0]
        assert round_.check(r"ARC-[0-9]{3}-[A-Z]")[0]
        assert round_.check(r"ARC-(?a:\d{3})-[A-Z]")[0]
        success, message = round_.check(r"ARC-\d{3}-[A-Z]")
        assert not success and "скрытый" in message and "٤٠٧" in message
        assert not round_.check(r"ARC-407-K")[0]

    def test_id_order_and_repetitions(self):
        round_ = CHAPTER.rounds[1]
        assert round_.check(r"\bCASE-[0-9]{2}\b")[0]
        assert round_.check(r"(?<!\w)CASE-[0-9][0-9](?!\w)")[0]
        success, message = round_.check(r"\bCASE-[0-9]{2}\b(?!\.)")
        assert not success and "открытый" in message and "CASE-17" in message
        success, message = round_.check(r"\bCASE-0[0-9]\b|\bCASE-17\b")
        assert not success and "скрытый" in message
