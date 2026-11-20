import subprocess
import sys
import unittest
from pathlib import Path

from passes import CHAPTER as PASSES
from report import CHAPTER as REPORT


ROOT = Path(__file__).resolve().parents[1]
SOLUTIONS = (
    r"ARC-[0-9]{3}-[A-Z]",
    r"\bCASE-[0-9]{2}\b",
    r"\bWK-[0-9]{4}\b",
    r"[ \t]*(?:[|;]|>>)[ \t]*",
)


def run_game(*commands, chapter=None):
    arguments = [sys.executable, "-X", "utf8", "main.py"]
    if chapter:
        arguments.extend(["--chapter", chapter])
    return subprocess.run(
        arguments,
        input="".join(f"{command}\n" for command in commands),
        encoding="utf-8",
        capture_output=True,
        cwd=ROOT,
        timeout=10,
        check=True,
    ).stdout


class GameTests(unittest.TestCase):
    def test_syntax_errors_in_every_round(self):
        for chapter in (PASSES, REPORT):
            for round_ in chapter.rounds:
                with self.subTest(round=round_.title):
                    success, message = round_.check("[")
                    assert not success and "re.error" in message

    def test_full_game_with_hint_and_retries(self):
        output = run_game(":hint", "[", r"ARC-\d{3}-[A-Z]", *SOLUTIONS)
        markers = [
            "Поддельный пропуск",
            "Подсказка:",
            "re.error",
            "Контрпример (скрытый",
            "Улика:",
            "Перехват",
            "Закрытые данные",
            "Последовательность событий",
            "Собранные улики",
            "Дело раскрыто",
        ]
        positions = [output.index(marker) for marker in markers]
        assert positions == sorted(positions)
        assert output.count("Улика:") == 4
        assert output.count("Все проверки пройдены") == 4

    def test_failed_attempt_does_not_unlock_next_round(self):
        output = run_game(".*", ":quit")
        assert "Контрпример" in output and "Перехват" not in output
        assert "Улика:" not in output and "Расследование прервано" in output
        assert "ARC-000-A" not in output

    def test_end_of_input(self):
        assert "Расследование прервано" in run_game()

    def test_chapters_can_be_run_separately(self):
        for name, answers, title in (
            ("passes", SOLUTIONS[:2], "След у проходной"),
            ("report", SOLUTIONS[2:], "Архивный журнал"),
        ):
            with self.subTest(chapter=name):
                output = run_game(*answers, chapter=name)
                assert f"Глава «{title}»" in output
                assert output.count("Улика:") == 2 and "Глава пройдена" in output
                assert "Дело раскрыто" not in output
