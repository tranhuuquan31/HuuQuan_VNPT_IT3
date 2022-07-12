import sqlite3
conn = sqlite3.connect('member.db')
cursor = conn.cursor()
student_update= '''UPDATE STUDENT SET CLASS ='C' WHERE NAME='Dung' '''
cursor.execute(student_update)
conn.commit()
conn.close()