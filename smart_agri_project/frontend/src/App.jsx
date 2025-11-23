import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import DiseaseDetection from './pages/DiseaseDetection';
import IrrigationPrediction from './pages/IrrigationPrediction';
import YieldPrediction from './pages/YieldPrediction';

function App() {
    return (
        <Router>
            <div className="min-h-screen bg-gray-50 font-sans">
                <Navbar />
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/disease" element={<DiseaseDetection />} />
                    <Route path="/irrigation" element={<IrrigationPrediction />} />
                    <Route path="/yield" element={<YieldPrediction />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
