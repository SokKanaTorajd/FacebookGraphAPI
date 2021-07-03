from facebook.fb import FacebookAPI
from pymongo import MongoClient
from time import sleep
import config


"""""
Tes ini hanya ditujukun untuk mengambil semua
    postingan dan komentar di akun user sendiri menggunakan Official API Resmi Facebook.
Dengan catatan IG ID dan Access Token sudah tersedia.
"""""

token_bumn_kota_malang = 'EAANmWNRMCPQBAKclZAxyjNJ2R3gBa4WML0YQ3MBtjgNAGRkaotsRVG3CkzSAGS0fD98vQlvti8j7AL6bsQ5c6w4nZB2WX0bU6vAj5VZBf3ZBIZCsSTmclzBAQzQ99VAxI0xPwbJ2I8ZAZBEaOJ31LvUxcVh7GZABEV9Qq2Fqqh6TAZBJVMZBMgWwimuQdYinsIm5w7wZBz1DGCbocHZAlOMioPGk6u99hjTN6g5SbJFpZAK0gCCK2RMszfIpK'
fb_id = '195075655824180' # Nur Hadi
page_id_bumn_kota_malang = '101163835217927'
ig_id = '17841445014200240'



api = FacebookAPI(token_bumn_kota_malang)
# id = config.TAMA_IG_ID
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
comment_collection = 'post-bumn-kota-malang'
post_collection = 'comment-bumn-kota-malang'
field_permalink = 'permalink'
field_mediaID = 'id'
field_comment_mediaID = 'media_id'

# fb_id = api.get_fbID()
all_media = api.getIgMediaObjects(ig_id)
for media in all_media:
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

