#sudo apt install python3-bs4
from bs4 import BeautifulSoup
import requests

new_days = open("/home/mim/Bureau/Dark/sites/LiensAhmia.txt",'w')
url = "https://ahmia.fi/address/"

page = requests.get(url)
data = page.text
soup = BeautifulSoup(data, "lxml")
nb = 0;

for link in soup.find_all('a'):
    if "onion" in link.get('href'):
        new_days.write(link.get('href').split('/')[2]+"\n")
        nb += 1

print("Nombre d'urls onion = ", nb)
new_days.close()
