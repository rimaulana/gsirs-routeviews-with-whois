import json
import urllib
import csv
import shutil
import sys

sourceFile = '{folder}/{filename}'.format(folder="worked",filename=sys.argv[1])
resultDest = '{folder}/{filename}'.format(folder="result",filename=sys.argv[1])
poolDest = '{folder}/{filename}'.format(folder="pool",filename=sys.argv[1])
result = []

with open(sourceFile) as source:
    reader = csv.DictReader(source)
    for task in reader:
        #do normal routine
        try:
            #normal
            url          = "https://stat.ripe.net/data/whois/data.json?resource="+task['ROUTE']+"/"+task['LENGTH']
            response     = urllib.urlopen(url)
            whois        = json.loads(response.read())
            prefix       = 0
            dateCreated  = ""
            iprange      = ""
            status       = ""
            country      = ""
            keyIndicator = "inetnum"
            authorities = ', '.join(whois["data"]["authorities"])
            if "arin" in whois["data"]["authorities"]:
                keyIndicator = "NetRange"
            for record in whois["data"]["records"]:
                isChange = False
                if record[0]["key"] == keyIndicator:
                    for item in record:
                        if item["key"] == "CIDR":
                            routes = item["value"].split(',')
                            for route in routes:
                                buff = route.split('/')
                                if(len(buff)>1):
                                    if prefix < int(buff[1]):
                                        prefix = int(buff[1])
                                        iprange = buff[0]
                                        isChange = True
                        if item["key"] == "inetnum":
                            routes = item["value"].split(',')
                            for route in routes:
                                buff = route.split('/')
                                if(len(buff)>1):
                                    if prefix < int(buff[1]):
                                        prefix = int(buff[1])
                                        iprange = buff[0]
                                        isChange = True
                        if item["key"] == "RegDate": # ARIN
                            if isChange:
                                dateCreated = item["value"]
                        if item["key"] == "created": # LACNIC, RIPE(different format than lacnic)
                            if isChange:
                                if "ripe" in whois["data"]["authorities"]:
                                    buff = item["value"].split('T')
                                    dateCreated = buff[0]
                                elif "lacnic" in whois["data"]["authorities"]:
                                    if len(item["value"]) > 7:
                                        dateCreated = item["value"][0:4]+"-"+item["value"][4:6]+"-"+item["value"][6:8]
                                    else:
                                        dateCreated = item["value"]
                                else:
                                    dateCreated = item["value"]
                        if item["key"] == "status":
                            if isChange:
                                status = item["value"]
                        if item["key"] == "country":
                            if isChange:
                                country = item["value"]
            result.append({
                'ORIGIN'        : task['ORIGIN'],
                'DATE'          : task['DATE'],
                'RV-ROUTE'      : task['ROUTE'],
                'RV-LENGTH'     : task['LENGTH'],
                'WHOIS-ROUTE'   : iprange.strip(),
                'WHOIS-LENGTH'  : str(prefix),
                'AUTHORITIES'   : authorities,
                'CREATED'       : dateCreated.strip(),
                'STATUS'        : status.strip(),
                'COUNTRY'       : country.strip()
            })
        except Exception as e:
            print e
            shutil.move(sourceFile,poolDest)
            sys.exit()

fileDest = open(resultDest,"w")
fileDest.write("\"ASN\",\"DATE\",\"RV-ROUTE\",\"RV-LENGTH\",\"WHOIS-ROUTE\",\"WHOIS-LENGTH\",\"AUTHORITIES\",\"CREATED\",\"STATUS\",\"COUNTRY\"\n")
for item in result:
    fileDest.write(item['ORIGIN']+","+item['DATE']+","+item['RV-ROUTE']+","+item['RV-LENGTH']+","+item['WHOIS-ROUTE']+","+item['WHOIS-LENGTH']+",\""+item['AUTHORITIES']+"\","+item['CREATED']+","+item['STATUS']+","+item['COUNTRY']+"\n")
fileDest.close()
