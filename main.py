import time
import json
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from Words import dictionary_possible_words

wDict = dictionary_possible_words


#setting up parameters for selenium
driver = webdriver.Chrome()
driver.get("https://www.nytimes.com/games/wordle/index.html")
delay = WebDriverWait(driver, 10)
delay.until(expected_conditions.title_contains("Wordle"))
time.sleep(0.3)
page = driver.find_element(By.TAG_NAME, "html")
page.click()

#does exactly likeit says, enters the word into the wordle interface
def enter_word(word):
    page.send_keys(word)
    page.send_keys(Keys.RETURN)
    time.sleep(2)

def get_data():
    local_data = driver.execute_script("return window.localStorage;")
    game_info = local_data["nyt-wordle-state"] #inspected page source found state of game you are on
    evaluator = json.loads(game_info)["evaluations"] #friend jason loads the game info and returns
    return evaluator

#main driver method on guessing and cross checking words from the word list.
def method():
    guesses = ['brown','quick', 'shady']
    possible_words = wDict
    known_letters = []
    word = guesses[0]
    enter_word(word)
    evaluator = get_data()

    for q in range(5):
        stats = evaluator[q]
        correct_tally = 0
        for i in range(4):
            if (stats[i] != "absent") and (not word[i] in known_letters):
                known_letters.append(word[i])
            if stats[i] == "correct":
                correct_tally += 1
        if correct_tally == 5:
            time.sleep(2.5)
            page.click()
            quit()
        for i in range(5):
            letter = word[i]
            if stats[i] == "absent":
                if letter in known_letters:
                    possible_words = [x for x in possible_words if (x.count(letter) == 1) and (x[i] != letter)]
                else:
                    possible_words = [x for x in possible_words if not letter in x]
            elif stats[i] == "present":
                possible_words = [x for x in possible_words if (letter in x) and (x[i] != letter)]
            elif stats[i] == "correct":
                possible_words = [x for x in possible_words if letter == x[i]]
        if q < 2:
            word = guesses[q + 1]
        else:
            word = possible_words[0]
        enter_word(word)
        evaluator = get_data()
        while type(evaluator[q + 1]) is not list:
            for i in range(5):
                page.send_keys(Keys.BACKSPACE)
            possible_words.remove(word)
            word = possible_words[0]
            enter_word(word)
            evaluator = get_data()


time.sleep(2.5)
method()
page.click()