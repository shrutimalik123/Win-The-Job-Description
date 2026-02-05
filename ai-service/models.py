from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class MessageRole(str, Enum):
    """Message role enumeration"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatMessage(BaseModel):
    """Chat message model"""
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class RAGQuery(BaseModel):
    """RAG query request model"""
    query: str = Field(..., description="User query for RAG system")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for context")
    top_k: int = Field(5, description="Number of documents to retrieve", ge=1, le=20)
    include_sources: bool = Field(True, description="Include source citations")


class DocumentChunk(BaseModel):
    """Retrieved document chunk"""
    content: str
    source: str
    score: float
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RAGResponse(BaseModel):
    """RAG response model"""
    answer: str
    sources: List[DocumentChunk] = Field(default_factory=list)
    conversation_id: str
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    processing_time_ms: float


class AgenticTask(BaseModel):
    """Agentic AI task request"""
    task_description: str = Field(..., description="Natural language task description")
    context: Dict[str, Any] = Field(default_factory=dict)
    max_steps: int = Field(10, description="Maximum reasoning steps", ge=1, le=50)
    tools: List[str] = Field(default_factory=list, description="Available tools")


class AgenticStep(BaseModel):
    """Single step in agentic reasoning"""
    step_number: int
    action: str
    tool_used: Optional[str] = None
    tool_input: Optional[Dict[str, Any]] = None
    observation: str
    reasoning: str


class AgenticResponse(BaseModel):
    """Agentic AI response"""
    task_id: str
    final_answer: str
    steps: List[AgenticStep]
    total_steps: int
    success: bool
    processing_time_ms: float


class RiskAssessmentRequest(BaseModel):
    """AI risk assessment request"""
    project_name: str
    description: str
    data_sources: List[str]
    use_case: str
    stakeholders: List[str]


class RiskScore(BaseModel):
    """Risk score for a specific dimension"""
    dimension: str
    score: float = Field(..., ge=0.0, le=10.0)
    severity: str  # "low", "medium", "high"
    explanation: str
    mitigation_recommendations: List[str]


class RiskAssessmentResponse(BaseModel):
    """AI risk assessment response"""
    project_name: str
    overall_risk_score: float = Field(..., ge=0.0, le=10.0)
    risk_level: str  # "low", "medium", "high"
    risk_scores: List[RiskScore]
    compliance_requirements: List[str]
    approval_required: bool
    assessment_timestamp: datetime = Field(default_factory=datetime.utcnow)


class HealthCheck(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    services: Dict[str, str] = Field(default_factory=dict)


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
