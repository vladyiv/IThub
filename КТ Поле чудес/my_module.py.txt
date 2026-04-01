import random

def get_word() -> list:
    f = open("words.txt", "r")
    for _ in range (random.randint(1, 5)):
        word_desc = f.readline().split(" - ")
    return word_desc

def get_lives() -> int:
    return 4

def hanging(lives) -> None:
    with open(f'{4-lives}.txt', 'r') as f:
        print(f.read())

def create_table(word: str) -> list:
    table = ["\u25A0"]*len(word)
    return table

def minus_life(lives: int) -> int:
    return lives - 1 if lives > 0 else 0

def is_alive(lives: int) -> bool:
    return lives > 0

def lives_str(lives: int) -> str:
    return f" | \u2665x{lives}"

def show_table(table: list, lives: int = 0) -> None:
    if lives > 0:
        for i in range(len(table)):
            print(table[i], end = " ")
        print(lives_str(lives))
    else:
        for i in range(len(table)):
            print(table[i], end = " ")
        print()

def prompt(msg: str) -> str:
    return input(msg).strip()

def show_message(msg: str) -> None:
    print(msg)

def is_word_correct(word: str, answer: str) -> bool:
    return len(answer) == len(word) and word.lower() == answer.lower()

def is_letter_correct(word: str, letter: str) -> bool:
    return len(letter) == 1 and letter.lower() in word.lower()

def modify_table(table: list, word: str, answer: str) -> list:
    if len(answer) == 1:
        for i in range(len(word)):
            if answer.lower() == word[i].lower():
                table[i] = word[i]
                i += 1
    elif len(answer) == len(word):
        for i in range(len(table)):
            table[i] = word[i]
            i += 1
    return table