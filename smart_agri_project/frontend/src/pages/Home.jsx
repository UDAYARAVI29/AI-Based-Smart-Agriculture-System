import React from 'react';
import { Link } from 'react-router-dom';
import { Activity, Droplets, Wheat, ArrowRight } from 'lucide-react';

const FeatureCard = ({ icon: Icon, title, description, link, color }) => (
    <Link to={link} className="group block p-6 bg-white rounded-2xl shadow-sm hover:shadow-md transition-all duration-300 border border-gray-100 hover:border-primary-200">
        <div className={`h-12 w-12 rounded-xl flex items-center justify-center mb-4 ${color}`}>
            <Icon className="h-6 w-6 text-white" />
        </div>
        <h3 className="text-xl font-semibold text-gray-900 mb-2 group-hover:text-primary-600 transition-colors">{title}</h3>
        <p className="text-gray-600 mb-4">{description}</p>
        <div className="flex items-center text-primary-600 font-medium">
            Try now <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
        </div>
    </Link>
);

const Home = () => {
    return (
        <div className="min-h-[calc(100vh-4rem)] bg-gradient-to-b from-primary-50 to-white">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
                <div className="text-center max-w-3xl mx-auto mb-16">
                    <h1 className="text-5xl font-bold text-gray-900 mb-6 tracking-tight">
                        Smart Agriculture with <span className="text-primary-600">Artificial Intelligence</span>
                    </h1>
                    <p className="text-xl text-gray-600 leading-relaxed">
                        Optimize your farming with our advanced AI tools. Detect diseases, manage irrigation, and predict yields with precision.
                    </p>
                </div>

                <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
                    <FeatureCard
                        icon={Activity}
                        title="Disease Detection"
                        description="Upload leaf images to instantly detect diseases and get treatment recommendations."
                        link="/disease"
                        color="bg-red-500"
                    />
                    <FeatureCard
                        icon={Droplets}
                        title="Smart Irrigation"
                        description="Get precise watering recommendations based on soil moisture and crop type."
                        link="/irrigation"
                        color="bg-blue-500"
                    />
                    <FeatureCard
                        icon={Wheat}
                        title="Yield Prediction"
                        description="Forecast your crop yield based on environmental factors and historical data."
                        link="/yield"
                        color="bg-yellow-500"
                    />
                </div>
            </div>
        </div>
    );
};

export default Home;
