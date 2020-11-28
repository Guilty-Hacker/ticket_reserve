import json

import pymysql


def load_data():
    with open('cities.json', 'r', encoding='utf8') as f:
        cities_json_str = f.read()
        cities_json = json.loads(cities_json_str)
    return cities_json


def insert_cities(cities_json):
    print(type(cities_json))

    cities = cities_json.get('returnValue')
    print(type(cities))

    keys = cities.keys()
    db = pymysql.connect(host='localhost',port=3306,user='root',password='dandan',charset='utf8',database='flask_TPP')
    cursor = db.cursor()
    print(keys)
    for key in keys:
        cursor.execute("insert into letter(letter) values ('%s');" %key)
        db.commit()

        cursor.execute("select letter.id from letter where letter='%s'"%key)
        letter_id = cursor.fetchone()[0]
        # print(key,cities.get(key))
        cities_letter = cities.get(key)
        for city in cities_letter:
            print(city)
            c_id = city.get("id")
            c_parent_id = city.get("parentId")
            c_region_name = city.get("regionName")
            c_city_code = city.get("cityCode")
            c_pinyin = city.get("pinYin")
            cursor.execute("insert into city(letter_id, c_id, c_parent_id, c_region_name, c_city_code, c_pinyin) VALUES (%d,%d,%d,'%s',%d,'%s');"%(letter_id,c_id,c_parent_id,c_region_name,c_city_code,c_pinyin))
            db.commit()
if __name__ == '__main__':
    cities_json = load_data()
    insert_cities(cities_json)