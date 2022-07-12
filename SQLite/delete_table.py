import sqlite3
conn = sqlite3.connect('member.db')
cursor= conn.cursor()
st_delete= "DELETE FROM STUDENT WHERE NAME ='Hieu' "
cursor.execute(st_delete)
conn.commit()
conn.close()