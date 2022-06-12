import os
import requests
import sqlite3
import json
from pprint import pprint

JAMO_START_LETTER = 44032
JAMO_END_LETTER = 55203

db = sqlite3.connect('word.db')
cursor = db.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS stdict (word TEXT, length INTEGER)')

APIKEY = os.environ.get("STDICT_APIKEY")
for charint in range(JAMO_START_LETTER, JAMO_END_LETTER+1):
    print(f"Trying {chr(charint)}")
    point = 0
    while True:
        print(f"Trying {point+1}th {chr(charint)}")
        result = requests.get(
            "http://stdict.korean.go.kr/api/search.do",
            params={
                "key": APIKEY,
                "method": "start",
                "req_type": "json",
                "q": chr(charint),
                "pos": [1, 2, 7, 8, 9, 11, 12, 13, 14],
                "num": 100,
                "start": point+1,
                "type1": "word",
                "letter_s": 2,
                "advanced": "y"},
            verify=False)
        content = json.loads(result.text)
        pprint(content)

        if "error" in content:
            if content['error']['error_code'] == "104":
                print("invalid start value.")
                break
            else:
                print(content['error']['error_code'], content['error']['message'])

        history = []

        for item in content['channel']['item']:
            word = item['word']
            word = word.replace('-', '')
            length = len(word)
            if word in history:
                continue
            print(word, length)
            cursor.execute('INSERT INTO stdict (word, length) VALUES (?, ?)', (word, length))
            history.append(word)
        point += 1
        db.commit()