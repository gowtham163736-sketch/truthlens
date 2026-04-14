// API module for communicating with the Flask backend

const API_URL = 'https://truthlens-84rd.onrender.com/api';

class FakeNewsAPI {
    /**
     * Send text to the backend for prediction
     * @param {string} text - The news article or headline
     * @returns {Promise<Object>} - The prediction result
     */
    static async predict(text) {
        try {
            const response = await fetch(`${API_URL}/predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to fetch prediction');
            }

            return await response.json();
        } catch (error) {
            console.error("API Error:", error);
            throw error;
        }
    }
}
