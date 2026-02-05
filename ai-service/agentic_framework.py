import os
from typing import List, Dict, Any, Optional
from openai import AzureOpenAI
import json
import logging

logger = logging.getLogger(__name__)


class AgenticFramework:
    """
    Agentic AI Framework with tool calling and multi-step reasoning
    Enables LLM to use tools and chain actions to complete complex tasks
    """
    
    def __init__(self):
        """Initialize agentic framework with Azure OpenAI"""
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4")
        
        # Define available tools
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "calculate_risk_score",
                    "description": "Calculate AI project risk score based on multiple dimensions",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "data_sensitivity": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                                "description": "Level of data sensitivity"
                            },
                            "has_pii": {
                                "type": "boolean",
                                "description": "Whether project handles PII"
                            },
                            "user_impact": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                                "description": "Impact on end users"
                            }
                        },
                        "required": ["data_sensitivity", "has_pii", "user_impact"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "query_governance_policy",
                    "description": "Query enterprise AI governance policies",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "policy_area": {
                                "type": "string",
                                "enum": ["data_privacy", "bias_fairness", "compliance", "security"],
                                "description": "Policy area to query"
                            }
                        },
                        "required": ["policy_area"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "check_compliance_requirements",
                    "description": "Check compliance requirements for an AI project",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "industry": {
                                "type": "string",
                                "description": "Industry sector (e.g., healthcare, finance)"
                            },
                            "data_types": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Types of data being processed"
                            },
                            "geographic_regions": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Geographic regions where AI will operate"
                            }
                        },
                        "required": ["industry", "data_types"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_project_metrics",
                    "description": "Get metrics and statistics for AI projects",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "metric_type": {
                                "type": "string",
                                "enum": ["count", "risk_distribution", "compliance_status"],
                                "description": "Type of metrics to retrieve"
                            },
                            "filter_by_risk": {
                                "type": "string",
                                "enum": ["low", "medium", "high", "all"],
                                "description": "Filter projects by risk level"
                            }
                        },
                        "required": ["metric_type"]
                    }
                }
            }
        ]
        
        logger.info("Agentic Framework initialized with tools")
    
    def calculate_risk_score(self, data_sensitivity: str, has_pii: bool, user_impact: str) -> Dict[str, Any]:
        """Tool: Calculate risk score"""
        risk_map = {"low": 2, "medium": 5, "high": 8}
        
        base_score = risk_map[data_sensitivity]
        if has_pii:
            base_score += 2
        base_score += risk_map[user_impact]
        
        risk_score = min(10, base_score)
        risk_level = "low" if risk_score < 4 else "medium" if risk_score < 7 else "high"
        
        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "factors": {
                "data_sensitivity": data_sensitivity,
                "has_pii": has_pii,
                "user_impact": user_impact
            }
        }
    
    def query_governance_policy(self, policy_area: str) -> Dict[str, Any]:
        """Tool: Query governance policies"""
        policies = {
            "data_privacy": {
                "summary": "All AI projects must comply with GDPR, CCPA, and data protection regulations",
                "key_requirements": [
                    "Data minimization",
                    "Encryption at rest and in transit",
                    "Role-based access control",
                    "Privacy impact assessment for PII"
                ],
                "approval_required": True
            },
            "bias_fairness": {
                "summary": "AI systems must be tested for bias and ensure fair outcomes",
                "key_requirements": [
                    "Diverse training data",
                    "Bias testing across demographics",
                    "Fairness metrics monitoring",
                    "Regular bias audits"
                ],
                "approval_required": False
            },
            "compliance": {
                "summary": "Ensure compliance with industry regulations and standards",
                "key_requirements": [
                    "Regulatory mapping",
                    "Compliance documentation",
                    "Audit trail maintenance",
                    "Regular compliance reviews"
                ],
                "approval_required": True
            },
            "security": {
                "summary": "Implement robust security measures for AI systems",
                "key_requirements": [
                    "Secure API endpoints",
                    "Input validation",
                    "Output sanitization",
                    "Security testing"
                ],
                "approval_required": False
            }
        }
        
        return policies.get(policy_area, {"error": "Policy area not found"})
    
    def check_compliance_requirements(
        self,
        industry: str,
        data_types: List[str],
        geographic_regions: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Tool: Check compliance requirements"""
        requirements = []
        
        # Industry-specific requirements
        if industry.lower() in ["healthcare", "health"]:
            requirements.append("HIPAA compliance required")
        if industry.lower() in ["finance", "banking", "financial"]:
            requirements.extend(["SOX compliance", "PCI DSS if handling payments"])
        
        # Data type requirements
        if any("pii" in dt.lower() or "personal" in dt.lower() for dt in data_types):
            requirements.append("GDPR compliance (if EU data)")
            requirements.append("CCPA compliance (if California residents)")
        
        if any("health" in dt.lower() or "medical" in dt.lower() for dt in data_types):
            requirements.append("HIPAA compliance")
        
        # Geographic requirements
        if geographic_regions:
            if "EU" in geographic_regions or "Europe" in geographic_regions:
                requirements.append("GDPR compliance mandatory")
            if "California" in geographic_regions or "US" in geographic_regions:
                requirements.append("CCPA compliance recommended")
        
        return {
            "industry": industry,
            "compliance_requirements": list(set(requirements)),
            "high_risk": len(requirements) > 2,
            "requires_legal_review": len(requirements) > 0
        }
    
    def get_project_metrics(self, metric_type: str, filter_by_risk: str = "all") -> Dict[str, Any]:
        """Tool: Get project metrics (mock data)"""
        if metric_type == "count":
            return {
                "total_projects": 24,
                "active_projects": 18,
                "completed_projects": 6,
                "by_risk": {"low": 9, "medium": 12, "high": 3}
            }
        elif metric_type == "risk_distribution":
            return {
                "low_risk": {"count": 9, "percentage": 37.5},
                "medium_risk": {"count": 12, "percentage": 50.0},
                "high_risk": {"count": 3, "percentage": 12.5}
            }
        elif metric_type == "compliance_status":
            return {
                "fully_compliant": 18,
                "partially_compliant": 4,
                "non_compliant": 2,
                "compliance_rate": 75.0
            }
        
        return {"error": "Unknown metric type"}
    
    def execute_tool(self, tool_name: str, tool_args: Dict[str, Any]) -> Any:
        """Execute a tool by name"""
        tool_map = {
            "calculate_risk_score": self.calculate_risk_score,
            "query_governance_policy": self.query_governance_policy,
            "check_compliance_requirements": self.check_compliance_requirements,
            "get_project_metrics": self.get_project_metrics
        }
        
        if tool_name in tool_map:
            return tool_map[tool_name](**tool_args)
        else:
            return {"error": f"Tool {tool_name} not found"}
    
    async def execute_task(
        self,
        task_description: str,
        context: Optional[Dict[str, Any]] = None,
        max_steps: int = 10
    ) -> Dict[str, Any]:
        """
        Execute an agentic task with multi-step reasoning
        
        Args:
            task_description: Natural language task description
            context: Additional context for the task
            max_steps: Maximum number of reasoning steps
        
        Returns:
            Task execution result with steps and final answer
        """
        steps = []
        messages = [
            {
                "role": "system",
                "content": """You are an AI assistant for enterprise AI governance.
You have access to tools to help answer questions and complete tasks.
Use the tools when needed to provide accurate, data-driven responses.
Think step-by-step and explain your reasoning."""
            },
            {
                "role": "user",
                "content": task_description
            }
        ]
        
        if context:
            messages[0]["content"] += f"\n\nContext: {json.dumps(context)}"
        
        for step_num in range(max_steps):
            # Call LLM with tools
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                tools=self.tools,
                tool_choice="auto",
                temperature=0.7
            )
            
            assistant_message = response.choices[0].message
            
            # Check if tool calls are needed
            if assistant_message.tool_calls:
                # Add assistant message to history
                messages.append(assistant_message)
                
                # Execute each tool call
                for tool_call in assistant_message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)
                    
                    logger.info(f"Step {step_num + 1}: Calling tool {tool_name}")
                    
                    # Execute tool
                    tool_result = self.execute_tool(tool_name, tool_args)
                    
                    # Add tool result to messages
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_name,
                        "content": json.dumps(tool_result)
                    })
                    
                    # Record step
                    steps.append({
                        "step_number": step_num + 1,
                        "action": f"Called tool: {tool_name}",
                        "tool_used": tool_name,
                        "tool_input": tool_args,
                        "observation": json.dumps(tool_result),
                        "reasoning": f"Using {tool_name} to gather information"
                    })
            else:
                # No more tool calls, we have the final answer
                final_answer = assistant_message.content
                
                return {
                    "final_answer": final_answer,
                    "steps": steps,
                    "total_steps": len(steps),
                    "success": True
                }
        
        # Max steps reached
        return {
            "final_answer": "Task exceeded maximum steps. Please refine the task or increase max_steps.",
            "steps": steps,
            "total_steps": len(steps),
            "success": False
        }
