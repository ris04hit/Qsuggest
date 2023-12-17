# **Qsuggest**  
Qsuggest is a tool designed to help users enhance their competitive programming skills by recommending suitable practice problems based on their history and performance.  

## **Initialization**
Before running any file/script/notebook execute in root directory: `make init`  
This will make sure the directory structure is correct.

## **Changing Directory Structure**
For changing directory structure, folder and file destination addresses need to be changed in [init_structure.py](init_structure.py) and [src/utils/address_utils.py](src/utils/address_utils.py). Also import locations in every file needs to be changed depending upon the new directory structure.

## **Pre Processing for Chrome Extension**
Before creating the extension, data needs to be scraped from [codeforces](www.codeforces.com), processed and different machine learning models need to be trained over the processed data.  
To perform all these action, execute: `make run`  
By default it will not overwrite any existing data or trained model. To overwrite, all of the existing data and models, execute: `make run overwrite=1`  


For performing each of these steps individually, read the sections following this section.

## **Data Scraping**  
Scraped data is uploaded in [data/scraped](data/scraped/) (data in [data/scraped/submission](data/scraped/submission/) is not uploaded due to its large size) and the scripts for scrapping the data is uploaded in [src/data](src/data/). You can run scripts individually or using Makefile. Just make sure to run it in root directory only.  
By default any data scraped will not overwrite existing data. For overwriting, set overwrite=1 in make command. For example to scrape all data and to overwrite it over existing data (if any) execute: `make scrape overwrite=1`  
### **Commands**
For scraping all the data, execute:  `make scrape`  


For scraping each file individually, run following commands in given order only (so that there is no data inconsistency):  
For scraping only [handles.csv](data/scraped/handles.csv)/[problems.csv](data/scraped/problems.csv)/[tags.csv](data/scraped/tags.csv), execute: `make scrape_raw`  
For scraping [sumbissions](data/scraped/submission), execute: `make scrape_submission`  

## **Data Processing**
Data which is processed from the scraped data but can not be directly used for model training is saved in [data/interim](data/interim). On the other hand, data which is processed and can be directly used for model training is saved in [data/processed](data/processed). Scripts for processing data are stored in [src/data](src/data).  
By default any processed data will not overwrite existing data. For overwriting, set overwrite=1 in make command. For example to process all data and to overwrite it over existing data (if any) execute: `make process overwrite=1`

### **Commands**
To process all the data, execute: `make process`  


For processing each file individually, run following commands in given order only (so that there is no data inconsistency):  
To create [data/interim/problem_difficulty.csv](data/interim/problem_difficulty.csv), execute: `make problem_diff`  
To create [data/processed/imputed_problem.npy](data/processed/imputed_problem.csv), execute: `make imputed_prob`

## **Training Models**
Data which is used to directly train the model is stored in [data/processed](data/processed/). Models are saved in [models](models/). Most of the data in [data/processed](data/processed/) is created directly by preprocessing of model without using any separate script. Scripts for training model are stored in [src/models](src/models/).  
By default training of model will not overwrite any of the preprocessed data and trained model. For overwriting, set overwrite=1 in make command. For example to train all models and to overwrite it over exisiting data (if any) execute: `make train overwrite=1`

### **Commands**
To train all the models, execute: `make train`  

