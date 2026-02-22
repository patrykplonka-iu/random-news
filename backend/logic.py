import random
from typing import TypedDict

from data import (
    news_headlines_man,
    news_headlines_woman,
    no_words,
    thanks_words,
    yes_words,
)


class ChatState(TypedDict):
    name: str
    is_woman: bool
    headline: str
    step: int
    done: bool


def is_woman_name(name: str) -> bool:
    return name.lower().endswith("a")


def contains_any(text: str, words: list[str]) -> bool:
    lowered = text.lower()
    return any(word in lowered for word in words)


def normalize_name(name: str) -> str:
    normalized = name.strip()
    if not normalized:
        return "Ty"
    return normalized.capitalize()


def _final_message_for_user(is_woman: bool) -> str:
    return "Taka jestes :)" if is_woman else "Taki jestes :)"


def start_chat(name: str) -> tuple[ChatState, str]:
    normalized_name = normalize_name(name)
    is_woman = is_woman_name(normalized_name)
    headline = random.choice(news_headlines_woman if is_woman else news_headlines_man)

    state: ChatState = {
        "name": normalized_name,
        "is_woman": is_woman,
        "headline": headline,
        "step": 0,
        "done": False,
    }
    first_message = f"Hej, {normalized_name}! Chce Ci przekazac, ze {headline}"
    return state, first_message


def continue_chat(state: ChatState, user_message: str) -> tuple[ChatState, str]:
    if state["done"]:
        return state, "Rozmowa zakonczona. Kliknij Wroc i zacznij od nowa."

    message = user_message.strip()
    if not message:
        return state, "Napisz prosze jakas wiadomosc."

    step = state["step"]
    is_woman = state["is_woman"]

    if step == 0:
        if contains_any(message, thanks_words):
            state["done"] = True
            return state, "Nie ma za co!"
        state["step"] = 1
        return state, "Okej, ale moze chcesz podziekowac?"

    if step == 1:
        if contains_any(message, yes_words):
            state["step"] = 2
            return state, "No to dawaj, napisz dzieki :)"
        if contains_any(message, no_words):
            state["done"] = True
            return state, _final_message_for_user(is_woman)
        state["done"] = True
        return state, "Nie rozumiem, ale spoko. Milego dnia!"

    if contains_any(message, thanks_words):
        state["done"] = True
        return state, "Nie ma za co!"

    state["done"] = True
    return state, _final_message_for_user(is_woman)
