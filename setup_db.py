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
post_content = "Selling some toilet papers to give back to the community! :)"
new_post = PostData(content=post_content, author="admin", item="toilet paper", stock=3)
db.session.add(new_post)
db.session.commit()