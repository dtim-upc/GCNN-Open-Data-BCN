# GCNN-Open-Data-BCN

This repository contains the following:

## Scripts

This folder contains the scripts used to extract and clean Open Data BCN's datasets. It also contains the profiling and model preparation pipeline. 
    
- 1.scraper.py: Extracts datasets from the Open Data BCN's website.
    
- 2.rename_datasets.py: Renames datasets to include their class labels.
    
- 3.clean_datasets.py: Cleans the datasets so they are compatible with the pofiling tool.
    
- 4.create_information_csv.py: Create a file with necessary information about the datasets in order to create their profiles.
    
- 5.profiling.scala: Creates profiles of the nominal attributes of the datasets. In order to use this code NextiaJD jars should be downloaded at: https://github.com/dtim-upc/NextiaJD2.
    
- 6.numeric_profiling.py: Creates profiles of the numeric attributes of the datasets.
    
- 7.create_input_models.py: Prepares training and tests sets and a map of the edges we need to create the input graph for the GCNN method.

## Data

This folder contains the datasets extracted from the Open Data BCN portal (using code 1.scraper.py) after the cleaning step (scripts 2.rename_datasets.py and 3.clean_datasets.py). For storage reasons, Git does not allow to upload files heavier than 25MB, which is why, a few datasets could not be uploaded. The datasets are separated in folders denoting thematic areas exactly in the same way as we can find them in Barcelona's website.


## Input for Models

This folder hosts the files returned by the code 7.create_input_models.py, which are the ones required to train and test the models. It contains:

- agg_profiles_train.csv & agg_profiles_test.csv: Profiles of the datasets used to train and test the models respectively.

- map_datasets_train.JSON & map_datasets_test.JSON: Dictionary to identify which profile corresponds to which dataset in both the train and the test files.

- map_of_edges_train.JSON: Adjacency matrix of the train set to construct the input graph for the GCNN model.

## Models

This folder contains the python notebook hosting the models implemented.

- Simpler_models_class_prediction.ipynb: Contains models: Logistic Regression, Random Forest, Support Vector Machines, Multi-Layer Perceptron. 

- GCNN_Class_Prediction.ipynb: Contains the GCNN approach (Link predcition). 

- model_class_prediction_final.pt: Final model chosen which provides our best results.

## Reproducing the models results

If you want to reproduce the results you need to download the files of *Input models* folder and locate them in a google drive folder. Download the notebooks which you are interested in reproduce the results and also store it in the same google drive folder as the other files. Replace the paths of the input data of the notebooks by the path of your google drive folder. Then, simply run the notebooks. 
