import time
from datetime import datetime
import json
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from Words import dictionary_possible_words


# from selenium.webdriver.support import expected_conditions as ec
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.remote.webelement import WebElement
#
class Wurdle:
    """Setup Class    """

    def __init__(self):
        self.driver = driver = webdriver.Chrome()
        self.driver.get("https://www.nytimes.com/games/wordle/index.html")
        driver.implicitly_wait(10)
        # action = ActionChains(driver)
        # WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="pz-gdpr-btn-accept"]'))).click()
        # uncomment if ccookies keeps poppping up

        # closeicon = driver.find_element(By.CLASS_NAME, "Modal-module_closeIcon__b4z74")
        # action.find_element(By.CLASS_NAME, "Modal-module_closeIcon__b4z74").click().perform()
        driver.find_element(By.CLASS_NAME, "Modal-module_closeIcon__b4z74").click()  # simplified popup close icon.
        time.sleep(1)
        self.page = driver.find_element(By.TAG_NAME, "html")
        self.page.click()
        self.wDict = dictionary_possible_words
        self.count = 0

    def enter_word(self, word):
        """Gets selected word and enters it into Selenium browser"""
        self.page.send_keys(word)
        self.page.send_keys(Keys.RETURN)
        time.sleep(2)

    def get_data(self):
        """goes and gets data from the website and the state of our inputted word. Whether it was correct,
        wrong, and correct letter placements"""
        local_data = self.driver.execute_script("return window.localStorage;")
        game_info = local_data["nyt-wordle-state"]  # inspected page source found state of game you are on
        evaluator = json.loads(game_info)["evaluations"]  # friend jason loads the game info and returns
        return evaluator

    def correct_stats(self, word):
        """After the Bot has completed the puzzle, it will upload its data to a csv file"""
        data = [datetime.now().date(), word, self.count]
        w = str(word)
        with open('worddata.csv', 'r') as f:
            s = f.read() #reads csv file completely
        if w not in s: #if word not in CSV s ^ then reopen the file
            with open('worddata.csv', 'a+') as f:
                writer = csv.writer(f) #csv writer declaration
                writer.writerow(data) #write data line to csv
        else:
            print("Word has already been solved and added to worddata.csv")


class Bot(Wurdle):
    """main program, iterates through list of words using Wurdle setup parameters, guessing and evaluating as it goes"""

    def eval(self):
        """inputs selected two guesses and edits our possible words list based off the response of evaluator,
         inputs a most probable answer after"""
        guesses = ['soare', 'clint']
        # ['brown', 'shade']
        #Next task, append known list for words already in worddata.csv
        # with open('worddata.csv', 'r') as f:
        #     s = csv.reader(f) #reads csv file completely
        #     c = datetime.now().date()
        #     for row in s:
        #         if str(c) in row[0]:
        #             possible_words = self.wDict
        #         else:
        #             possible_words = [word for word in self.wDict if (word.isalpha() not in list(s))]
       #idea almost working


        # [possible_words not in solved in self.wDict]
        # something like possible_words = [x for x in dictionary_possible_words if x not in v]
        # print("in list before are:", possible_words)
        possible_words = self.wDict

        known_l = []
        # known letters list
        word = guesses[0]
        self.enter_word(word)
        evaluator = self.get_data()


        for q in range(5):
            stats = evaluator[q]
            correct_tally = 0
            for i in range(5):
                if (stats[i] != "absent") and (not word[i] in known_l):
                    known_l.append(word[i])

                elif stats[i] == "correct":
                    correct_tally += 1
            if correct_tally == 5:
                time.sleep(2.5)
                self.page.click()
                quit()
            for i in range(5):
                letter = word[i]
                if stats[i] == "absent":
                    if letter in known_l:
                        possible_words = [x for x in possible_words if (x.count(letter) == 1) and (x[i] != letter)]
                    else:
                        possible_words = [x for x in possible_words if letter not in x]
                elif stats[i] == "present":
                    possible_words = [x for x in possible_words if (letter in x) and (x[i] != letter)]
                elif stats[i] == "correct":
                    possible_words = [x for x in possible_words if letter == x[i]]
            if q < 1:
                word = guesses[q + 1]

            else:
                word = possible_words[0]

            self.enter_word(word)
            self.count += 1
            evaluator = self.get_data()
            while type(evaluator[q + 1]) is not list:
                try:
                    for i in range(5):
                        word = possible_words[0]
                        self.page.send_keys(Keys.BACKSPACE)
                        possible_words.remove(word)

                        self.enter_word(word)
                finally:
                    self.correct_stats(word)
                    return self.count

        time.sleep(2.5)
        self.page.click()


wurdle = Bot()
wurdle.eval()

# 92% success rate since April 13th
# edited by request to increase competitiveness, now guesses in 3 rather than 2.
