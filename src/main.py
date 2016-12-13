from flask import Flask,render_template,request,url_for, request
import requests
import json
app = Flask(__name__)
app.config.update(TEMPLATES_AUTO_RELOAD=True)
    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search',methods=['POST'])
def search():
    with open('config.json') as jData:
        apiKey = json.load(jData)['ApiKey']
    gameTitle = request.form['searchPath']
    response = requests.get("https://igdbcom-internet-game-database-v1.p.mashape.com/games/?fields=name&limit=3&offset=0&order=rating_count%3Adesc&search={}".format(gameTitle),headers={"X-Mashape-Key": apiKey,"Accept": "application/json"})
    title = response.json()[0]["name"]               
    return render_template('search_result.html',title = title)


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
