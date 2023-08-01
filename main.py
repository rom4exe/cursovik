import json
import time
import tqdm
from time import sleep
from tqdm import tqdm
import requests


class YaUploaderVK:
    def __init__(self, vk_id: str, ya_token: str, vk_token: str, count = '5', album_id= 'profile', version='5.131'):
        self.id = vk_id
        self.ya_token = ya_token
        self.vk_token = vk_token
        self.version = version
        self.count = count
        self.album_id = album_id
        self.params_vk = {'access_token': self.vk_token, 'v': self.version}


    def upload(self):
        url_vk = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id, 'album_id': self.album_id, 'extended': 1, 'count': self.count}
        response_vk = requests.get(url_vk, params={**self.params_vk, **params})
        data_vk = response_vk.json()

        url_ya = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = {'Authorization': 'OAuth ' + self.ya_token}

        info_ya_d = 'https://cloud-api.yandex.net/v1/disk/resources'
        response_info = requests.get(info_ya_d, headers=headers, params= {'path':'/'})
        inf = response_info.json()
        res = list(filter(lambda x: x['name'] == 'uploaded_files', inf['_embedded']['items']))
        if not res:
            requests.put(info_ya_d, headers=headers, params= {'path':'/uploaded_files'})
        ss =[]
        for photo_i in tqdm(data_vk['response']['items']):
            photo_i['sizes'].sort(key=lambda x: x['height'])
            d = ''
            name = str(photo_i['likes']['count'])
            param = {'path': '/uploaded_files/' + name, 'url': photo_i['sizes'][-1]['url']}
            response_ya = requests.get(url_ya, headers=headers, params=param)
            data_ya = response_ya.json()
            if response_ya.status_code != 200:
                if 'уже существует' in data_ya['message']:
                    n = photo_i['date']
                    d = time.strftime(" -%Y-%m-%d", time.gmtime(n))
                    name = str(photo_i['likes']['count']) + str(d)
                    param = {'path': f'uploaded_files/' + name, 'url': photo_i['sizes'][-1]['url']}
                    requests.post(url_ya, headers=headers, params=param)
                    sleep(0.1)
                else: print(data_ya['message'])
            else:
                requests.post(url_ya, headers=headers, params=param)
                sleep(0.1)
            ss += [{'file_name': name, 'file_size': photo_i['sizes'][-1]['type']}]
        tqdm.write('Файлы загружены')
        tojson = json.dumps(ss)
        result_file = 'result_file.json'
        with open(result_file, 'w') as f_result:
            f_result.write(tojson)
        return tojson


acc_token = 'vk1.a.TquOUMe6rGs3BTHpeJ1X6AHrrddGb-r04uz05wi_lY18iyF646QPftMCdzl3WDn46' \
            'Goz_b0v5_7MyYNF0D1UUvx1Y6DfX6exXWAjH0Dh69GGUBsUv4Q60XCTNrfFiftDjc7KoSoWU' \
            '7ZGHdVVLPvWCoAacq-15M1QmBxgkLI29XdhY1ptXvC01s2VwH9wVN0U7dxYMLh8fOxvcrX0n1G0og'
user_id = '316661918'
ya_token = ""

uploader = YaUploaderVK(user_id, ya_token, acc_token, count_photo:=5, album_id:= 'profile')

result = uploader.upload()
print(result)