overwrite = 0

init:
	python3 init_structure.py

run:
	make scrape
	make process
#	make train

scrape:
	make scrape_raw
	make scrape_submission

scrape_raw:
	python3 src/data/scrape_raw.py $(overwrite)

scrape_submission:
	python3 src/data/scrape_submission.py $(overwrite)

process:
	make problem_diff
	make impute_prob

problem_diff:
	python3 src/data/problem_difficulty.py $(overwrite)

impute_prob:
	python3 src/data/impute_problem.py $(overwrite)

# train:
# 	make knn_problem_diff

# knn_problem_diff:
# 	python3 src/models/knn_problem_difficulty.py $(overwrite)