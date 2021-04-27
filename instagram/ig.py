import requests
from . import config


class InstagramAPI():
    def __init__(self):
        self.app_id = config.APP_ID
        self.redirect_uri = 'https://facebook-kecilin.herokuapp.com/'

    
    def authorization(self):
        """Autorisasi ini hanya berlaku satu jam"""

        params = (
            ('client_id', self.app_id),
            ('redirect_uri', self.redirect_uri),
            ('scope', 'user_profile,user_media'),
            ('response_type', 'code'),)
        response = requests.get('https://api.instagram.com/oauth/authorize%20', params=params)
        # response = requests.get('https://api.instagram.com/oauth/authorize?client_id=self.app_id&redirect_uri=self.redirect_uri&scope=user_profile,user_media&response_type=code')
        
        return response

    def access_token(self):


    