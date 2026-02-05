from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time
import uuid
import logging
from typing import Optional

from models import (
    RAGQuery, RAGResponse, AgenticTask, AgenticResponse,
    RiskAssessmentRequest, RiskAssessmentResponse,
    HealthCheck, ErrorResponse, DocumentChunk
)
from rag_system import RAGSystem
from agentic_framework import AgenticFramework

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global instances
rag_system: Optional[RAGSystem] = None
agentic_framework: Optional[AgenticFramework] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle management for FastAPI app"""
    global rag_system, agentic_framework
    
    # Startup
    logger.info("Initializing AI Service...")
    try:
        rag_system = RAGSystem()
        rag_system.seed_sample_data()  # Seed with sample data
        agentic_framework = AgenticFramework()
        logger.info("AI Service initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize AI Service: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down AI Service...")


# Create FastAPI app
app = FastAPI(
    title="AI Enterprise Platform - AI Service",
    description="Python FastAPI service for generative AI, RAG, and agentic AI capabilities",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=HealthCheck)
async def root():
    """Root endpoint with service information"""
    return HealthCheck(
        status="healthy",
        version="1.0.0",
        services={
            "rag": "operational",
            "agentic": "operational"
        }
    )


@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint"""
    return HealthCheck(
        status="healthy",
        version="1.0.0",
        services={
            "rag": "operational" if rag_system else "unavailable",
            "agentic": "operational" if agentic_framework else "unavailable"
        }
    )


@app.post("/api/rag/query", response_model=RAGResponse)
async def rag_query(query: RAGQuery):
    """
    Query the RAG system
    
    Retrieves relevant context and generates AI response
    """
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    start_time = time.time()
    
    try:
        # Generate conversation ID if not provided
        conversation_id = query.conversation_id or str(uuid.uuid4())
        
        # Execute RAG query
        result = await rag_system.query(
            query=query.query,
            top_k=query.top_k,
            conversation_history=None  # Could be retrieved from database
        )
        
        processing_time = (time.time() - start_time) * 1000
        
        # Format response
        sources = [
            DocumentChunk(
                content=chunk['content'],
                source=chunk['source'],
                score=chunk['score'],
                metadata=chunk.get('metadata', {})
            )
            for chunk in result['sources']
        ] if query.include_sources else []
        
        return RAGResponse(
            answer=result['answer'],
            sources=sources,
            conversation_id=conversation_id,
            confidence_score=result['confidence_score'],
            processing_time_ms=processing_time
        )
    
    except Exception as e:
        logger.error(f"RAG query failed: {e}")
        raise HTTPException(status_code=500, detail=f"RAG query failed: {str(e)}")


@app.post("/api/agentic/execute", response_model=AgenticResponse)
async def execute_agentic_task(task: AgenticTask):
    """
    Execute an agentic AI task
    
    Uses LLM with tool calling for multi-step reasoning
    """
    if not agentic_framework:
        raise HTTPException(status_code=503, detail="Agentic framework not initialized")
    
    start_time = time.time()
    
    try:
        task_id = str(uuid.uuid4())
        
        # Execute agentic task
        result = await agentic_framework.execute_task(
            task_description=task.task_description,
            context=task.context,
            max_steps=task.max_steps
        )
        
        processing_time = (time.time() - start_time) * 1000
        
        return AgenticResponse(
            task_id=task_id,
            final_answer=result['final_answer'],
            steps=result['steps'],
            total_steps=result['total_steps'],
            success=result['success'],
            processing_time_ms=processing_time
        )
    
    except Exception as e:
        logger.error(f"Agentic task execution failed: {e}")
        raise HTTPException(status_code=500, detail=f"Task execution failed: {str(e)}")


@app.post("/api/risk/assess", response_model=RiskAssessmentResponse)
async def assess_risk(request: RiskAssessmentRequest):
    """
    Assess risk for an AI project
    
    Uses agentic AI to analyze project and calculate risk scores
    """
    if not agentic_framework:
        raise HTTPException(status_code=503, detail="Agentic framework not initialized")
    
    try:
        # Determine risk factors
        has_pii = any(
            keyword in request.description.lower() or keyword in ' '.join(request.data_sources).lower()
            for keyword in ['pii', 'personal', 'customer', 'user data', 'email', 'phone']
        )
        
        # Determine data sensitivity
        sensitive_keywords = ['health', 'medical', 'financial', 'payment', 'ssn', 'credit card']
        data_sensitivity = "high" if any(kw in request.description.lower() for kw in sensitive_keywords) else "medium"
        
        # Determine user impact
        high_impact_keywords = ['customer-facing', 'production', 'critical', 'automated decision']
        user_impact = "high" if any(kw in request.description.lower() for kw in high_impact_keywords) else "medium"
        
        # Calculate overall risk
        risk_result = agentic_framework.calculate_risk_score(
            data_sensitivity=data_sensitivity,
            has_pii=has_pii,
            user_impact=user_impact
        )
        
        # Check compliance requirements
        compliance_result = agentic_framework.check_compliance_requirements(
            industry="general",
            data_types=request.data_sources,
            geographic_regions=None
        )
        
        # Build risk scores for different dimensions
        risk_scores = [
            {
                "dimension": "Data Privacy & Security",
                "score": 8.0 if has_pii else 4.0,
                "severity": "high" if has_pii else "medium",
                "explanation": "Project handles PII and requires enhanced data protection" if has_pii else "Standard data protection measures required",
                "mitigation_recommendations": [
                    "Implement encryption at rest and in transit",
                    "Apply role-based access control",
                    "Conduct privacy impact assessment"
                ] if has_pii else ["Implement standard security measures"]
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
            },
            {
                "dimension": "Regulatory Compliance",
                "score": 7.0 if compliance_result['requires_legal_review'] else 3.0,
                "severity": "high" if compliance_result['requires_legal_review'] else "low",
                "explanation": f"Compliance requirements: {', '.join(compliance_result['compliance_requirements'])}",
                "mitigation_recommendations": compliance_result['compliance_requirements']
            }
        ]
        
        overall_risk = risk_result['risk_score']
        risk_level = risk_result['risk_level']
        
        return RiskAssessmentResponse(
            project_name=request.project_name,
            overall_risk_score=overall_risk,
            risk_level=risk_level,
            risk_scores=risk_scores,
            compliance_requirements=compliance_result['compliance_requirements'],
            approval_required=risk_level in ["medium", "high"] or compliance_result['requires_legal_review']
        )
    
    except Exception as e:
        logger.error(f"Risk assessment failed: {e}")
        raise HTTPException(status_code=500, detail=f"Risk assessment failed: {str(e)}")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc)
        ).dict()
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
