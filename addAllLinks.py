import mysql.connector 

f = open("/home/mim/Bureau/Dark/sites/allLinks.txt")
lines = f.readlines()

conn = mysql.connector.connect(host="localhost",user="root",password="root", database="Dark")
cursor = conn.cursor()

for line in lines:
	try:
		cursor.execute("""INSERT INTO site(url) VALUES(%s)""", (str(line), ) )
		conn.commit()
	except mysql.connector.Error as e:
		print("msg: " + e.msg)
		print("erreur: " + line)

conn.close()