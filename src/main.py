from flask import Flask,render_template,request,url_for, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search',methods=['POST'])
def search():
    gameTitle = request.form['searchPath']
    return render_template('search_result.html',gameTitle = gameTitle)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return index()
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run()
