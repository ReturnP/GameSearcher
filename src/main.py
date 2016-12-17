from flask import Flask,render_template,g,request,url_for, request,jsonify,redirect,session,flash
import requests
import json
import sqlite3
from functools import wraps
import random

app = Flask(__name__)


app.secret_key = "returnp" #TODO put in config file
app.database = "gameSearch.db"


def connect_db():
    return sqlite3.connect(app.database)

app.config.update(TEMPLATES_AUTO_RELOAD=True)
def login_req(s):
    @wraps(s)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return s(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap

app.config["TEMPLATES_AUTO_RELOAD"] = True

    
with open('config.json') as jData:
    apiKey = json.load(jData)['ApiKey']

@app.route('/')
def index():
    with open("static/img_links.txt") as f:
        img_list = f.readlines()
    img_url = random.choice(img_list)
    return render_template('index.html', img_url = img_url)

@app.route('/search')
def search():
    gameTitle = request.args.get("title","NONE",type=str)
    gameTitle = gameTitle.replace(' ', '')
    gameTitle = ''.join([i for i in gameTitle if not i.isdigit()])
    response = requests.get('https://igdbcom-internet-game-database-v1.p.mashape.com/games/?fields=name%2Ccover&limit=10&offset=0&order=rating%3Adesc&search={}'.format(gameTitle),headers={"X-Mashape-Key": apiKey,"Accept": "application/json"})
    title = response.json()
    return jsonify(result=title)


@app.route('/displayGame/<gameId>',methods=['GET','POST'])
def displayGame(gameId):

  
    response = requests.get("https://igdbcom-internet-game-database-v1.p.mashape.com/games/{}?fields=*".format(gameId), headers={
    "X-Mashape-Key": apiKey,
    "Accept": "application/json"
    })

    info = response.json()[0]
    title = info['name']
    comment = None
    if 'summary' in info:
        summary = info['summary']
    else:
        summary = 'No summary'
    if 'rating' in info:
        rating = info['rating']
        rating = str(("%.2f" % int(rating)))
    else:
        rating = 'No rating'
    if 'cover' in info:
        cover = info['cover']['url']
        cover = cover.replace('t_thumb','t_cover_big')
    else:
        cover = 'No photo'
    if 'screenshots' in info:
        screenshot = info['screenshots'][0]['url']
        screenshot = screenshot.replace('t_thumb','t_screenshot_big')
    else:
        screenshot = 'No photo'
    if request.method == 'POST':
        comment = str(request.form['comment'])
        g.db = connect_db()
        g.db.execute('INSERT INTO comments VALUES("'+comment+'","'+session['username']+'","'+gameId+'")')
        g.db.commit()
        g.db.close()

    return render_template('search_result.html',title = title,cover=cover,summary = summary,rating = rating,comment = comment,gameId = gameId, screenshot = screenshot)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = str(request.form['username'])
        password = str(request.form['password'])
        g.db = connect_db()
        allUsers = g.db.execute('Select * from users')
        validUser = [(row[0], row[1]) for row in allUsers.fetchall()]
        
        if (user,password) in validUser :
            g.db.close()
            session['logged_in'] = True
            session['username'] = user
            return redirect(url_for('index'))
        else:
            error = 'Invalid username or password'
    return render_template('login.html', error=error)

@app.route('/logout')
@login_req
def logout():
    session.clear()
    return render_template('index.html')

@app.route('/register',methods=['GET', 'POST'])
def register():
    error = None

    if request.method == 'POST':
        user = str(request.form['username'])
        password = str(request.form['password'])

        #Establish a connection the the database and save user info there, if user is not taken
        g.db = connect_db()
        allUsers = g.db.execute('Select * from users')
        validUser = [row[0]for row in allUsers.fetchall()]
        
        if user not in validUser:
            g.db.execute('INSERT INTO users VALUES("'+user+'","'+password+'")')
            g.db.commit()
            g.db.close()
            session['logged_in'] = True
            session['username'] = user
            return redirect(url_for('index'))
        else:
            error = 'User name is taken. Please try again.'
    return render_template('register.html',error = error)






if __name__ == '__main__':
    app.run()
