from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

# Database that contains all posts made by every user
class PostData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='Unknown')
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    likes = db.Column(db.Integer, nullable=False, default=0)
    dislikes = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return "Post ID: " + str(self.id)

# Model for database that is used with comments on posts
class CommentData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Which post that this comment belong to
    post_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='Unknown')
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    # likes = db.Column(db.Integer, nullable=False, default=0)
    # dislikes = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return "Comment ID: " + str(self.id) + "Post ID: " + str(self.post_id)

# Model for database that stores user credentials
class UserData(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    # profile_img = db.Column(db.String(50), nullable=False, default='default.jpg')

    def __repr__(self):
        return "Username: " + str(self.username)

@login_manager.user_loader
def load_user(user_id):
    return UserData.query.get(int(user_id))

class VoteData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    like_post = db.Column(db.Boolean, nullable=False)