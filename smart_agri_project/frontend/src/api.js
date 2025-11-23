import axios from 'axios';

const API_URL = 'http://localhost:8000'; // Adjust if backend runs on a different port

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const predictDisease = async (formData) => {
    try {
        const response = await api.post('/predict/disease/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    } catch (error) {
        console.error("Error predicting disease:", error);
        throw error;
    }
};

export const predictIrrigation = async (data) => {
    try {
        const response = await api.post('/predict/irrigation/', data);
        return response.data;
    } catch (error) {
        console.error("Error predicting irrigation:", error);
        throw error;
    }
};

export const predictYield = async (data) => {
    try {
        const response = await api.post('/predict/yield/', data);
        return response.data;
    } catch (error) {
        console.error("Error predicting yield:", error);
        throw error;
    }
};

export const getAIRecommendation = async (taskType, inputs, prediction) => {
    try {
        const response = await api.post('/ai/recommend', {
            task_type: taskType,
            inputs: inputs,
            prediction: prediction
        });
        return response.data.recommendation;
    } catch (error) {
        console.error("Error getting AI recommendation:", error);
        throw error;
    }
};

export default api;
