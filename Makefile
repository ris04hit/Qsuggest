init:
	python3 init_structure.py

scrape:
	make scrape_user
	make scrape_problem

scrape_user:
	python3 src/data/scrape_data.py user

scrape_problem:
	python3 src/data/scrape_data.py problem