from flask import Flask, jsonify
from main import res_main as rmain

app = Flask(__name__)

@app.route("/respond/<string:text>")
def respond(text):
    json_api=rmain(text)
    rec = jsonify(json_api)
    return rec    

def main():
    if __name__== "__main__":
        app.run(debug=True)

main()