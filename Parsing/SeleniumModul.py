from selenium.webdriver.common.keys import Keys


def click_input_Enter(tmp_element, input_text):
    tmp_element.click()
    tmp_element.clear()
    tmp_element.send_keys(input_text)
    tmp_element.send_keys(Keys.RETURN)


def click_input(tmp_element, input_text):
    tmp_element.click()
    tmp_element.clear()
    tmp_element.send_keys(input_text)
