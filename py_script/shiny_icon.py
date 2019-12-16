import requests
from bs4 import BeautifulSoup as bs
import re
import sqlite3
import os

def main():
    url = "https://imas-shinycolors.boom-app.wiki/checker/idolcard/"
    # header = {'User-Agent' : "Mozilla/5.0"}
    soup = bs(requests.get(url).content, 'html.parser')

    group = soup.find_all('div', class_='checker-group2')
    # print(items[0])
    dir_images = '../app/assets/images/icon/'
    dir_update = 'update/icon'
    for g in group:
        items = g.find_all('img')
        cardtype = g.find('div', class_='checker-status-sm')
        cardtype = cardtype.text

        dir_name = os.path.join(dir_images, return_cardtype(cardtype))
        dir_name_update = os.path.join(dir_update, return_cardtype(cardtype))
        os.makedirs(dir_name, exist_ok=True)
        os.makedirs(dir_name_update, exist_ok=True)

        for i in items:
            image_url = i.get('src')
            # print(image_url)
            filename = os.path.basename(image_url)
            image_path = os.path.join(dir_name, filename)
            save_path = os.path.join(dir_name_update, filename)
            if not os.path.exists(image_path):
                print('save: {}'.format(save_path))
                image = download_image(image_url)
                save_image(save_path, image)
            # else:
            #     print('pass: {}'.format(image_path))

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

def return_cardtype(cardtype):
    if 'プロデュース' in cardtype:
        kind = 'p'
    elif 'サポート' in cardtype:
        kind = 's'
    else:
        kind = None

    if 'SSR' in cardtype:
        rare = 'SSR'
    elif 'SR' in cardtype:
        rare = 'SR'
    elif 'R' in cardtype:
        rare = 'R'
    elif 'N' in cardtype:
        rare = 'N'
    else:
        rare = None

    return '{}{}'.format(kind, rare)

if __name__ == '__main__':
    main()