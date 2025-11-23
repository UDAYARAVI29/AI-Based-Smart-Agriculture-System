import React, { useState } from 'react';
import { Droplets, Loader2, AlertCircle } from 'lucide-react';
import { predictIrrigation } from '../api';

const IrrigationPrediction = () => {
    const [formData, setFormData] = useState({
        temperature: '',
        humidity: '',
        rainfall: '',
        soil_type: '',
        ph: '',
        ec: '',
        previous_moisture: ''
    });
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setResult(null);

        try {
            // Convert numeric strings to numbers
            const payload = {
                ...formData,
                temperature: parseFloat(formData.temperature),
                humidity: parseFloat(formData.humidity),
                rainfall: parseFloat(formData.rainfall),
                ph: parseFloat(formData.ph),
                ec: parseFloat(formData.ec),
                previous_moisture: parseFloat(formData.previous_moisture),
                // soil_type kept as string/int as per schema
            };

            const data = await predictIrrigation(payload);
            setResult(data);
        } catch (err) {
            setError('Failed to get recommendation. Please check your inputs.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto px-4 py-12">
            <div className="text-center mb-12">
                <h1 className="text-3xl font-bold text-gray-900 mb-4">Smart Irrigation</h1>
                <p className="text-gray-600">Get precise watering recommendations based on soil and environmental conditions.</p>
            </div>

            <div className="grid md:grid-cols-3 gap-8">
                <div className="md:col-span-2 bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
                    <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Temperature (°C)</label>
                            <input
                                type="number"
                                step="0.1"
                                name="temperature"
                                value={formData.temperature}
                                onChange={handleChange}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition-all"
                                required
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Humidity (%)</label>
                            <input
                                type="number"
                                step="0.1"
                                name="humidity"
                                value={formData.humidity}
                                onChange={handleChange}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition-all"
                                required
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Rainfall (mm)</label>
                            <input
                                type="number"
                                step="0.1"
                                name="rainfall"
                                value={formData.rainfall}
                                onChange={handleChange}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition-all"
                                required
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Soil Type</label>
                            <input
                                type="text"
                                name="soil_type"
                                value={formData.soil_type}
                                onChange={handleChange}
                                placeholder="e.g. Clay, Sandy"
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition-all"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">pH Level</label>
                            <input
                                type="number"
                                step="0.1"
                                name="ph"
                                value={formData.ph}
                                onChange={handleChange}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition-all"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">EC (Electrical Conductivity)</label>
                            <input
                                type="number"
                                step="0.01"
                                name="ec"
                                value={formData.ec}
                                onChange={handleChange}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition-all"
                            />
                        </div>
                        <div className="md:col-span-2">
                            <label className="block text-sm font-medium text-gray-700 mb-2">Previous Soil Moisture</label>
                            <input
                                type="number"
                                step="0.1"
                                name="previous_moisture"
                                value={formData.previous_moisture}
                                onChange={handleChange}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition-all"
                                required
                            />
                        </div>

                        <div className="md:col-span-2 pt-4">
                            <button
                                type="submit"
                                disabled={loading}
                                className="w-full bg-primary-600 text-white py-3 rounded-lg font-medium hover:bg-primary-700 transition-colors flex items-center justify-center"
                            >
                                {loading ? <Loader2 className="animate-spin mr-2" /> : <Droplets className="mr-2 h-5 w-5" />}
                                {loading ? 'Calculating...' : 'Get Recommendation'}
                            </button>
                        </div>
                    </form>
                </div>

                <div className="md:col-span-1">
                    {result ? (
                        <div className="space-y-6">
                            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
                                <h3 className="text-lg font-semibold text-gray-900 mb-4">Recommendation</h3>
                                <div className={`p-4 rounded-xl mb-6 ${result.recommendation.includes('No') ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'
                                    }`}>
                                    <p className="text-xl font-bold text-center">{result.recommendation}</p>
                                </div>

                                <div className="space-y-4">
                                    <div>
                                        <p className="text-sm text-gray-500 mb-1">Predicted Moisture</p>
                                        <p className="text-2xl font-semibold text-gray-900">{result.predicted_moisture.toFixed(1)}%</p>
                                    </div>
                                </div>
                            </div>

                            <AIRecommendationSection
                                taskType="Irrigation Prediction"
                                inputs={formData}
                                prediction={result}
                            />
                        </div>
                    ) : (
                        <div className="bg-gray-50 rounded-2xl border border-gray-100 p-6 h-full flex flex-col items-center justify-center text-center text-gray-500">
                            <Droplets className="h-12 w-12 mb-4 text-gray-300" />
                            <p>Fill out the form to get irrigation advice.</p>
                        </div>
                    )}

                    {error && (
                        <div className="mt-4 p-4 bg-red-50 text-red-700 rounded-lg flex items-center">
                            <AlertCircle className="w-5 h-5 mr-2" />
                            {error}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

const AIRecommendationSection = ({ taskType, inputs, prediction }) => {
    const [advice, setAdvice] = useState(null);
    const [loading, setLoading] = useState(false);
    const [show, setShow] = useState(false);

    const handleGetAdvice = async () => {
        setLoading(true);
        try {
            const { getAIRecommendation } = await import('../api');
            const text = await getAIRecommendation(taskType, inputs, prediction);
            setAdvice(text);
            setShow(true);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-xl p-6 border border-indigo-100">
            <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-indigo-900 flex items-center">
                    <span className="mr-2">🤖</span> AI Agronomist
                </h3>
                {!show && (
                    <button
                        onClick={handleGetAdvice}
                        disabled={loading}
                        className="text-sm bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50"
                    >
                        {loading ? 'Thinking...' : 'Get Advice'}
                    </button>
                )}
            </div>

            {show && advice && (
                <div className="prose prose-indigo max-w-none">
                    <div className="whitespace-pre-line text-indigo-800 bg-white/50 p-4 rounded-lg">
                        {advice}
                    </div>
                </div>
            )}
        </div>
    );
};

export default IrrigationPrediction;
