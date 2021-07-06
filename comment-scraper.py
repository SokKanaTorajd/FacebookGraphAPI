from database.model import MongoDBModel
# import requests, json
from time import sleep
from instaloader import Instaloader, Post



# def getHashtagId(ig_id, access_token, hashtag_name):
#     """
#     returns object: 
#     {
#         "data": [{"id": "hashtag_id"}]
#     }
#     """
#     params = (
#         ('user_id', ig_id),
#         ('q', hashtag_name),
#         ('access_token', access_token),)
#     response = requests.get('https://graph.facebook.com/v10.0/ig_hashtag_search', params=params)

#     return response.json()


# def getHashtagTopMedia(ig_id, access_token, hashtag_id):
#     """
#     return a list of instagram posts contain of id, caption, comments_count, 
#         like_count, media_type, permalink, and timestamp.
#     """
#     params = (
#         ('user_id', ig_id),
#         ('fields', 'id,caption,comments_count,like_count,media_type,permalink,timestamp'),
#         ('access_token', access_token),
#         ('limit', 50),
#     )
#     url = 'https://graph.facebook.com/v10.0/{}/top_media'.format(hashtag_id)
#     response = requests.get(url, params=params)
#     response = response.json()
#     top_medias = [media for media in response['data']]

#     while 'next' in response['paging'].keys():
#         try:
#             if len(response['data']) > 0:
#                 param_after = (('after', response['paging']['cursors']['after']),)
#                 params = params + param_after
#                 response = requests.get(url, params=params)
#                 response = response.json()
#                 for media in response['data']:
#                     top_medias.append(media)
#                 sleep(5)
#             if len(response['data']) == 0:
#                 break

#         except KeyError:
#             break

#     return top_medias


# def getHashtagRecentMedia(ig_id, access_token, hashtag_id):  # INI DAPETNYA DIKIT AMAT SIH
#     """
#     returns a list of of instagram posts based on recent timeline uploaded by users.
#      each data in the list contains id, caption, like_count, comments_count, media_type, permalink, timestamp.
#     """
#     params = (
#         ('user_id', ig_id),
#         ('fields', 'id,caption,comments_count,like_count,media_type,permalink,timestamp'),
#         ('access_token', access_token),
#         ('limit', 50),
#     )
#     url = 'https://graph.facebook.com/v10.0/{}/recent_media'.format(hashtag_id)
#     response = requests.get(url, params=params)
#     response = response.json()
#     recent_medias = [media for media in response['data']]
#     i = 1
#     while 'next' in response['paging'].keys():
#         try:
#             if len(response['data']) > 0:
#                 param_after = (('after', response['paging']['cursors']['after']),)
#                 params = params + param_after
#                 response = requests.get(url, params=params)
#                 response = response.json()
#                 for media in response['data']:
#                     recent_medias.append(media)
#                     print(media)
#                 print('looping ke', i)
#                 i+=1
#                 # sleep(5)

#             if len(response['data']) == 0:
#                 break

#         except KeyError:
#             break
    
#     return recent_medias


# def getIgMediaObjects(ig_id, access_token):
#     """
#     return a list of all user's posts in instagram contain id, caption, comments_count,
#         like_count, media_type, permalink, and timestamp.
    
#     """
#     params = (
#         ('fields', 'id,caption,comments_count,like_count,media_type,permalink,timestamp'),
#         ('access_token', access_token),
#         ('limit', 50),
#     )
#     url = 'https://graph.facebook.com/v10.0/{}/media'.format(ig_id)
#     response = requests.get(url, params=params)
#     response = response.json()
#     all_medias = [media for media in response['data']]

#     while 'next' in response['paging'].keys():
#         try:
#             if len(response['data']) > 0:
#                 param_after = (('after', response['paging']['cursors']['after']),)
#                 params = params + param_after
#                 response = requests.get(url, params=params)
#                 response = response.json()
#                 for data in response['data']:
#                     all_medias.append(data)
#                 sleep(5)

#             if len(response['data']) == 0:
#                 break
                
#         except KeyError:
#             break
        
#     return all_medias


# def getIgPostComments(media_id, access_token):
#     """
#     return a list of comments from user's instagram account.
#     Each data in comments contain of id(comment_id),text,timestamp,username,like_count
#     """
#     params = (
#         ('fields', 'id,text,timestamp,username,like_count'),
#         ('access_token', access_token),
#         ('limit', 50),
#     )
#     url = 'https://graph.facebook.com/{}/comments'.format(media_id)
#     response = requests.get(url, params=params)
#     response = response.json()
#     comments = [comment for comment in response['data']]

#     try:

#         while 'next' in response['paging'].keys():
#             try:

#                 if len(response['data']) > 0:
#                     param_after = (('after', response['paging']['cursors']['after']),)
#                     params = params + param_after
#                     response = requests.get(url, params=params)
#                     response = response.json()
#                     for comment in response['data']:
#                         comments.append(comment)
#                     sleep(5)

#                 if len(response['data']) == 0:
#                     break

#             except KeyError:
#                 break

#     except KeyError:
#         return comments
    
#     return comments

# ig_id = '17841447551005404'
# tama_id = '17841403354856241'
# access_token = 'EAANmWNRMCPQBAAeM9DymW59NHNTQnuyQ5ZCXILvwMytSA3kFVVP96ZAZBht6Bgc0CeCu3Qkg17ZCMZC7spqQi0dQmI1rhjFCQqYhcqN8JmrAXnZBWCIk4WCZAJ1rkc0IVJtJclzqAz7ZCRekq6TZAZAUFSwZCTVek370k93NdtpaEEZAHY0WbBSIGHxlS8LoiEeMv6XcUKeT5G9YFQZDZD'

mongo = MongoDBModel('kecilin-intern')
collection = 'bumnhadiruntuknegeri_topMedia'
comment_coll = 'bumnhadiruntuknegeri_Comments'

loader = Instaloader()
loader.login('luckylake7', 'Root_12345')

all_links = mongo.getIgPermalink(collection)

for url in all_links:
    link = url['permalink']
    existed = mongo.checkExistingDocs(comment_coll, 'post_permalink', link)

    if existed == True:
        print('The comments with url {} is already scraped.'.format(link))

    if existed == False:
        code = link.split('/')
        post = Post.from_shortcode(loader.context, code[4])
        sleep(5)
        comments = post.get_comments()
        scraped_comments = []
        for field in comments:
            if len(scraped_comments) <= 100:
                data = {
                    'comment_id' : field.id,
                    'username': field.owner.username,
                    'text': field.text,
                    'timestamp' : field.created_at_utc,
                    'likes_count': field.likes_count,
                }
                scraped_comments.append(data)

        post_comments = {
            'post_permalink': link,
            'comments' : scraped_comments,
            'shortcode': post.shortcode
        }
        mongo.insert(post_comments, comment_coll)
        print('comments from post {} has been scraped.'.format(link))
        print('break for 30 seconds...')
        sleep(30)

    
