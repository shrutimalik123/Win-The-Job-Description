# AI Enterprise Platform - Quick Start Guide

## 🎯 Project Summary

This is a **portfolio demonstration project** for the AI Implementation Engineer position at Fiserv (R-10367735). It showcases:

- ✅ **Python AI Service**: RAG system + Agentic AI with Azure OpenAI
- ✅ **.NET Governance Service**: Risk assessment + Compliance tracking
- ✅ **React Frontend**: Modern dashboard with 4 major components
- ✅ **Enterprise Architecture**: Microservices, APIs, multi-database

## 📁 Project Structure

```
Win-The-Job-Description/
├── ai-service/              # Python FastAPI - RAG & Agentic AI
│   ├── app.py              # Main application
│   ├── rag_system.py       # RAG implementation
│   ├── agentic_framework.py # Agentic AI with tools
│   ├── models.py           # Pydantic models
│   └── requirements.txt
│
├── governance-service/      # .NET ASP.NET Core - Governance
│   ├── Controllers/        # API controllers
│   ├── Services/           # Business logic
│   ├── Models/             # Domain models
│   ├── Data/               # Entity Framework
│   └── Program.cs
│
├── frontend/               # React - Dashboard UI
│   ├── src/
│   │   ├── components/    # Dashboard, Projects, RAG, Risk
│   │   ├── services/      # API integration
│   │   └── App.jsx
│   └── package.json
│
├── README.md              # Full documentation
├── .env.example           # Environment template
└── .gitignore
```

## 🚀 Quick Setup

### Prerequisites
- Python 3.11+
- .NET SDK 8.0+
- Node.js 18+
- Azure OpenAI API key (or AWS Bedrock)

### Step 1: Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your Azure OpenAI credentials:
# AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
# AZURE_OPENAI_API_KEY=your-api-key
# AZURE_OPENAI_DEPLOYMENT=gpt-4
```

### Step 2: Run Python AI Service
```bash
cd ai-service
pip install -r requirements.txt
python app.py
# Runs on http://localhost:8000
# API docs: http://localhost:8000/docs
```

### Step 3: Run .NET Governance Service
```bash
cd governance-service
dotnet restore
dotnet run
# Runs on http://localhost:5000
```

### Step 4: Run React Frontend
```bash
cd frontend
npm install
npm run dev
# Runs on http://localhost:3000
```

## 🎬 Demo Features

### 1. Dashboard (http://localhost:3000)
- View project metrics and statistics
- Risk distribution charts
- Recent projects overview

### 2. Project Registry (http://localhost:3000/projects)
- Register new AI projects
- Automatic risk assessment
- Project status tracking

### 3. AI Assistant (http://localhost:3000/assistant)
- Ask questions about AI governance
- RAG-powered responses with sources
- Suggested questions

### 4. Risk & Compliance (http://localhost:3000/risk)
- View risk assessments
- Compliance requirements
- Mitigation recommendations

## 🎯 Skills Demonstrated

| Category | Technologies |
|----------|-------------|
| **Python** | FastAPI, LangChain, Pydantic, async/await |
| **.NET** | ASP.NET Core 8, Entity Framework, LINQ |
| **React** | React 18, Hooks, Router, TailwindCSS |
| **AI/ML** | Azure OpenAI, RAG, Vector Embeddings, Agentic AI |
| **Databases** | SQL Server, ChromaDB (vector store) |
| **Architecture** | Microservices, REST APIs, Multi-database |

## 📊 Project Metrics

- **Files Created**: 25+
- **Lines of Code**: ~3,500+
- **Services**: 3 (Python, .NET, React)
- **API Endpoints**: 15+
- **Components**: 4 major React components

## 📝 Important Notes

### This is a Portfolio Project
- Demonstrates technical capabilities for job application
- Uses sample data and mock implementations where appropriate
- Production deployment would require additional security and infrastructure

### API Keys Required
- **Azure OpenAI**: Required for RAG and AI features
- Without API keys, the AI service will not function
- Frontend and governance service work independently

### Database
- .NET service uses LocalDB by default
- Can be configured for SQL Server
- Python service uses ChromaDB (embedded)

## 🔗 Additional Resources

- **Full README**: See [README.md](README.md) for complete documentation
- **Walkthrough**: See walkthrough.md in artifacts for detailed feature breakdown
- **Implementation Plan**: See implementation_plan.md for architecture details

## 👤 Contact

**Shruti Malik**  
Portfolio Project for AI Implementation Engineer Position  
Application Reference: R-10367735  
Company: Fiserv  
Date: February 4, 2026

---

**Next Steps**: Review the code, run the services, and explore the features!
