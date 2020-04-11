from os import system, mkdir
from os.path import exists
import subprocess
from datetime import datetime
import allVariables
import mysql.connector 


def aspire(url):

    if not exists(allVariables.pathToPage):
        mkdir(allVariables.pathToPage)

    request = "torify wget http://" + url + " -O " + allVariables.pathToPage + url + ".html -t 1 -T 15"   # requête wget

    ## call wget command ##
    p = subprocess.Popen(request, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    ## Wait for wget to terminate. Get return returncode ##
    p_status = p.wait()
    print("Command output : ", output)
    print("Command exit status/return code : ", p_status)

    if (p_status == 8 or p_status == 0):
        error = "ok"
    else:
        print("Erreur dans l'url")
        error = "nok"

    return error

def saveErrorSite(url):
    #*******************************a changer**************************
    conn = mysql.connector.connect(host = allVariables.hostDB, user = allVariables.userDB, password = allVariables.passwordDB, database = allVariables.database)
    cursor = conn.cursor()

    now = datetime.now()

    try:
        onion = "%" + url + "%"

        cursor.execute("""UPDATE site SET date = %s, erreur = %s, enCours = %s WHERE url like %s """, (now, 1, 2, onion,)) 
        conn.commit()
    except mysql.connector.Error as e:
        print("msg update: " + e.msg)

    print(url.rstrip('\n'), " Erreur envoyée dans la base")
    conn.close()
#***************************************************

if not exists(allVariables.pathToSite):
    mkdir(allVariables.pathToSite)

f = open(allVariables.pathToSite + "siteOnion.txt")
lines = f.readlines()
f.close()

for line in lines:
    url = line
    url = url.rstrip('\n')

    if url.endswith("/"):
        url = url[:-1]

    #lancer aspiration site + mettre les fichiers au bon endroit
    aspireError = aspire(url)

    if(aspireError == "ok"):
        print("ok")
        #recuperer fichier JSON sur Alyze
        system("python3 " + allVariables.pathToProg + "htmlextract.py " + url)
        system("python3 " + allVariables.pathToProg + "Count.py " + url)
    else:
        print("Erreur wget pour aspirer le site : ", url)
        saveErrorSite(url)


system("rm -r " + allVariables.pathToHtml)
system("rm -r " + allVariables.pathToPage)