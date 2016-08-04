import csv
import os
import sys

rootFolder = os.path.abspath(os.path.dirname(__file__))
MaxRecordPerFile = 4
with open(sys.argv[1]) as source:
    reader = csv.DictReader(source)
    writeCounter= 0
    fileCounter = 0
    for line in reader:
        if writeCounter == 0:
            fileName = '{root}/{folder}/{name}.{frmt}'.format(root=rootFolder,folder="pool",name=str(fileCounter),frmt="csv")
            writer = open(fileName,"w")
            # Writing header
            writer.write("\"ORIGIN\",\"DATE\",\"ROUTE\",\"LENGTH\"\n")
            writer.write('{0},{1},{2},{3}\n'.format(line['ORIGIN'],line['DATE'],line['ROUTE'],line['LENGTH']))
        elif writeCounter == (MaxRecordPerFile-1):
            writer.write('{0},{1},{2},{3}\n'.format(line['ORIGIN'],line['DATE'],line['ROUTE'],line['LENGTH']))
            writer.close()
            fileCounter += 1
            writeCounter = -1
        else:
            writer.write('{0},{1},{2},{3}\n'.format(line['ORIGIN'],line['DATE'],line['ROUTE'],line['LENGTH']))
        writeCounter += 1
