import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from flask import Flask, request, jsonify

def create_dummy_model():
    # Simple dummy data
    texts = [
        "The earth is flat and the sun orbits around it.",
        "Scientists confirmed that water boils at 100 degrees Celsius.",
        "Aliens have landed in New York and are giving away free ice cream.",
        "The stock market experienced a slight dip yesterday due to interest rate concerns."
    ]
    labels = [0, 1, 0, 1] # 0 = Fake, 1 = Real
    
    # Train vectorizer
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)
    
    # Train model
    model = SVC(kernel='rbf', probability=True)
    model.fit(X, labels)
    
    # Save to standard paths
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    os.makedirs(backend_dir, exist_ok=True)
    
    with open(os.path.join(backend_dir, 'model.pkl'), 'wb') as f:
        pickle.dump(model, f)
        
    with open(os.path.join(backend_dir, 'vectorizer.pkl'), 'wb') as f:
        pickle.dump(vectorizer, f)
        
    print("Dummy model and vectorizer created successfully in backend/ directory.")

if __name__ == '__main__':
    app = Flask(__name__)
    app.run(debug=True, port=5000, ssl_context='adhoc')  # removes warning
