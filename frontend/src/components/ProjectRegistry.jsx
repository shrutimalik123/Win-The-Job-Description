import { useState, useEffect } from 'react';
import { Plus, Search, Filter } from 'lucide-react';
import { getProjects, createProject } from '../services/api';

function ProjectRegistry() {
    const [projects, setProjects] = useState([]);
    const [showForm, setShowForm] = useState(false);
    const [loading, setLoading] = useState(true);
    const [formData, setFormData] = useState({
        name: '',
        description: '',
        useCase: '',
        dataSources: '',
        stakeholders: ''
    });

    useEffect(() => {
        loadProjects();
    }, []);

    const loadProjects = async () => {
        try {
            const data = await getProjects();
            setProjects(data);
        } catch (error) {
            console.error('Error loading projects:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const projectData = {
                ...formData,
                dataSources: formData.dataSources.split(',').map(s => s.trim()),
                stakeholders: formData.stakeholders.split(',').map(s => s.trim())
            };
            await createProject(projectData);
            setShowForm(false);
            setFormData({ name: '', description: '', useCase: '', dataSources: '', stakeholders: '' });
            loadProjects();
        } catch (error) {
            console.error('Error creating project:', error);
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-3xl font-bold text-white">AI Project Registry</h2>
                    <p className="text-slate-400 mt-1">Register and track all AI initiatives</p>
                </div>
                <button
                    onClick={() => setShowForm(!showForm)}
                    className="btn-primary flex items-center space-x-2"
                >
                    <Plus className="w-4 h-4" />
                    <span>New Project</span>
                </button>
            </div>

            {/* Create Project Form */}
            {showForm && (
                <div className="card">
                    <h3 className="text-xl font-semibold text-white mb-4">Register New AI Project</h3>
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div>
                            <label className="block text-slate-300 mb-2">Project Name *</label>
                            <input
                                type="text"
                                required
                                className="input-field"
                                value={formData.name}
                                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                placeholder="e.g., Customer Sentiment Analysis"
                            />
                        </div>

                        <div>
                            <label className="block text-slate-300 mb-2">Description *</label>
                            <textarea
                                required
                                className="input-field"
                                rows="3"
                                value={formData.description}
                                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                                placeholder="Describe the AI project and its objectives"
                            />
                        </div>

                        <div>
                            <label className="block text-slate-300 mb-2">Use Case *</label>
                            <input
                                type="text"
                                required
                                className="input-field"
                                value={formData.useCase}
                                onChange={(e) => setFormData({ ...formData, useCase: e.target.value })}
                                placeholder="e.g., Customer Experience Enhancement"
                            />
                        </div>

                        <div>
                            <label className="block text-slate-300 mb-2">Data Sources (comma-separated) *</label>
                            <input
                                type="text"
                                required
                                className="input-field"
                                value={formData.dataSources}
                                onChange={(e) => setFormData({ ...formData, dataSources: e.target.value })}
                                placeholder="e.g., Customer reviews, Support tickets, Survey data"
                            />
                        </div>

                        <div>
                            <label className="block text-slate-300 mb-2">Stakeholders (comma-separated) *</label>
                            <input
                                type="text"
                                required
                                className="input-field"
                                value={formData.stakeholders}
                                onChange={(e) => setFormData({ ...formData, stakeholders: e.target.value })}
                                placeholder="e.g., Product Team, Customer Success, Data Science"
                            />
                        </div>

                        <div className="flex space-x-3">
                            <button type="submit" className="btn-primary">
                                Register Project
                            </button>
                            <button
                                type="button"
                                onClick={() => setShowForm(false)}
                                className="btn-secondary"
                            >
                                Cancel
                            </button>
                        </div>
                    </form>
                </div>
            )}

            {/* Projects List */}
            <div className="card">
                <div className="flex items-center justify-between mb-4">
                    <h3 className="text-xl font-semibold text-white">All Projects ({projects.length})</h3>
                    <div className="flex items-center space-x-2">
                        <div className="relative">
                            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-slate-400" />
                            <input
                                type="text"
                                placeholder="Search projects..."
                                className="input-field pl-10 w-64"
                            />
                        </div>
                    </div>
                </div>

                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead>
                            <tr className="border-b border-slate-700">
                                <th className="text-left py-3 px-4 text-slate-300 font-semibold">Project Name</th>
                                <th className="text-left py-3 px-4 text-slate-300 font-semibold">Use Case</th>
                                <th className="text-left py-3 px-4 text-slate-300 font-semibold">Risk Level</th>
                                <th className="text-left py-3 px-4 text-slate-300 font-semibold">Status</th>
                                <th className="text-left py-3 px-4 text-slate-300 font-semibold">Created</th>
                            </tr>
                        </thead>
                        <tbody>
                            {projects.map((project) => (
                                <tr key={project.id} className="border-b border-slate-700/50 hover:bg-slate-700/30">
                                    <td className="py-3 px-4 text-white font-medium">{project.name}</td>
                                    <td className="py-3 px-4 text-slate-300">{project.useCase}</td>
                                    <td className="py-3 px-4">
                                        <span className={`badge-${project.riskLevel?.toLowerCase() || 'medium'}`}>
                                            {project.riskLevel || 'Unknown'}
                                        </span>
                                    </td>
                                    <td className="py-3 px-4">
                                        <span className="text-slate-300">{project.status}</span>
                                    </td>
                                    <td className="py-3 px-4 text-slate-400">
                                        {new Date(project.createdAt).toLocaleDateString()}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}

export default ProjectRegistry;
