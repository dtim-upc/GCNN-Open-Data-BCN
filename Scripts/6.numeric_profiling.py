import pandas as pd
import os
import csv
import numpy as np
import csv as csv_

#Function that computes the profiles of the numeric attributes of a dataset. 
# Output: csv with columns: Datasetname, attribute names, count, mean, std, 25%, 50%, 75% (percentiles), min, max

def num_profiling(path):
    ds_names = [file for file in os.listdir(path) if file.endswith('.csv')]
    os.mkdir("../Numeric_profiles")

    non_numeric_files = []
    for dir in ds_names:
        try:
            file = pd.read_csv(path+dir, index_col= False)
            file = file.select_dtypes(['number'])

            describe_prof = file.describe().transpose()
            num_prof = pd.DataFrame()

            num_prof['Dataset_name'] = np.resize(dir,len(file.columns))
            num_prof['Attribute_name'] = file.columns

            num_prof = pd.merge(num_prof,describe_prof, left_on='Attribute_name', right_on = describe_prof.index)
            prof_name = dir.replace(".csv","_num_profile.csv")
            num_prof.to_csv("../Numeric_profiles/"+prof_name, index=False)
        except:
            non_numeric_files.append(dir)
    
    with open("../Error_files/non_numeric_datasets.txt", "w") as outfile:
        outfile.write("\n".join(non_numeric_files))


#Aggregates numeric profiles by computing the mean and the std of each attribute profile. 
#Reunites all aggregated profiles in a single .csv file called aggregated_numeric_profiles.csv
def aggregate_num(path):
    first = True
    aggregated_num_prof = pd.DataFrame()

    for dir in os.listdir(path):
        df_profile = pd.read_csv(path+dir, index_col= False)
        df_profile.drop('Attribute_name', axis = 1, inplace = True)
        
        #Aggregate numeric meta features
        if(first):
            aggregated_num_prof = pd.DataFrame(df_profile.groupby('Dataset_name', as_index = True).agg(['mean', np.std]))
            first = False

        else:
            aggregated_profile = pd.DataFrame(df_profile.groupby('Dataset_name', as_index = True).agg(['mean', np.std]))
            aggregated_num_prof = pd.concat([aggregated_num_prof,aggregated_profile])
            
    aggregated_num_prof.columns = ["_".join(x) for x in aggregated_num_prof.columns.ravel()]
    aggregated_num_prof["Dataset_name"] = aggregated_num_prof.index
    aggregated_num_prof = aggregated_num_prof.fillna(0)
    
    aggregated_num_prof.to_csv("../Numeric_profiles/aggregated_numeric_profiles.csv", index = False)

            
#num_profiling("C:/Users/User/Desktop/TFG/all_datasets/all_datasets_clean/")
aggregate_num("C:/Users/User/Desktop/TFG/Numeric_profiles/")