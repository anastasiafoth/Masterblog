from flask import Flask, render_template
import json


BLOG_POSTS_FILE = 'data/blog_posts.json'

app = Flask(__name__)

@app.route('/')
def index():
    #Reading blog posts from json file
    try:
       with open(BLOG_POSTS_FILE, 'r') as fileobj:
           blog_posts = json.load(fileobj)

    except FileNotFoundError:
        blog_posts = []
        print("Error loading blog posts")

    #generating html based on template
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)