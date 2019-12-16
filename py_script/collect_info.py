import os
from pathlib import Path
import requests
from bs4 import BeautifulSoup as bs
import re
import sqlite3

def main():
    url = 'https://imas-shinycolors.boom-app.wiki/entry'

    # カード用データベース
    file_carddb = '../db/card.sqlite3'
    conn = sqlite3.connect(file_carddb)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE TYPE='table' AND NAME='card_list';")
    if cur.fetchone() == (0,):
        cur.execute('CREATE TABLE card_list(ID int, card_name text);')
        cur.execute('CREATE UNIQUE INDEX idindex_card_list ON card_list(ID);')

    cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE TYPE='table' AND NAME='card_info';")
    if cur.fetchone() == (0,):
        cur.execute('CREATE TABLE card_info(ID int, idea text, unit text, obtain text, implement text);')
        cur.execute('CREATE UNIQUE INDEX idindex_card_info ON card_info(ID);')

    cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE TYPE='table' AND NAME='card_possession';")
    if cur.fetchone() == (0,):
        cur.execute('CREATE TABLE card_possession(ID int, possession int);')
        cur.execute('CREATE UNIQUE INDEX idindex_card_possession ON card_possession(ID);')

    p = Path('update/icon')
    dirs = list(p.glob(u'**/'))
    # カレントディレクトリも入るので削除
    dirs.pop(0)

    for d in dirs:
        # print(d)
        p = Path(d)
        pics = list(p.glob(u'*.jpg'))
        for pic in pics:
            print(pic)
            filename = os.path.basename(pic)
            id, ext = os.path.splitext(filename)
            card_url = os.path.join(url, 'card-{}'.format(int(id)))
            card_title, dic_info = return_cardinfo(card_url)
            card_name = '{}{}'.format(card_title, dic_info['アイドル'])
            if not 'アイデア' in dic_info:
                dic_info['アイデア'] = '-'

            insert_card = 'INSERT INTO card_list VALUES ({}, "{}")'.format(id, card_name)
            try:
                cur.execute(insert_card)
            except sqlite3.IntegrityError:
                print('insert error(unique index)')

            insert_card_info = 'INSERT INTO card_info VALUES ({}, "{}", "{}", "{}", "{}")'.format(id, dic_info['アイデア'], dic_info['ユニット'], dic_info['入手方法'], dic_info['実装日'])
            try:
                cur.execute(insert_card_info)
            except sqlite3.IntegrityError:
                print('insert error(unique index)')

            insert_card_possession = 'INSERT INTO card_possession VALUES ({}, {})'.format(id, 0)
            try:
                cur.execute(insert_card_possession)
            except sqlite3.IntegrityError:
                print('insert error(unique index)')

    conn.commit()
    cur.close()
    conn.close()

def return_cardinfo(card_url):
    dic_info = {}

    soup = bs(requests.get(card_url).content, 'html.parser')
    title = soup.find('title')
    title = title.text

    pattern = r'\w+【.+】'
    card_title = re.search(pattern, title)[0]

    pattern = r'【.+】'
    card_title = re.search(pattern, card_title)[0]

    entry_body = soup.find_all('div', class_='entry-body')[0]
    table = entry_body.find('table')
    card_info = table.find_all('tr')
    # print(card_info)

    for i in card_info:
        key = i.th.text
        value = i.td.text
        dic_info[key] = value

    return card_title, dic_info

if __name__ == '__main__':
    main()