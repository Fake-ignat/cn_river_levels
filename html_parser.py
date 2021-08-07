import datetime
from paths_manager import PathsManager
import dateutil.parser
import requests
from Kml_reader import KMLReader
from bs4 import BeautifulSoup
import sqlite3 as sq
import re

DB_NAME = 'storage/chinese_levels.db'
CHINA_URL = 'http://xxfb.mwr.cn/hydroSearch/greatRiver'

storage_dir = 'storage'
querry_data = []
posts = {}


SELECT_DATA = "SELECT cn_name, ru_name FROM posts"
INSERT_DATA = "INSERT INTO levels  VALUES (?, ?, ?)"
UPDATE_DATA = "UPDATE levels SET level = ? WHERE date=? and cn_name=?"


with sq.connect(DB_NAME) as con:
    # print(list(con.cursor().execute(SELECT_DATA)))
    for cn_name, ru_name in con.cursor().execute(SELECT_DATA):
        posts[cn_name] = ru_name


def get_data_from_url(URL):
    response = requests.get(URL)
    result = response.json()['result']
    match = re.findall(r'\d+', result['date'])
    level_date = '.'.join(reversed(match))

    level_data = result['data']
    levels = {}

    for point in level_data:
        st_name = point['stnm'].strip()
        level = float(point['zl'])
        levels[st_name] = level

    return level_date, levels


def get_dataset(level_date, levels):
    dataset = []
    for cn_name, ru_name in posts.items():
        if cn_name in levels:
            a = [level_date, ru_name, levels[cn_name]]
            dataset.append(tuple(a))
            print(f'{ru_name}, {levels[cn_name]}')
        else:
            print(f'{ru_name} не найден')
    return dataset






class PageParser():
    table_id = 'hdtable'
    date_id = 'hddate'

    def __init__(self, addres, posts):
        self.soup = self.get_soup(addres)
        self.table = self.get_table()
        self.cn_names = posts.keys()
        self.data = self.extract_data()

    def get_table(self):
        table = self.soup.find('div', {'id': PageParser.table_id})
        return table.find_all('tr')

    def get_timestamp(self):
        date_text = self.soup.find('span', {'id': PageParser.date_id}).text
        match = re.findall(r'\d+', date_text)
        timestamp = '.'.join(reversed(match))
        return timestamp

    def extract_data(self):
        data = {}
        timestamp = self.get_timestamp()
        for line in self.table:
            cells = line.findAll('td')
            cn_name = self.elem_text(cells[3])
            if cn_name in self.cn_names:
                data[cn_name] = {'level': float(self.elem_text(cells[5])),
                                 'date': timestamp}

        return data

    @staticmethod
    def elem_text(elem):
        return elem.text.strip()

    @staticmethod
    def get_soup(addres):
        with open(addres, 'rb') as page:
            return BeautifulSoup(page, 'lxml')

# last_dates = PathsManager(storage_dir).get_last_dates()
# # last_dates = [f'{d}.07.2021' for d in range(23, 26)]
#
# saved_pages = [f'storage\\{dates}.html' for dates in last_dates]
#
# for i, page in enumerate(saved_pages):
#     try:
#         parser = PageParser(page, posts)
#         for k, v in parser.data.items():
#             a = [last_dates[i], posts[k], float(v['level'])]
#             querry_data.append(tuple(a))
#             print(f"{last_dates[i]}, {posts[k]:<7}, {v['level']:<5}")
#
#     except Exception as e:
#         print(e)


# записываем в базу данных все посты
def insert_in_DB(db_name, insertQuerry, data):
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.executemany(insertQuerry, data)

#insert_in_DB(DB_NAME, INSERT_DATA, querry_data)


# with sq.connect(DB_NAME) as con:
#     cur = con.cursor()
#     DELETE_QUERRY = 'DELETE from levels'
#     cur.execute(DELETE_QUERRY)


level_date, levels = get_data_from_url(CHINA_URL)
querry_data = get_dataset(level_date, levels)

with sq.connect(DB_NAME) as con:
    Q = 'SELECT * FROM levels WHERE date ="07.08.2021"'
    for post in con.cursor().execute(Q):
        print(post)