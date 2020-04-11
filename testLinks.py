import allVariables

f = open(allVariables.pathToSite + "LiensAhmia.txt")
lines = f.readlines()
f.close()

s = open(allVariables.pathToSite + "allLinks.txt")
sites = s.readlines()
s.close()

cp=0

for line in sites:
	if line not in lines:
		print("lines: ",str(line.rstrip('\n')))
		cp += 1

print("\n\tTotal: ", cp)

print("\nAllLinks: ", len(sites))
print("LiensAhmia: ", len(lines))

print("\nLiensAhmia ne contient pas " + str(len(sites)-cp) + " liens de AllLinks")