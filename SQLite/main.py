import sqlite3

conn = sqlite3.connect("member.db")
cursor = conn.cursor()

table = """CREATE TABLE STUDENT (NAME VARCHAR(255), CLASS VARCHAR(255), SECTION VARCHAR(255));"""
cursor.execute(table)

cursor.execute('''INSERT INTO STUDENT VALUES ('Quan', 'IT3', 'A')''')
cursor.execute('''INSERT INTO STUDENT VALUES ('Hieu', 'IT3', 'A')''')
cursor.execute('''INSERT INTO STUDENT VALUES ('Dung', 'IT3', 'B')''')
data = cursor.execute('''SELECT *FROM STUDENT''')
for row in data:
    print(row)

conn.commit()
conn.close()