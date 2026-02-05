# AI Enterprise Platform - Endpoints Summary

## ✅ All Endpoints Demonstrated

### 🤖 Python AI Service (FastAPI) - Port 8000

#### 1. RAG Query - `POST /api/rag/query`
**Purpose**: Query the RAG system with enterprise documentation  
**Features**:
- Vector-based semantic search
- Context retrieval from enterprise docs
- Source citations
- Confidence scoring

**Sample Request**:
```json
{
  "query": "What are the data privacy requirements for AI projects?",
  "conversation_id": "demo-123",
  "top_k": 5,
  "include_sources": true
}
```

**Sample Response**:
```json
{
  "answer": "All AI projects must comply with data privacy regulations including GDPR and CCPA...",
  "sources": [{
    "content": "...",
    "source": "AI_Governance_Policy_v2.1.pdf",
    "score": 0.92
  }],
  "confidence_score": 0.89,
  "processing_time_ms": 1234.5
}
```

---

#### 2. Agentic Task Execution - `POST /api/agentic/execute`
**Purpose**: Execute multi-step reasoning with tool calling  
**Features**:
- LLM-driven tool selection
- Multi-step reasoning
- Tool execution (risk calculator, policy query, compliance checker, metrics)
- Step-by-step transparency

**Sample Request**:
```json
{
  "task_description": "What is the current risk distribution across all AI projects?",
  "max_steps": 10
}
```

**Sample Response**:
```json
{
  "task_id": "task-456",
  "final_answer": "Based on the project metrics, the current risk distribution is: Low Risk: 9 projects (37.5%), Medium Risk: 12 projects (50%), High Risk: 3 projects (12.5%)...",
  "steps": [{
    "step_number": 1,
    "action": "Called tool: get_project_metrics",
    "tool_used": "get_project_metrics",
    "observation": "..."
  }],
  "total_steps": 1,
  "success": true
}
```

---

#### 3. Risk Assessment - `POST /api/risk/assess`
**Purpose**: Assess risk for a new AI project  
**Features**:
- Multi-dimensional risk scoring
- Compliance requirement determination
- Mitigation recommendations
- Automatic risk level classification

**Sample Request**:
```json
{
  "project_name": "Customer Sentiment Analysis",
  "description": "Analyze customer feedback using NLP",
  "data_sources": ["Customer reviews", "Support tickets"],
  "use_case": "Customer Experience Enhancement"
}
```

**Sample Response**:
```json
{
  "overall_risk_score": 6.5,
  "risk_level": "Medium",
  "risk_scores": [
    {
      "dimension": "Data Privacy & Security",
      "score": 7.0,
      "severity": "high",
      "mitigation_recommendations": [...]
    }
  ],
  "compliance_requirements": ["GDPR compliance review", "AI Ethics Board review"],
  "approval_required": true
}
```

---

### 🏢 .NET Governance Service (ASP.NET Core) - Port 5000

#### 4. Get All Projects - `GET /api/projects`
**Purpose**: Retrieve all AI projects with optional filtering  
**Query Parameters**: `?status=Pending&riskLevel=High`  
**Returns**: Array of AI projects with full details

#### 5. Get Single Project - `GET /api/projects/{id}`
**Purpose**: Get detailed information for a specific project  
**Includes**: Risk assessments, compliance checks, audit history

#### 6. Create Project - `POST /api/projects`
**Purpose**: Register a new AI project  
**Features**:
- Automatic risk assessment on creation
- Audit trail logging
- Compliance policy application

#### 7. Update Project - `PUT /api/projects/{id}`
**Purpose**: Update project details  
**Features**: Tracks changes, updates timestamps

#### 8. Delete Project - `DELETE /api/projects/{id}`
**Purpose**: Remove a project from registry  
**Features**: Cascade delete of related data, audit logging

#### 9. Approve Project - `POST /api/projects/{id}/approve`
**Purpose**: Approve a pending AI project  
**Features**: Status update, approval workflow, audit trail

#### 10. Get Metrics - `GET /api/projects/metrics`
**Purpose**: Get organization-wide AI project metrics  
**Returns**:
```json
{
  "totalProjects": 24,
  "activeProjects": 18,
  "pendingApproval": 6,
  "riskDistribution": [
    {"riskLevel": "Low", "count": 9},
    {"riskLevel": "Medium", "count": 12},
    {"riskLevel": "High", "count": 3}
  ]
}
```

---

### ⚛️ React Frontend (Vite) - Port 3000

#### 11. Dashboard - `http://localhost:3000/`
**Features**:
- Project metrics cards (Total, Active, Pending, High Risk)
- Risk distribution pie chart (Recharts)
- Recent projects list
- Key insights panel

#### 12. Project Registry - `http://localhost:3000/projects`
**Features**:
- Create new AI project form
- Projects table with search/filter
- Risk level badges (color-coded)
- Status tracking
- Automatic risk assessment on submission

#### 13. AI Assistant - `http://localhost:3000/assistant`
**Features**:
- Chat interface with RAG system
- Message history
- Source citations for transparency
- Suggested questions
- Real-time responses

#### 14. Risk & Compliance - `http://localhost:3000/risk`
**Features**:
- Risk overview cards (Low/Medium/High counts)
- Project selection dropdown
- Risk dimension breakdown with scores
- Compliance requirements list
- Mitigation recommendations

---

## 📊 Summary Statistics

| Category | Count |
|----------|-------|
| **Total Endpoints** | 14 |
| **Python AI Service** | 3 endpoints |
| **.NET Governance Service** | 7 endpoints |
| **React Frontend Routes** | 4 routes |

## 🎯 Technologies Demonstrated

### Backend
- **Python**: FastAPI, async/await, Pydantic, LangChain
- **.NET**: ASP.NET Core 8, Entity Framework Core, LINQ
- **AI/ML**: Azure OpenAI, RAG, Vector Embeddings, Agentic AI

### Frontend
- **React**: Hooks, Router, State Management
- **UI**: TailwindCSS, Recharts, Lucide Icons
- **API Integration**: Axios, async/await

### Architecture
- **Microservices**: Independent, scalable services
- **REST APIs**: Well-defined contracts
- **Multi-database**: SQL Server + ChromaDB
- **Cloud-ready**: Azure OpenAI integration

---

## 🚀 Running the Services

### Python AI Service
```bash
cd ai-service
pip install -r requirements.txt
python app.py
# Access: http://localhost:8000
# Docs: http://localhost:8000/docs
```

### .NET Governance Service
```bash
cd governance-service
dotnet restore
dotnet run
# Access: http://localhost:5000
# Swagger: http://localhost:5000/swagger
```

### React Frontend
```bash
cd frontend
npm install
npm run dev
# Access: http://localhost:3000
```

---

**Project**: AI Enterprise Platform  
**Purpose**: Portfolio demonstration for AI Implementation Engineer position  
**Application**: R-10367735 - Fiserv  
**Date**: February 4, 2026
