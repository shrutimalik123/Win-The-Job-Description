import { useState, useEffect } from 'react';
import { BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp, AlertTriangle, CheckCircle, Clock } from 'lucide-react';
import { getMetrics, getProjects } from '../services/api';

const COLORS = ['#10b981', '#f59e0b', '#ef4444'];

function Dashboard() {
    const [metrics, setMetrics] = useState(null);
    const [projects, setProjects] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            const [metricsData, projectsData] = await Promise.all([
                getMetrics(),
                getProjects()
            ]);
            setMetrics(metricsData);
            setProjects(projectsData);
        } catch (error) {
            console.error('Error loading dashboard data:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center h-64">
                <div className="text-white text-lg">Loading dashboard...</div>
            </div>
        );
    }

    const riskData = metrics?.riskDistribution?.map(item => ({
        name: item.riskLevel,
        value: item.count
    })) || [];

    const stats = [
        {
            name: 'Total Projects',
            value: metrics?.totalProjects || 0,
            icon: TrendingUp,
            color: 'text-blue-400',
            bgColor: 'bg-blue-500/20'
        },
        {
            name: 'Active Projects',
            value: metrics?.activeProjects || 0,
            icon: CheckCircle,
            color: 'text-green-400',
            bgColor: 'bg-green-500/20'
        },
        {
            name: 'Pending Approval',
            value: metrics?.pendingApproval || 0,
            icon: Clock,
            color: 'text-yellow-400',
            bgColor: 'bg-yellow-500/20'
        },
        {
            name: 'High Risk',
            value: riskData.find(d => d.name === 'High')?.value || 0,
            icon: AlertTriangle,
            color: 'text-red-400',
            bgColor: 'bg-red-500/20'
        }
    ];

    return (
        <div className="space-y-8">
            <div>
                <h2 className="text-3xl font-bold text-white mb-2">AI Governance Dashboard</h2>
                <p className="text-slate-400">Monitor and manage AI projects across the organization</p>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {stats.map((stat) => {
                    const Icon = stat.icon;
                    return (
                        <div key={stat.name} className="card">
                            <div className="flex items-center justify-between">
                                <div>
                                    <p className="text-slate-400 text-sm">{stat.name}</p>
                                    <p className="text-3xl font-bold text-white mt-2">{stat.value}</p>
                                </div>
                                <div className={`${stat.bgColor} p-3 rounded-lg`}>
                                    <Icon className={`w-6 h-6 ${stat.color}`} />
                                </div>
                            </div>
                        </div>
                    );
                })}
            </div>

            {/* Charts */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Risk Distribution */}
                <div className="card">
                    <h3 className="text-xl font-semibold text-white mb-4">Risk Distribution</h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <PieChart>
                            <Pie
                                data={riskData}
                                cx="50%"
                                cy="50%"
                                labelLine={false}
                                label={({ name, value }) => `${name}: ${value}`}
                                outerRadius={100}
                                fill="#8884d8"
                                dataKey="value"
                            >
                                {riskData.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                ))}
                            </Pie>
                            <Tooltip />
                        </PieChart>
                    </ResponsiveContainer>
                </div>

                {/* Recent Projects */}
                <div className="card">
                    <h3 className="text-xl font-semibold text-white mb-4">Recent Projects</h3>
                    <div className="space-y-3">
                        {projects.slice(0, 5).map((project) => (
                            <div key={project.id} className="flex items-center justify-between p-3 bg-slate-700/50 rounded-lg">
                                <div className="flex-1">
                                    <p className="text-white font-medium">{project.name}</p>
                                    <p className="text-slate-400 text-sm">{project.useCase}</p>
                                </div>
                                <span className={`badge-${project.riskLevel?.toLowerCase() || 'medium'}`}>
                                    {project.riskLevel || 'Unknown'}
                                </span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Key Insights */}
            <div className="card">
                <h3 className="text-xl font-semibold text-white mb-4">Key Insights</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="p-4 bg-blue-500/10 border border-blue-500/30 rounded-lg">
                        <h4 className="text-blue-400 font-semibold mb-2">Governance Coverage</h4>
                        <p className="text-slate-300 text-sm">
                            All AI projects are registered and tracked through the governance platform
                        </p>
                    </div>
                    <div className="p-4 bg-green-500/10 border border-green-500/30 rounded-lg">
                        <h4 className="text-green-400 font-semibold mb-2">Risk Management</h4>
                        <p className="text-slate-300 text-sm">
                            Automated risk assessment ensures compliance with organizational policies
                        </p>
                    </div>
                    <div className="p-4 bg-purple-500/10 border border-purple-500/30 rounded-lg">
                        <h4 className="text-purple-400 font-semibold mb-2">AI Assistant</h4>
                        <p className="text-slate-300 text-sm">
                            RAG-powered assistant provides instant access to governance documentation
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Dashboard;
