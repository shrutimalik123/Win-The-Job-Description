"""
AI Enterprise Platform - Demo Script
Demonstrates the key endpoints and functionality
"""

import json
from datetime import datetime

print("=" * 80)
print("AI ENTERPRISE PLATFORM - ENDPOINT DEMO")
print("=" * 80)
print()

# Simulate AI Service Endpoints
print("🤖 PYTHON AI SERVICE (FastAPI) - Port 8000")
print("-" * 80)

print("\n1. RAG Query Endpoint: POST /api/rag/query")
print("   Description: Query the RAG system with enterprise documentation")
rag_request = {
    "query": "What are the data privacy requirements for AI projects?",
    "conversation_id": "demo-123",
    "top_k": 5,
    "include_sources": True
}
print(f"   Request: {json.dumps(rag_request, indent=2)}")

rag_response = {
    "answer": "All AI projects must comply with data privacy regulations including GDPR and CCPA. Key requirements include: 1) Data minimization - collect only necessary data, 2) Encryption at rest and in transit, 3) Role-based access control (RBAC), 4) Privacy impact assessment for projects handling PII, and 5) Data retention policies.",
    "sources": [
        {
            "content": "All AI projects must comply with data privacy regulations...",
            "source": "AI_Governance_Policy_v2.1.pdf",
            "score": 0.92,
            "metadata": {"category": "governance", "version": "2.1"}
        }
    ],
    "conversation_id": "demo-123",
    "confidence_score": 0.89,
    "processing_time_ms": 1234.5
}
print(f"   Response: {json.dumps(rag_response, indent=2)}")

print("\n2. Agentic Task Endpoint: POST /api/agentic/execute")
print("   Description: Execute multi-step reasoning with tool calling")
agentic_request = {
    "task_description": "What is the current risk distribution across all AI projects?",
    "context": {},
    "max_steps": 10
}
print(f"   Request: {json.dumps(agentic_request, indent=2)}")

agentic_response = {
    "task_id": "task-456",
    "final_answer": "Based on the project metrics, the current risk distribution is: Low Risk: 9 projects (37.5%), Medium Risk: 12 projects (50%), High Risk: 3 projects (12.5%). This indicates that half of our AI projects are at medium risk and require additional review.",
    "steps": [
        {
            "step_number": 1,
            "action": "Called tool: get_project_metrics",
            "tool_used": "get_project_metrics",
            "tool_input": {"metric_type": "risk_distribution"},
            "observation": '{"low_risk": {"count": 9, "percentage": 37.5}, "medium_risk": {"count": 12, "percentage": 50.0}, "high_risk": {"count": 3, "percentage": 12.5}}',
            "reasoning": "Using get_project_metrics to gather risk distribution data"
        }
    ],
    "total_steps": 1,
    "success": True,
    "processing_time_ms": 2345.6
}
print(f"   Response: {json.dumps(agentic_response, indent=2)}")

print("\n3. Risk Assessment Endpoint: POST /api/risk/assess")
print("   Description: Assess risk for a new AI project")
risk_request = {
    "project_name": "Customer Sentiment Analysis",
    "description": "Analyze customer feedback using NLP to identify sentiment and key themes",
    "data_sources": ["Customer reviews", "Support tickets", "Survey responses"],
    "use_case": "Customer Experience Enhancement",
    "stakeholders": ["Product Team", "Customer Success", "Data Science"]
}
print(f"   Request: {json.dumps(risk_request, indent=2)}")

risk_response = {
    "project_name": "Customer Sentiment Analysis",
    "overall_risk_score": 6.5,
    "risk_level": "Medium",
    "risk_scores": [
        {
            "dimension": "Data Privacy & Security",
            "score": 7.0,
            "severity": "high",
            "explanation": "Project handles PII and requires enhanced data protection measures",
            "mitigation_recommendations": [
                "Implement encryption at rest and in transit",
                "Apply role-based access control",
                "Conduct privacy impact assessment"
            ]
        },
        {
            "dimension": "Bias & Fairness",
            "score": 5.0,
            "severity": "medium",
            "explanation": "AI models require bias testing and fairness evaluation",
            "mitigation_recommendations": [
                "Test model across demographic groups",
                "Implement fairness metrics",
                "Regular bias audits"
            ]
        }
    ],
    "compliance_requirements": [
        "GDPR compliance review",
        "AI Ethics Board review",
        "Security assessment"
    ],
    "approval_required": True,
    "assessment_timestamp": datetime.utcnow().isoformat()
}
print(f"   Response: {json.dumps(risk_response, indent=2, default=str)}")

# Simulate Governance Service Endpoints
print("\n" + "=" * 80)
print("🏢 .NET GOVERNANCE SERVICE (ASP.NET Core) - Port 5000")
print("-" * 80)

