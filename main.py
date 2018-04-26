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


@app.route('/', methods=['POST','GET'])
def index():
    

    posts = Task.query.all()
    completed_posts = Task.query.filter_by(completed=True).all()
    return render_template('todos.html',title="Blogosphere", 
        posts=posts, completed_posts=completed_posts)


@app.route('/posting', methods=['POST','GET'])
def posting_task():

    error1 = ""
    error2 = ""
    if request.args.get('error1'):
        error1 = request.args.get('error1')
    if request.args.get('error2'):
        error2 = request.args.get('error2')

    return render_template('posting.html',title="Post",e1=error1,e2=error2)

@app.route('/posted', methods=['POST','GET'])
def posted(): 

    post_title = request.form['title']
    post_body = request.form['post']
    error=False
    error1=''
    error2=''

    if post_title == '':
        error1 = "Must Have Title"
        error=True
    elif len(post_title) > 30:
        error1 = "Title Must Be Less than 30 Characters"
        error=True

    if post_body == '':
        error2 = "Cannot Be Blank"
        error=True
    elif len(post_body) > 120:
        error2 = "This post is too dang long"
        error=True

    if error:
        return redirect('/posting?error1='+error1+"&error2="+error2) #?error1='+error1+"&error2="+error2
    
    new_post = Task(post_title,post_body)    
    db.session.add(new_post)
    db.session.commit()
    post_id = str(new_post.id)

    return redirect('/view?id='+ post_id )

@app.route('/view', methods=['GET'])
def view(): 

    post_id = request.args.get('id')
    post = Task.query.get(post_id)
    post_title=post.title
    post_name=post.name

    return render_template('view.html',post_title=post_title,post_name=post_name)      

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