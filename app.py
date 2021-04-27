from flask import Flask, request, render_template, \
    url_for, redirect, jsonify
from flask_cors import CORS
import requests
import config

app = Flask(__name__)
CORS(app)

ig_auth_url = "https://api.instagram.com/oauth/authorize"

@app.route('/', )
def index():
    return render_template('index.html')

@app.route('/auth', methods=['POST'])
def auth():
    if request.method == 'POST':
        params = (
                ('client_id', config.APP_ID),
                ('redirect_uri', 'https://facebook-kecilin.herokuapp.com/auth/'),
                ('scope', 'user_profile,user_media'),
                ('response_type', 'code'),)
            response = requests.get('https://api.instagram.com/oauth/authorize%20', params=params)
            # response = requests.get('https://api.instagram.com/oauth/authorize?client_id=self.app_id&redirect_uri=self.redirect_uri&scope=user_profile,user_media&response_type=code')
            
            return redirect(response)

    
# @app.route('/callback', methods=['GET'])
# def callback():
#     if request.method == 'GET':

        




if __name__=="__main__":
    app.run()