import random

# Definicja randomowych nagłówków wiadomości
news_headlines_man = (
    "jesteś fajny",
    "dzisiaj będzie wybitna pogoda",
    "nauka jest super",
    "programowanie jest zabawne",
    "kawa jest najlepsza",
    "jesteś inteligentny",
    "masz świetne poczucie humoru",
)

news_headlines_woman = (
    "jesteś piękna",
    "dzisiaj będzie ładna pogoda",
    "nauka może być super",
    "programowanie nie jest dla Ciebie",
    "kawa z mlekiem jest najlepsza",
    "jesteś inteligentna",
    "masz poczucie humoru",
)

thanks_words = ["dziękuję", "dzięki", "dziękuje", "dziekuje", "dzieki"]
yes_words = ["tak", "ok", "okej", "oki"]
no_words = ["nie", "nope", "n"]

random_name = input("Podaj swoje imię: ").strip()
random_name = random_name.capitalize()

is_woman = random_name.lower().endswith("a")

random_headline = random.choice(news_headlines_woman if is_woman else news_headlines_man)

print("Hej, " + random_name + "!")
print("Chcę Ci przekazać, że " + random_headline)

# 1 runda rozmowy (możesz to potem przerobić na więcej rund)
random_answer = input(random_name + ": ").strip()

if any(word in random_answer.lower() for word in thanks_words):
    print("Nie ma za co!")
else:
    print("Okej, ale może chcesz podziękować?")
    random_thought = input().strip().lower()

    if any(word in random_thought for word in yes_words):
        # DRUGA SZANSA: ponownie pytamy o odpowiedź
        random_answer2 = input(random_name + ": ").strip()

        if any(word in random_answer2.lower() for word in thanks_words):
            print("Nie ma za co!")
        else:
            # nadal nie podziękował
            if is_woman:
                print("Taka jesteś :)")
            else:
                print("Taki jesteś :)")

    elif any(word in random_thought for word in no_words):
        if is_woman:
            print("Taka jesteś :)")
        else:
            print("Taki jesteś :)")
    else:
        # jeśli wpisze coś innego niż tak/nie
        print("Nie rozumiem, ale spoko. Miłego dnia!")