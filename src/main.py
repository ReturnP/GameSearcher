from flask import Flask,render_template,request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/search',methods=['POST'])
def search():
    gameTitle = request.form['searchPath']
    return render_template('search_result.html',gameTitle = gameTitle)
if __name__ == '__main__':
    app.run()
