from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def click_input_Enter(tmp_element,input_text):
    tmp_element.click()
    tmp_element.clear()
    tmp_element.send_keys(input_text)
    tmp_element.send_keys(Keys.RETURN)


def click_input(tmp_element,input_text):
    tmp_element.click()
    tmp_element.clear()
    tmp_element.send_keys(input_text)