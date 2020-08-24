from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

# Model for database that is used for posts
class FeedPost(db.Model):
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
class PostComments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Which post that this comment belong to
    post_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='Unknown')
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    likes = db.Column(db.Integer, nullable=False, default=0)
    dislikes = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return "Comment ID: " + str(self.id) + "Post ID: " + str(self.post_id)

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    img_profile = db.Column(db.String(50), nullable=False, default='default.jpg')

    def __repr__(self):
        return "Username: " + str(self.username)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))