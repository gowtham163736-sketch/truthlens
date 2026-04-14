from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pickle
import os
import sqlite3
import datetime

# Serve static files from the parent directory (the root of your project)
app = Flask(__name__, static_folder='../', static_url_path='/')
CORS(app)

DB_PATH = os.path.join(os.path.dirname(__file__), 'history.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            prediction TEXT NOT NULL,
            probability REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize DB
init_db()

# Load model and vectorizer
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')
VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), 'vectorizer.pkl')

try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(VECTORIZER_PATH, 'rb') as f:
        vectorizer = pickle.load(f)
    print("Model and vectorizer loaded successfully.")
except Exception as e:
    print(f"Error loading model/vectorizer: {e}")
    model = None
    vectorizer = None

# --- Static File Routes ---
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# --- API Routes ---
@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    text = data['text']
    
    if not model or not vectorizer:
         return jsonify({'error': 'Model not loaded'}), 500

    try:
        # 1. Vectorize text
        vectorized_text = vectorizer.transform([text])
        # 2. Predict
        prediction = model.predict(vectorized_text)[0]
        probability = max(model.predict_proba(vectorized_text)[0])
        
        result = "Real News" if prediction == 1 else "Fake News"
        prob_float = float(probability)
        
        # Save to DB
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO predictions (text, prediction, probability, timestamp) VALUES (?, ?, ?, ?)',
            (text, result, prob_float, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()
        conn.close()
        
        return jsonify({
            'prediction': result,
            'probability': prob_float
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def history():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT text, prediction, probability, timestamp FROM predictions ORDER BY id DESC LIMIT 50')
        rows = cursor.fetchall()
        conn.close()
        
        history_data = []
        for row in rows:
            history_data.append({
                'text': row[0][:150] + "..." if len(row[0]) > 150 else row[0],
                'prediction': row[1],
                'probability': row[2],
                'timestamp': row[3]
            })
            
        return jsonify(history_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
