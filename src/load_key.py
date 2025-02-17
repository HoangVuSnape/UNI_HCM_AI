from dotenv import load_dotenv
import os
from pathlib import Path
from google.oauth2 import service_account
class EnvLoader:
    def __init__(self, env_path="../.env", credentials_path="../creadientials_vertex.json"):
        self.env_path = env_path
        self.credentials_path = credentials_path
        self.credentials = self.load_credentials()
        self.keys = {}

    def load_credentials(self):
        """Load Google service account credentials."""
        self.credentials = service_account.Credentials.from_service_account_file(self.credentials_path)
        # print("Google service account credentials loaded.")

    def load_env(self):
        """Load environment variables from the specified .env file."""
        load_dotenv(Path(self.env_path), override=True)
        # print(f"Environment variables loaded from {self.env_path}.")

    def retrieve_keys(self):
        """Retrieve API keys from environment variables."""
        self.keys = {
            'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
            'QDRANT_API': os.getenv('QDRANT_API'),
            'QDRANT_API_2': os.getenv('QDRANT_API_2'),
            
            'QDRANT_URL': os.getenv('QDRANT_URL'),
            'QDRANT_URL_2': os.getenv('QDRANT_URL_2'),
            'GROQ_API_KEY': os.getenv('GROQ_API_KEY'),
            'GOOGLE_API_KEY': os.getenv('GOOGLE_API_KEY'),
            'TAVILY_API_KEY': os.getenv('TAVILY_API_KEY'),
        }

    def check_keys(self):
        """Check and print the status of each API key."""
        for key, value in self.keys.items():
            if not value:
                print(f"{key} is missing.")

    def load_all(self):
        """Load all necessary configurations: credentials and environment variables."""
        self.load_credentials()
        self.load_env()
        self.retrieve_keys()
        self.check_keys()

# Usage example
if __name__ == "__main__":
    env_loader = EnvLoader()
    env_loader.load_all()
