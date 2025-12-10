from flask import Flask, render_template, request, redirect, url_for
import json


BLOG_POSTS_FILE = 'data/blog_posts.json'

app = Flask(__name__)

def reading_file():
    """ Reading blog posts from json file"""
    try:
       with open(BLOG_POSTS_FILE, 'r') as fileobj:
           blog_posts = json.load(fileobj)

    except FileNotFoundError:
        blog_posts = []
        print("Error loading blog posts")
    return blog_posts


@app.route('/')
def index():
    blog_posts = reading_file()

    #generating html based on template
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        try:
            blog_posts = reading_file()
            # looking up existing IDs, so we can generate one
            if blog_posts:
                new_id = max(post['id'] for post in blog_posts) + 1
            else:
                new_id = 1

            #checks if there are any blog posts, if not, creates a list
            if type(blog_posts) == list:
                new_post = {
                    "id" : new_id,
                    "author": request.form['author'],
                    "title" : request.form['title'],
                    "content" : request.form['content']
                }
                blog_posts.append(new_post)
            else:
                blog_posts = [{
                    "id": new_id,
                    "author": request.form['author'],
                    "title": request.form['title'],
                    "content": request.form['content']
                }]

            with open(BLOG_POSTS_FILE, 'w') as fileobj:
                json.dump(blog_posts, fileobj, indent=4)

            return redirect(url_for('index'))
        except Exception as e:
            print(f"Error saving post: {e}")
            return "Error saving post", 500

    return render_template('add.html')

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    """ Find the blog post with the given id and
    remove it from the list and redirect back to homepage """

    try:
        blog_posts = reading_file()
        blog_posts_new = []

        for post in blog_posts:
            if post_id != post['id']:
                blog_posts_new.append(post)

        with open(BLOG_POSTS_FILE, 'w') as fileobj:
            json.dump(blog_posts_new, fileobj, indent=4)

        print("The post was successfully deleted.")
        return redirect(url_for('index'))

    except Exception as e:
        print(f"Error deleting post: {e}")
        return "Error deleting post", 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)