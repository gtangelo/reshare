from flask import Flask, render_template

app = Flask(__name__)

feed_posts = [
    {
        'id' : 0,
        'title': 'I am a comp god',
        'content': 'comp god rant',
        'author': 'Ray Zone',
        'date': '01/06/20',
        'likes': 53,
        'dislikes': 1
    },
    {
        'id' : 1,
        'title': 'I am a sci god',
        'content': 'comp 2041 rant',
        'author': 'Alex Zone',
        'date': '01/06/20',
        'likes': 53,
        'dislikes': 1
    },
      {
        'id' : 2,
        'title': 'I am a math god',
        'content': 'king rant',
        'author': 'John Smith',
        'date': '01/06/20',
        'likes': 53,
        'dislikes': 1
    }
]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/home')
def home():
    return render_template("home.html", feed=feed_posts)

@app.route('/settings')
def settings():
    return render_template("settings.html")

@app.route('/about')
def about():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)