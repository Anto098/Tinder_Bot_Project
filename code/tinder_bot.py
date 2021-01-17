from random import randrange
import subprocess
import sys

reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
#print(f"installed_packages : {installed_packages}")

from selenium import webdriver
from time import sleep
import requests
from bs4 import BeautifulSoup
from secrets import username, password
from enum import Enum
import json

class ActionType(Enum):
    CLICK = 1
    INPUT = 2
CLICK = ActionType.CLICK
INPUT = ActionType.INPUT

PICKUP_LINES_FILE = 'borat_pickup_lines.json'

with open(PICKUP_LINES_FILE) as json_file:
    pickup_lines = json.load(json_file)

class TinderBot():
    def __init__(self):
        self.driver = webdriver.Chrome()

    def find_and_execute_action(self, actionType, toFind, toInput=""):
        btn = ''
        while not btn:
            try:
                btn = self.driver.find_element_by_xpath(toFind)
                if actionType.name == ActionType.CLICK.name:
                    btn.click()
                elif actionType.name == ActionType.INPUT.name:
                    btn.send_keys(toInput)
            except:
                sleep(1)
                continue


    def login(self):
        self.driver.get('https://tinder.com')

        # accept cookies or w/e
        self.find_and_execute_action(CLICK,'//*[@id="content"]/div/div[2]/div/div/div[1]/button')

        # click on login button
        self.find_and_execute_action(CLICK,'//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/button')
        
        # click on google login button
        login_w_google_btn=''
        while not login_w_google_btn:
            try:
                login_w_google_btn = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[1]/div/div[3]/span/div[1]/div/button')
            except:
                sleep(1)
                continue
        # for some reason this stupid button sometimes doesn't react when clicked once so I have to do this
        # it's really ugly but I have to yet to find a better way to do this
        while len(self.driver.window_handles) < 2:
            login_w_google_btn.click()
            sleep(0.5)

        # save base window and switch to popup window          
        sleep(2)
        base_window = self.driver.window_handles[0]
        self.driver.switch_to.window(self.driver.window_handles[1])

        #input username
        self.find_and_execute_action(INPUT,'//*[@id="identifierId"]', username)
        #click next
        self.find_and_execute_action(CLICK,'//*[@id="identifierNext"]/div/button')

        #input password
        self.find_and_execute_action(INPUT,'//*[@id="password"]/div[1]/div/div[1]/input', password)
        #click next/confirm or whatever
        self.find_and_execute_action(CLICK,'//*[@id="passwordNext"]/div/button')

        #go back to base window
        self.driver.switch_to.window(base_window)

        #remove first popup
        self.find_and_execute_action(CLICK,'//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
        #remove second popup
        self.find_and_execute_action(CLICK,'//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')

    def like(self):
        self.find_and_execute_action(CLICK,'//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button')

    def dislike(self):
        self.find_and_execute_action(CLICK,'//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[2]/button')

    def auto_swipe(self):
        sleep(10)
        while True:
            sleep(0.5)
            try:
                print("trying to like")
                self.find_and_execute_action(CLICK,'//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button')
                print("liked")
                try:
                    print("trying to close match")
                    self.close_match()
                except Exception:
                    print(f"Exception : {Exception}")
                    pass
                try:
                    print("trying to close upgrade your like")
                    self.close_upgrade_your_like()
                except Exception:
                    print(f"Exception : {Exception}")
                    pass
                try:
                    print("trying to close add to home screen")
                    self.close_add_to_home_screen()
                except Exception:
                    print(f"Exception : {Exception}")
                    pass
                try:
                    print("trying to close out of likes")
                    answer = self.close_out_of_likes()
                    print(f"answer = {answer}")
                    if answer:
                        print("closed out of likes")
                        break
                except Exception:
                    print(f"Exception : {Exception}")
                    pass
            except:
                pass

    def close_add_to_home_screen(self): #add tinder to your home screen
        try:
            sleep(0.5)
            button = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[2]/button[2]')
            button.click()
            print("first popup closed")
            sleep(0.5)
        except:
            pass
        
    def close_upgrade_your_like(self):
        try:
            sleep(0.5)
            btn = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/button[2]')
            btn.click()
            print("second popup closed")
            sleep(0.5)
        except:
            pass

    def close_out_of_likes(self):
        try:
            sleep(0.5)
            out_of_likes_button = self.driver.find_element_by_xpath('// *[@id = "modal-manager"]/div/div/div[3]/button[2]')
            out_of_likes_button.click()
            print("clicked on out of likes button")
            sleep(0.5)
            return True
        except:
            return False

                
    def close_match(self): # possibly wrong xpath
        sleep(0.5)
        close_match_btn = self.driver.find_elements_by_xpath('//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[4]/button')
        close_match_btn.click()
        sleep(0.5)

    def message_all(self):
        # find matchList
        matches = self.driver.find_elements_by_class_name("matchListItem")
        print(f"matches : {matches}")
        while matches:
            print(f"in while loop, matches : {matches}")
            # remove first element (just shows how many people liked you)
            # 2nd iteration and onwards : delete the match you just messaged
            matches[0].click()
            print(f"matches[0] : {matches[0]}")
            try:
                self.driver.find_element_by_xpath('//*[@id="chat-text-area"]')
                print(f"trying to input text")
                self.find_and_execute_action(INPUT, '//*[@id="chat-text-area"]', pickup_lines[str(randrange(len(pickup_lines)-1))])
                print(f"trying to click send")
                print('trying to enter a while loop')
                send_btn = ''
                while not send_btn:
                    print('In the while loop')
                    send_btn = self.driver.find_elements_by_class_name('button')[1]
                    print(f"send_btn : {send_btn}")
                    sleep(1)
                send_btn.click()
                #self.find_and_execute_action(CLICK, '//*[@id="content"]/div/div[1]/div/div/main/div/div[2]/form/button')
                print("clicking on the match tab")
            except:
                pass
            self.find_and_execute_action(CLICK, '//*[@id="match-tab"]')
            matches = matches[1:]


bot = TinderBot()
bot.login()
bot.auto_swipe()
bot.message_all()
