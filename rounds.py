"""Данные раунда и общая проверка регулярных выражений."""

import re
from dataclasses import dataclass
from typing import Callable, Tuple, Union


Result = Union[bool, str, list]
Operation = Callable[[re.Pattern, str], Result]


@dataclass(frozen=True)
class Case:
    source: str
    expected: Result


def describe(result: Result) -> str:
    if isinstance(result, bool):
        return "пропуск принят" if result else "пропуск отклонён"
    return repr(result)


@dataclass(frozen=True)
class Round:
    title: str
    task: str
    operation: Operation
    public: Tuple[Case, ...]
    hidden: Tuple[Case, ...]
    hint: str
    clue: str

    def check(self, pattern: str) -> Tuple[bool, str]:
        try:
            regex = re.compile(pattern)
        except re.error as error:
            return False, f"Ошибка синтаксиса (re.error): {error}"
        except (OverflowError, RecursionError):
            return False, "Шаблон слишком сложен для компиляции. Упростите его."

        for label, cases in (("открытый", self.public), ("скрытый", self.hidden)):
            for number, case in enumerate(cases, 1):
                actual = self.operation(regex, case.source)
                if actual != case.expected:
                    return False, (
                        f"Контрпример ({label} тест №{number})\n"
                        f"  Вход: {case.source!r}\n"
                        f"  Ожидалось: {describe(case.expected)}\n"
                        f"  Получилось: {describe(actual)}"
                    )

        return True, f"Все проверки пройдены ({len(self.public) + len(self.hidden)})."


@dataclass(frozen=True)
class Chapter:
    title: str
    rounds: Tuple[Round, ...]
