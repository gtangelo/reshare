from app import app, db, bcrypt
from app.models import PostData, CommentData, UserData

db.drop_all()
db.create_all()

# Creating dummy data

# Create admin user
hash_password = bcrypt.generate_password_hash("admin").decode('utf-8')
new_user = UserData(username="admin", password=hash_password)
db.session.add(new_user)

# Create first post
post_content = "Welcome to my forum! Hope you have a great time!"
new_post = PostData(title="Announcement", content=post_content, author="admin")
db.session.add(new_post)
db.session.commit()