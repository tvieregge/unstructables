from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import random


app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def home():
    return generate_html()

def generate_html():
    base_url = 'https://www.instructables.com'
    homepage = requests.get(base_url)


    # Create a BeautifulSoup object
    soup = BeautifulSoup(homepage.text, 'html.parser')

    instruction_categories = list()
    # Find category links
    for link in soup.find('div', {'id': "home-categories-menu"}):
        instruction_categories.append(link.get('href'))


    ## Search for individual instructions
    test_topic = random.choice(instruction_categories)
    topic_page = requests.get(base_url + test_topic)
    soup2 = BeautifulSoup(topic_page.text, 'html.parser')


    article_list = list()

    for link in soup2.findAll(class_='title'):
        article_list.append(link.find('a').get('href'))

    test_article = random.choice(article_list)


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

    
    return render_template('content.html', content=step_body)


if __name__ == '__main__':
    app.run(debug=True)