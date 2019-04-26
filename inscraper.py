# Import libraries
import requests
from bs4 import BeautifulSoup
import random


base_url = 'https://www.instructables.com'
homepage = requests.get(base_url)


# Create a BeautifulSoup object
soup = BeautifulSoup(homepage.text, 'html.parser')

instruction_categories = list()
# Find category links
for link in soup.find('div', {'id': "home-categories-menu"}):
    instruction_categories.append(link.get('href'))


## Search for individual instructions
test_topic = instruction_categories[0]
topic_page = requests.get(base_url + test_topic)
soup2 = BeautifulSoup(topic_page.text, 'html.parser')


article_list = list()

for link in soup2.findAll(class_='title'):
    article_list.append(link.find('a').get('href'))
    # Randomize selection here?

test_article = article_list[0]


# Get text from an individual article
instruction_page = requests.get(base_url+test_article)
instructable = BeautifulSoup(instruction_page.text, 'html.parser')


##### 
# Work with the test page.
title = instructable.find('h1').text

step_titles = list()
for step in instructable.findAll(class_='step-title'):
    step_titles.append(step.text)


step_body = list()
for text in instructable.findAll(class_='step-body'):
    step_body.append(text.text)