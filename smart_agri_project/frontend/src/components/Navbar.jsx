import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Sprout, Droplets, Wheat, Activity } from 'lucide-react';

const Navbar = () => {
    const location = useLocation();

    const isActive = (path) => {
        return location.pathname === path ? 'bg-primary-600 text-white' : 'text-gray-600 hover:bg-primary-50 hover:text-primary-600';
    };

    return (
        <nav className="bg-white shadow-sm border-b border-gray-100">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between h-16">
                    <div className="flex">
                        <Link to="/" className="flex-shrink-0 flex items-center">
                            <Sprout className="h-8 w-8 text-primary-600" />
                            <span className="ml-2 text-xl font-bold text-gray-900">SmartAgri AI</span>
                        </Link>
                        <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                            <Link
                                to="/"
                                className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${location.pathname === '/'
                                        ? 'border-primary-500 text-gray-900'
                                        : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                                    }`}
                            >
                                Home
                            </Link>
                            <Link
                                to="/disease"
                                className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${location.pathname === '/disease'
                                        ? 'border-primary-500 text-gray-900'
                                        : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                                    }`}
                            >
                                Disease Detection
                            </Link>
                            <Link
                                to="/irrigation"
                                className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${location.pathname === '/irrigation'
                                        ? 'border-primary-500 text-gray-900'
                                        : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                                    }`}
                            >
                                Irrigation
                            </Link>
                            <Link
                                to="/yield"
                                className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${location.pathname === '/yield'
                                        ? 'border-primary-500 text-gray-900'
                                        : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                                    }`}
                            >
                                Yield Prediction
                            </Link>
                        </div>
                    </div>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
