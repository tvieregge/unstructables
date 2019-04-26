from flask import Flask, render_template
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
    test_topic = choice(instruction_categories)
    topic_page = requests.get(base_url + test_topic)
    soup2 = BeautifulSoup(topic_page.text, 'html.parser')

    article_list = list()

    for link in soup2.findAll(class_='title'):
        article_list.append(link.find('a').get('href'))

    return article_list;

def get_two_articles(articles):
    article1 = choice(articles)
    articles.remove(article1)
    article2 = choice(articles)
    return (article1, article2)

def parse_article(article):
    instruction_page = requests.get(article)
    instructable = BeautifulSoup(instruction_page.text, 'html.parser')

    # Work with the test page.
    title = instructable.find('h1').text

    step_titles = list()
    for step in instructable.findAll(class_='step-title'):
        step_titles.append(step.text)


    step_bodies = list()
    for text in instructable.findAll(class_='step-body'):
        step_bodies.append(text.text)

    return (step_titles, step_bodies)


def generate_html():
    base_url = 'https://www.instructables.com'

    all_articles = get_articles(base_url)
    if len(all_articles) < 2:
        return "Not enough articles :("

    article_pair = get_two_articles(all_articles)

    # Get text from an individual article
    (step_titles, step_body) = parse_article(base_url+article_pair[0])

    return render_template('content.html', content=step_body)


if __name__ == '__main__':
    app.run(debug=True)
