import random
import curses as cursed

# Inicjalizujemy obiekt do pracy z TUI
screen = cursed.Screen()

# Lista słów do wyboru
words = ["apple", "banana", "orange", "strawberry"]

# Wybieramy losowe słowo
word = random.choice(words)

# Inicjalizujemy zmienną przechowującą stan gry
game_state = ["_"] * len(word)

# Inicjalizujemy zmienną przechowującą liczbę pozostałych prób
tries = 6

while tries > 0:
    # Wyświetlamy aktualny stan gry
    screen.clear()
    screen.print(0, 0, " ".join(game_state))
    # Pytamy gracza o literę
    letter = screen.input(1, 0, "Podaj literę: ")
    # Sprawdzamy, czy litera jest w słowie
    if letter in word:
        # Jeśli tak, to aktualizujemy stan gry
        for i in range(len(word)):
            if word[i] == letter:
                game_state[i] = letter
    else:
        # Jeśli nie, to odejmujemy 1 próbę
        tries -= 1
        screen.print(2, 0, f"Niestety, litera {letter} nie występuje w słowie. Pozostało Ci {tries} prób.")
    # Sprawdzamy, czy gra została rozwiązana
    if all(letter in game_state for letter in word):
        screen.print(3, 0, "Brawo! Odgadłeś słowo:", word)
        break
else:
    # Jeśli nie udało się odgadnąć słowa, wyświetlamy komunikat o przegranej
    screen.print(3, 0, "Niestety, przegrałeś :( Słowo, którego szukałeś, to:", word)

