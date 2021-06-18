import pandas as pd
import os
import csv
import numpy as np
import csv as csv_

def create_csv(path):
    ds_names = os.listdir(path)
    n = len(ds_names)
    df = pd.DataFrame(columns = ['filename', 'delimiter', 'multiline', 'file', 'file_size', 'ignoreTrailing', 'source'])
    delimiter = []
    file_size = []
    source = []
    
    for file in ds_names:
        with open(path+file, 'r', encoding = "cp437") as csvfile:
            delim = csv.Sniffer().sniff(csvfile.readline()).delimiter
            if (delim not in [',', ';', '|', '/']):
                delim = ','
            #delim = '"'+delim+'"'
            delimiter.append(delim)
        file_size.append(max(round(os.path.getsize(path+file) / 1000),1))
        source.append(path+file)

    df['filename'] = ds_names
    df['delimiter'] = delimiter
    df['multiline'] = False
    df['file'] = 'csv'
    df['file_size'] = file_size
    df['ignoreTrailing'] = True
    df['source'] = source

    df.to_csv('C:/Users/User/Desktop/TFG/information_csv_all_datasets.csv', index = False)
    print("Done!")


create_csv("C:/Users/User/Desktop/TFG/all_datasets/all_datasets_clean/")
