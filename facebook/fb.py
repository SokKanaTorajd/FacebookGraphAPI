from time import sleep
import requests, json

class FacebookAPI(object):
    """
    Bisa digunakan dengan persyaratan dibawah ini:
    1. Akun Instagram User merupakan AKUN BISNIS. Akun Kreator dan akun non-bisnis tidak bisa digunakan.
    2. Sudah terhubung ke Aplikasi pihak ketiga(dalam hal ini adalah integratedmedia) melalui facebook.
    3. Akun Instagram User terhubung dengan Page atau Halaman yang dikelolanya di Facebook.

    !!! PERLU DIINGAT !!!
    1. Akses Token yang digunakan merupakan token yang cepat expired.
    2. Postingan ke IG terbatas hanya 25 post/hari.
    """

    def __init__(self, user_access_token):
        self.access_token = user_access_token

    def get_fbID(self):
        """
        'me' dapat diubah menjadi fb_id
        https://graph.facebook.com/v10.0/{fb_id}

        --Ouput berupa dictionary
        {
            "name": <nama_fb>,
            "id": <id_akun_fb>
        }
        """
        params = (
            ('accounts', ''),
            ('access_token', self.access_token),)
        response = requests.get('https://graph.facebook.com/v10.0/me', params=params)
        resp = response.json()
        return resp

    def get_fbUserPages(self, fb_id:str):
        """
        Mengembalikan kumpulan Halaman Facebook yang dapat digunakan 
        oleh Pengguna Facebook saat ini untuk melakukan 
        tugas MANAGE, CREATE_CONTENT, MODERATE, atau ADVERTISE.

        --Output berupa dictionary
        {
            "data": [
                {
                    "page_access_token": <token>,
                    "category": <kategori>,
                    "category_list": [
                    {
                        "id": <id>,
                        "name": <Nama Page>
                    }],
                    "name": <Nama App>,
                    "id": <fb-page_id>, 
                    "tasks": [
                        "ANALYZE",
                        "ADVERTISE",
                        "MODERATE",
                        "CREATE_CONTENT",
                        "MANAGE"]
                }
            ]
        }
        """
        params = (('access_token', self.access_token),)
        url = 'https://graph.facebook.com/v10.0/{}/accounts'.format(fb_id)
        response = requests.get(url, params=params)
        resp = response.json()

        return resp

    def getIgUser(self, page_id:str):
        """
        Mengembalikan Pengguna IG (Akun Bisnis atau Creator Instagram) 
        yang terhubung ke Halaman Facebook.
        --Output 
        {
            "instagram_business_account": {
                "id": <ig-user-id>},
            "id": <fb-page-id>
            }
        """
        params = (
                ('fields', 'instagram_business_account'),
                ('access_token', self.access_token),)
        url = 'https://graph.facebook.com/v10.0/{}'.format(page_id)
        response = requests.get(url, params=params)
        resp = response.json()
        return resp

    def getIgUserInfo(self, ig_id:str):
        """
        Mengembalikan id, username, name, profile picture url, biography, 
        jumlah posting, jumlah follower, dan jumlah yang di-follow.
        --Output
        {
            "id": <ig-user-id>,
            "username": <ig-username>,
            "media_count": <jumlah postingan>,
            "follows_count": <jumlah yang di-follow>,
            "followers_count": <jumlah follower>
        }
        Read more at https://developers.facebook.com/docs/instagram-basic-display-api/guides/getting-profiles-and-media
        """
        params = (
            ('fields', 'id,username,name,profile_picture_url,biography,media_count,follows_count,followers_count'),
            ('access_token',self.access_token),)
        url = 'https://graph.facebook.com/v10.0/{}'.format(ig_id)
        response = requests.get(url, params=params)
        response = response.json()
        return response

    def getIgMediaObjects(self, ig_id:str):
        """
        Mengembalikan semua ID dari Objek IG Media
        --Output Example
        {
            "data": [
                {"id": <id-objek-1>},
                {"id": <id-objek-2>},
                {"id": <id-objek-3>},
                {"id": <id-objek-4>},
                {"id": <id-objek-5>},
                {"id": <id-objek-6>},
                ...
            ],
            "paging": {
                "cursors": {
                    "before": "<key-cursor-before>",
                    "after": "<key-cursor-after>"
                },
                ,
                "next": "https://graph.facebook.com/v10.0/<user-id>/media?access_token=self.access_token&pretty=0&limit=25&after=<key-cursor-after>"
            }
        }
        """
        params = (
            ('fields', 'id,caption,comments_count,like_count,media_type,permalink,timestamp'),
            ('access_token', self.access_token),
            ('limit', 50),)
        url = 'https://graph.facebook.com/v10.0/{}/media'.format(ig_id)
        response = requests.get(url, params=params)
        response = response.json()

        try:
            all_medias = [media for media in response['data']]
            while 'next' in response['paging'].keys():
                try:
                    if len(response['data']) > 0:
                        param_after = (('after', response['paging']['cursors']['after']),)
                        params = params + param_after
                        response = requests.get(url, params=params)
                        response = response.json()
                        for data in response['data']:
                            all_medias.append(data)
                        sleep(5)
                    if len(response['data']) == 0:
                        break
                        
                except KeyError:
                    break
                
            return all_medias

        except KeyError:
            return response

    def getIgComments(self, media_id):
        """
        return a list of comments from user's instagram account.
        Each data in comments contain of id(comment_id),text,timestamp,username,like_count
        """
        params = (
            ('fields', 'id,text,timestamp,username,like_count'),
            ('access_token', self.access_token),
            ('limit', 50),)
        url = 'https://graph.facebook.com/{}/comments'.format(media_id)
        response = requests.get(url, params=params)
        response = response.json()
        
        try:
            comments = [comment for comment in response['data']]
            while 'next' in response['paging'].keys():
                try:
                    if len(response['data']) > 0:
                        param_after = (('after', response['paging']['cursors']['after']),)
                        params = params + param_after
                        response = requests.get(url, params=params)
                        response = response.json()
                        for comment in response['data']:
                            comments.append(comment)
                        sleep(5)
                    if len(response['data']) == 0:
                        break

                except KeyError:
                    break
            
            return comments

        except KeyError:
            return response

    def getHashtagId(self, ig_id, hashtag_name):
        """
        returns object: 
        {
            "data": [{"id": "hashtag_id"}]
        }
        """
        params = (
            ('user_id', ig_id),
            ('q', hashtag_name),
            ('access_token', self.access_token),)
        response = requests.get('https://graph.facebook.com/v10.0/ig_hashtag_search', params=params)

        return response.json()
    
    def getHashtagTopMedia(self, ig_id, hashtag_id):
        """
        return a list of instagram posts contain of id, caption, comments_count, 
            like_count, media_type, permalink, and timestamp.
        """
        params = (
            ('user_id', ig_id),
            ('fields', 'id,caption,comments_count,like_count,media_type,permalink,timestamp'),
            ('access_token', self.access_token),
            ('limit', 50),
        )
        url = 'https://graph.facebook.com/v10.0/{}/top_media'.format(hashtag_id)
        response = requests.get(url, params=params)
        response = response.json()

        try:
            top_medias = [media for media in response['data']]
            while 'next' in response['paging'].keys():
                try:
                    if len(response['data']) > 0:
                        param_after = (('after', response['paging']['cursors']['after']),)
                        params = params + param_after
                        response = requests.get(url, params=params)
                        response = response.json()
                        for media in response['data']:
                            top_medias.append(media)
                        sleep(5)
                    if len(response['data']) == 0:
                        break

                except KeyError:
                    break

            return top_medias

        except KeyError:
            return response
    
    def getHashtagRecentMedia(self, ig_id, hashtag_id):
        """
        returns a list of of instagram posts based on recent timeline uploaded by users.
        each data in the list contains id, caption, like_count, comments_count, media_type, permalink, timestamp.
        """
        params = (
            ('user_id', ig_id),
            ('fields', 'id,caption,comments_count,like_count,media_type,permalink,timestamp'),
            ('access_token', self.access_token),
            ('limit', 50),
        )
        url = 'https://graph.facebook.com/v10.0/{}/recent_media'.format(hashtag_id)
        response = requests.get(url, params=params)
        response = response.json()

        try:
            recent_medias = [media for media in response['data']]

            while 'next' in response['paging'].keys():
                try:
                    if len(response['data']) > 0:
                        param_after = (('after', response['paging']['cursors']['after']),)
                        params = params + param_after
                        response = requests.get(url, params=params)
                        response = response.json()
                        for media in response['data']:
                            recent_medias.append(media)
                            print(media)
                        sleep(5)
                    if len(response['data']) == 0:
                        break

                except KeyError:
                    break
            
            return recent_medias

        except KeyError:
            return response
    
    def postIgPhoto(self, ig_id:str, image_path:str, caption:str):
        """
        mengembalikan ID kontainer POST /{ig-user-id}/media, kemudian 
        akan diposting menggunakan endpoint POST /{ig-user-id}/media_publish.
        --Output untuk POST /{ig-user-id}/media
        {
            "id": <container_id>
        }
        Read More at https://developers.facebook.com/docs/instagram-api/reference/ig-user/media#create-container

        --Output untuk POST /{ig-user-id}/media_publish (Jika endpoint media berhasil)
        {
            "id": <id-objek atau id-postingan>
        }
        --Output jika endpoint media gagal (example)
            {'error': 
                {
                    'message': '(#10) The user is not an Instagram Business', 
                    'type': 'OAuthException', 
                    'code': 10, 
                    'fbtrace_id': 'AZGz2JvbUwqgG0LUkuNnt3t'
                }
            }
        --Notes:
            Hanya dapat digunakan untuk menerbitkan ke akun Pengguna Instagram Business; Akun Pengguna Instagram Kreator tidak didukung.
            Akun dibatasi hingga 25 postingan yang diterbitkan API dalam periode 24 jam.
            JPEG adalah satu-satunya format gambar yang didukung. Format JPEG yang diperluas seperti MPO dan JPS tidak didukung.
            Cerita tidak didukung.
            Tanda belanja tidak didukung.
            Tanda konten bermerek tidak didukung.
            Filter tidak didukung.
            Postingan banyak gambar tidak didukung.
            Jika keterangan berisi tagar, itu harus berenkode URL HTML sebagai %23 dalam permintaan.
            Menerbitkan ke IGTV tidak didukung.

            *)Instagram akan melakukan cURL pada objek media menggunakan URL yang diteruskan,
            sehingga objek tersebut harus berada di server publik.
        -Read More at https://developers.facebook.com/docs/instagram-api/guides/content-publishing
        -- Photo Requirements  
            Maximum file size: 8MiB
            Aspect ratio: Must be within a 4:5 to 1.91:1 range
            Minimum width: 320 (will be scaled up to the minimum if necessary)
            Maximum width: 1440 (will be scaled down to the maximum if necessary)
            Height: Varies, depending on width and aspect ratio
            Formats: JPEG
        -Read More at https://developers.facebook.com/docs/instagram-api/reference/ig-user/media
        """
        # ======= POST MEDIA =======
        params = (
            ('image_url', image_path),
            ('caption', caption),
            ('access_token', self.access_token),)
        url = 'https://graph.facebook.com/v10.0/{}/media'.format(ig_id)
        resp = requests.post(url, params=params)
        resp = resp.json()
        sleep(3)
        # ======= POST MEDIA END ======
        
        try:
            # ======= POST CONTAINER ======
            container_id = resp['id']
            publish_params = (
                ('creation_id', container_id),
                ('access_token', self.access_token),)
            publish_url = 'https://graph.facebook.com/v10.0/{}/media_publish'.format(ig_id)
            response = requests.post(publish_url, params=publish_params)
            resp = response.json()
            return (container_id, resp)
            # ===== POST CONTAINER END======
            
        except KeyError:
            return resp

    def postIgVideo(self, ig_id:str, video_path:str, caption:str):
        """
        Alurnya Mirip dengan postIgPhoto, hanya saja ini digunakan untuk posting video.
        --Limitations
            Publishing to IGTV is not supported.
            Video Requirements

        --Videos must meet the following specifications:
            Container: MOV or MP4 (MPEG-4 Part 14), no edit lists, moov atom at the front of the file.
            Audio codec: AAC, 48khz sample rate maximum, 1 or 2 channels (mono or stereo).
            Video codec: HEVC or H264, progressive scan, closed GOP, 4:2:0 chroma subsampling.
            Frame rate: 23-60 FPS.
            Picture size:
                Maximum columns (horizontal pixels): 1920
                Minimum aspect ratio [cols / rows]: 4 / 5
                Maximum aspect ratio [cols / rows]: 16 / 9 
            Video bitrate: VBR, 5Mbps maximum
            Audio bitrate: 128kbps
            Duration: 60 seconds maximum, 3 seconds minimum
            File size: 100MB maximum
        -Read More at https://developers.facebook.com/docs/instagram-api/reference/ig-user/media#create-video-container
        https://developers.facebook.com/docs/instagram-api/guides/content-publishing#publish-videos 
        """
        # ======= POST MEDIA =======
        params = (
            ('media_type', 'VIDEO'),
            ('video_url', video_path),
            ('caption', caption),
            ('access_token', self.access_token),)
        url = 'https://graph.facebook.com/v10.0/{}/media'.format(ig_id)
        response = requests.post(url, params=params)
        response = response.json()
        sleep(3)
        # ======= POST MEDIA END ======
        
        # ======= POST CONTAINER ======
        try:
            container_id = response['id']
            publish_params = (
                ('creation_id', container_id),
                ('access_token', self.access_token),)
            publish_url = 'https://graph.facebook.com/v10.0/{}/media_publish'.format(ig_id)
            resp = requests.post(publish_url, params=publish_params)
            resp = resp.json()
            return (container_id, resp)

        except KeyError:
            return response
        # ===== POST CONTAINER END======
        
    def checkIgLimitUsage(self, ig_id):
        """
        Akun Intagram dibatasi hingga 25 postingan yang diterbitkan API dalam periode bergerak 24 jam.
        Fungsi ini hanya bisa digunakan jika akun instagram merupakan akun bisnis.
        --Output:
        {
            'data':[
                {'quota_usage': <jumlah_quota_yang_sudah_digunakan>}
            ]
        }
        """
        try:
            params = (('access_token', self.access_token),)
            url = 'https://graph.facebook.com/v10.0/{}/content_publishing_limit'.format(ig_id)
            response = requests.get(url, params=params)
            resp = response.json()

            if resp['data'][0]['quota_usage']==25:
                resp['data'][0]['quota_usage'] = 'Limit has been reached'
                return resp
            
            return resp
        
        except KeyError:
            return resp

    def get_fbProfile(self, fb_id):
        """
        --Output
        {
            "id": <fb_id>,
            "name": <fb_name>,
            "picture": {
                "data": {
                    "height": <int>,
                    "is_silhouette": <boolean>,
                    "url": <url>,
                    "width": <int>
                }}
        }
        """
        params = (
            ('fields', 'id,name,picture'),
            ('access_token', self.access_token),)
        url = 'https://graph.facebook.com/v10.0/{}'.format(fb_id)
        response = requests.get(url, params=params)
        response = response.json()
        return response

    def get_fbFriendsCount(self):
        """
        --Output
        {
            "data": [ <hanya mengambalikan teman yg juga menginstall aplikasi. 
            jika tidak, hanya return summary>
            ],
            "summary": {
                "total_count": 323
            }
        }
        """
        params = (('access_token', self.access_token),)
        url = 'https://graph.facebook.com/v10.0/me/friends'#.format(fb_id)
        response = requests.get(url, params=params)
        response = response.json()
        return response

    def get_fbGroups(self, fb_id:str):
        """
        !! Attention
        1. untuk mendapatkan member_count dan privacy, user perlu menjadi admin dalam grup tersebut.
        2. jika user bukan admin, hanya akan mengembalikan id dan group_name saja
        --Output
        {
            "data": [
                {
                "id": <grup1_id>,
                "name": <grup1_name>,
                "member_count": <member's count>,
                "privacy": <privacy type (OPEN/CLOSED/SECRET)>
                },
                {
                "id": <grup2_id>,
                "name": <grup2_name>
                },...
                ],
            "paging": {
                "cursors": {
                "before": <...>,
                "after": <...>
                }
            }
        }
        """
        params=(
            ('fields', 'id,name,member_count,privacy'),
            ('access_token', self.access_token)
        )
        url = 'https://graph.facebook.com/v10.0/{}/groups'.format(fb_id)
        response = requests.get(url, params=params)
        response = response.json()
        return response

    def get_fbPageAccessToken(self, page_id:str):
        """
        Untuk mendapatkan page access token membutuhkan user access token.
        User Access Token ini harus dibuat oleh orang yang dapat melakukan tindakan di Halaman(Page).

        !!!Notes:
        1. Masih menggunakan short-lived user access token, jadi Page Access Token hanya valid selama 1 jam.
       --Output
       {}
        "access_token":"{page-access-token}",
        "id":"{page-id}"
        }
        """
        params = (
            ('fields', 'access_token'),
            ('access_token', self.access_token),)
        url = 'https://graph.facebook.com/v10.0/{}'.format(page_id)
        response = requests.get(url, params=params)
        response = response.json()
        return response

    def post_fbPhoto(self, page_id:str, page_access_token:str, img_path):
        """
        Posting satu image ke facebook dengan catatan UNPUBLISHED (tidak akan muncul di Page).
        Hanya mengembalikan Image-Post-ID.
        --Output
        {'id': '<image-post-id>'}
        """
        img_src = open(img_path, 'rb')
        params = (
            ('published', 'false'),
            ('access_token', page_access_token),)
        url = 'https://graph.facebook.com/v10.0/{}/photos'.format(page_id)
        response = requests.post(url, params=params, files={'source': img_src})
        response = response.json()
        return response

    def post_fbMultiPhotos(self, page_id:str, page_access_token:str, message:str, img_paths:list):
        """
        Posting multi-foto/gambar di Halaman(Page) Facebook. 
        Foto atau Gambar pertama kali diarahkan ke post_fbPhoto untuk diposting namun tidak dipublish. Bertujuan untuk mengumpulkan post-id agar bisa memposting banyak foto.
        id-id yang dihasilkan kemudian dimasukkan ke media_fbid dalam parameter request dengan key attached_media.
        --Output
        {'id': '<post-id>', post_supports_client_mutation_id': True}
        !!! Notes
        1. Jumlah image yang diposting sejauh ini ada 4 gambar. masih belum diketahui jumlah maksimal upload.
        2. Sleep bertujuan memberikan jeda waktu (dalam detik) ketika melakukan request post ke facebook graph api.
            Sejauh ini, jeda waktu diberikan 30 detik/image-post.
        3. Posting yang dilakukan disini langsung terpublikasikan di Page Facebook.
        -- Read More at https://developers.facebook.com/docs/graph-api/reference/page/photos/#upload
        """
        id_list = []
        medias = []
        for img in img_paths:
            uploaded_id = self.post_fbPhoto(page_id, page_access_token, img)
            sleep(3)
            id_list.append(uploaded_id)
        for i in range(len(id_list)):
            attach = 'attached_media[{}]'.format(i)
            media_fbid = {'media_fbid':id_list[i]['id']}
            data = (attach, str(media_fbid))
            medias.append(data)
        params = (
            ('message', message),
            ('is_published', 'true'),
            ('access_token', page_access_token),)
        params+=tuple(medias)
        url = 'https://graph.facebook.com/v10.0/{}/feed'.format(page_id)
        response = requests.post(url, params=params)
        response = response.json()
        return response

