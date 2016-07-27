import json
import csv
import urllib
import threading

MaxNumberofThread = 8
job = []
# Initializing 
for i in range (0,MaxNumberofThread):
	job.append([])

class worker (threading.Thread):
    def __init__(self, job, outputfile):
        threading.Thread.__init__(self)
        self.job = job
        self.outputfile = outputfile
    def run(self):
        for task in self.job:
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
						buff = item["value"].split('/')
						if(len(buff)>1):
							if prefix < int(buff[1]):
								prefix = int(buff[1])
								iprange = buff[0]
								isChange = True
					if item["key"] == "inetnum":
							buff = item["value"].split('/')
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
        	threadLock.acquire()
        	self.outputfile.write(task['ORIGIN']+","+task['DATE']+","+task['ROUTE']+","+task['LENGTH']+","+iprange.strip()+","+str(prefix)+",\""+authorities+"\","+created+","+status.strip()+","+country.strip()+"\n")
        	threadLock.release()

with open("input.csv") as routeviewsfile:
	reader = csv.DictReader(routeviewsfile)
	counter = 0
	for line in reader:
		job[counter%MaxNumberofThread].append(line)
		counter += 1

threads = []
output = open('output.csv','w')
output.write("\"ASN\",\"DATE\",\"RV-ROUTE\",\"RV-LENGTH\",\"WHOIS-ROUTE\",\"WHOIS-LENGTH\",\"AUTHORITIES\",\"CREATED\",\"STATUS\",\"COUNTRY\"\n")
threadLock = threading.Lock()
for i in range (0,MaxNumberofThread):
	thread = worker(job[i],output)
	thread.start()
	threads.append(thread)

for t in threads:
    t.join()
output.close()

# arin = "23.29.96.0/24"
# ripe = "5.1.112.0/24"
# lacnic = "148.249.0.0/24"
# apnic = "1.2.4.0/24"
# afrinic = "41.0.0.0/18"
# url = "https://stat.ripe.net/data/whois/data.json?resource="+apnic
# print iprange+"/"+str(prefix)+" created: "+created+" status: "+status+" country: "+country
