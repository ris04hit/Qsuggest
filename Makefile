init:
	python3 init_structure.py

scrape:
	make scrape_raw

scrape_raw:
	python3 src/data/scrape_raw.py
