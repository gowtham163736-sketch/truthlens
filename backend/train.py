import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import pickle
import os

def load_and_train():
    print("Loading Fake and True datasets...")
    # Paths to the CSV files
    base_dir = os.path.dirname(__file__)
    fake_path = os.path.join(base_dir, 'dataset', 'Fake.csv')
    true_path = os.path.join(base_dir, 'dataset', 'True.csv')
    
    if not os.path.exists(fake_path) or not os.path.exists(true_path):
        print("Error: Missing True.csv or Fake.csv in backend/dataset/")
        return
        
    fake_df = pd.read_csv(fake_path)
    true_df = pd.read_csv(true_path)
    
    # Add labels: 0 for Fake, 1 for True
    fake_df['class'] = 0
    true_df['class'] = 1
    
    # Combine datasets
    df = pd.concat([fake_df, true_df], axis=0)
    
    # We will use text (combined title and text represents the news content)
    df['content'] = df['title'] + " " + df['text']
    
    # Shuffle the data
    df = df.sample(frac=1).reset_index(drop=True)
    
    # Fill NaN values with empty strings
    df['content'] = df['content'].fillna('')
    
    X = df['content']
    y = df['class']
    
    print(f"Total samples: {len(df)}. Splitting into train/test...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Vectorizing text... (this may take a few moments for large datasets)")
    vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    print("Training SVM Model...")
    model = SVC(kernel='linear', probability=True)
    model.fit(X_train_tfidf, y_train)
    
    accuracy = model.score(X_test_tfidf, y_test)
    print(f"Model trained! Accuracy on test set: {accuracy * 100:.2f}%")
    
    print("Saving model and vectorizer...")
    with open(os.path.join(base_dir, 'model.pkl'), 'wb') as f:
        pickle.dump(model, f)
        
    with open(os.path.join(base_dir, 'vectorizer.pkl'), 'wb') as f:
        pickle.dump(vectorizer, f)
        
    print("Done! Restart your Flask server to use the real model.")

if __name__ == '__main__':
    load_and_train()
