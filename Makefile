overwrite = 0

# Initializing directory structure
init:
	python3 init_structure.py

# Executing all steps
run:
	make scrape
	make process
	make train


# Executing steps for scraping data
scrape:
	make scrape_raw
	make scrape_submission

# Scraping raw data
scrape_raw:
	python3 src/data/scrape_raw.py $(overwrite)

# Scraping submission directory
scrape_submission:
	python3 src/data/scrape_submission.py $(overwrite)


# Executing steps for processing data
process:
	make problem_diff
	make impute_prob

# Calculating problem difficulties
problem_diff:
	python3 src/data/problem_difficulty.py $(overwrite)

# Imputing problem data
impute_prob:
	python3 src/data/impute_problem.py $(overwrite)


# Training all models
train:
	make problem_classify

# Training model for problem classification
problem_classify:
	python3 src/models/problem_classify.py $(overwrite)