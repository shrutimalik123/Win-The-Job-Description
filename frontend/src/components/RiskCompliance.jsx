import { useState, useEffect } from 'react';
import { Shield, AlertTriangle, CheckCircle } from 'lucide-react';
import { getProjects } from '../services/api';

function RiskCompliance() {
    const [projects, setProjects] = useState([]);
    const [selectedProject, setSelectedProject] = useState(null);

    useEffect(() => {
        loadProjects();
    }, []);

    const loadProjects = async () => {
        try {
            const data = await getProjects();
            setProjects(data);
            if (data.length > 0) {
                setSelectedProject(data[0]);
            }
        } catch (error) {
            console.error('Error loading projects:', error);
        }
    };

    const getRiskColor = (level) => {
        const colors = {
            Low: 'text-green-400',
            Medium: 'text-yellow-400',
            High: 'text-red-400'
        };
        return colors[level] || 'text-slate-400';
    };

    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-3xl font-bold text-white">Risk & Compliance</h2>
                <p className="text-slate-400 mt-1">Monitor risk assessments and compliance status</p>
            </div>

            {/* Risk Overview */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="card">
                    <div className="flex items-center space-x-3 mb-2">
                        <CheckCircle className="w-5 h-5 text-green-400" />
                        <h3 className="text-lg font-semibold text-white">Low Risk</h3>
                    </div>
                    <p className="text-3xl font-bold text-green-400">
                        {projects.filter(p => p.riskLevel === 'Low').length}
                    </p>
                    <p className="text-slate-400 text-sm mt-1">Projects</p>
                </div>

                <div className="card">
                    <div className="flex items-center space-x-3 mb-2">
                        <AlertTriangle className="w-5 h-5 text-yellow-400" />
                        <h3 className="text-lg font-semibold text-white">Medium Risk</h3>
                    </div>
                    <p className="text-3xl font-bold text-yellow-400">
                        {projects.filter(p => p.riskLevel === 'Medium').length}
                    </p>
                    <p className="text-slate-400 text-sm mt-1">Projects</p>
                </div>

                <div className="card">
                    <div className="flex items-center space-x-3 mb-2">
                        <Shield className="w-5 h-5 text-red-400" />
                        <h3 className="text-lg font-semibold text-white">High Risk</h3>
                    </div>
                    <p className="text-3xl font-bold text-red-400">
                        {projects.filter(p => p.riskLevel === 'High').length}
                    </p>
                    <p className="text-slate-400 text-sm mt-1">Projects</p>
                </div>
            </div>

            {/* Project Selection */}
            <div className="card">
                <h3 className="text-xl font-semibold text-white mb-4">Project Risk Details</h3>
                <select
                    className="input-field mb-6"
                    value={selectedProject?.id || ''}
                    onChange={(e) => {
                        const project = projects.find(p => p.id === e.target.value);
                        setSelectedProject(project);
                    }}
                >
                    {projects.map((project) => (
                        <option key={project.id} value={project.id}>
                            {project.name}
                        </option>
                    ))}
                </select>

                {selectedProject && (
                    <div className="space-y-6">
                        {/* Project Info */}
                        <div>
                            <h4 className="text-lg font-semibold text-white mb-2">{selectedProject.name}</h4>
                            <p className="text-slate-300">{selectedProject.description}</p>
                            <div className="mt-3 flex items-center space-x-4">
                                <span className={`badge-${selectedProject.riskLevel?.toLowerCase() || 'medium'}`}>
                                    Risk: {selectedProject.riskLevel}
                                </span>
                                <span className="text-slate-400">
                                    Score: {selectedProject.riskScore?.toFixed(2) || 'N/A'}/10
                                </span>
                            </div>
                        </div>

                        {/* Risk Dimensions */}
                        {selectedProject.riskAssessments && selectedProject.riskAssessments.length > 0 && (
                            <div>
                                <h4 className="text-lg font-semibold text-white mb-3">Risk Dimensions</h4>
                                <div className="space-y-3">
                                    {selectedProject.riskAssessments[0].riskDimensions?.map((dimension, index) => (
                                        <div key={index} className="bg-slate-700/50 rounded-lg p-4">
                                            <div className="flex items-center justify-between mb-2">
                                                <h5 className="text-white font-medium">{dimension.name}</h5>
                                                <span className={`badge-${dimension.severity?.toLowerCase() || 'medium'}`}>
                                                    {dimension.score?.toFixed(1)}/10
                                                </span>
                                            </div>
                                            <p className="text-slate-300 text-sm mb-2">{dimension.explanation}</p>
                                            {dimension.mitigationRecommendations && dimension.mitigationRecommendations.length > 0 && (
                                                <div className="mt-2">
                                                    <p className="text-slate-400 text-xs mb-1">Recommendations:</p>
                                                    <ul className="list-disc list-inside space-y-1">
                                                        {dimension.mitigationRecommendations.map((rec, idx) => (
                                                            <li key={idx} className="text-slate-300 text-xs">{rec}</li>
                                                        ))}
                                                    </ul>
                                                </div>
                                            )}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Compliance Requirements */}
                        {selectedProject.riskAssessments && selectedProject.riskAssessments[0]?.complianceRequirements && (
                            <div>
                                <h4 className="text-lg font-semibold text-white mb-3">Compliance Requirements</h4>
                                <div className="space-y-2">
                                    {selectedProject.riskAssessments[0].complianceRequirements.map((req, index) => (
                                        <div key={index} className="flex items-center space-x-2 text-slate-300">
                                            <CheckCircle className="w-4 h-4 text-green-400" />
                                            <span>{req}</span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}

export default RiskCompliance;
