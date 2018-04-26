from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:beproductive@localhost:8889/get-it-done'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    name = db.Column(db.String(500))
    completed = db.Column(db.Boolean)

    def __init__(self, title, name):
        self.title = title
        self.name = name
        self.completed = False


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        post_title = request.form['title']
        post_name = request.form['post']
        new_post = Task(post_title,post_name)
        db.session.add(new_post)
        db.session.commit()

    posts = Task.query.all()
    completed_posts = Task.query.filter_by(completed=True).all()
    return render_template('todos.html',title="Blogosphere", 
        posts=posts, completed_posts=completed_posts)



@app.route('/delete-post', methods=['POST'])
def delete_task():

    post_id = int(request.form['post-id'])
    post = Task.query.get(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect('/')

@app.route('/like-post', methods=['POST'])
def like_task():

    post_id = int(request.form['post-id'])
    post = Task.query.get(post_id)
    post.completed = True
    db.session.add(post)
    db.session.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run()