import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

root_url = 'https://hertie-scraping-website.vercel.app/'

req = requests.get(root_url)

s = BeautifulSoup(req.content, 'html.parser')

flag_text = re.compile("^flag")

flags = set()

# Get the first 8 flags
for flag in s.find_all('p'):
    flag = flag.get_text()
    if flag_text.match(flag):
        flags.add(flag)

# The bottom two also address the hidden img flag

# Get the flags stored in divs that start with "flag" (div)
for flag in s.find_all('div', class_=flag_text):
    flags.add(flag['class'][0])

# Get the flags stored in divs that start with "flag" (class)
for flag in s.find_all('div', id = flag_text):
    flags.add(flag['id'])


page2 = "wowimlevel2"
req = requests.get(root_url + page2)
s = BeautifulSoup(req.content, 'html.parser')

# Get the 41st flag
flags.add(re.findall('flag-[0-9]{2}', s.find('div', class_='my-4').get_text())[0])

# Get the flags stored in divs that start with "flag" (div)
for flag in s.find_all('div', class_=flag_text):
    flags.add(flag['class'][0])

# Get the flags stored in divs that start with "flag" (class)
for flag in s.find_all('div', id = flag_text):
    flags.add(flag['id'])

# Some of the remaing flags live inside scripts
for script in s.find_all('script'):
    try:
        for flag in re.findall('flag-[0-9]+', script.get_text()):
            flags.add(flag)
    except:
        pass

# Page 3 buttons before clicking
page3 = "goodjobfindinglevel3"
req = requests.get(root_url + page3)
s = BeautifulSoup(req.content, 'html.parser')
for button in s.find_all('button', id = flag_text):
    flags.add(button['id'])

options = webdriver.FirefoxOptions()
options.binary_location = "~/Downloads/geckodriver"
driver = webdriver.Firefox()

# Page 3 buttons after clicking
driver.get(root_url + page3)
buttons = driver.find_elements(By.XPATH, "//button")
for button in buttons:
    try:
        button.click()
    except:
        pass
buttons = driver.find_elements(By.XPATH, "//button")
for button in buttons:
    flags.add(button.text)

# Page 4 uses a hidden input field
page4 = "finalboss"
driver.get(root_url + page4)
input_element = driver.find_element(By.CSS_SELECTOR, 'input[type="text"]')
input_element.clear()
input_element.send_keys("!!flag-61!!")
divs = driver.find_elements(By.XPATH, "//div")
print(divs)
for div in divs:
    for flag in re.findall('flag-[0-9]+', div.text):
        flags.add(flag)

# Print flags in order
sorted_flags = sorted(flags, key=lambda x: int(x.split('-')[1]))
for flag in sorted_flags:
    print(flag)