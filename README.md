# ReShare

ReShare is a simple web application that is designed as a trading/sharing platform between users. It uses Python Flask as its infrastructure to allow users to create an account, sell or buy items. 

As seen with the recent COVID-19 pandemic, common household items such as toilet paper can be made scarce. Therefore, the purpose of ReShare is to act as a simple trading platform, where users who are feeling generous can post up items as donations to other users seeking these items immediately. With the scarcity of some products, all users are only able to purchase one item to prevent scalping of such items.

This web application is meant to be a simplified version of other selling platforms (i.e. eBay) and is intended for myself to experiment using APIs and databases for the first time.

# Requirements
- Python 3 or above
- pip3

# Techstack
- Flask framework that serves the backend for the database and API calls
- Jinja2
- Vanilla Javascript for client side DOM manipulation

# Setup
*Important Note: A bug exist where images may not be shown to the user.*
Users can either visit the hosted version at http://reshare.azurewebsites.net/ or simply setup this locally with these steps:
1) Clone the repository locally
`git clone https://github.com/gtangelo/ReShare.git`
2) Set up virtual environment inside the directory by using the following commands (linux):
`python3 -m virtualenv venv`
`source venv/bin/activate`
`pip3 install -r requirements.txt`
`python3 run.py`
Then open ReShare at your localhost (i.e. http://127.0.0.1:5001/)

# Features of ReShare
Features can be explored simply by using the website. However, the following lists out on what the user can do in ReShare:
1) Create an account
2) View Purchase History
3) Add review comments to certain posts
4) Buy/Sell/View items from different users
5) Like/Dislike items through a like bar

Three main sections:
Home: Lists all items
Feed: Lists other user's items
Your Posts: List your items

# Admin Privileges
Using the username `admin` and password `admin` grants full admin privileges of the forum application. From here, `admin` user can:
- delete and/or edit all user's posts
- delete comments
- delete certain users

# Placeholder Data
ReShare has placeholder users that you can use with the following credentials:
- Username: John Smith  Password: johnsmith  
- Username: Taylor      Password: taylor  
- Username: Andrew      Password: andrew  
- Username: user1       Password: user1  
- Username: user2       Password: user2  
- Username: user3       Password: user3

