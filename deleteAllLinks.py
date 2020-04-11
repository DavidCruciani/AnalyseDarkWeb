from connexion import connect
import mysql.connector 

f = open("/home/mim/Bureau/Dark/sites/allLinks.txt")
lines = f.readlines()

conn = mysql.connector.connect(host="localhost",user="root",password="root", database="Dark")
cursor = conn.cursor()

#connect(conn, cursor)

for i in range( len(lines)+1 ):
	try:
		cursor.execute("""DELETE from allLinks where id=%s""", (i, ) )
		conn.commit()
	except mysql.connector.Error as e:
		print("msg: " + e.msg)

conn.close()