from pathlib import Path

import requests
from bs4 import BeautifulSoup

from image import embed_watermark

import cv2



def send_post(username, password, text, file_path, url):
    s = requests.session()

    r = s.get(url + '/auth/login')
    soup = BeautifulSoup(r.text, 'html.parser')

    csrf_token = soup.find(id="csrf_token")['value']

    params = {
        'email': username,
        'password': password,
        'csrf_token': csrf_token
    }
    r = s.post(url + '/auth/login', data=params)
    if not r.status_code == 200:
        print('Login failed.')
        return

    image = Path(file_path)
    from_data = {'text': text}
    file = {'image': (image.name, open(image, 'rb'))}

    r = s.post(url + '/api/posts', data=from_data, files=file)
    # if not r.status_code == 201:
    #     print('Upload post failed.')
    #     return



def send_post(username, password, text, file_path, url):
    s = requests.session()

    r = s.get(url + '/auth/login')
    soup = BeautifulSoup(r.text, 'html.parser')

    csrf_token = soup.find(id="csrf_token")['value']

    params = {
        'email': username,
        'password': password,
        'csrf_token': csrf_token
    }
    r = s.post(url + '/auth/login', data=params)
    if not r.status_code == 200:
        print('Login failed.')
        return

    image = Path(file_path)
    from_data = {'text': text}
    file = {'image': (image.name, open(image, 'rb'))}

    r = s.post(url + '/api/posts', data=from_data, files=file)
    # if not r.status_code == 201:
    #     print('Upload post failed.')
    return

watermark_path = r''
# 将水印图片变为二进制
def image_to_binary(watermark_path):
    watermark_path = r''
    with open(watermark_path, 'rb') as f:
        img = cv2.imread(watermark_path)
        img_byte_arr = cv2.imencode('.jpg', img)[1].tobytes()
    return img_byte_arr

if __name__ == '__main__':
    username = ''
    password = ''

    text = ''
    image_file = r''
    url = 'http://127.0.0.1:5000'

    new_image = Path(image_file).with_name('embed.jpg')

    embed_watermark(image_file, image_to_binary(watermark_path), str(new_image))

    send_post(username, password, text, str(new_image), url)
