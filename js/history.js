document.addEventListener('DOMContentLoaded', async () => {
    const table = document.getElementById('historyTable');
    const tbody = document.getElementById('historyBody');
    const loader = document.getElementById('loadingHistory');
    const noHistory = document.getElementById('noHistory');

    try {
        const response = await fetch('https://truthlens-84rd.onrender.com/api/history');
        if (!response.ok) throw new Error('Failed to fetch history');
        
        const data = await response.json();
        
        loader.classList.add('hidden');
        
        if (data.length === 0) {
            noHistory.classList.remove('hidden');
        } else {
            table.classList.remove('hidden');
            
            data.forEach(row => {
                const tr = document.createElement('tr');
                
                const dateTd = document.createElement('td');
                dateTd.textContent = row.timestamp;
                
                const textTd = document.createElement('td');
                textTd.className = 'history-text';
                textTd.textContent = row.text;
                textTd.title = row.text; // show full text on hover
                
                const predTd = document.createElement('td');
                const badge = document.createElement('span');
                badge.className = `prediction-badge ${row.prediction === 'Fake News' ? 'badge-fake' : 'badge-real'}`;
                badge.textContent = row.prediction;
                predTd.appendChild(badge);
                
                const probTd = document.createElement('td');
                probTd.textContent = `${(row.probability * 100).toFixed(1)}%`;
                
                tr.appendChild(dateTd);
                tr.appendChild(textTd);
                tr.appendChild(predTd);
                tr.appendChild(probTd);
                
                tbody.appendChild(tr);
            });
        }
    } catch (error) {
        console.error("Error fetching history:", error);
        loader.classList.add('hidden');
        noHistory.classList.remove('hidden');
        noHistory.innerHTML = "<p style='color: #ff4757;'>Error loading history. Is the backend running?</p>";
    }
});
