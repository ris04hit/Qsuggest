overwrite = 0

# Initializing directory structure
init:
	python3 init_structure.py

# Executing all steps
run:
	make scrape
	make preprocess_train


# Executing steps for scraping data
scrape:
	make scrape_raw
	make scrape_submission
	make scrape_rating

# Scraping raw data
scrape_raw:
	python3 src/data/scrape_raw.py $(overwrite)

# Scraping submission directory
scrape_submission:
	python3 src/data/scrape_submission.py $(overwrite)

# Scraping rating directory
scrape_rating:
	python3 src/data/scrape_rating.py $(overwrite)


# Preprocessing and training each model
preprocess_train:
	make problem_classify_model
	make up_prob_model

# Preprocessing and training for problem classification model
problem_classify_model:
	make problem_diff
	make impute_prob
	make problem_classify

# Preprocessing and training for user problem solve probability model
up_prob_model:
	make up_prob_data
	make up_prob_train


# Executing steps for processing data
process:
	make problem_diff
	make impute_prob
	make up_prob_data

# Calculating problem difficulties
problem_diff:
	python3 src/data/problem_difficulty.py $(overwrite)

# Imputing problem data
impute_prob:
	python3 src/data/impute_problem.py $(overwrite)

# Pre processing user problem probability data
up_prob_data:
	python3 src/data/user_problem_prob.py $(overwrite)


# Training all models
train:
	make problem_classify
	make up_prob_train

# Training model for problem classification
problem_classify:
	python3 src/models/problem_classify.py $(overwrite)

# Training model for user problem probability of solving
up_prob_train:
	python3 src/models/up_probability_model.py $(overwrite)


# Starting Server
run_server:
	python3 server/app.py