import json
import csv
import urllib

MaxNumberofThread = 8
job = []
# Initializing 
for i in range (0,MaxNumberofThread):
	job.append([])

# with open('names.csv', 'w') as outputfile:
# 	fieldnames = ['ORIGIN','DATE','RV-ROUTE','RV-LENGTH','AUTHORITIES']
# 	writer = csv.DictWriter(outputfile, fieldnames=fieldnames)
# 	writer.writeheader()

with open("/home/rio/pandas/hijack.csv") as routeviewsfile:
	reader = csv.DictReader(routeviewsfile)
	counter = 0
	for line in reader:
		job[counter%MaxNumberofThread].append(line)
		counter += 1
		# url = "https://stat.ripe.net/data/whois/data.json?resource="+line['RV-ROUTE']+"/"+line['RV-LENGTH']
		# response = urllib.urlopen(url)
		# whois = json.loads(response.read())
		# authorities = ", ".join(whois["data"]["authorities"])
		# writer.writerow({'ORIGIN': line['ORIGIN'], 'DATE': line['DATE'], 'RV-ROUTE': line['RV-ROUTE'], 'RV-LENGTH':line['RV-LENGTH'], 'AUTHORITIES':authorities})
		# print line['RV-ROUTE']+"/"+line['RV-LENGTH']+" --> "+authorities

print job[0]
print job[7]
