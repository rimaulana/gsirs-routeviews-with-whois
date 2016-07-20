import json
import csv
import urllib

with open('names.csv', 'w') as outputfile:
	fieldnames = ['ORIGIN','DATE','RV-ROUTE','RV-LENGTH','AUTHORITIES']
	writer = csv.DictWriter(outputfile, fieldnames=fieldnames)
	writer.writeheader()
	with open("/home/rio/output/rv-raw.csv") as routeviewsfile:
		reader = csv.DictReader(routeviewsfile)
		for line in reader:
			url = "https://stat.ripe.net/data/whois/data.json?resource="+line['RV-ROUTE']+"/"+line['RV-LENGTH']
			response = urllib.urlopen(url)
			whois = json.loads(response.read())
			authorities = ", ".join(whois["data"]["authorities"])
			writer.writerow({'ORIGIN': line['ORIGIN'], 'DATE': line['DATE'], 'RV-ROUTE': line['RV-ROUTE'], 'RV-LENGTH':line['RV-LENGTH'], 'AUTHORITIES':authorities})
			print line['RV-ROUTE']+"/"+line['RV-LENGTH']+" --> "+authorities