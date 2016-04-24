# python commonWords.py <<filename>>
# input file format: 0/n 0.002*frate + 0.001*tedeschi/n

import sys

inputfile = open(sys.argv[1])
outputfile = open('commonWords.txt', 'w')

index = 0

def parse(line):
	tokens = line.split()
	returnList = []
	for t in tokens:
		if t != '+':
			returnList.append(t[6:])
	return returnList

listOfWords = []

for line in inputfile:
	index = index+1
	if (index%2 == 0):
		listOfWords = listOfWords+parse(line)

occurences = [(x,float(listOfWords.count(x))/(index/2)) for x in set(listOfWords)]

for o in occurences:
	if o[1] > 0.25:
		outputfile.write(o[0]+'\n')
		print o[0]

inputfile.close()
outputfile.close()
