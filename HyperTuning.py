import subprocess
import sys
import numpy

print len(sys.argv)
if len(sys.argv)!= 12:
        print "usage: application <low Topics> <high Topics> <values to test> <low no_above> <high no_above> <values to test> <low no_below> <high no_below> <values to test> <results dir>"
        sys.exit(1)

low_topics = int(float(sys.argv[1]))
high_topics = int(float(sys.argv[2]))
num_topics = int(float(sys.argv[3]))
#topics_spacing = int((high_topics+low_topics)/(num_topics-1))

#percentage
low_above = float(sys.argv[4])
high_above = float(sys.argv[5])
num_above = float(sys.argv[6])

#absolute number
low_below = int(float(sys.argv[7]))
high_below = int(float(sys.argv[8]))
num_below = int(float(sys.argv[9]))

inputFilename = sys.argv[10]
resultsDir = sys.argv[11]

for above in numpy.linspace(low_above,high_above,num_above).tolist() :
    for below in numpy.linspace(low_below,high_below,num_below).tolist() :
        for topics in numpy.linspace(low_topics,high_topics,num_topics).tolist() :
                    listPassed =["/home/sotos/Enthought/Canopy_64bit/User/bin/python2.7", "LDA_with_arguments.py", inputFilename, str(topics), str(above), str(below), resultsDir]
                    subprocess.Popen(listPassed)
