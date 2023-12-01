# **Qsuggest**  
Qsuggest is a tool designed to help users enhance their competitive programming skills by recommending suitable practice problems based on their history and performance.  

## **Initialization**
Before running any file/script/notebook execute in root directory: `make init`  
This will make sure the directory structure is correct.

## **Data Scraping**  
Scraped data is uploaded in [data/scraped](data/scraped/) and the scripts for scrapping the data is uploaded in [src/data](src/data/). You can run scripts individually or using Makefile. Just make sure to run it in root directory only.  
For scraping all the data execute:  `make scrape`  
For scraping only handles.csv/problems.csv/tags.csv execute: `make scrape_raw`  