from flask import Flask
import requests
from bs4 import BeautifulSoup
from random import choice

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def home():
    return generate_html()

def get_articles(base_url):
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

    return article_list;

def get_two_articles(articles):
    return (articles[0], articles[1])

def generate_html():
    base_url = 'https://www.instructables.com'

    all_articles = get_articles(base_url)
    if len(all_articles) < 2:
        return "Not enough articles :("

    test_article = all_articles[0]
    article_pair = get_two_articles(all_articles)

    # Get text from an individual article
    instruction_page = requests.get(base_url+test_article)
    instructable = BeautifulSoup(instruction_page.text, 'html.parser')

    # Work with the test page.
    title = instructable.find('h1').text

    step_titles = list()
    for step in instructable.findAll(class_='step-title'):
        step_titles.append(step.text)


    step_body = list()
    for text in instructable.findAll(class_='step-body'):
        step_body.append(text.text)

    return str(step_titles)


if __name__ == '__main__':
    app.run(debug=True)
