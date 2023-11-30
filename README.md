# **Qsuggest**  
Qsuggest is a tool designed to help users enhance their competitive programming skills by recommending suitable practice problems based on their history and performance.  

## **Initialization**
Before running any file/script/notebook execute in root directory: `make init`  
This will make sure the directory structure is correct.

## **Data Scraping**  
I have not uploaded the scraped data on git repo, but the scripts for scrapping the data is uploaded in [src/data](src/data/). You can run scripts individually or using Makefile. Just make sure to run any of two in root directory only.  
For scraping all the data execute:  `make scrape`  
For scraping only handles.csv execute: `make scrape_user`  
For scraping only problems.csv execute: `make scrape_problem`