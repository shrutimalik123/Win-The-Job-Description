import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:4000';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// AI Service APIs
export const ragQuery = async (query, conversationId = null) => {
    const response = await api.post('/api/ai/rag/query', {
        query,
        conversation_id: conversationId,
        top_k: 5,
        include_sources: true,
    });
    return response.data;
};

export const executeAgenticTask = async (taskDescription, context = {}) => {
    const response = await api.post('/api/ai/agentic/execute', {
        task_description: taskDescription,
        context,
        max_steps: 10,
    });
    return response.data;
};

export const assessRisk = async (projectData) => {
    const response = await api.post('/api/ai/risk/assess', projectData);
    return response.data;
};

// Governance Service APIs
export const getProjects = async (filters = {}) => {
    const params = new URLSearchParams(filters);
    const response = await api.get(`/api/governance/projects?${params}`);
    return response.data;
};

export const getProject = async (id) => {
    const response = await api.get(`/api/governance/projects/${id}`);
    return response.data;
};

export const createProject = async (projectData) => {
    const response = await api.post('/api/governance/projects', projectData);
    return response.data;
};

export const updateProject = async (id, projectData) => {
    const response = await api.put(`/api/governance/projects/${id}`, projectData);
    return response.data;
};

export const deleteProject = async (id) => {
    const response = await api.delete(`/api/governance/projects/${id}`);
    return response.data;
};

export const approveProject = async (id) => {
    const response = await api.post(`/api/governance/projects/${id}/approve`);
    return response.data;
};

export const getMetrics = async () => {
    const response = await api.get('/api/governance/projects/metrics');
    return response.data;
};

export default api;
