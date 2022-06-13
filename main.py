import os
import requests
import sqlite3
import json
from pprint import pprint
import logger
from logger import log

JAMO_START_LETTER = 44032
JAMO_END_LETTER = 55203

db = sqlite3.connect('word.db')
cursor = db.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS stdict (word TEXT, length INTEGER)')
db.commit()
cursor.execute('DELETE FROM stdict')
db.commit()

log.info("Initialized.")

APIKEY = os.environ.get("STDICT_APIKEY")
log.info(f"API KEY: {APIKEY}")
for charint in range(JAMO_START_LETTER, JAMO_END_LETTER+1):
    log.info(f"Trying {chr(charint)}")
    point = 0
    while True:
        log.info(f"Trying {point+1}th {chr(charint)}")
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
        print(result.status_code)
        print(result.text)
        content = json.loads(result.text)
        pprint(content)

        if "error" in content:
            if content['error']['error_code'] == "104":
                log.warning("Invalid start value.")
                break
            else:
                log.warning(f"{content['error']['error_code']}: {content['error']['message']}")

        history = []
        if not content:
            break

        for item in content['channel']['item']:
            word = item['word']
            word = word.replace('-', '').replace('ㆍ', '')
            length = len(word)
            if word in history:
                continue
            log.info(f"Add {word} | {length}")
            cursor.execute('INSERT INTO stdict (word, length) VALUES (?, ?)', (word, length))
            history.append(word)
        point += 1
        db.commit()