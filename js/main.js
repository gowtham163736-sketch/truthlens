document.addEventListener('DOMContentLoaded', () => {
    const newsInput = document.getElementById('newsInput');
    const charCount = document.getElementById('charCount');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const btnText = analyzeBtn.querySelector('.btn-text');
    const btnIcon = analyzeBtn.querySelector('i');
    const btnLoader = document.getElementById('btnLoader');
    
    const resultContainer = document.getElementById('resultContainer');
    const resultCard = resultContainer.querySelector('.result-card');
    const resultIcon = document.getElementById('resultIcon');
    const resultTitle = document.getElementById('resultTitle');
    const confidenceBar = document.getElementById('confidenceBar');
    const confidenceScore = document.getElementById('confidenceScore');

    // Word count update
    newsInput.addEventListener('input', () => {
        const text = newsInput.value.trim();
        const words = text ? text.split(/\s+/).length : 0;
        charCount.textContent = words;
        
        // Reset results when typing new text
        if (!resultContainer.classList.contains('hidden') && analyzeBtn.disabled === false) {
            resultContainer.classList.add('hidden');
        }
    });

    analyzeBtn.addEventListener('click', async () => {
        const text = newsInput.value.trim();
        if (!text) {
            newsInput.style.borderColor = '#ff4757';
            setTimeout(() => newsInput.style.borderColor = '', 1000);
            return;
        }

        // UI Loading State
        analyzeBtn.disabled = true;
        btnText.textContent = "Analyzing...";
        btnIcon.style.display = "none";
        btnLoader.style.display = "block";
        resultContainer.classList.add('hidden');
        confidenceBar.style.width = '0%';

        try {
            // Call Backend API
            const result = await FakeNewsAPI.predict(text);
            
            // Artificial delay for UI effect
            await new Promise(r => setTimeout(r, 600));

            displayResult(result);
            
        } catch (error) {
            alert("Error: Could not connect to the analysis engine. Is the backend running?");
        } finally {
            // Restore UI State
            analyzeBtn.disabled = false;
            btnText.textContent = "Analyze Content";
            btnIcon.style.display = "inline-block";
            btnLoader.style.display = "none";
        }
    });

    function displayResult(result) {
        resultContainer.classList.remove('hidden');
        resultCard.className = 'result-card'; // reset classes
        
        const isFake = result.prediction.toLowerCase().includes('fake');
        const prob = (result.probability * 100).toFixed(1);
        
        if (isFake) {
            resultCard.classList.add('is-fake');
            resultIcon.className = 'fa-solid fa-circle-exclamation';
            resultTitle.textContent = 'Likely Fake News';
        } else {
            resultCard.classList.add('is-real');
            resultIcon.className = 'fa-solid fa-circle-check';
            resultTitle.textContent = 'Likely Real News';
        }
        
        confidenceScore.textContent = `${prob}%`;
        
        // Timeout to allow DOM update before animating width
        setTimeout(() => {
            confidenceBar.style.width = `${prob}%`;
        }, 50);
    }
});
