"""Консольный запуск игры «Regex-детектив»."""

import argparse

from rounds import describe


def play(chapters):
    clues = []
    print("Regex-детектив | Дело №17")
    print("Введите регулярное выражение. Команды: :hint — подсказка, :quit — выход.")

    for chapter in chapters:
        print(f"\nГлава «{chapter.title}»")
        for number, round_ in enumerate(chapter.rounds, 1):
            print(f"\nРаунд {number}/{len(chapter.rounds)}. {round_.title}")
            print(round_.task)
            print("Открытые примеры")
            for case in round_.public:
                print(f"  {case.source!r} → {describe(case.expected)}")

            while True:
                try:
                    pattern = input("regex> ")
                except (EOFError, KeyboardInterrupt):
                    pattern = ":quit"
                if pattern == ":quit":
                    print("\nРасследование прервано.")
                    return
                if pattern == ":hint":
                    print(f"Подсказка: {round_.hint}")
                    continue

                success, message = round_.check(pattern)
                print(message)
                if success:
                    clues.append(round_.clue)
                    print(f"Улика: {round_.clue}")
                    break
                print("Попробуйте снова или введите :hint.")

    print("\nСобранные улики")
    for clue in clues:
        print(f"  • {clue}")
    if len(chapters) == 2:
        print("\nДело раскрыто. Дежурная перенесла папку в резервный сейф "
              "после сбоя замка. Папка возвращена в архив.")
    else:
        print("\nГлава пройдена.")


def main():
    parser = argparse.ArgumentParser(description="Консольная игра «Regex-детектив»")
    parser.add_argument("--chapter", choices=("passes", "report"), help="запустить одну главу")
    selection = parser.parse_args().chapter

    chapters = []
    if selection in (None, "passes"):
        from passes import CHAPTER

        chapters.append(CHAPTER)
    if selection in (None, "report"):
        from report import CHAPTER

        chapters.append(CHAPTER)
    play(chapters)


if __name__ == "__main__":
    main()
