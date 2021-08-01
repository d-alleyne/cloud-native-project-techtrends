import sys
import sqlite3
import logging
from flask import Flask, render_template, request, url_for, redirect, flash, json

# Function to get a database connection.
# This function connects to database with the name `database.db`
DATABASE_FILE = './database.db'

def get_db_connection():
    app.logger.debug(f'Connecting to database file {DATABASE_FILE}')
    try:
        connection = sqlite3.connect(DATABASE_FILE)
        result = connection.execute("SELECT COUNT(name) FROM sqlite_master WHERE name='posts'").fetchone()
        if result[0] != 1:
            message = "The required database table 'posts' is missing"
            app.logger.debug(message)
            raise Exception(message)
    except Exception as e:
        raise e
    else:
        connection.row_factory = sqlite3.Row
        return connection

# Function to get a post using its ID


def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                              (post_id,)).fetchone()
    connection.close()
    return post


# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application


@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered
# If the post ID is not found a 404 page is shown


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)

    if post is None:
        app.logger.debug(f'article with post ID {post_id} does not exist.')
        return render_template('404.html'), 404
    else:
        app.logger.debug(
            f'Article "{post["title"]}" page retrieved.')
        return render_template('post.html', post=post)

# Define the About Us page


@app.route('/about')
def about():
    app.logger.debug(
            f'The "About Us" page retrieved.')
    return render_template('about.html')

# Define the Health endpoint


@app.route('/healthz')
def status():
    try: 
        get_db_connection()
    except Exception as e:
        return app.response_class(
            response=json.dumps({'result':f'Error - {e.args[0]}'}),
            status=500,
            mimetype='application/json'
        )
    else:
        return {
            "result": "OK - healthy"
        }

# Define the metrics endpoint


@app.route('/metrics')
def metrics():
    connection = get_db_connection()
    post_count = 0
    with connection:
        posts = connection.execute('SELECT COUNT(*) FROM posts').fetchone()
        post_count = posts[0]

    return {
        'db_connection_count': 1,
        'post_count': post_count
    }


# Define the post creation functionality
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                               (title, content))
            connection.commit()
            connection.close()
            app.logger.debug(f'New page created, with Title "{title}"')

            return redirect(url_for('index'))

    return render_template('create.html')


# start the application on port 3111
if __name__ == "__main__":
    FORMAT = '%(asctime)-15s -- %(funcName)s -- %(message)s'
    logging.basicConfig(
        level=logging.DEBUG,
        format=FORMAT,
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler(),
            logging.StreamHandler(stream=sys.stdout)
        ])
    app.run(host='0.0.0.0', port='3111')
