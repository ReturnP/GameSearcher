from flask import Flask,render_template,request,url_for, request,jsonify
import requests
import json
app = Flask(__name__)
app.config.update(TEMPLATES_AUTO_RELOAD=True)
    
with open('config.json') as jData:
    apiKey = json.load(jData)['ApiKey']

@app.route('/')
def index():
    

    return render_template('index.html')

@app.route('/search')
def search():

    gameTitle = request.args.get("title","NONE",type=str)
    response = requests.get("https://igdbcom-internet-game-database-v1.p.mashape.com/games/?fields=name&limit=5&offset=1&order=name&order=rating_count&order=popularity%3Adesc&search={}".format(gameTitle),headers={"X-Mashape-Key": apiKey,"Accept": "application/json"})
    title = response.json()
    return jsonify(result=title)


@app.route('/displayGame/<gameId>',methods=['GET','POST'])
def displayGame(gameId):
    response = requests.get("https://igdbcom-internet-game-database-v1.p.mashape.com/games/{}?fields=*".format(gameId), headers={
    "X-Mashape-Key": apiKey,
    "Accept": "application/json"
  })
    
    title = response.json()[0]['name']
    cover = response.json()[0]['cover']['url']
    summary = response.json()[0]['summary']#TODO: make empty if game has no summary
    rating = response.json()[0]['rating']
    rating = rating
    rating = str(("%.2f" % int(rating)))

    return render_template('search_result.html',title = title,cover=cover,summary = summary,rating = rating)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return index()#TODO: change this to redirect?
    return render_template('login.html', error=error)



if __name__ == '__main__':
    app.run()
