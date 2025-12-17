import os

# Define the paths you are trying to load
model_path = 'models/gold_price_model.pkl'
data_path = 'data/gold_price_data.csv'

def check_path(path):
    print(f"Checking: {path}...")
    if not os.path.exists(path):
        print(f"❌ DOES NOT EXIST. Current working dir is: {os.getcwd()}")
        return
    
    if os.path.isdir(path):
        print("❌ ERROR: This is a FOLDER, not a file! Delete this folder and re-save your model.")
    elif os.path.isfile(path):
        print("✅ Found file.")
        try:
            with open(path, 'rb') as f:
                print("✅ Permission Check: Can read file successfully.")
        except Exception as e:
            print(f"❌ PERMISSION ERROR: {e}")
            print("👉 Fix: Close any programs (like Excel) using this file or check user permissions.")
    else:
        print("⚠️ Unknown file type.")
    print("-" * 30)

check_path(model_path)
check_path(data_path)
