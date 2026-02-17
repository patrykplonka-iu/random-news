import random

from data import (
    news_headlines_man,
    news_headlines_woman,
    no_words,
    thanks_words,
    yes_words,
)


def is_woman_name(name: str) -> bool:
    return name.lower().endswith("a")


def contains_any(text: str, words: list[str]) -> bool:
    lowered = text.lower()
    return any(word in lowered for word in words)


def run() -> None:
    random_name = input("Podaj swoje imię: ").strip().capitalize()
    is_woman = is_woman_name(random_name)

    random_headline = random.choice(
        news_headlines_woman if is_woman else news_headlines_man
    )

    print("Hej, " + random_name + "!")
    print("Chcę Ci przekazać, że " + random_headline)

    random_answer = input(random_name + ": ").strip()

    if contains_any(random_answer, thanks_words):
        print("Nie ma za co!")
        return

    print("Okej, ale może chcesz podziękować?")
    random_thought = input().strip().lower()

    if contains_any(random_thought, yes_words):
        random_answer2 = input(random_name + ": ").strip()

        if contains_any(random_answer2, thanks_words):
            print("Nie ma za co!")
        else:
            print("Taka jesteś :)" if is_woman else "Taki jesteś :)")
    elif contains_any(random_thought, no_words):
        print("Taka jesteś :)" if is_woman else "Taki jesteś :)")
    else:
        print("Nie rozumiem, ale spoko. Miłego dnia!")
