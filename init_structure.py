import os

def create_directory(directory_path):
    # Check if the directory exists
    if not os.path.exists(directory_path):
        # Create the directory
        os.makedirs(directory_path)
        
create_directory('chrome_extensions')
create_directory('data')
create_directory('data/interim')
create_directory('data/scraped')
create_directory('includes')
create_directory('logs')
create_directory('models')
create_directory('notebooks')
create_directory('src')
create_directory('src/data')
create_directory('src/models')
create_directory('src/utils')
