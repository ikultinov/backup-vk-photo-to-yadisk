import sys
import requests
import json
from tqdm import tqdm


class YaUploader:
    url = 'https://cloud-api.yandex.net/v1/disk/resources/'

    def __init__(self):
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {token_YD}'
        }

    def create_folder(self, path_to_file):
        """
        Создает директорию "/vk_photo_backup" для фото на Я.Диске.
        """
        params = {'path': path_to_file}
        requests.put(self.url, params=params, headers=self.headers)

    def upload_photo(self, dict_photo, path_to_file):
        """
        Загружает фото на Я.Диск и отображает прогресс загрузки.
        """
        for name, url in tqdm(dict_photo.items(), desc='Загрузка...'):
            params = {
                'path': path_to_file + name,
                'url': url
            }
            requests.post(self.url + 'upload/', params=params,
                          headers=self.headers)
        print("\033[31m{}".format('Успешно!!!'))


with open('token_vk_photo.txt', 'r') as f:
    token = f.read().strip()


class VKPhoto:
    url_vk = 'https://api.vk.com/method/'
    params = {
        'access_token': token,
        'v': '5.131'
    }

    def download_photos(self, id_user):
        """
        Получает url-ссылки на фото, именует фото и создает json файл.
        """
        download_photos_params = {
            'owner_id': id_user,
            'album_id': 'profile',
            'extended': 1
        }

        req = requests.get(self.url_vk + 'photos.get',
                           params={**self.params,
                                   **download_photos_params}).json()
        try:
            req = req['response']['items']
        except KeyError:
            print('Пользователь скрыл свои данные, укажите другой id.')
            sys.exit()
        path_to_file = f'/vk_id_{id_user}/'

        uploader.create_folder(path_to_file)

        list_json = []
        dict_photos = {}
        for info_photo in req:
            name_photo = str(info_photo['likes']['count'])
            for name_key in dict_photos.keys():
                if name_photo == name_key:
                    name_photo = f"{name_photo}_{info_photo['date']}"
            url_photo = info_photo['sizes'][-1]['url']
            temp_dict = dict_photos.fromkeys([name_photo], url_photo)
            dict_photos.update(temp_dict)

            size = info_photo['sizes'][-1]['type']
            dict_temp_json = dict(file_name=f'{name_photo}.jpg', size=size)
            list_json.append(dict_temp_json)

        with open('file_json.json', 'w', encoding='utf-8') as file:
            json.dump(list_json, file)

        uploader.upload_photo(dict_photos, path_to_file)


if __name__ == '__main__':
    user_vk = VKPhoto()
    print(f'Для сохранения фото в Яндекс.Диск из профиля VK,\nВам потребуется'
          f' указать токен Я.Диска и id пользователя vk.\n'
          + "\033[3m{}".format(f'\nПримечание: Посмотреть ID можно в адресной'
                               f' строке браузера.\nЕсли профилю присвоен'
                               f' буквенно-цифровой адрес, то ID можно\n'
                               f'определить так: откройте любую фотографию'
                               f' пользователя,\nпервые цифры после слова'
                               f' photo (XXXXXX в ссылке\n'
                               f'https://vk.com/photoXXXXXX_YYYYYYY)'
                               f'— это интересующий вас ID.\n'))
    token_YD = input("\033[31m{}".format('Введите токен Яндекс.Диска:'))
    uploader = YaUploader()
    user_vk.download_photos(input("\033[31m{}\033[0m".format('Введите id '
                                                             'пользователя '
                                                             'vk:')))