print("\n4. Get All Projects: GET /api/projects")
print("   Description: Retrieve all AI projects with optional filtering")
projects_response = [
    {
        "id": "proj-001",
        "name": "Customer Sentiment Analysis",
        "description": "Analyze customer feedback using NLP",
        "useCase": "Customer Experience Enhancement",
        "dataSources": ["Customer reviews", "Support tickets"],
        "stakeholders": ["Product Team", "Customer Success"],
        "status": "Pending",
        "riskScore": 6.5,
        "riskLevel": "Medium",
        "approvalRequired": True,
        "createdAt": "2026-02-04T15:30:00Z",
        "updatedAt": "2026-02-04T15:30:00Z"
    },
    {
        "id": "proj-002",
        "name": "Fraud Detection System",
        "description": "ML-based fraud detection for transactions",
        "useCase": "Risk Management",
        "dataSources": ["Transaction data", "User behavior"],
        "stakeholders": ["Risk Team", "Engineering"],
        "status": "Approved",
        "riskScore": 8.2,
        "riskLevel": "High",
        "approvalRequired": True,
        "createdAt": "2026-02-03T10:00:00Z",
        "updatedAt": "2026-02-04T09:15:00Z"
    }
]
print(f"   Response: {json.dumps(projects_response, indent=2)}")

print("\n5. Create Project: POST /api/projects")
print("   Description: Register a new AI project (triggers automatic risk assessment)")
create_request = {
    "name": "Chatbot Assistant",
    "description": "AI-powered customer support chatbot",
    "useCase": "Customer Support Automation",
    "dataSources": ["FAQ database", "Support history"],
    "stakeholders": ["Support Team", "Engineering"]
}
print(f"   Request: {json.dumps(create_request, indent=2)}")

create_response = {
    "id": "proj-003",
    "name": "Chatbot Assistant",
    "description": "AI-powered customer support chatbot",
    "useCase": "Customer Support Automation",
    "dataSources": ["FAQ database", "Support history"],
    "stakeholders": ["Support Team", "Engineering"],
    "status": "Pending",
    "riskScore": 4.5,
    "riskLevel": "Medium",
    "approvalRequired": True,
    "createdAt": datetime.utcnow().isoformat(),
    "updatedAt": datetime.utcnow().isoformat()
}
print(f"   Response: {json.dumps(create_response, indent=2, default=str)}")

print("\n6. Get Project Metrics: GET /api/projects/metrics")
print("   Description: Get organization-wide AI project metrics")
metrics_response = {
    "totalProjects": 24,
    "activeProjects": 18,
    "pendingApproval": 6,
    "riskDistribution": [
        {"riskLevel": "Low", "count": 9},
        {"riskLevel": "Medium", "count": 12},
        {"riskLevel": "High", "count": 3}
    ]
}
print(f"   Response: {json.dumps(metrics_response, indent=2)}")

print("\n7. Approve Project: POST /api/projects/{id}/approve")
print("   Description: Approve a pending AI project")
approve_response = {
    "id": "proj-001",
    "name": "Customer Sentiment Analysis",
    "status": "Approved",
    "updatedAt": datetime.utcnow().isoformat()
}
print(f"   Response: {json.dumps(approve_response, indent=2, default=str)}")

# React Frontend Routes
print("\n" + "=" * 80)
print("⚛️  REACT FRONTEND (Vite) - Port 3000")
print("-" * 80)

print("\n8. Dashboard: http://localhost:3000/")
print("   Features:")
print("   - Project metrics cards (Total, Active, Pending, High Risk)")
print("   - Risk distribution pie chart")
print("   - Recent projects list")
print("   - Key insights panel")

print("\n9. Project Registry: http://localhost:3000/projects")
print("   Features:")
print("   - Create new AI project form")
print("   - Projects table with search/filter")
print("   - Risk level badges")
print("   - Status tracking")

print("\n10. AI Assistant: http://localhost:3000/assistant")
print("    Features:")
print("    - Chat interface with RAG system")
print("    - Message history")
print("    - Source citations")
print("    - Suggested questions")

print("\n11. Risk & Compliance: http://localhost:3000/risk")
print("    Features:")
print("    - Risk overview cards (Low/Medium/High)")
print("    - Project selection dropdown")
print("    - Risk dimension breakdown")
print("    - Compliance requirements list")
print("    - Mitigation recommendations")

# Summary
print("\n" + "=" * 80)
print("📊 SUMMARY")
print("-" * 80)
print(f"✅ Total Endpoints Demonstrated: 11")
print(f"✅ Python AI Service: 3 endpoints (RAG, Agentic, Risk Assessment)")
print(f"✅ .NET Governance Service: 4 endpoints (CRUD + Metrics)")
print(f"✅ React Frontend: 4 routes (Dashboard, Projects, Assistant, Risk)")
print()
print("🎯 Skills Showcased:")
print("   - Python: FastAPI, async/await, LangChain, Pydantic")
print("   - .NET: ASP.NET Core, Entity Framework, LINQ")
print("   - React: Hooks, Router, State Management, TailwindCSS")
print("   - AI/ML: RAG, Vector Embeddings, Agentic AI, Risk Assessment")
print("   - Architecture: Microservices, REST APIs, Multi-database")
print()
print("=" * 80)
print("Demo complete! This showcases the AI Enterprise Platform capabilities.")
print("=" * 80)
