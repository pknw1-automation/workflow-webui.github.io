from flask import Flask, url_for, redirect
from dotenv import load_dotenv
from os import getenv
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)

app.secret_key = "mysecretkey"

oauth = OAuth(app)

github = oauth.register(
    name='github',
    client_id=getenv("CLIENT_ID"),
    client_secret=getenv("SECRET_ID"),
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)


@app.route("/")
def saludo():
    return "Hello"

@app.route("/login")
def login():
    redirect_url = url_for("authorize", _external=True)
    return github.authorize_redirect(redirect_url)


@app.route("/authorize")
def authorize():
    token = github.authorize_access_token()
    resp = github.get('user', token=token)
    profile = resp.json()
    # do something with the token and profile
    print(profile, token)
    return redirect('/')

    

if __name__ == '__main__':
    load_dotenv()
    app.run(debug=True, port=4000, host="0.0.0.0")

