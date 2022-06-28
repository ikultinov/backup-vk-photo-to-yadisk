import requests
import time
from pprint import pprint


with open('token_y_disk.txt', 'r') as f:
    token_YD = f.read().strip()


class YaUploader:
    url = 'https://cloud-api.yandex.net/v1/disk/resources/'

    def __init__(self):
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {token_YD}'
        }

    def create_folder(self):
        """
        Создает директорию для фото на Я.Диске.
        Название задается пользователем.
        """
        params = {'path': path_to_file}
        requests.put(self.url, params=params, headers=self.headers)
        time.sleep(0.33)

    def upload_photo(self, file_path: str, name_photo):
        """
        Загружает фото на Я.Диск.
        """
        params = {
            'path': path_to_file + name_photo,
            'url': file_path
        }
        response = requests.post(self.url + 'upload/', params=params,
                                 headers=self.headers)
        # Здесь нужен бар загрузки, посмотреть в других библиотеках.
        time.sleep(0.33)
        response.raise_for_status()
        if response.status_code == 202:
            print('Photo upload')

    def contains_photo(self, name_photo):
        """
        Проверяет, содержится ли фото в текущем каталоге.
        """
        params = {
            'path': path_to_file,
            'limit': '1000'
        }
        req = requests.get(self.url, params=params,
                           headers=self.headers).json()
        print('name_photo: ', name_photo)
        for elem in req['_embedded']['items']:
            if name_photo == elem['name']:
                match = True
                return match


with open('token_vk_photo.txt', 'r') as f:
    token = f.read().strip()


class VKPhoto:
    url_vk = 'https://api.vk.com/method/'
    params = {
        'access_token': token,
        'v': '5.131'
    }

    def download_photos(self, id_user=None):
        download_photos_params = {
            'owner_id': id_user,
            'album_id': 'profile',
            'extended': 1
        }
        req = requests.get(self.url_vk + 'photos.get',
                           params={**self.params,
                                   **download_photos_params}).json()
        time.sleep(0.33)
        req = req['response']['items']
        # pprint(req)
        uploader.create_folder()
        for info_photo in req:
            match = False
            name_photo = str(info_photo['likes']['count'])
            match = uploader.contains_photo(name_photo)
            if match:
                name_photo = f"{name_photo}_{info_photo['date']}"
            url_photo = info_photo['sizes'][-1]['url']

            # pprint(name_photo)
            uploader.upload_photo(url_photo, name_photo)


def manages_functions():
    """
    Сделать функцию которая будет запускать весь код и предлагать пользователю
    выбор. Например: Для сохранения фото из VK введите пожалуйста id
    пользователя, по умолчанию будут сохранены Ваши фото.
    Укажите токен для Я.Диска.
    """

if __name__ == '__main__':
    path_to_file = f'/vk_photo_backup/'
    user_vk = VKPhoto()
    uploader = YaUploader()
    user_vk.download_photos()
