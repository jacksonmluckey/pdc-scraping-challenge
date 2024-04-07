import requests
from bs4 import BeautifulSoup
import re

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

for flag in flags:
    print(flag)