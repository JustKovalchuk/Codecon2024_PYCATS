import time
import requests
from bs4 import BeautifulSoup
from SeleniumModul import *

parse_category = ["Армія","Переселенці"]

url="https://volonter.org/dopomoga-volonterski-proekty"
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(url)


class Info():
    def __init__(self,name,location,owner,date,url):
        self.name=name
        self.location=location
        self.owner=owner
        self.date=date
        self.url = url

    def Display(self):
        print("="*20)
        print(f"Name:: {self.name}")
        print(f"Location:: {self.location}")
        print(f"Owner:: {self.owner}")
        print(f"Date:: {self.date}")
        print(f"Url:: {self.url}")



element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="wrapper"]/div/div/div/section/div[2]/ul')))

li_elements = element.find_elements(By.TAG_NAME,"li")

for li in li_elements:
    name_element = li.find_element(By.CLASS_NAME,"text").text.lower()
    for category in parse_category:
        if category and name_element == category.lower():
            li.click()
search_btn = driver.find_element(By.XPATH,'//*[@id="wrapper"]/div/div/div/section/div[3]/a[2]')
search_btn.click()

time.sleep(2)

#more
flag = True
name_and_url = []

while flag:

    try:
        more_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='wrapper']/div/div/section/div[4]/a")))
        more_btn.click()
    except:
        flag=False

        name_elements = driver.find_elements(By.XPATH, '//*[@id="wrapper"]/div/div/section/div[3]/*/div/h3')
        count_new = 0
        for i in name_elements:
            tmp_data = {"name": "", "url": ""}
            tmp_name_element = i.find_element(By.TAG_NAME,'a')
            tmp_url = tmp_name_element.get_attribute("href")
            tmp_data["name"] = tmp_name_element.text
            tmp_data["url"] = tmp_url
            name_and_url.append(tmp_data)



info_results = []

for i in name_and_url:
    driver.get(i['url'])

    tmp_element = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div/div[1]/ul')
    tmp = tmp_element.find_elements(By.TAG_NAME,'li')
    owner = driver.find_element(By.CLASS_NAME, 'author-name')
    info_results.append(Info(i['name'],tmp[1].text,owner.text,tmp[0].text, i['url']))
    print('•',end='')

print()

for i in info_results:
    i.Display()

input()
driver.quit()


