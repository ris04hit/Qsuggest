class Log:
    def __init__(self, prefix = 'log/', suffix = '') :
        self.prefix = prefix
        self.suffix = suffix
        self.scrape_raw = f'{self.prefix}scrape_raw.log{self.suffix}'
        self.scrape_submission = f'{self.prefix}scrape_submission.log{self.suffix}'
        self.problem_diff = f'{self.prefix}problem_difficulty.log{self.suffix}'
        # self.knn_probem_diff = f'{self.prefix}knn_problem_difficulty.log{self.suffix}'

class Data:
    def __init__(self, prefix = 'data/', suffix = ''):
        self.prefix = prefix
        self.suffix = suffix
        self.handles = f'{self.prefix}scraped/handles.csv{self.suffix}'
        self.problems = f'{self.prefix}scraped/problems.csv{self.suffix}'
        self.tags = f'{self.prefix}scraped/tags.csv{self.suffix}'
        self.submission_dir = f'{self.prefix}scraped/submission/'
        self.problem_diff = f'{self.prefix}interim/problem_difficulty.csv{self.suffix}'
        self.temp_dir = f'{self.prefix}temp/'
        self.imputed_prob = f'{self.prefix}processed/imputed_problem.npy{self.suffix}'
    
    def submission(self, handle, prefix = ''):
        return f'{prefix}{self.submission_dir}{handle}.csv{self.suffix}'
    
    def temp(self, filename, prefix = ''):
        return f'{prefix}{self.temp_dir}{filename}{self.suffix}'

class Src:
    def __init__(self, prefix = 'src/', suffix = ''):
        self.prefix = prefix
        self.suffix = suffix
        self.scrape_raw = f'{self.prefix}data/scrape_raw.py{self.suffix}'
        self.scrape_submission = f'{self.prefix}data/scrape_submission.py{self.suffix}'
        self.problem_diff = f'{self.prefix}data/problem_difficulty.py{self.suffix}'
        # self.knn_problem_diff = f'{self.prefix}models/knn_problem_difficulty.py{self.suffix}'

class Model:
    def __init__(self, prefix = 'models/', suffix = ''):
        self.prefix = prefix
        self.suffix = suffix
        self.prob_classify = f'{self.prefix}problem_classify.pkl{self.suffix}'
        # self.knn_probem_diff = f'{self.prefix}knn_problem_diff.npy{self.suffix}'

class Address:
    def __init__(self, prefix = '', suffix = ''):
        self.prefix = prefix
        self.suffix = suffix
        self.data = Data(prefix + 'data/', suffix)
        self.log = Log(prefix + 'log/', suffix)
        self.src = Src(prefix + 'src/', suffix)
        self.model = Model(prefix + 'models/', suffix)
    
address = Address()     # For general purpose, calling it from root directory