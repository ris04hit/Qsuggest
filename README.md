# **Qsuggest**  
Qsuggest is a tool designed to help users enhance their competitive programming skills by recommending suitable practice problems based on their history and performance.  

## **Initialization**
Before running any file/script/notebook execute in root directory: `make init`  
This will make sure the directory structure is correct.

## **Changing Directory Structure**
For changing directory structure, folder and file destination addresses need to be changed in [init_structure.py](init_structure.py) and [src/utils/address_utils.py](src/utils/address_utils.py). Also import locations in every file needs to be changed depending upon the new directory structure. Addresses need to be explicitly changed in notebooks.

## **Data Scraping**  
Scraped data is uploaded in [data/scraped](data/scraped/) (data in [data/scraped/submission](data/scraped/submission/) is not uploaded due to its large size) and the scripts for scrapping the data is uploaded in [src/data](src/data/). You can run scripts individually or using Makefile. Just make sure to run it in root directory only.  
By default any data scraped will not overwrite existing data. For overwriting set overwrite=1 in make command. For example to scrape all data and to overwrite it over existing data (if any) execute: `make scrape overwrite=1`  
### **Commands**
For scraping all the data execute:  `make scrape`  


For scraping each file individually, run following commands in given order only (so that there is no data inconsistency):  
For scraping only [handles.csv](data/scraped/handles.csv)/[problems.csv](data/scraped/problems.csv)/[tags.csv](data/scraped/tags.csv) execute: `make scrape_raw`  
For scraping [sumbissions](data/scraped/submission) execute: `make scrape_submission`  
