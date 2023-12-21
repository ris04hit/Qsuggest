import os


class Log:
    def __init__(self, prefix = 'log/', suffix = '') :
        self.prefix = prefix
        self.suffix = suffix
        
        self.scrape_raw = os.path.join(self.prefix, f'scrape_raw.log{self.suffix}')
        self.scrape_submission = os.path.join(self.prefix, f'scrape_submission.log{self.suffix}')
        self.problem_diff = os.path.join(self.prefix, f'problem_difficulty.log{self.suffix}')
        # self.knn_probem_diff = os.path.join(self.prefix, f'knn_problem_difficulty.log{self.suffix}')


class Data:
    def __init__(self, prefix = 'data/', suffix = ''):
        self.prefix = prefix
        self.suffix = suffix
        
        self.handles = os.path.join(self.prefix, f'scraped/handles.csv{self.suffix}')
        self.problems = os.path.join(self.prefix, f'scraped/problems.csv{self.suffix}')
        self.tags = os.path.join(self.prefix, f'scraped/tags.csv{self.suffix}')
        self.submission_dir = os.path.join(self.prefix, f'scraped/submission/')
        
        self.problem_diff = os.path.join(self.prefix, f'interim/problem_difficulty.csv{self.suffix}')
        
        self.temp_dir = os.path.join(self.prefix, f'temp/')
        
        self.imputed_prob = os.path.join(self.prefix, f'processed/imputed_problem.npy{self.suffix}')
        self.problem_class = os.path.join(self.prefix, f'processed/problem_class.npy{self.suffix}')
    
    def submission(self, handle, prefix = ''):
        return os.path.join(prefix, self.submission_dir, f'{handle}.csv{self.suffix}')
    
    def temp(self, filename, prefix = ''):
        return os.path.join(prefix, self.temp_dir, f'{filename}{self.suffix}')


class Src:
    def __init__(self, prefix = 'src/', suffix = ''):
        self.prefix = prefix
        self.suffix = suffix
        
        self.scrape_raw = os.path.join(self.prefix, f'data/scrape_raw.py{self.suffix}')
        self.scrape_submission = os.path.join(self.prefix, f'data/scrape_submission.py{self.suffix}')
        self.problem_diff = os.path.join(self.prefix, f'data/problem_difficulty.py{self.suffix}')
        # self.knn_problem_diff = os.path.join(self.prefix, f'models/knn_problem_difficulty.py{self.suffix}')


class Model:
    def __init__(self, prefix = 'models/', suffix = ''):
        self.prefix = prefix
        self.suffix = suffix
        
        self.prob_classify = os.path.join(self.prefix, f'problem_classify.pkl{self.suffix}')
        # self.knn_probem_diff = os.path.join(self.prefix, f'knn_problem_diff.npy{self.suffix}')


class Address:
    def __init__(self, prefix = '', suffix = ''):
        self.prefix = prefix
        self.suffix = suffix
        
        self.data = Data(os.path.join(prefix, 'data/'), suffix)
        self.log = Log(os.path.join(prefix, 'log/'), suffix)
        self.src = Src(os.path.join(prefix, 'src/'), suffix)
        self.model = Model(os.path.join(prefix, 'models/'), suffix)
    
address = Address()     # For general purpose, calling it from root directory