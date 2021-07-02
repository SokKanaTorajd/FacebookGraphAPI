from facebook.fb import FacebookAPI
from pymongo import MongoClient
from time import sleep
import config


"""""
Tes ini hanya ditujukun untuk mengambil semua
    postingan dan komentar di akun user sendiri menggunakan Official API Resmi Facebook.
Dengan catatan IG ID dan Access Token sudah tersedia.
"""""

api = FacebookAPI(config.TAMA_TOKEN)
id = config.TAMA_IG_ID
client = MongoClient()

def inputData(db_name, collection, data):
    db = client[db_name]
    return db[collection].insert_one(data)

def getOneField(db_name, collection, field):
    db = client[db_name]
    query = {field:1, '_id':0}
    data = db[collection].find({}, query)
    return data

def checkExistingDocs(db_name, collection, field, value):
    db = client[db_name]
    result = db[collection].find_one({field: value})
    if result is None:
        return False
    else:
        return True

db_name = 'kecilin-intern'
comment_collection = 'tama-post-comment'
post_collection = 'tama-ig_media'
field_permalink = 'permalink'
field_mediaID = 'id'
field_comment_mediaID = 'media_id'

tama_medias = api.getIgMediaObjects(id)
for media in tama_medias:
    inputData(db_name, post_collection, media)
    print('media inserted')

print('sleep for 30 seconds')
sleep(30)

link_medias = getOneField(db_name, post_collection, field_mediaID)
for link in link_medias:
    id = link['id']
    docs = checkExistingDocs(db_name, comment_collection, field_comment_mediaID, id)
    if docs is False:
        post_comments = api.getIgComments(id)
        data = {
            'media_id' : id,
            'all_comments': post_comments
        }
        inputData(db_name, comment_collection, data)
        print('comment inserted')
        sleep(10)
    else:
        print('documents already existed.')


print('scrape completed!')

