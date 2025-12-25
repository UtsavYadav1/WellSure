import pandas as pd
import numpy as np
import torch
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from torch.utils.data import Dataset
import pickle
import os
import random

# Configuration
MODEL_NAME = "distilbert-base-uncased"
DATA_PATH = "symptoms_df_clean.csv" # NEW Clean Dataset
OUTPUT_DIR = "medical_bert_output"
MODEL_SAVE_PATH = "medical_bert_model"
SAMPLES_PER_DISEASE = 100 # Augmenting data: 41 * 100 = 4100 examples

def generate_synthetic_data(df, samples_per_disease=50):
    """
    Generates synthetic text data from the symptoms dataframe.
    """
    synthetic_rows = []
    
    # Iterate over each disease
    for index, row in df.iterrows():
        disease = row['Disease']
        # Extract valid symptoms (excluding NaNs or empty strings)
        symptoms = [str(row[col]).replace('_', ' ') for col in df.columns if col.startswith('Symptom_') and pd.notna(row[col]) and str(row[col]) != 'nan']
        
        if not symptoms:
            continue
            
        # Generate N samples
        for _ in range(samples_per_disease):
            # Randomly select a subset of symptoms (between 1 and len(symptoms))
            # We skew towards 2-5 symptoms as that's typical for a user query
            num_symptoms = random.randint(1, min(6, len(symptoms)))
            sampled_symptoms = random.sample(symptoms, num_symptoms)
            
            # Create a sentence
            text_patterns = [
                f"I have {', '.join(sampled_symptoms)}",
                f"Experiencing {', '.join(sampled_symptoms)}",
                f"My symptoms are {', '.join(sampled_symptoms)}",
                f"Suffering from {', '.join(sampled_symptoms)}",
                f"{', '.join(sampled_symptoms)}", # Keyword only
                f"I feel {', '.join(sampled_symptoms)}",
                f"Doctor I have {', '.join(sampled_symptoms)}"
            ]
            
            text = random.choice(text_patterns)
            synthetic_rows.append({"text": text, "label": disease})
            
    return pd.DataFrame(synthetic_rows)

class DiseaseDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

def train():
    print(f"Using device: {'cuda' if torch.cuda.is_available() else 'cpu'}")
    
    if not os.path.exists(DATA_PATH):
        print(f"Error: {DATA_PATH} not found!")
        return

    print("Loading clean data...")
    df = pd.read_csv(DATA_PATH)
    
    print("Generating synthetic data for training...")
    train_df = generate_synthetic_data(df, samples_per_disease=SAMPLES_PER_DISEASE)
    print(f"Generated {len(train_df)} training examples.")
    
    # Label Encoding
    le = LabelEncoder()
    train_df['label_id'] = le.fit_transform(train_df['label'])
    
    # Save Label Encoder
    with open('label_encoder.pkl', 'wb') as f:
        pickle.dump(le, f)
    print("Label encoder saved.")

    # Split Data
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        train_df['text'].tolist(), train_df['label_id'].tolist(), test_size=0.1, random_state=42
    )
    
    print("Loading Tokenizer and Model...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=len(le.classes_))
    
    print("Tokenizing...")
    train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=64)
    val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=64)
    
    train_dataset = DiseaseDataset(train_encodings, train_labels)
    val_dataset = DiseaseDataset(val_encodings, val_labels)
    
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=3, # 3 Epochs should be enough for augmented data
        per_device_train_batch_size=16,
        per_device_eval_batch_size=64,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir='./logs',
        logging_steps=100,
        eval_strategy="steps",
        eval_steps=500,
        save_strategy="no",
        load_best_model_at_end=False,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
    )

    print("Starting Training...")
    trainer.train()
    
    print("Saving Model...")
    model.save_pretrained(MODEL_SAVE_PATH)
    tokenizer.save_pretrained(MODEL_SAVE_PATH)
    print(f"Model saved to {os.path.abspath(MODEL_SAVE_PATH)}")

if __name__ == "__main__":
    train()
