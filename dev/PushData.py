from datasets import Dataset
import pandas as pd
from huggingface_hub import HfApi, HfFolder
import json

# Đường dẫn file Excel và credentials
file_path = r"E:\LLM_clone\Tdtu-chatbot\notebooks\data_finetune\Donedata\Done.xlsx"
credentials_path = r"E:\LLM_clone\Tdtu-chatbot\credentials.json"

# Load credentials
with open(credentials_path, "r") as f:
    credentials = json.load(f)

# Đăng nhập vào Hugging Face
hf_token = credentials["Huggingface"]
HfFolder.save_token(hf_token)

# Load dữ liệu từ file Excel
df = pd.read_excel(file_path)
print("Preview Dataset:")
print(df.head())

# Chuyển đổi DataFrame sang Dataset
dataset = Dataset.from_pandas(df)

# Đặt tên repository
repo_name = "HoangVuSnape/TDTU_QA_v1"

# Push dataset lên Hugging Face
dataset.push_to_hub(repo_name, token=hf_token)

print(f"Dataset uploaded successfully to: https://huggingface.co/datasets/{repo_name}")
