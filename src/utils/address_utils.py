class Log:
    def __init__(self, prefix = '', suffix = '') :
        self.prefix = prefix
        self.suffix = suffix
        self.scrape_raw = f'{self.prefix}logs/scrape_raw.log{self.suffix}'
        self.scrape_submission = f'{self.prefix}logs/scrape_submission.log{self.suffix}'
        self.problem_diff = f'{self.prefix}logs/problem_difficulty.log{self.suffix}'

class Data:
    def __init__(self, prefix = '', suffix = ''):
        self.prefix = prefix
        self.suffix = suffix
        self.handles = f'{self.prefix}data/scraped/handles.csv{self.suffix}'
        self.problems = f'{self.prefix}data/scraped/problems.csv{self.suffix}'
        self.tags = f'{self.prefix}data/scraped/tags.csv{self.suffix}'
        self.submission_dir = f'{self.prefix}data/scraped/submission/'
        self.problem_diff = f'{self.prefix}data/interim/problem_difficulty.csv{self.suffix}'
    
    def submission(self, handle, prefix = ''):
        return f'{prefix}{self.submission_dir}{handle}.csv{self.suffix}'

class Src:
    def __init__(self, prefix = '', suffix = ''):
        self.prefix = prefix
        self.suffix = suffix
        self.scrape_raw = f'{self.prefix}src/data/scrape_raw.py{self.suffix}'
        self.scrape_submission = f'{self.prefix}src/data/scrape_submission.py{self.suffix}'

class Address:
    def __init__(self, prefix = '', suffix = ''):
        self.prefix = prefix
        self.suffix = suffix
        self.data = Data(prefix, suffix)
        self.log = Log(prefix, suffix)
        self.src = Src(prefix, suffix)
    
address = Address()     # For general purpose, calling it from root directory