from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

# Model for database contating posts
class FeedPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='Unknown')
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "Post ID: " + str(self.id)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/home', methods=['GET', 'POST'])
def home():
    # Get all data from the form, process it and send it to the db
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = FeedPost(title = post_title, content = post_content, author = post_author)
        db.session.add(new_post)
        # Save posts for future
        db.session.commit()
        return redirect('/home')
    else:
        # Get post from db and order it by date in descending order
        feed_posts = FeedPost.query.order_by(FeedPost.date.desc()).all()
        return render_template("home.html", feed=feed_posts)

@app.route('/home/delete/<int:id>')
def delete_post(id):
    post = FeedPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/home')

@app.route('/home/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = FeedPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        db.session.commit()
        return redirect('/home')
    else:
        return render_template('edit.html', post=post)

def settings():
    return render_template("settings.html")


@app.route('/settings')
def settings():
    return render_template("settings.html")

@app.route('/about')
def about():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)