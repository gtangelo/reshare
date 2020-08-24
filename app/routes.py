from flask import render_template, request, redirect, url_for, flash
from app import app
from app.models import FeedPost, PostComments, Users
from app.forms import LoginUser, RegisterUser


@app.route('/')
def index():
    return render_template("index.html")

# Shows feed of top posts
@app.route('/home', methods=['GET', 'POST'])
def home():
    # Get all data from the form, process it and send it to the db
    if request.method == 'POST':
        post_title = request.form['title'] if request.form['title'] != '' else '[deleted]'
        post_content = request.form['content'] if request.form['content'] != '' else '[deleted]'
        post_author = request.form['author'] if request.form['author'] != '' else '[deleted]'
        new_post = FeedPost(title = post_title, content = post_content, author = post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/home')
    else:
        # TODO: Change it into ordering by popular posts
        # Get post from db and order it by date in descending order
        feed_posts = FeedPost.query.order_by(FeedPost.date.desc()).all()
        return render_template("home.html", feed=feed_posts)

# Deletes selected posts and all comments associated with that post
@app.route('/home/delete/<int:id>')
def delete_post(id):
    post = FeedPost.query.get_or_404(id)
    comments = PostComments.query.filter_by(post_id = id).all()
    for comment in comments:
        db.session.delete(comment)
    db.session.delete(post)
    db.session.commit()
    return redirect('/home')

# Deletes a specified comment
@app.route('/post/comment/delete/<int:id>')
def delete_comment(id):
    comment = PostComments.query.get_or_404(id)
    post_id = comment.post_id
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('display_post', id=post_id))

# Allows to edit a post
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


# Shows full context of posts and its comments
@app.route('/post/<int:id>', methods=['GET', 'POST'])
def display_post(id):
    post = FeedPost.query.get_or_404(id)
    if request.method == 'POST':
        comment_post_id = request.form['post-id']
        comment_content = request.form['content'] if request.form['content'] != '' else '[deleted]'
        comment_author = "John Smith"
        new_comment = PostComments(post_id = comment_post_id, content = comment_content, author = comment_author)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('display_post', id=id))
    else:
        # TODO: Change it into ordering by popular posts
        comments = PostComments.query.filter_by(post_id=id).order_by(PostComments.date.desc()).all()
        return render_template('display_post.html', post=post, comments=comments)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterUser()
    if form.validate_on_submit():
        user_username = request.form['username']
        user_password = request.form['password']
        new_user = Users(username = user_username, password = user_password)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Account created for {form.username.data}', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginUser()
    if form.validate_on_submit():
        if form.username.data == 'admin' and form.username.data == 'admin':
            flash('Admin Login', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Failed', 'danger')
    return render_template('login.html', form=form)

@app.route('/settings')
def settings():
    return render_template("settings.html")

@app.route('/about')
def about():
    return render_template("index.html")
