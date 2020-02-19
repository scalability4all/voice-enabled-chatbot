from flask import Flask, render_template, redirect, session, url_for, request
from splitwise import Splitwise
import config as Config

app = Flask(__name__)
app.secret_key = "test_secret_key"


@app.route("/")
def home():
    if 'access_token' in session:
        return redirect(url_for("friends"))
    return render_template("home.html")


@app.route("/login")
def login():

    sObj = Splitwise(Config.consumer_key, Config.consumer_secret)
    url, secret = sObj.getAuthorizeURL()
    session['secret'] = secret
    return redirect(url)


@app.route("/authorize")
def authorize():

    if 'secret' not in session:
        return redirect(url_for("home"))

    oauth_token = request.args.get('oauth_token')
    oauth_verifier = request.args.get('oauth_verifier')

    sObj = Splitwise(Config.consumer_key, Config.consumer_secret)
    access_token = sObj.getAccessToken(oauth_token, session['secret'], oauth_verifier)
    session['access_token'] = access_token

    return redirect(url_for("friends"))


@app.route("/friends")
def friends():
    if 'access_token' not in session:
        return redirect(url_for("home"))

    sObj = Splitwise(Config.consumer_key, Config.consumer_secret)
    sObj.setAccessToken(session['access_token'])

    friends = sObj.getFriends()
    return render_template("friends.html", friends=friends)


if __name__ == "__main__":
    app.run(threaded=True, debug=True)
