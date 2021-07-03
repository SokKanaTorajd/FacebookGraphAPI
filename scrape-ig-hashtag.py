from facebook.fb import FacebookAPI
from pymongo import MongoClient
from time import sleep


token_bumn_kota_malang = 'EAANmWNRMCPQBALwWMgWaTNd4xzoZCZAzKWTZCm1evRE2NOyIjw8CkdMZBSn1PMAxQMqfpHcETFIZAjV7aRsH0OfawqxtvoAq0sZCuiH8ZBUgDd25WWK8hboVfUviHaVNGtrKlZAGap1oTVXgGIqbmaSs2cxIuFcNcFGw7mhjcpoeZBAUnKgZCV2aST3N7xaBxoLt2IhpRFKOHPXEe2T2362IIY4ZAlfZBYpW0Jli0Yk3UWKZCib8SAZBYZCAZCAz'
fb_id = '195075655824180' # Nur Hadi
page_id_bumn_kota_malang = '101163835217927'
ig_id = '17841445014200240'

api = FacebookAPI(token_bumn_kota_malang)
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
top_media_col = 'ig-posts-top-media'
recent_media_col = 'ig-posts-recent-media'

# hashtag = '#bumnuntukindonesia'
# hashtag_id = '17863450460140059'

hashtag = 'bumnhadiruntuknegeri'

hashtag_id = api.getHashtagId(ig_id, hashtag)
# hashtag_id = '17863450460140059'
print(hashtag_id)
recents = api.getHashtagRecentMedia(ig_id, hashtag_id['data'][0]['id'])
print(recents)
try:
    i = 0
    for media in recents:
        # print(len(media))
        inputData(db_name, recent_media_col, media)
        print(i+1)
        i+=1
except TypeError:
    print(media)
    print('check your json ouput')

sleep(30)

top_medias = api.getHashtagTopMedia(ig_id, hashtag_id['data'][0]['id'])


try:
    i = 0
    for media in top_medias:
        inputData(db_name, top_media_col, media)
        print(i+1)
        i+=1
except TypeError:
    print(media)
    print('check your json output')

