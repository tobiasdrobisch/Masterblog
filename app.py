from flask import Flask,request, render_template, redirect,url_for
import json

app = Flask(__name__)

blog_posts = [
    {"id": 1, "author": "John Doe", "title": "First Post", "content": "This is my first post."},
    {"id": 2, "author": "Jane Doe", "title": "Second Post", "content": "This is another post."}
]
def load_json():

    # Datei öffnen und JSON laden
    with open("blog_posts.json", "r", encoding="utf-8") as f:
        blog_posts  = json.load(f)
        return blog_posts

def save_to_json(blog_posts):
    with open("blog_posts.json", "w", encoding="utf-8") as f:
        json.dump(blog_posts, f, indent=4, ensure_ascii=False)


@app.route('/')
def index():
    # add code here to fetch the job posts from a file
    # JSON-Datei laden
    with open("blog_posts.json", "r", encoding="utf-8") as f:
        blog_posts = json.load(f)

    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':

        posts = load_json()

        if posts:
            new_id = max(post["id"] for post in posts) + 1
        else:
            new_id = 1

        new_post = {
            "id":       new_id,
            "title":    request.form.get("title"),
            "author":   request.form.get("author"),
            "content":  request.form.get("content")
        }

        posts.append(new_post)
        save_to_json(posts)

        # We will fill this in the next step
        # Add the code that handles adding a new blog
        ...
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    posts = load_json()
    for post in posts:
        # Find the blog post with the given id and remove it from the list
        if post["id"] == post_id:
            posts.remove(post)
            break
    save_to_json(posts)
    # Redirect back to the home page
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    posts = load_json()
    for post in posts:
        if post is None:
            # Post not found
            return "Post not found", 404

        # Fetch the blog posts from the JSON file
        if post["id"] == post_id:
            if request.method == 'POST':
                # Update the post in the JSON file
                post["title"] = request.form.get("title")
                post["author"] = request.form.get("author")
                post["content"] = request.form.get("content")

                save_to_json(posts)
                # Redirect back to index
                return redirect(url_for('index'))
            # Else, it's a GET request
            else:
                # So display the update.html page
                return render_template('update.html', post=post)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)