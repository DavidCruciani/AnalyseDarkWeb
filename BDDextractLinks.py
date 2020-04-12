import allVariables
import mysql.connector 
from os import mkdir
from os.path import exists
import sys

conn = mysql.connector.connect(host = allVariables.hostDB, user = allVariables.userDB, password = allVariables.passwordDB, database = allVariables.database)
cursor = conn.cursor()

if not exists(allVariables.pathToSite):
    mkdir(allVariables.pathToSite)

links = open(allVariables.pathToSite + "siteOnion.txt",'w')

if len(sys.argv) < 2:
    print("il manque le nombre d'url a extraire")
    exit(-1)

NB_MAX_URLS_TO_EXTRACT = int(sys.argv[1])   #nombre de sites à extraire de la base de données

# On suppose que NumberOfLine > NB_MAX_URLS_TO_EXTRACT
for x in range(0, NB_MAX_URLS_TO_EXTRACT):
    try:
        cursor.execute("""SELECT MIN(id) FROM site WHERE enCours = 0 """)
        rows = cursor.fetchone()

        if rows != (None,):
            try:
                cursor.execute("""SELECT url FROM site WHERE id = %s """, (rows[0],))
                url = cursor.fetchone()

                cursor.execute("""UPDATE site SET enCours = %s WHERE id=%s""", (1, rows[0], ) )
                conn.commit()

                #print('ok')
                print("id: " + str(rows[0]))
                print("url: " + url[0])

                links.write(url[0])

            except mysql.connector.Error as e:
                print("msg update: " + e.msg)
        else:
            print('\nTout analysé')
            break

    except mysql.connector.Error as e:
        print("msg select id: " + e.msg)
            
conn.close()
links.close()
