"""Глава 1. Пропуска и перехваченное сообщение."""

from rounds import Case, Chapter, Round


def validate_pass(regex, source):
    return regex.fullmatch(source) is not None


def find_ids(regex, source):
    return [match.group(0) for match in regex.finditer(source)]


CHAPTER = Chapter(
    "След у проходной",
    (
        Round(
            title="Поддельный пропуск",
            task=(
                "Из архива исчезла папка дела №17. Охрана сохранила журнал пропусков.\n"
                "Проверьте всю строку через re.fullmatch. Допустимы префикс ARC, "
                "дефис, ровно три цифры ASCII (0–9), дефис и одна заглавная "
                "латинская буква A–Z. Регистр важен, пробелы запрещены."
            ),
            operation=validate_pass,
            public=(
                Case("ARC-407-K", True),
                Case("ARC-40-K", False),
                Case("ARC-407-k", False),
            ),
            hidden=(
                Case("ARC-000-A", True),
                Case("ARC-999-Z", True),
                Case("ARC-4077-K", False),
                Case(" ARC-407-K", False),
                Case("ARC-407-K\n", False),
                Case("ARC-٤٠٧-K", False),
                Case("ARC-407-Ж", False),
                Case("arc-407-K", False),
                Case("XARC-407-K", False),
                Case("", False),
            ),
            hint="Используйте [0-9] с квантификатором {3}. fullmatch проверит всю строку.",
            clue="В 21:14 по пропуску ARC-407-K прошли к служебному терминалу.",
        ),
        Round(
            title="Перехват",
            task=(
                "В сообщении терминала указаны дела, которые перемещали этой ночью. Найдите все номера дел "
                "в порядке появления, сохраняя повторы. Пропускайте даты и обычные числа. Номер дела — "
                "CASE- и ровно две цифры ASCII. Регистр важен. "
                "Непосредственно слева и справа должна быть граница строки или "
                "символ, который Python не считает словесным (\\W). "
                "Из каждого совпадения берётся весь текст (group(0))."
            ),
            operation=find_ids,
            public=(
                Case("20.11.2026: CASE-07, CASE-17, 42, CASE-07.", ["CASE-07", "CASE-17", "CASE-07"]),
                Case("Отбросить XCASE-31 и CASE-310.", []),
            ),
            hidden=(
                Case("CASE-99,CASE-00\nCASE-03", ["CASE-99", "CASE-00", "CASE-03"]),
                Case("яCASE-04 CASE-05_ _CASE-06 CASE-07я", []),
                Case("CASE-٩٩ box-88 CASE-1 CASE-123 [CASE-42]", ["CASE-42"]),
                Case("CASE-04/CASE-04", ["CASE-04", "CASE-04"]),
                Case("13.11.2026, 21:14, 17", []),
                Case("", []),
            ),
            hint="Начните с CASE- и двух цифр. Проверьте границы через \\b с обеих сторон.",
            clue="В очереди перемещения было дело CASE-17. В его карточке нашли черновик отчёта.",
        ),
    ),
)
