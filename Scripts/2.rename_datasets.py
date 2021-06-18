import os
import csv

general = os.listdir("../all_datasets")


id_map = {
	"Administracio":1,
	"Ciutat i Serveis":2,
	"Economia":3,
	"Poblacio":4,
	"Territori":5,

}

for dire in general:
	if dire != ".DS_Store":
		subdir = os.listdir("../all_datasets/" + dire)
		if dire in id_map.keys():
			class_id = id_map[dire]
			for file in subdir:
				os.rename("../all_datasets/" + dire + "/" + file, "../all_datasets/" + dire + "/" + str(class_id) + "_" + file)
print("DONE!")