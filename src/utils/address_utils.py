class Log:
    def __init__(self) :
        self.scrape_raw = 'logs/scrape_raw.log'
        self.scrape_submission = 'logs/scrape_submission.log'

class Data:
    def __init__(self):
        self.handles = 'data/scraped/handles.csv'
        self.problems = 'data/scraped/problems.csv'
        self.tags = 'data/scraped/tags.csv'
        self.submission_dir = 'data/scraped/submission/'
    
    def submission(self, handle):
        return f'{self.submission_dir}{handle}.csv'

class Src:
    def __init__(self):
        self.scrape_raw = 'src/data/scrape_raw.py'
        self.scrape_submission = 'src/data/scrape_submission.py'

class Address:
    def __init__(self):
        self.data = Data()
        self.log = Log()
        self.src = Src()
    
address = Address()