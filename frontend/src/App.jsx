import { Routes, Route, Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, FolderKanban, Shield, MessageSquare, BarChart3 } from 'lucide-react';
import Dashboard from './components/Dashboard';
import ProjectRegistry from './components/ProjectRegistry';
import RiskCompliance from './components/RiskCompliance';
import RAGAssistant from './components/RAGAssistant';

function App() {
    const location = useLocation();

    const navigation = [
        { name: 'Dashboard', path: '/', icon: LayoutDashboard },
        { name: 'Projects', path: '/projects', icon: FolderKanban },
        { name: 'Risk & Compliance', path: '/risk', icon: Shield },
        { name: 'AI Assistant', path: '/assistant', icon: MessageSquare },
    ];

    return (
        <div className="min-h-screen bg-slate-900">
            {/* Header */}
            <header className="gradient-bg shadow-lg">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                            <BarChart3 className="w-8 h-8 text-white" />
                            <div>
                                <h1 className="text-2xl font-bold text-white">AI Enterprise Platform</h1>
                                <p className="text-purple-200 text-sm">Governance & Risk Management</p>
                            </div>
                        </div>
                        <div className="flex items-center space-x-4">
                            <span className="text-white text-sm">Portfolio Project - Shruti Malik</span>
                        </div>
                    </div>
                </div>
            </header>

            {/* Navigation */}
            <nav className="bg-slate-800 border-b border-slate-700">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex space-x-8">
                        {navigation.map((item) => {
                            const Icon = item.icon;
                            const isActive = location.pathname === item.path;
                            return (
                                <Link
                                    key={item.path}
                                    to={item.path}
                                    className={`flex items-center space-x-2 px-3 py-4 text-sm font-medium border-b-2 transition-colors ${isActive
                                            ? 'border-purple-500 text-white'
                                            : 'border-transparent text-slate-400 hover:text-white hover:border-slate-500'
                                        }`}
                                >
                                    <Icon className="w-4 h-4" />
                                    <span>{item.name}</span>
                                </Link>
                            );
                        })}
                    </div>
                </div>
            </nav>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <Routes>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/projects" element={<ProjectRegistry />} />
                    <Route path="/risk" element={<RiskCompliance />} />
                    <Route path="/assistant" element={<RAGAssistant />} />
                </Routes>
            </main>

            {/* Footer */}
            <footer className="bg-slate-800 border-t border-slate-700 mt-16">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                    <p className="text-center text-slate-400 text-sm">
                        AI Enterprise Platform - Portfolio Project for AI Implementation Engineer Position (R-10367735)
                    </p>
                </div>
            </footer>
        </div>
    );
}

export default App;
