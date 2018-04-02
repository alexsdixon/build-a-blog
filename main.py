from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime



app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:beproductive@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'f8wv3w2f>v9j4sEuhcNYydAGMzzZJgkGgyHE9gUqaJcCk^f*^o7fQyBT%XtTvcYM'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    b_info= db.Column(db.String(120))
    posted = db.Column(db.DateTime)
    
    def __init__(self, name, b_info):
        self.name = name
        self.b_info = b_info
        self.posted = datetime.utcnow()




@app.route('/', methods=['GET'])
def index():

    return redirect("/blog")

@app.route("/blog")
def list_blogs():

    blog_id = request.args.get('id')
    if (blog_id):
        blog = Blog.query.get(blog_id)
        return render_template('blog_page.html', title="Build A Blog", blog=blog)
    
    sort = request.args.get('sort')
    if (sort=="newest"):
        all_blogs = Blog.query.order_by(Blog.posted.desc()).all()
    else:
        all_blogs = Blog.query.all()
    return render_template('view.html', title="Build A Blog", all_blogs=all_blogs)
     


@app.route('/add', methods=['GET', 'POST'])
def add():
    name_error = ''
    body_error = ''

    if request.method == 'POST':
        blog_name = request.form['blog']
        blog_body = request.form['blog_info']
        if blog_name.strip() == "":
            name_error = 'please enter a Blog Title'
            blog_name = ''
            
        if blog_body.strip() == "":
            body_error = 'please enter something to get posted'
            blog_body = ''
        if not name_error and not body_error:
             new_blog = Blog(blog_name, blog_body)
             db.session.add(new_blog)
             db.session.commit()
             url = "/blog?id=" + str(new_blog.id)
             return redirect(url)
        else:
            return render_template('add.html',blog_name=blog_name, blog_body=blog_body, name_error=name_error, body_error=body_error)
    else:

        return render_template('add.html')

if __name__ == '__main__':
    app.run()