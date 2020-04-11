import os
import subprocess
import time
import json


def saveErrorSite(url):
    x = {
        "url": url,
        "date": time.strftime("%d/%m/%Y")
    }
    with open("/home/mim/Bureau/Dark/sites/siteOnionFail.json", 'a') as outfile:
        json.dump(x, outfile, indent=4)


f = open("/home/mim/Bureau/Dark/sites/siteOnion.txt")
error = open("/home/mim/Bureau/Dark/sites/siteOnionFail.txt",'a')
success = open("/home/mim/Bureau/Dark/sites/siteOnionSuccess.txt",'a')
#outfile = open("/home/mim/Bureau/Dark/sites/siteOnionFail.json", 'a+')
lines = f.readlines()

f.close()

for line in lines:

	print("site analysé: ", line)
	#requete = "timeout 10s torify curl 6vx54aliqrmlj7supc4spigwg5pie7jxge2q57rv7i25tzdobuyggkyd.onion"
	#requete = "timeout 10s torify curl 22222222222qerho.onion"
	requete = "timeout 15s torify curl " + line

	p = subprocess.Popen(requete, stdout=subprocess.PIPE, shell=True)
	(output, err) = p.communicate()
	## Wait for wget to terminate. Get return returncode ##
	p_status = p.wait()
	#print("Command output : ", output)
	if p_status == 0:
		print("Command exit status/return code : ", p_status)
		success.write(line)
	else:
		print("\nfail")
		error.write(line)
		saveErrorSite(line)

error.close()
success.close()
#outfile.close()

total = ''

err = open("/home/mim/Bureau/Dark/sites/siteOnionFail.txt")
lEr = err.readlines()

succ = open("/home/mim/Bureau/Dark/sites/siteOnionSuccess.txt")
lSuc = succ.readlines()

with open("/home/mim/Bureau/Dark/sites/allLinks.txt") as fichier:
	for l in fichier:
		if not l in lEr and not l in lSuc:
			total += l


tri = open("/home/mim/Bureau/Dark/sites/SiteTrie.txt",'w')
tri.write(total)