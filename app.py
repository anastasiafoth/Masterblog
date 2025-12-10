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


def writing_files(blog_posts):
    with open(BLOG_POSTS_FILE, 'w') as fileobj:
        json.dump(blog_posts, fileobj, indent=4)

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

            writing_files(blog_posts)

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

        writing_files(blog_posts_new)

        print("The post was successfully deleted.")
        return redirect(url_for('index'))

    except Exception as e:
        print(f"Error deleting post: {e}")
        return "Error deleting post", 500


def fetch_post_by_id(post_id):
    blog_posts = reading_file()
    for post in blog_posts:
        if post['id'] == post_id:
            return post
    return None


@app.route('/update/<int:post_id>', methods=['GET','POST'])
def update_post(post_id):
    """ Updates a blogpost """
    # Fetch the blog posts from the JSON file
    post = fetch_post_by_id(post_id)

    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        try:
            # Get updated data from form
            updated_post = {
                'id' : post_id,
                'author' : request.form.get('author', ''),
                'title' : request.form.get('title', ''),
                'content' : request.form.get('content', '')
            }

            # Read all posts
            blog_posts = reading_file()

            # Update the post in the JSON file
            new_blog_posts = []
            for p in blog_posts:
                if p['id'] == post_id:
                    new_blog_posts.append(updated_post)
                else:
                    new_blog_posts.append(p)

            writing_files(new_blog_posts)

            # Redirect back to index
            return redirect(url_for('index'))

        except Exception as e:
            print(f"Error updating post: {e}")
            return "Error updating post", 500

    # GET request displays the update.html page
    return render_template('update.html', post=post)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)