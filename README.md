# TruthLens - Fake News Detector

TruthLens is a machine learning-powered web application built to analyze the linguistic patterns and truthfulness of textual news articles and headlines. This project is structured as a modular codebase, separating frontend aesthetics and backend functionality.

## Project Structure

```
fake-news-detector/
│
├── index.html              # Main UI (news input)
├── simulation.html         # 3D simulation page
│
├── css/
│   ├── main.css            # main page styling
│   ├── simulation.css      # 3D page styling
│
├── js/
│   ├── main.js             # handles input + button
│   ├── api.js              # connects frontend to backend
│   ├── simulation.js       # gravity + 3D logic
│
├── backend/
│   ├── app.py              # Flask server
│   ├── model.pkl           # trained ML model
│   ├── vectorizer.pkl      # text processing
│
├── assets/
│   ├── images/
│   ├── icons/
│
├── libs/
│   └── three.js            # 3D library
│
├── requirements.txt        # Python libraries
├── save_model.py           # Script to generate dummy model files
└── README.md               # project explanation
```

## How to Run

1. **Install Requirements:**
   Make sure you have python installed.
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate the Model (If Needed):**
   ```bash
   python save_model.py
   ```

3. **Start the Backend:**
   Run the Flask server:
   ```bash
   python backend/app.py
   ```
   The backend API will be available at `http://localhost:5000/api/predict`

4. **Launch Frontend:**
   Use a local web server (like VS Code Live Server) to open `index.html`. You can also just double click `index.html` to open it in your browser.

## Features

- **Modern Aesthetics**: Interactive UI with particle effects and smooth animations.
- **REST API**: Decoupled Flask backend architecture.
- **3D Interactive Engine**: Visually simulate Data Propagation using Three.js on the `simulation.html` page.
