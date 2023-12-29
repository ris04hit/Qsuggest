import os


class Log:
    def __init__(self, prefix = 'logs/', suffix = '') :
        self.prefix = prefix
        self.suffix = suffix
        
        self.scrape_raw = os.path.join(self.prefix, f'scrape_raw.log{self.suffix}')
        self.scrape_submission = os.path.join(self.prefix, f'scrape_submission.log{self.suffix}')
        self.scrape_rating = os.path.join(self.prefix, f'scrape_rating.log{self.suffix}')
        self.problem_diff = os.path.join(self.prefix, f'problem_difficulty.log{self.suffix}')
        self.user_problem = os.path.join(self.prefix, f'user_problem.log{self.suffix}')
        self.up_train = os.path.join(self.prefix, f'up_train.log{self.suffix}')


class Data:
    def __init__(self, prefix = 'data/', suffix = ''):
        self.prefix = prefix
        self.suffix = suffix
        
        self.temp_dir = os.path.join(self.prefix, f'temp/')
        
        self.handles = os.path.join(self.prefix, f'scraped/handles.csv{self.suffix}')
        self.problems = os.path.join(self.prefix, f'scraped/problems.csv{self.suffix}')
        self.tags = os.path.join(self.prefix, f'scraped/tags.csv{self.suffix}')
        self.submission_dir = os.path.join(self.prefix, f'scraped/submission/')
        self.rating_dir = os.path.join(self.prefix, f'scraped/rating/')
        
        self.problem_diff = os.path.join(self.prefix, f'interim/problem_difficulty.csv{self.suffix}')
        
        self.imputed_prob = os.path.join(self.prefix, f'processed/imputed_problem.npy{self.suffix}')
        self.problem_class = os.path.join(self.prefix, f'processed/problem_class.npy{self.suffix}')
        self.user_problem_dir = os.path.join(self.prefix, f'processed/user_problem')
        self.user_problem_stat = os.path.join(self.prefix, f'processed/user_problem_stat.npz{self.suffix}')
    
    def submission(self, handle, prefix = ''):
        return os.path.join(prefix, self.submission_dir, f'{handle}.csv{self.suffix}')
    
    def rating(self, handle, prefix = ''):
        return os.path.join(prefix, self.rating_dir, f'{handle}.csv{self.suffix}')
    
    def temp(self, filename, prefix = ''):
        return os.path.join(prefix, self.temp_dir, f'{filename}{self.suffix}')
    
    def user_problem(self, chunk_ind, prefix = ''):
        return os.path.join(prefix, self.user_problem_dir, f'{chunk_ind}.npz{self.suffix}')


class Src:
    def __init__(self, prefix = 'src/', suffix = ''):
        self.prefix = prefix
        self.suffix = suffix
        
        self.scrape_raw = os.path.join(self.prefix, f'data/scrape_raw.py{self.suffix}')
        self.scrape_submission = os.path.join(self.prefix, f'data/scrape_submission.py{self.suffix}')
        self.scrape_rating = os.path.join(self.prefix, f'data/scrape_rating.py{self.suffix}')
        self.problem_diff = os.path.join(self.prefix, f'data/problem_difficulty.py{self.suffix}')
        self.impute_problem = os.path.join(self.prefix, f'data/impute_problem.py{self.suffix}')
        self.user_problem_prob = os.path.join(self.prefix, f'data/user_problem_prob.py{self.suffix}')
        
        self.problem_classify = os.path.join(self.prefix, f'models/problem_classify.py{self.suffix}')
        self.up_prob_model = os.path.join(self.prefix, f'models/up_probability_model.py{self.suffix}')
        self.problem_insert = os.path.join(self.prefix, f'models/problem_insert.py{self.suffix}')
        
        self.address_utils = os.path.join(self.prefix, f'utils/address_utils.py{self.suffix}')
        self.data_process_utils = os.path.join(self.prefix, f'utils/data_process_utils.py{self.suffix}')
        self.model_utils = os.path.join(self.prefix, f'utils/model_utils.py{self.suffix}')
        self.scrape_utils = os.path.join(self.prefix, f'utils/scrape_utils.py{self.suffix}')
        self.predictor_util = os.path.join(self.prefix, f'utils/predictor_util.py{self.suffix}')


class Model:
    def __init__(self, prefix = 'models/', suffix = ''):
        self.prefix = prefix
        self.suffix = suffix
        
        self.prob_classify = os.path.join(self.prefix, f'problem_classify.pkl{self.suffix}')
        self.user_problem = os.path.join(self.prefix, f'user_problem.pt{self.suffix}')
        self.problem_insert = os.path.join(self.prefix, f'problem_inserter.pkl{self.suffix}')


class Address:
    def __init__(self, prefix = '', suffix = ''):
        self.prefix = prefix
        self.suffix = suffix
        
        self.data = Data(os.path.join(prefix, 'data/'), suffix)
        self.log = Log(os.path.join(prefix, 'logs/'), suffix)
        self.src = Src(os.path.join(prefix, 'src/'), suffix)
        self.model = Model(os.path.join(prefix, 'models/'), suffix)
    
address = Address()     # For general purpose, calling it from root directory