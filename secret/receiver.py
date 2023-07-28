from pathlib import Path
import cv2
import numpy as np
import requests

from image import extract_watermark


def download_file(url):
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    # f.flush()
    return local_filename


def get_post(url):
    s = requests.session()

    r = s.get(url + '/api/posts')

    posts = r.json()['results']

    for post in posts:
        image_file = download_file(url + '/images/' + post['image'])
        decoded_watermark=extract_watermark(image_file)
        binary_to_image(decoded_watermark)


# 将二进制数据变为图片
def binary_to_image(binary_data):
    # 将二进制数据转换为 numpy 数组
    nparr = np.frombuffer(binary_data.encode(), 'u1')
    print(nparr)
    #cv2.imwrite('C:\\Users\\86186\\Desktop\\6.jpg', nparr)
    # 将 numpy 数组解码为图像
    watermark_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # cv2.imshow('Watermark Image', watermark_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # 将图像保存为文件
    try:
        cv2.imwrite('', watermark_img)
    except cv2.error as e:
        print(e)



if __name__ == '__main__':
    url = 'http://127.0.0.1:5000'

    get_post(url)