import os
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the current directory
model_path = os.path.join(BASE_DIR, "item_based_model.pkl")  # Construct full path

