import os

# Define the folder structure
folders = [
    'data/raw',
    'data/processed',
    'src',
    'models',
    'notebooks',
    'tests',
    'config',
    'logs'
]

# Create each folder in the list
for folder in folders:
    os.makedirs(folder, exist_ok=True)  # `exist_ok=True` avoids error if folder already exists

# Create key files (empty for now)
files = [
    'data/intents.json',
    'src/chatbot.py',
    'src/preprocess.py',
    'src/model.py',
    'src/utils.py',
    'tests/test_chatbot.py',
    'config/config.yaml',
    'logs/training.log',
    'README.md',
    'requirements.txt',
    '.gitignore'
]

# Create each file
for file in files:
    with open(file, 'w') as f:
        pass  # This creates an empty file

print("Folder structure and files have been created successfully!")
