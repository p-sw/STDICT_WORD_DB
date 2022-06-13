import sqlite3

db = sqlite3.connect('word.db')
cursor = db.cursor()

sql1 = "UPDATE stdict SET word=REPLACE(word, 'ㆍ', '') WHERE word LIKE '%ㆍ%'"
sql2 = "UPDATE stdict SET length=LENGTH(word) WHERE LENGTH(word) != length"

cursor.execute(sql2)
db.commit()