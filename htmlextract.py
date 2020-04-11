from html.parser import HTMLParser
import re
import unicodedata
import sys
from os import mkdir
from os.path import exists
import mysql.connector 
import allVariables

#sudo torify wget http://6vx54aliqrmlj7supc4spigwg5pie7jxge2q57rv7i25tzdobuyggkyd.onion -O /home/mim/Bureau/Dark/page/6vx54aliqrmlj7supc4spigwg5pie7jxge2q57rv7i25tzdobuyggkyd.html -t 1 -T 10

url=''
 
class MyHTMLParser(HTMLParser):

    #Initializing lists
    lsStartTags = list()
    lsEndTags = list()
    lsStartEndTags = list()
    lsComments = list()
    lsData = ''
    lsPi = list()
    lsLinks = list()
    match = False
    title = ''

    #HTML Parser Methods
    def handle_starttag(self, startTag, attrs):
        global url

        if startTag == 'title':
            self.match = True

        self.lsStartTags.append(startTag)

        for attr in attrs:
            if startTag == "a":
                if attr[0] == "href":
                    if "onion" in attr[1]:
                        if attr[1].startswith("https"):
                            self.lsLinks.append(attr[1][8:])
                        elif attr[1].startswith("http"):
                            self.lsLinks.append(attr[1][7:])
                        else:
                            self.lsLinks.append(attr[1])

    def handle_endtag(self, endTag):
        self.lsEndTags.append(endTag)

    def handle_startendtag(self,startendTag, attrs):
        self.lsStartEndTags.append(startendTag)

    def handle_comment(self,data):
        self.lsComments.append(data)

    def handle_data(self, data):
        if self.match:
            self.title = data
            self.match = False

        data = data.lower()
        self.lsData += data

    def handle_pi(self, data):
        self.lsPi.append(data)

if __name__ == "__main__":

    url = sys.argv[1]  

    if not exists(allVariables.pathToHtml):
        mkdir(allVariables.pathToHtml)

    #creating an object of the overridden class
    parser = MyHTMLParser()


    with open(allVariables.pathToPage + url + '.html', encoding="utf-8") as html_p:

        """encoding = "utf-8"
        html_page = html_page.read().decode(encoding)
        html_page = unicodedata.normalize('NFD', html_page).encode('ascii', 'ignore')"""

        html_page = html_p.read()
        #suppression des accents
        html_page = unicodedata.normalize('NFD', html_page).encode('ascii', 'ignore')

        regex = re.compile('<style .*>(.*)</style>')
        html_page = regex.sub(" ", str(html_page))

        #Feeding the content
        parser.feed(str(html_page))

        fichier = open(allVariables.pathToHtml + url +'.txt', 'w', encoding="utf-8")
        fichier.write(parser.lsData)
        fichier.close()

        #printing the extracted values

        print("Links find", parser.lsLinks)
        
        conn = mysql.connector.connect(host = allVariables.hostDB, user = allVariables.userDB, password = allVariables.passwordDB, database = allVariables.database)
        cursor = conn.cursor()

        try:
            onion = "%" + url + "%"
            cursor.execute("""UPDATE site SET titre = %s WHERE url like %s """, (parser.title, onion,)) 
            conn.commit()
        except mysql.connector.Error as e:
            print("msg update: " + e.msg)

        for i in range(0,len(parser.lsLinks)):
            try:
                row = "%"+str(parser.lsLinks[i])+"%"
                cursor.execute("""SELECT id FROM site WHERE url like %s """, (row,)) 
                rows = cursor.fetchone()

                if rows == (None,):
                    try:
                        cursor.execute("""INSERT INTO site(url) VALUES(%s)""", (str(parser.lsLinks[i]), ) )
                        conn.commit()
                    except mysql.connector.Error as e:
                        print("msg update: " + e.msg)

            except mysql.connector.Error as e:
                print("msg update: " + e.msg)
        conn.close()
            

        #print("Start tags", parser.lsStartTags)
        #print("End tags", parser.lsEndTags)
        #print("Start End tags", parser.lsStartEndTags)
        #print("Comments", parser.lsComments)
        #print("Data: ", parser.lsData)
        #print("Pi", parser.lsPi)