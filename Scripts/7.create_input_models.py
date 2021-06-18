import pandas as pd
import os
import csv
import numpy as np
import json

def aggregate(path):
    first = True
    aggregated_profiles = pd.DataFrame()
    id = 0
    profile_not_aggr = []
    broken_profiles = 0

    ds_class = 0

    for dire in os.listdir(path):

        dire_class = dire[0]
        try:
                profile_name = [file for file in os.listdir(path+dire) if file.endswith('.csv')][0]
                df_profile = pd.read_csv(path+dire+'/'+profile_name, index_col= False)
                if (df_profile.shape[0] == 0):
                    continue

                #Apply One-Hot-Encoding to non-numeric variables and add them to profile
                dummy_dataType = pd.get_dummies(df_profile.dataType, prefix = 'datatype')
                dummy_dataType = dummy_dataType.rename(columns=str.lower)
                dummy_specificType = pd.get_dummies(df_profile.specificType, prefix = 'specifictype')
                dummy_specificType = dummy_specificType.rename(columns=str.lower)
                
                df_profile = pd.concat([df_profile, dummy_dataType,dummy_specificType], join = "inner", axis = 1)
                
                #Erase unwanted MF of profile
                df_profile = df_profile.drop(columns = ['Attribute_name', 'dataType', 'specificType'])
                
                #Aggregate MF
                if(first):
                    aggregated_profiles = pd.DataFrame(df_profile.groupby('Dataset_name', as_index = False).agg(['mean', np.std]))
                    first = False

                else:
                    aggregated_profile = pd.DataFrame(df_profile.groupby('Dataset_name', as_index = False).agg(['mean', np.std]))
                    aggregated_profiles = pd.concat([aggregated_profiles,aggregated_profile])
        except:
                broken_profiles = broken_profiles + 1
                profile_not_aggr.append(dire)
                print("I don't like this profile so I skip it")
    #aggregated_profiles = aggregated_profiles.drop(columns='Dataset_name')

    #Separate mean and std columns, filling empty columns droping index and adding dataset_name as a column
    aggregated_profiles.columns = ["_".join(x) for x in aggregated_profiles.columns.ravel()]
    aggregated_profiles["Dataset_name"] = aggregated_profiles.index
    aggregated_profiles.reset_index(drop=True, inplace=True)
    aggregated_profiles = aggregated_profiles.fillna(0)

    #Insert all possible dummy categories to have profiles of the same size
    dummies_list = ['datatype_alphabetic_mean','datatype_numeric_mean', 'datatype_alphanumeric_mean', 'datatype_nonalphanumeric_mean', 'datatype_datetime_mean', 
                    'datatype_isnull_mean', 'specifictype_other_mean', 'specifictype_otherst_mean','specifictype_space_mean','specifictype_email_mean',
                    'specifictype_ip_mean','specifictype_phone_mean','specifictype_url_mean','specifictype_username_mean','specifictype_phrases_mean',
                    'specifictype_general_mean','specifictype_date_mean','specifictype_time_mean','specifictype_datetime_mean', 'specifictype_isnull_mean']

    for attr in dummies_list:
        attr_std = attr.replace('_mean','_std')
        if (attr not in aggregated_profiles):
            aggregated_profiles[attr] = 0
            aggregated_profiles[attr_std] = 0

    #Reorder columns alphabetycally
    aggregated_profiles = aggregated_profiles.reindex(sorted(aggregated_profiles.columns), axis=1)
    #Merging with numeric profiles
    num_prof = pd.read_csv("../Numeric_profiles/aggregated_numeric_profiles.csv", index_col = False)

    profiles_agg = pd.merge(aggregated_profiles, num_prof, how = 'left', on = 'Dataset_name', suffixes = ('_categorical','_numeric')).fillna(0)

    profiles_agg['Class'] = profiles_agg['Dataset_name'].str[:1]
    #profiles_agg.drop('Dataset_name', axis=1, inplace=True)

    #Saving profiles and maps of datasets
    profiles_agg.rename(columns=str.lower, inplace=True)

    profiles_agg.to_csv("C:/Users/User/Desktop/TFG/Input models/agg_profiles_2.csv", index = False)

    with open("../Error_files/profiles_with_errors.txt", "w") as outfile:
        outfile.write("\n".join(profile_not_aggr))

def split_test_train(path):
    profiles = pd.read_csv(path, index_col= False)
    idx_test = [0,3,7,8,13,23,26,33,41,42,48,50,52,67,68, 75,83,88,89,93,96,104,116,117,114,129,131,133,141,142,144,146,158,164, 169,175, 182,184,185,194,198,208,212,213,218,219,220,238,240,242,248,256,258,262, 263,272,281,282,285,294,296,304,311,315]
    profiles_test = profiles.iloc[idx_test,:].reset_index()
    profiles_train = profiles.drop(profiles.index[idx_test]).reset_index()
    
    map_datasets_train = {}
    map_datasets_test = {}

    for idx, row in profiles_train.iterrows():
        map_datasets_train[idx] = row['dataset_name']
    
    n = len(profiles_train)

    for idx, row in profiles_test.iterrows():
        map_datasets_test[idx+n] = row['dataset_name']

    profiles_test.drop('dataset_name', axis=1, inplace=True)
    profiles_test.drop("index", axis=1, inplace=True)
    profiles_train.drop('dataset_name', axis=1, inplace=True)
    profiles_train.drop("index", axis=1, inplace=True)

    profiles_test.to_csv("C:/Users/User/Desktop/TFG/Input models/agg_profiles_test.csv", index = False)
    profiles_train.to_csv("C:/Users/User/Desktop/TFG/Input models/agg_profiles_train.csv", index = False)

    with open("C:/Users/User/Desktop/TFG/Input models/map_datasets_train.json", "w", encoding= 'utf8') as outfile:  
        json.dump(map_datasets_train, outfile, ensure_ascii= False)
    
    with open("C:/Users/User/Desktop/TFG/Input models/map_datasets_test.json", "w", encoding= 'utf8') as outfile:  
        json.dump(map_datasets_test, outfile, ensure_ascii= False)

def create_edge_matrix(path):
    
    with open(path, encoding='utf8') as json_file: 
        ds_dict = json.load(json_file)
    
    adj_map = {}

    for node_1 in ds_dict.keys():
        node1_adj = []
        for node_2 in ds_dict.keys():
            if (ds_dict[node_1][0] == ds_dict[node_2][0]):
                node1_adj.append(node_2)
            
        adj_map[node_1] = node1_adj

    with open("C:/Users/User/Desktop/TFG/Input models/map_of_edges_train.json", "w", encoding='utf8') as outfile:  
        json.dump(adj_map, outfile, ensure_ascii= False) 

        
#aggregate("C:/Users/User/Desktop/TFG/Profiles_all/")
split_test_train("C:/Users/User/Desktop/TFG/Input models/agg_profiles.csv")
create_edge_matrix("C:/Users/User/Desktop/TFG/Input models/map_datasets_train.json")






















