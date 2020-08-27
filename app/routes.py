from flask import render_template, request, redirect, url_for, flash, request, jsonify
from app import app, db, bcrypt
from app.models import PostData, CommentData, UserData, VoteData
from app.forms import LoginUser, RegisterUser, CreatePost, CreateComment
from flask_login import login_user, login_required, logout_user, current_user


# Index Page
@app.route('/')
def index():
    feed_posts = PostData.query.filter_by(author="admin").order_by(PostData.likes.desc()).all()
    return render_template("index.html", feed=feed_posts)

# Shows home page for user
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    form = CreatePost()
    # Get all data from the form, process it and send it to the db
    if form.validate_on_submit():
        new_post = PostData(title=form.title.data, 
                            content=form.content.data, 
                            author = current_user.username)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        # Get post from db and order it by most voted posts in descending order
        feed_posts = PostData.query.order_by(PostData.likes.desc()).all()
        return render_template("home.html", form=form, feed=feed_posts)

# Shows all user own post on page
@app.route('/user/post')
@login_required
def user_posts():
    # Get post from db and order it by most voted posts in descending order
    feed_posts = PostData.query.filter_by(author=current_user.username).order_by(PostData.likes.desc()).all()
    return render_template("posts.html", feed=feed_posts)


# Shows full context of posts and its comments
@app.route('/post/<int:id>', methods=['GET', 'POST'])
def display_post(id):
    post = PostData.query.get_or_404(id)
    form = CreateComment()
    if form.validate_on_submit():
        new_comment = CommentData(post_id = id, content = form.content.data, author = current_user.username)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('display_post', id=id))
    else:
        # TODO: Change it into ordering by popular posts
        comments = CommentData.query.filter_by(post_id=id).order_by(CommentData.date).all()
        return render_template('display_post.html', post=post, comments=comments, form=form)

# Allows user of the post to edit its contents
@app.route('/home/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = PostData.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title'] if request.form['title'] != '' else '[deleted]'
        post.content = request.form['content'] if request.form['content'] != '' else '[deleted]'
        db.session.commit()
        flash(f'All changes to the post have been saved', 'success')
        return redirect(request.referrer)
    else:
        return render_template('edit.html', post=post)

# Deletes user account from database
@app.route('/user/delete/<int:id>')
def delete_user(id):
    user = UserData.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin'))

# Deletes the selected post and all comments associated with that post
@app.route('/post/delete/<int:id>')
def delete_post(id):
    post = PostData.query.get_or_404(id)
    comments = CommentData.query.filter_by(post_id = id).all()
    for comment in comments:
        db.session.delete(comment)
    db.session.delete(post)
    db.session.commit()
    return redirect(request.referrer)

# Deletes a specified comment
@app.route('/post/comment/delete/<int:id>')
def delete_comment(id):
    comment = CommentData.query.get_or_404(id)
    post_id = comment.post_id
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('display_post', id=post_id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterUser()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = UserData(username=form.username.data, password=hash_password)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Account created for {form.username.data}. You are now logged in as {form.username.data}', 'success')
        user = UserData.query.filter_by(username=form.username.data).first()
        login_user(user)
        return redirect(url_for('home'))
    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginUser()
    if form.validate_on_submit():
        user = UserData.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'You are now logged in as {user.username}', 'success')
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
        else:
            flash('Login Failed. Incorrect username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# @app.route('/account')
# def account():
#     img = url_for('static', filename='default.jpg')
#     return render_template("settings.html", img = img)

@app.route('/about')
def about():
    return render_template("about.html")

# Admin panel to show all posts and users for convienance
@app.route('/admin')
@login_required
def admin():
    feed_posts = PostData.query.order_by(PostData.date.desc()).all()
    users = UserData.query.filter(UserData.username!="admin").order_by(UserData.id.desc()).all()
    return render_template("admin.html", feed=feed_posts, users=users)

# Keeps track on which posts the user has liked or disliked. Data on 
# liked/disliked posts are stored in a database
@app.route('/post/votes/<int:id>', methods=['GET','POST'])
def manage_votes(id):
    post = PostData.query.get(id)
    if request.method == "GET":
        return jsonify({'likes':post.likes, 'dislikes':post.dislikes})
    else:
        post.likes = request.form['likes']
        post.dislikes = request.form['dislikes']
        status = request.form['status']
        isLike = request.form['vote']
        if status == "remove":
            VoteData.query.filter_by(post_id=request.form['post_id'], user_id=current_user.id).delete()
        elif status == "add":
            new_vote = VoteData(post_id=request.form['post_id'], user_id=current_user.id, like_post=int(isLike))
            db.session.add(new_vote)
        elif status == "change":
            user_vote = VoteData.query.filter_by(post_id=request.form['post_id'], user_id=current_user.id).first()
            user_vote.like_post = not user_vote.like_post
        db.session.commit()
        return redirect(request.referrer)

# API to return if a post has been voted by the user or not
@app.route('/post/votes/status/<int:id>')
def get_vote_status(id):
    post = VoteData.query.filter_by(post_id=id, user_id=current_user.id).first()
    if post:
        return jsonify({"status": post.like_post})
    else:
        return jsonify({"status": "null"})


