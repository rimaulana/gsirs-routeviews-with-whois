import json
import csv
import urllib
import threading
import os

MaxNumberofThread = 8
job = []
openFiles = []
# Initializing
for i in range (0,MaxNumberofThread):
	# job.append([])
	temp = open("Thread-"+str(i)+"-source.csv","w")
	temp.write("\"ORIGIN\",\"DATE\",\"ROUTE\",\"LENGTH\"\n")
	openFiles.append(temp)

class worker (threading.Thread):
    def __init__(self, number):
        threading.Thread.__init__(self)
        self.number = number
        self.output = open("Thread-"+str(self.number)+"-output.csv","w")
        self.ErrorFlag = False
    def run(self):
        self.output.write("\"ASN\",\"DATE\",\"RV-ROUTE\",\"RV-LENGTH\",\"WHOIS-ROUTE\",\"WHOIS-LENGTH\",\"AUTHORITIES\",\"CREATED\",\"STATUS\",\"COUNTRY\"\n")
	with open("Thread-"+str(self.number)+"-source.csv") as source:
        	reader =csv.DictReader(source)
        	for task in reader:
            		if not self.ErrorFlag:
				try:
			    		url = "https://stat.ripe.net/data/whois/data.json?resource="+task['ROUTE']+"/"+task['LENGTH']
			    		response = urllib.urlopen(url)
			    		whois = json.loads(response.read())
			    		prefix = 0
			    		created = ""
			    		iprange = ""
			    		status = ""
			    		country = ""
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
			                        			created = item["value"]
			                		if item["key"] == "created": # LACNIC, RIPE(different format than lacnic)
			                    			if isChange:
			                        			if "ripe" in whois["data"]["authorities"]:
			                            				buff = item["value"].split('T')
			                            				created = buff[0]
			                        			elif "lacnic" in whois["data"]["authorities"]:
			                            				if len(item["value"]) > 7:
			                                				created = item["value"][0:4]+"-"+item["value"][4:6]+"-"+item["value"][6:8]
			                            				else:
			                                				created = item["value"]
			                        			else:
			                            				created = item["value"]
			                		if item["key"] == "status":
			                    			if isChange:
			                        			status = item["value"]
			                		if item["key"] == "country":
			                    			if isChange:
			                        			country = item["value"]
			    		self.output.write(task['ORIGIN']+","+task['DATE']+","+task['ROUTE']+","+task['LENGTH']+","+iprange.strip()+","+str(prefix)+",\""+authorities+"\","+created+","+status.strip()+","+country.strip()+"\n")
				except:
			    		self.ErrorFlag = True
			    		self.output.close()
			    		self.failsave = open("Thread-"+str(self.number)+"-failsave.csv","w")
			    		self.failsave.write("\"ORIGIN\",\"DATE\",\"ROUTE\",\"LENGTH\"\n")
			    		self.failsave.write(task['ORIGIN']+","+task['DATE']+","+task['ROUTE']+","+task['LENGTH']+"\n")
			else:
			    	self.failsave.write(task['ORIGIN']+","+task['DATE']+","+task['ROUTE']+","+task['LENGTH']+"\n")
		if self.ErrorFlag:
			self.failsave.close()
		else:
			self.output.close()
			#os.remove("Thread-"+str(self.number)+"-source.csv")

with open("test.csv") as routeviewsfile:
	reader = csv.DictReader(routeviewsfile)
	counter = 0
	for line in reader:
		openFiles[counter%MaxNumberofThread].write(line['ORIGIN']+","+line['DATE']+","+line['ROUTE']+","+line['LENGTH']+"\n")
		counter += 1

for files in openFiles:
	files.close()

threads = []
output = open('output.csv','w')
output.write("\"ASN\",\"DATE\",\"RV-ROUTE\",\"RV-LENGTH\",\"WHOIS-ROUTE\",\"WHOIS-LENGTH\",\"AUTHORITIES\",\"CREATED\",\"STATUS\",\"COUNTRY\"\n")
threadLock = threading.RLock()
for i in range (0,MaxNumberofThread):
	thread = worker(i)
	thread.start()
	threads.append(thread)

for t in threads:
    t.join()
# output.close()
