overwrite = 0

init:
	python3 init_structure.py

scrape:
	make scrape_raw
	make scrape_submission
	make problem_diff

scrape_raw:
	python3 src/data/scrape_raw.py $(overwrite)

scrape_submission:
	python3 src/data/scrape_submission.py $(overwrite)

problem_diff:
	python3 src/data/problem_difficulty.py $(overwrite)