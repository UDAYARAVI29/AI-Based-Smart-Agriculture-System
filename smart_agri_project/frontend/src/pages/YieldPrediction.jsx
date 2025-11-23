import React, { useState } from 'react';
import { Wheat, Loader2, AlertCircle } from 'lucide-react';
import { predictYield } from '../api';

const YieldPrediction = () => {
    const [formData, setFormData] = useState({
        crop: 'rice',
        area: '',
        rainfall: '',
        temperature: '',
        season: 'kharif',
        soil_type: '',
        ph: '',
        fertilizer_level: ''
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
            const payload = {
                ...formData,
                area: parseFloat(formData.area),
                rainfall: parseFloat(formData.rainfall),
                temperature: parseFloat(formData.temperature),
                ph: parseFloat(formData.ph),
                fertilizer_level: parseFloat(formData.fertilizer_level),
            };

            const data = await predictYield(payload);
            setResult(data);
        } catch (err) {
            setError('Failed to predict yield. Please check your inputs.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto px-4 py-12">
            <div className="text-center mb-12">
                <h1 className="text-3xl font-bold text-gray-900 mb-4">Crop Yield Prediction</h1>
                <p className="text-gray-600">Forecast your harvest based on environmental factors and historical data.</p>
            </div>

            <div className="grid md:grid-cols-3 gap-8">
                <div className="md:col-span-2 bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
                    <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Crop</label>
                            <select
                                name="crop"
                                value={formData.crop}
                                onChange={handleChange}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition-all"
                            >
                                <option value="rice">Rice</option>
                                <option value="wheat">Wheat</option>
                                <option value="maize">Maize</option>
                                <option value="cotton">Cotton</option>
                                <option value="sugarcane">Sugarcane</option>
                            </select>
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Season</label>
                            <select
                                name="season"
                                value={formData.season}
                                onChange={handleChange}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition-all"
                            >
                                <option value="kharif">Kharif</option>
                                <option value="rabi">Rabi</option>
                                <option value="summer">Summer</option>
                                <option value="winter">Winter</option>
                                <option value="whole_year">Whole Year</option>
                            </select>
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Area (Hectares)</label>
                            <input
                                type="number"
                                step="0.01"
                                name="area"
                                value={formData.area}
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
                            <label className="block text-sm font-medium text-gray-700 mb-2">Soil Type</label>
                            <input
                                type="text"
                                name="soil_type"
                                value={formData.soil_type}
                                onChange={handleChange}
                                placeholder="e.g. Clay"
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
                                required
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Fertilizer Level</label>
                            <input
                                type="number"
                                step="0.1"
                                name="fertilizer_level"
                                value={formData.fertilizer_level}
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
                                {loading ? <Loader2 className="animate-spin mr-2" /> : <Wheat className="mr-2 h-5 w-5" />}
                                {loading ? 'Calculating...' : 'Predict Yield'}
                            </button>
                        </div>
                    </form>
                </div>

                <div className="md:col-span-1">
                    {result ? (
                        <div className="space-y-6">
                            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
                                <h3 className="text-lg font-semibold text-gray-900 mb-4">Prediction Result</h3>
                                <div className="bg-yellow-50 text-yellow-800 p-6 rounded-xl mb-6 text-center">
                                    <p className="text-sm font-medium mb-2">Estimated Yield</p>
                                    <p className="text-3xl font-bold">{result.predicted_yield.toFixed(2)}</p>
                                    <p className="text-sm opacity-75">{result.unit}</p>
                                </div>
                            </div>

                            <AIRecommendationSection
                                taskType="Yield Prediction"
                                inputs={formData}
                                prediction={result}
                            />
                        </div>
                    ) : (
                        <div className="bg-gray-50 rounded-2xl border border-gray-100 p-6 h-full flex flex-col items-center justify-center text-center text-gray-500">
                            <Wheat className="h-12 w-12 mb-4 text-gray-300" />
                            <p>Fill out the form to get yield prediction.</p>
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

export default YieldPrediction;
