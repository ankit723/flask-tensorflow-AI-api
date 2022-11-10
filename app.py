from flask import Flask, jsonify, render_template, url_for, redirect, request
from main import res_main as rmain

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/respond/<string:text>")
def respond(text):
    json_api=rmain(text)
    rec = jsonify(json_api)
    return rec    

@app.route("/submit",methods=['POST', 'GET'])
def submit():
    requested = ''
    if request.method =='post':
        requested = request.form['query']
        
    return redirect(url_for('respond', text=requested))

def main():
    if __name__== "__main__":
        app.run(debug=True)

main()