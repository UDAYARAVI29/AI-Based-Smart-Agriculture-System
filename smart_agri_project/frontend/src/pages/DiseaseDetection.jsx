import React, { useState } from 'react';
import { Upload, AlertCircle, CheckCircle, Loader2 } from 'lucide-react';
import { predictDisease } from '../api';

const DiseaseDetection = () => {
    const [file, setFile] = useState(null);
    const [preview, setPreview] = useState(null);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile) {
            setFile(selectedFile);
            setPreview(URL.createObjectURL(selectedFile));
            setResult(null);
            setError(null);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file) return;

        setLoading(true);
        setError(null);
        const formData = new FormData();
        formData.append('file', file);

        try {
            const data = await predictDisease(formData);
            setResult(data);
        } catch (err) {
            setError('Failed to analyze image. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto px-4 py-12">
            <div className="text-center mb-12">
                <h1 className="text-3xl font-bold text-gray-900 mb-4">Disease Detection</h1>
                <p className="text-gray-600">Upload a photo of your crop leaf to detect diseases and get treatment recommendations.</p>
            </div>

            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
                <form onSubmit={handleSubmit} className="space-y-8">
                    <div className="flex flex-col items-center justify-center w-full">
                        <label htmlFor="dropzone-file" className="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100 transition-colors">
                            {preview ? (
                                <img src={preview} alt="Preview" className="h-full object-contain rounded-lg" />
                            ) : (
                                <div className="flex flex-col items-center justify-center pt-5 pb-6">
                                    <Upload className="w-10 h-10 mb-3 text-gray-400" />
                                    <p className="mb-2 text-sm text-gray-500"><span className="font-semibold">Click to upload</span> or drag and drop</p>
                                    <p className="text-xs text-gray-500">SVG, PNG, JPG or GIF (MAX. 800x400px)</p>
                                </div>
                            )}
                            <input id="dropzone-file" type="file" className="hidden" onChange={handleFileChange} accept="image/*" />
                        </label>
                    </div>

                    <div className="flex justify-center">
                        <button
                            type="submit"
                            disabled={!file || loading}
                            className={`flex items-center px-8 py-3 rounded-lg text-white font-medium transition-colors ${!file || loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-primary-600 hover:bg-primary-700'
                                }`}
                        >
                            {loading ? <Loader2 className="animate-spin mr-2" /> : null}
                            {loading ? 'Analyzing...' : 'Analyze Image'}
                        </button>
                    </div>
                </form>

                {error && (
                    <div className="mt-8 p-4 bg-red-50 text-red-700 rounded-lg flex items-center">
                        <AlertCircle className="w-5 h-5 mr-2" />
                        {error}
                    </div>
                )}

                {result && (
                    <div className="mt-8 space-y-6">
                        <div className="p-6 bg-green-50 rounded-xl border border-green-100">
                            <div className="flex items-start">
                                <CheckCircle className="w-6 h-6 text-green-600 mr-3 mt-1" />
                                <div>
                                    <h3 className="text-lg font-semibold text-green-900 mb-2">Analysis Result</h3>
                                    <div className="space-y-2">
                                        <p className="text-green-800"><span className="font-medium">Predicted Disease:</span> {result.predicted_class}</p>
                                        <p className="text-green-800"><span className="font-medium">Confidence:</span> {(result.confidence * 100).toFixed(2)}%</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <AIRecommendationSection
                            taskType="Disease Detection"
                            inputs={{ image: file.name }}
                            prediction={result}
                        />
                    </div>
                )}
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

export default DiseaseDetection;
