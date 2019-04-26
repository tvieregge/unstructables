from flask import Flask
app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def home():
    return generate_html()

def generate_html():
    return 'Hello, World!'
