from flask import Flask,render_template,request,url_for, request,jsonify,redirect,session,flash
import requests
import json
from functools import wraps

app = Flask(__name__)


app.secret_key = "returnp" #TODO put in config file



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
    
    return render_template('index.html')

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
            

    return render_template('search_result.html',title = title,cover=cover,summary = summary,rating = rating)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash("Að vera innskráður fyllir þig með ákvörðun")
            return redirect(url_for('index'))#TODO: change this to redirect?
    return render_template('login.html', error=error)

@app.route('/logout')
@login_req
def logout():
    session.pop('logged_in',None)
    flash("Logged out!")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
