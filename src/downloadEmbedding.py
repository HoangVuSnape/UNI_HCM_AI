from transformers import AutoModel, AutoTokenizer

# Đường dẫn lưu trữ local
local_model_dir = "E:/LLM_clone/Tdtu-chatbot/modelEmbedding"

# Tải mô hình và tokenizer từ Hugging Face
tokenizer = AutoTokenizer.from_pretrained("VoVanPhuc/sup-SimCSE-VietNamese-phobert-base")
model = AutoModel.from_pretrained("VoVanPhuc/sup-SimCSE-VietNamese-phobert-base")

# Lưu mô hình và tokenizer về local
tokenizer.save_pretrained(local_model_dir)
model.save_pretrained(local_model_dir)

print(f"Model và tokenizer đã được lưu tại: {local_model_dir}")
