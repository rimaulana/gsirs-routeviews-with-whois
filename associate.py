import json
import csv
import urllib
import threading

# MaxNumberofThread = 8
# job = []
# # Initializing 
# for i in range (0,MaxNumberofThread):
# 	job.append([])

# class worker (threading.Thread):
#     def __init__(self, job, outputfile):
#         threading.Thread.__init__(self)
#         self.job = job
#         self.outputfile = outputfile
#     def run(self):
#         for task in self.job:
#         	url = "https://stat.ripe.net/data/whois/data.json?resource="+task['ROUTE']+"/"+task['LENGTH']
#         	# response = urllib.urlopen(url)
#         	# whois = json.loads(response.read())
#         	# authorities = ", ".join(whois["data"]["authorities"])
#         	threadLock.acquire()
#         	self.outputfile.write(url+"\n")
#         	threadLock.release()

# with open("/home/rio/output/rv-raw.csv") as routeviewsfile:
# 	reader = csv.DictReader(routeviewsfile)
# 	counter = 0
# 	for line in reader:
# 		job[counter%MaxNumberofThread].append(line)
# 		counter += 1

# threads = []
# output = open('output.csv','w')
# threadLock = threading.Lock()
# for i in range (0,MaxNumberofThread):
# 	thread = worker(job[i],output)
# 	thread.start()
# 	threads.append(thread)

# for t in threads:
#     t.join()
# output.close()
url = "https://stat.ripe.net/data/whois/data.json?resource=4.15.210.128/26"
response = urllib.urlopen(url)
whois = json.loads(response.read())
for record in whois["data"]["records"]:
	# ARIN -> NetRange, LACNIC -> inetnum, RIPE -> inetnum, AFRINIC -> inetnum, APNIC -> inetnum
	if record[0]["key"] == "NetRange":
		for item in record:
			if item["key"] == "CIDR":
				# do stuff
			if item["key"] == "RegDate": # ARIN
				# do stuff
			if item["key"] == "CIDR":
				# do stuff
			if item["key"] == "created": # LACNIC, RIPE(different format than lacnic)
