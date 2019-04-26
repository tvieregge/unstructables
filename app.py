from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from random import choice, randint
from collections import namedtuple

Article = namedtuple('Article', 'pagetitle intro author avatar step_bodies step_titles')

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def home():
    return generate_html()

def get_pages(base_url):
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

def get_two_pages(pages):
    page1 = choice(pages)
    pages.remove(page1)
    page2 = choice(pages)
    return (page1, page2)

def parse_article(article):
    instruction_page = requests.get(article)
    instructable = BeautifulSoup(instruction_page.text, 'html.parser')

    # Work with the test page.
    pagetitle = instructable.find('h1').text
    intro_section = instructable.find('section',{'id':'intro'})

    print(article)
    intro_p = intro_section.find('p').text
    author = intro_section.find(class_="author").text
    avatar = intro_section.find(class_="avatar").find('img')['src']

    step_titles = list()
    for step in instructable.findAll(class_='step-title'):
        step_titles.append(step.text)


    step_bodies = list()
    for text in instructable.findAll(class_='step-body'):
        step_bodies.append(text.text)
    step_bodies.pop(0)

    return Article(pagetitle, intro_p, author, avatar, step_bodies, step_titles)


def combine_lists(list1, list2):
    ret_list = []
    for e in zip(list1, list2):
        pick = randint(0,1)
        ret_list.append(e[pick])
        print("+++")
        print(pick)

    return ret_list


def combine_articles(article1, article2):
    comb_titles = combine_lists(article1.step_titles, article2.step_titles)
    comb_bodies = combine_lists(article1.step_bodies, article2.step_bodies)
    return Article(article2.pagetitle, article1.intro, article1.author, article1.avatar, comb_bodies, comb_titles)

def generate_html():
    base_url = 'https://www.instructables.com'

    all_pages = get_pages(base_url)
    if len(all_pages) < 2:
        return "Not enough articles :("

    print("---------")
    page_pair = get_two_pages(all_pages)
    print(page_pair)

    # Get text from an individual article
    article1 = parse_article(base_url+page_pair[0])
    article2 = parse_article(base_url+page_pair[1])

    output_article = combine_articles(article1, article2)
    print(output_article)

    print("---------")
    return render_template('content.html',
        pagetitle=output_article.pagetitle, intro=output_article.intro, author=output_article.author, avatar=output_article.avatar,
        content=output_article.step_bodies, titles=output_article.step_titles)

if __name__ == '__main__':
    app.run(debug=True)
