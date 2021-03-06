#sudo apt install python3-sklearn
from sklearn.feature_extraction.text import CountVectorizer
import re
import json
import sys
import mysql.connector 
from datetime import datetime
import allVariables

def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)
 
def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """return n-gram counts in descending order of counts"""
    
    #use only topn items from vector
    sorted_items = sorted_items[:topn]
 
    results=[]
    
    # word index, count i
    for idx, count in sorted_items:
        
        # get the ngram name
        n_gram=feature_names[idx]
        
        # collect as a list of tuples
        results.append((n_gram,count))
 
    return results

###################################################################################

documents = []

if len(sys.argv) != 3:
        print("il manque l'identifiant ainsi que l'url a extraire")
        exit(-1)

i_d = sys.argv[1] 
url = sys.argv[2]


pattern = re.compile('^([0-9]+)|[0-9]+')

content = ''

try:
    with open(allVariables.pathToHtml + url + ".txt", 'rb') as file:
        for line in file:
            word = str(line).split(" ")
            for m in word:
                #if not re.match("^[0-9]+",str(m)) and not re.match("[0-9]+",str(m)):
                if not( pattern.match(str(m)) ):
                    content += str(m)+" "
except FileNotFoundError:
    print("le fichier voulu n'existe pas")
    exit(-1)


documents = [content]

documents[0] = documents[0][2:]
documents[0] = documents[0][:-1]

cv = CountVectorizer(stop_words="english")

count_vector = None
try:
    count_vector=cv.fit_transform(documents)
except ValueError:
    try:
        conn = mysql.connector.connect(host = allVariables.hostDB, user = allVariables.userDB, password = allVariables.passwordDB, database = allVariables.database)
        cursor = conn.cursor()

        now = datetime.now()

        cursor.execute("""UPDATE site SET date = %s, erreur = %s, titreErreur = %s, enCours = %s  WHERE id = %s """, (now, 1, "le site semble vide", 2, i_d, )) 
        conn.commit()

        print("Le site semble vide")
        conn.close()

    except mysql.connector.Error as e:
        print("msg update: " + e.msg)

    exit(-1)


#sort the counts of first book title by descending order of counts
sorted_items=sort_coo(count_vector[0].tocoo())

#Get feature names (words/n-grams). It is sorted by position in sparse matrix
feature_names=cv.get_feature_names()
n_grams=extract_topn_from_vector(feature_names,sorted_items,20)
motBDD=extract_topn_from_vector(feature_names,sorted_items,6)

"""for i in motBDD:
    print(i[0], i[1])"""


listCat = {}

with open(allVariables.pathToProg + "wordClassification/categories.json") as json_file:
    dataCateg = json.load(json_file)

    for key in dataCateg.keys():
        listCat[key] = 0

    for key in dataCateg.keys():
        for i in n_grams:
            if i[0] in dataCateg[key]:
                listCat[key] += i[1]
        
     
print("fichier: ", url)
print("listCat: ", listCat)

cpt = 0
k = ""
for j in listCat:
    if cpt < listCat[j]:
        cpt = listCat[j]
        k = j

if k == "":
    k="Other"

print("---------affichage: ", k)
print()


conn = mysql.connector.connect(host = allVariables.hostDB, user = allVariables.userDB, password = allVariables.passwordDB, database = allVariables.database)
cursor = conn.cursor()

now = datetime.now()

try:
    cursor.execute("""UPDATE site SET date = %s,  cat = %s, enCours = %s  WHERE id = %s """, (now, k, 2, i_d, )) 
    conn.commit()
except mysql.connector.Error as e:
    print("msg update: " + e.msg)

nb = 1

for i in motBDD:
    try:
        cursor.execute("""UPDATE site SET mc%s = %s WHERE id = %s """, (nb, i[0], i_d, )) 
        conn.commit()
        nb += 1
    except mysql.connector.Error as e:
        print("msg update: " + e.msg)

conn.close()
