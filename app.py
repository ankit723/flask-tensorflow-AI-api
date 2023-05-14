from flask import Flask, jsonify, render_template, redirect, url_for, request
from main import res_main as rmain
import sign


app = Flask(__name__)



@app.route("/")
def home():
    return render_template('index.html')

@app.route("/signup")
def signup():
    return render_template("sign_up.html")
    
@app.route("/signlog/<string:res>")
def signlog(res):
    return render_template("sign_up.html", result = res)

@app.route("/checker")
def checker():
    return render_template("checker.html")

@app.route("/apiroutechecker", methods=["POST", "GET"])
def apiroutechecker():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
    authtoken=f"{email}_{password}"
    log=sign_in(authtoken)
    if log=="True":
        api=sign.routecheck(email)
        apiroute=f"Your API ID is {api}. To use Iris API Route add API ID, after respond in the url.For Eg: https://website.com/respond/api_id/query"
        return render_template("checker.html", api=apiroute)
    return render_template("checker.html", api="Your Email Id or Password Are Incorrect")

@app.route("/respond/<string:authtoken>/<string:text>")
def respond(authtoken, text):
    username, password= authtoken.split("_")
    auth=sign.signin_username((username, password))
    if auth =="True":
        json_api=rmain(text, username)
        rec = jsonify(json_api)
        return rec
    return(f"BAD REQUEST Please Check Your Auth Token")    


@app.route("/sign_up", methods=['POST', "GET"])
def sign_up(): 
    if request.method=='POST':
        username=request.form['username']
        name=request.form['name']
        password=request.form['password']
        email=request.form['email']
    created =sign.signup((username, name, password, email))
    if created == "username_exists":
        failed='oops Username Already Exists'
        return render_template("sign_up.html", result = failed)
    return render_template("sign_up.html", result = created)
    
    
@app.route("/sign_up/<string:username>/<string:name>/<string:password>/<string:email>")
def sign_up_api(username, name, email, password): 
    created =sign.signup((username, name, password, email))
    if created == "username_exists":
        failed='oops Username Already Exists'
        return render_template("sign_up.html", result = failed)
    return render_template("sign_up.html", result = created)
    

@app.route("/tryout_main")
def tryout_main():
    return render_template('tryout.html')

@app.route("/tryout", methods=['POST', 'GET'])
def tryout():
    if request.method=='POST':
        text=request.form['query']
    json=rmain(text, 'admin')
    result=json['Result']
    return(render_template('tryout.html', result=result))



def sign_in(authtoken):
    email, password= authtoken.split("_")#admin_adminrootmaster
    created =sign.signin((email,password))
    return created



def main():
    if __name__== "__main__":
        app.run(debug=True)

main()