import pandas as pd
import os
import csv
import numpy as np
import csv as csv_

def prepare_datasets(path):
    ds_names = os.listdir(path)
    os.mkdir(path+"all_datasets_clean")
    #information_csv = pd.read_csv(path+'information_csv.csv')
    #first = True

    datasets_notsaved = []
    broken_datasets = 0

    for file in ds_names:
        file2 = file.replace(" ", "_")
        print(file2)
        try:
            with open(path+file, 'r', encoding = "cp437") as csvfile:
                delim = csv_.Sniffer().sniff(csvfile.readline()).delimiter
                if (delim not in [',', ';', '|', '/']):
                    delim = ','
            csv = pd.read_csv(path+file, delimiter = delim)
            df_file = pd.DataFrame(csv)
            df_file.columns = df_file.columns.str.replace(".", "")
            df_file.columns = df_file.columns.str.replace("(", "")
            df_file.columns = df_file.columns.str.replace(")", "")
            df_file.columns = df_file.columns.str.replace(";", "")
            df_file.columns = df_file.columns.str.replace("-", "")
            df_file.columns = df_file.columns.str.replace("/", "")
            df_file.to_csv(path+"all_datasets_clean/"+file2, index = False, quoting=csv_.QUOTE_NONNUMERIC)
        except:
            broken_datasets = broken_datasets + 1
            datasets_notsaved.append(file2)
            print("I don't like this dataset so I skip it")
    
    with open("../all_datasets/datasets_with_errors.txt", "w") as outfile:
        outfile.write("\n".join(datasets_notsaved))

prepare_datasets("C:/Users/User/Desktop/TFG/all_datasets/")