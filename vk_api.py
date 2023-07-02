import requests
import time
import constants
from datetime import datetime


class API:
    def __init__(self):
        self.base_url = 'https://api.vk.com/method/'
        self.params = {"v": constants.API_VERSION, "access_token": constants.TOKEN}

    def send_message(self, user_id, message):
        method = 'messages.send'
        params = {'user_id': user_id,
                  'random_id': 0,
                  'message': message}
        self._get(method, params)

    def _get(self, method, params=None):
        if params is not None:
            params.update(self.params)
        else:
            params = self.params
        url = self.base_url + method
        request_obj = requests.get(url=url, params=params)
        time.sleep(0.1)
        # print(request_obj.json())
        return request_obj.json()
    
    def get_member_info(self, member_id):
        # по vk id выдает список: [имя, фамилия, возраст, пол, город]
        method = 'users.get'
        params = {'user_id': member_id,
                  'fields': 'bdate, city, sex'}
        r = self._get(method, params)
        first_name = r['response'][0]['first_name']
        last_name = r['response'][0]['last_name']
        age = datetime.now().year - int(r['response'][0]['bdate'][-4:])
        gender = r['response'][0]['sex']
        if 'city' in r['response'][0]: #['city']['title']:
            city = r['response'][0]['city']['title']
        else:
            city = 'Город не указан'
        member_info = [first_name, last_name, age, gender, city]
        return member_info
    
    def get_photos(self, member_id):
        # по vk id выдает список с 3 фото размера Х с макс.кол-вом лайков
        method = 'photos.get'
        params = {'owner_id': member_id,
                    'album_id': 'profile',
                    'extended': 1
                    }
        r = self._get(method, params)
        photos = {}
        url = None
        for item in r['response']['items']:
            likes = item['likes']['count']
            for photo in item['sizes']:
                if photo['type'] == 'x':
                    url = photo['url']
            photos[url] = likes
        photos = dict(sorted(photos.items(), key=lambda item: item[1],
                             reverse=True))
        photo_urls = []
        count = 0
        for photo in photos:
            if count < 3:
                photo_urls.append(photo)
                count += 1
        return photo_urls
            
if __name__ == '__main__':
    api = API()
    # api.get_photos('1')
    print(api.get_member_info('788770602'))
    
    