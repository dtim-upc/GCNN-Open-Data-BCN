import csv
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import sys
from IPython import embed

base = "https://opendata-ajuntament.barcelona.cat"


#csv.field_size_limit(sys.maxsize)

###################### Administració ######################

'''
urls = [
"https://opendata-ajuntament.barcelona.cat/data/ca/organization/administracio?page=1",
"https://opendata-ajuntament.barcelona.cat/data/ca/organization/administracio?page=2",
"https://opendata-ajuntament.barcelona.cat/data/ca/organization/administracio?page=3",
"https://opendata-ajuntament.barcelona.cat/data/ca/organization/administracio?page=4",
"https://opendata-ajuntament.barcelona.cat/data/ca/organization/administracio?page=5"

]
'''

###################### Ciutats i serveis ######################

'''
urls = [
"https://opendata-ajuntament.barcelona.cat/data/ca/organization/entorn-urba?page=1",
"https://opendata-ajuntament.barcelona.cat/data/ca/organization/entorn-urba?page=2",
"https://opendata-ajuntament.barcelona.cat/data/ca/organization/entorn-urba?page=3",
"https://opendata-ajuntament.barcelona.cat/data/ca/organization/entorn-urba?page=4",
"https://opendata-ajuntament.barcelona.cat/data/ca/organization/entorn-urba?page=5",
"https://opendata-ajuntament.barcelona.cat/data/ca/organization/entorn-urba?page=6",
"https://opendata-ajuntament.barcelona.cat/data/ca/organization/entorn-urba?page=7",
"https://opendata-ajuntament.barcelona.cat/data/ca/organization/entorn-urba?page=8",
]
'''

###################### Població ######################

'''
urls = [
"https://opendata-ajuntament.barcelona.cat/data/ca/organization/poblacio?page=1",
"https://opendata-ajuntament.barcelona.cat/data/ca/organization/poblacio?page=2",
"https://opendata-ajuntament.barcelona.cat/data/ca/organization/poblacio?page=3",
"https://opendata-ajuntament.barcelona.cat/data/ca/organization/poblacio?page=4",
"https://opendata-ajuntament.barcelona.cat/data/ca/organization/poblacio?page=5",
"https://opendata-ajuntament.barcelona.cat/data/ca/organization/poblacio?page=6"
]
'''


###################### Territori ######################
'''
urls = [
"https://opendata-ajuntament.barcelona.cat/data/ca/organization/territori?page=1",
"https://opendata-ajuntament.barcelona.cat/data/ca/organization/territori?page=2",
"https://opendata-ajuntament.barcelona.cat/data/ca/organization/territori?page=3",
"https://opendata-ajuntament.barcelona.cat/data/ca/organization/territori?page=4",
"https://opendata-ajuntament.barcelona.cat/data/ca/organization/territori?page=5",
"https://opendata-ajuntament.barcelona.cat/data/ca/organization/territori?page=6"
]
'''


###################### Economia ######################


urls = [
"https://opendata-ajuntament.barcelona.cat/data/ca/organization/economia"
]


all_datasets = []
datasets_notsaved = []
dataset_now = ''
broken_datasets = 0

for url in urls:
	datasets = []
	all_datasets.append(url)
	html = requests.get(url)
	content = html.text
	soup = BeautifulSoup(content, "html.parser")

	for a in soup.find_all('a',href=True):
		if re.findall('dataset/', a['href']):
			datasets.append(a["href"])

	datasets = list(set(datasets))

	i = 0
	print("I AM IN URL: " +str(url))
	for d in datasets:
		html = requests.get(base + d)
		content = html.content
		soup = BeautifulSoup(content, "html.parser")
		found = False

		for a in soup.find_all('a',href=True):
			if re.findall('.csv', a['href']) or re.findall('download', a['href']):
			#if re.findall('.csv', a['href']):
				meta = soup.find_all("meta")
				if len(meta) > 0:
					for tag in meta:
						#print(tag)
						if tag.get("property", None) == "og:title":
							title = tag.get("content", None)
							title = ' '.join(str(title).split(' ')[:-4])
							dataset_now = title
							all_datasets.append(title)
							print(title)
							break
				
				download = requests.get(a["href"])
				#print(download.headers)
				#print(download.content)
				
				try:
					ct_ty = download.headers["Content-Type"]
				except:
					print("NO CONTENT TYPE")
					broken_datasets = broken_datasets + 1
					datasets_notsaved.append(dataset_now)
					break

				if ct_ty == "text/csv":
					try:
						decoded_content = download.content.decode('utf-8')
						cr = csv.reader(decoded_content.splitlines(), delimiter=',')
						my_list = list(cr)
						with open("../all_datasets/Economia/" + str(title).replace("/", "-")+  ".csv", 'w', newline='', encoding="utf-8") as f_output:
							writer = csv.writer(f_output, delimiter =",",quoting=csv.QUOTE_MINIMAL)
							for row in my_list[:-1]:
								writer.writerow(row)
					except:
						print("I don't like this .csv. I'm not saving it.")
						broken_datasets = broken_datasets + 1
						datasets_notsaved.append(dataset_now)
						break
					
					break
				else:
					try:
						decoded_content = download.content.decode('utf-8')
						cr = csv.reader(decoded_content.splitlines(), delimiter=',')
						my_list = list(cr)
						with open("../all_datasets/Economia-Bad/" + str(title).replace("/", "-")+  ".csv", 'w', newline='', encoding="utf-8") as f_output:
							writer = csv.writer(f_output, delimiter =",",quoting=csv.QUOTE_MINIMAL)
							for row in my_list[:-1]:
								writer.writerow(row)
					except:
						print("I don't like this file. I'm not saving it.")
						broken_datasets = broken_datasets + 1
						datasets_notsaved.append(dataset_now)
						break
					
					break
				
		print(i)
		i+=1
		

print("THERE ARE: " +str(broken_datasets)+ " DATASETS WITH ERRORS. GOOD LUCK!")

with open("../all_datasets/Economia-Bad/datasets_with_errors.txt", "w") as outfile:
    outfile.write("\n".join(datasets_notsaved))
	
with open("../all_datasets/datasets-Economia_names.txt", "w") as outfile:
    outfile.write("\n".join(all_datasets))

