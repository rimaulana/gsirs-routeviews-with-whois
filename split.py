import csv

MaxRecordPerFile = 4
with open("test.csv") as source:
    reader = csv.DictReader(source)
    writeCounter= 0
    fileCounter = 0
    for line in reader:
        if writeCounter == 0:
            fileName = '{folder}/{name}.{frmt}'.format(folder="pool",name=str(fileCounter),frmt="csv")
            writer = open(fileName,"w")
            # Writing header
            writer.write("\"ORIGIN\",\"DATE\",\"ROUTE\",\"LENGTH\"\n")
            writer.write('{0},{1},{2},{3}\n'.format(line['ROUTE'],line['DATE'],line['ROUTE'],line['LENGTH']))
        elif writeCounter == (MaxRecordPerFile-1):
            writer.write('{0},{1},{2},{3}\n'.format(line['ROUTE'],line['DATE'],line['ROUTE'],line['LENGTH']))
            writer.close()
            fileCounter += 1
            writeCounter = -1
        else:
            writer.write('{0},{1},{2},{3}\n'.format(line['ROUTE'],line['DATE'],line['ROUTE'],line['LENGTH']))
        writeCounter += 1
