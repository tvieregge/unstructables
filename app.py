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
    pagetitle = instructable.find('h1').text
    intro_section = instructable.find('section',{'id':'intro'})

    intro_p = intro_section.find('p').text
    author = intro_section.find(class_="author").text
    avatar = intro_section.find(class_="avatar").find('img')['src']

    step_titles = list()
    for step in instructable.findAll(class_='step-title'):
        step_titles.append(step.text)


    step_body = list()
    for text in instructable.findAll(class_='step-body'):
        step_body.append(text.text)
    step_body.pop(0)

    return render_template('content.html', 
        pagetitle=pagetitle, intro=intro_p, author=author, avatar=avatar,
        content=step_body, titles=step_titles)


if __name__ == '__main__':
    app.run(debug=True)
