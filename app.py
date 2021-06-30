# from flask import Flask, request, render_template, \
#     url_for, redirect, jsonify
# from flask_cors import CORS
from pymongo import collection
from facebook.fb import FacebookAPI
from database.model import MongoDBModel
from instaloader import Instaloader, Post
from time import sleep
import os, requests
import config

# INITIATE
db = os.environ.get('DB_NAME')
# db = 'kecilin-intern'
# top_media_collection = os.environ.get('COLLECTION_TOP_MEDIA')
# top_comments_collection = os.environ.get('COLLECTION_TOP_COMMENTS')
# top_media_collection = 'ig-posts-top-media'

recent_media_collection = os.environ.get('COLLECTION_RECENT_MEDIA')
recent_comments_collection = os.environ.get('COLLECTION_RECENT_COMMENTS')
# recent_media_collection = 'ig-posts-recent-media'


mongodb = MongoDBModel(db)
fb_api = FacebookAPI(config.USER_TOKEN)

# SCRAPING MEDIA BASED ON HASHTAG
hashtag = 'sobatbumn'
hashtag_id = fb_api.getHashtagId(config.LUCKY_ID, hashtag)
print(hashtag_id)
# top_media = fb_api.getHashtagTopMedia(config.LUCKY_ID, hashtag_id['data'][0]['id'])
recent_media = fb_api.getHashtagRecentMedia(config.LUCKY_ID, hashtag_id['data'][0]['id'])

# SAVE SCRAPED DATA INTO DATABASE
# for media in top_media:
#     mongodb.insert(media, top_media_collection)

for media in recent_media:
    mongodb.insert(media, recent_media_collection)


# SCRAPING FOR COMMENTS
loader = Instaloader()
loader.login(os.environ.get('LUCKY_USERNAME'), os.environ.get('LUCKY_PASS'))
# top_media_links = mongodb.getIgPermalink(top_media_collection)

# for data in top_media_links:
#     permalink = data['permalink']
#     shortcode = permalink.split('/')
#     post = Post.from_shortcode(loader.context, shortcode[4])
#     sleep(2)
#     comments = post.get_comments()
#     for field in comments:
#         data = {
#             'ig_post_permalink': permalink,
#             'comment_id': field.id,
#             'text': field.text,
#             'created_at_utc': field.created_at_utc,
#             'username': field.owner.username,
#             'likes_count': field.likes_count
#         }
#         mongodb.insert(data, top_comments_collection)
#     sleep(3)

recent_media_links = mongodb.getIgPermalink(recent_media_collection)

for data in recent_media_links:
    permalink = data['permalink']
    shortcode = permalink.split('/')
    post = Post.from_shortcode(loader.context, shortcode[4])
    sleep(2)
    comments = post.get_comments()
    for field in comments:
        replies = []
        for reply in field.anwers:
            reply = {
                'id': reply.id,
                'text': reply.text,
                'created_at_utc': reply.created_at_utc,
                'username': reply.owner.username,
                'likes_count': reply.likes_count
            }
            replies.append(reply)
        
        data = {
            'ig_post_permalink': permalink,
            'comment_id': field.id,
            'text': field.text,
            'created_at_utc': field.created_at_utc,
            'username': field.owner.username,
            'likes_count': field.likes_count,
            'answers': replies,
            'shortcode': post.shortcode
        }
        mongodb.insert(data, recent_comments_collection)
    sleep(3)



# app = Flask(__name__)
# CORS(app)

# ig_auth_url = "https://api.instagram.com/oauth/authorize"
# redirect_uri = 'https://facebook-kecilin.herokuapp.com/auth/'

# @app.route('/', )
# def index():
#     return render_template('index.html')

# @app.route('/auth/', methods=['POST'])
# def auth():
#     if request.method == 'POST':
#         params = (
#                 ('client_id', config.APP_ID),
#                 ('redirect_uri', redirect_uri),
#                 ('scope', 'user_profile,user_media'),
#                 ('response_type', 'code')),
#         response = requests.get('https://api.instagram.com/oauth/authorize%20', params=params)
#         # response = requests.get('https://api.instagram.com/oauth/authorize?client_id=config.APP_ID&redirect_uri=redirect_uri&scope=user_profile,user_media&response_type=code')
        
#         return redirect(response)

# # @app.route('/callback', methods=['GET'])
# # def callback():
# #     if request.method == 'GET':

# if __name__=="__main__":
#     app.run()