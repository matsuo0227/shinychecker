import os
from pathlib import Path
import requests
from bs4 import BeautifulSoup as bs
import re
import sqlite3

def main():
    url = 'https://imas-shinycolors.boom-app.wiki/entry'

    dir_icon = 'update/icon/'
    p = Path(dir_icon)
    dirs = list(p.glob(u'**/'))
    # カレントディレクトリも入るので削除
    dirs.pop(0)

    dir_card = '../app/assets/images/card/'
    dir_update = 'update/card/'

    for d in dirs:
        # print(d)
        p = Path(d)
        pics = list(p.glob(u'*.jpg'))
        for pic in pics:
            dir_name, file_name = os.path.split(pic)
            id, ext = os.path.splitext(file_name)
            card_url = os.path.join(url, 'card-{}'.format(int(id)))
            path_rare = os.path.join(dir_card, os.path.basename(dir_name))
            path_rare_update = os.path.join(dir_update, os.path.basename(dir_name))
            os.makedirs(path_rare, exist_ok=True)
            os.makedirs(path_rare_update, exist_ok=True)
            image_path = os.path.join(path_rare, 'card-{}.jpg'.format(id))
            save_path = os.path.join(path_rare_update, 'card-{}.jpg'.format(id))
            if not os.path.exists(image_path):
                print('save: {}'.format(save_path))
                image_url = return_image_url(card_url)
                image = download_image(image_url)
                save_image(save_path, image)
            # else:
            #     print('pass: {}'.format(save_path))

def return_image_url(card_url):
    soup = bs(requests.get(card_url).content, 'html.parser')
    info_header = soup.find(text=re.compile('.+基本情報$'))
    imagelist = info_header.find_next()
    img = imagelist.find('img')

    image_url = img.get('src')

    return image_url

# 画像をダウンロードする
def download_image(url, timeout = 10):
    response = requests.get(url, allow_redirects=False, timeout=60)
    if response.status_code != 200:
        e = Exception("HTTP status: " + response.status_code)
        raise e

    content_type = response.headers["content-type"]
    if 'image' not in content_type:
        e = Exception("Content-Type: " + content_type)
        raise e

    return response.content

# 画像を保存する
def save_image(save_path, image):
    with open(save_path, "wb") as f:
        f.write(image)

if __name__ == '__main__':
    main()