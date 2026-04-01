from my_module import *

current_word = get_word()[0]
description = get_word()[1]
table = create_table(current_word)
lives = get_lives()

show_table(table)
while is_alive(lives):
    show_message(description)
    answer = prompt("Назовите букву или слово целиком: ")
    modify_table(table, current_word, answer)
    if is_word_correct(current_word, answer):
        table = modify_table(table, current_word, answer)
        show_table(table)
        show_message("Вы выиграли! приз в студию!")
        break
    elif is_letter_correct(current_word, answer):
        table = modify_table(table, current_word, answer)
        if is_word_correct(current_word, answer):
            show_table(table)
            show_message("Вы выиграли! приз в студию!")
            break
        show_table(table, lives)
    else:
        show_message("Неправильно. Вы теряете жизнь.")
        lives = minus_life(lives)
        hanging(lives)
        if not is_alive(lives):
            show_message("Жизней не осталось. Игра окончена.")
            break
        show_table(table, lives)