import os
from typing import List, Dict, Any, Optional
from openai import AzureOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings
import chromadb
from chromadb.config import Settings
import logging

logger = logging.getLogger(__name__)


class RAGSystem:
    """
    Retrieval Augmented Generation System
    Implements semantic search and context-aware generation
    """
    
    def __init__(self):
        """Initialize RAG system with Azure OpenAI and vector store"""
        # Azure OpenAI Configuration
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4")
        self.embedding_deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-ada-002")
        
        # Embeddings
        self.embeddings = AzureOpenAIEmbeddings(
            azure_deployment=self.embedding_deployment,
            openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY")
        )
        
        # Vector Store (ChromaDB for local development)
        self.chroma_client = chromadb.Client(Settings(
            anonymized_telemetry=False,
            allow_reset=True
        ))
        
        # Create or get collection
        self.collection = self.chroma_client.get_or_create_collection(
            name="enterprise_docs",
            metadata={"description": "Enterprise documentation and policies"}
        )
        
        # Text splitter for chunking
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        logger.info("RAG System initialized successfully")
    
    async def add_documents(self, documents: List[Dict[str, Any]]) -> int:
        """
        Add documents to the vector store
        
        Args:
            documents: List of documents with 'content', 'source', and 'metadata'
        
        Returns:
            Number of chunks added
        """
        total_chunks = 0
        
        for doc in documents:
            # Split document into chunks
            chunks = self.text_splitter.split_text(doc['content'])
            
            # Generate embeddings and add to vector store
            for i, chunk in enumerate(chunks):
                chunk_id = f"{doc['source']}_{i}"
                
                # Get embedding
                embedding = await self.embeddings.aembed_query(chunk)
                
                # Add to ChromaDB
                self.collection.add(
                    ids=[chunk_id],
                    embeddings=[embedding],
                    documents=[chunk],
                    metadatas=[{
                        "source": doc['source'],
                        "chunk_index": i,
                        **doc.get('metadata', {})
                    }]
                )
                
                total_chunks += 1
        
        logger.info(f"Added {total_chunks} chunks from {len(documents)} documents")
        return total_chunks
    
    async def retrieve_context(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant context for a query
        
        Args:
            query: User query
            top_k: Number of top results to return
        
        Returns:
            List of relevant document chunks with metadata
        """
        # Generate query embedding
        query_embedding = await self.embeddings.aembed_query(query)
        
        # Search vector store
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # Format results
        context_chunks = []
        if results['documents'] and len(results['documents']) > 0:
            for i in range(len(results['documents'][0])):
                context_chunks.append({
                    'content': results['documents'][0][i],
                    'source': results['metadatas'][0][i].get('source', 'unknown'),
                    'score': 1.0 - results['distances'][0][i] if 'distances' in results else 0.0,
                    'metadata': results['metadatas'][0][i]
                })
        
        logger.info(f"Retrieved {len(context_chunks)} context chunks for query")
        return context_chunks
    
    async def generate_response(
        self,
        query: str,
        context_chunks: List[Dict[str, Any]],
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Generate response using retrieved context
        
        Args:
            query: User query
            context_chunks: Retrieved context chunks
            conversation_history: Previous conversation messages
        
        Returns:
            Generated response with metadata
        """
        # Build context string
        context_str = "\n\n".join([
            f"[Source: {chunk['source']}]\n{chunk['content']}"
            for chunk in context_chunks
        ])
        
        # Build system prompt
        system_prompt = """You are an AI assistant for an enterprise AI governance platform.
Your role is to provide accurate, helpful information based on the provided context.

Guidelines:
1. Answer based primarily on the provided context
2. If the context doesn't contain enough information, acknowledge this
3. Cite sources when providing information
4. Be clear, concise, and professional
5. If asked about AI governance, emphasize compliance and risk management

Context:
{context}
"""
        
        # Build messages
        messages = [
            {"role": "system", "content": system_prompt.format(context=context_str)}
        ]
        
        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history[-5:])  # Last 5 messages for context
        
        # Add current query
        messages.append({"role": "user", "content": query})
        
        # Generate response
        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=messages,
            temperature=0.7,
            max_tokens=800,
            top_p=0.95
        )
        
        answer = response.choices[0].message.content
        
        # Calculate confidence score (simplified)
        confidence = min(0.95, sum(chunk['score'] for chunk in context_chunks) / len(context_chunks))
        
        return {
            'answer': answer,
            'confidence_score': confidence,
            'tokens_used': response.usage.total_tokens
        }
    
    async def query(
        self,
        query: str,
        top_k: int = 5,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Complete RAG pipeline: retrieve and generate
        
        Args:
            query: User query
            top_k: Number of context chunks to retrieve
            conversation_history: Previous conversation
        
        Returns:
            Complete RAG response
        """
        # Retrieve context
        context_chunks = await self.retrieve_context(query, top_k)
        
        # Generate response
        response_data = await self.generate_response(query, context_chunks, conversation_history)
        
        return {
            'answer': response_data['answer'],
            'sources': context_chunks,
            'confidence_score': response_data['confidence_score'],
            'tokens_used': response_data['tokens_used']
        }
    
    def seed_sample_data(self):
        """Seed vector store with sample enterprise documentation"""
        sample_docs = [
            {
                'content': """AI Governance Policy - Data Privacy and Security
                
All AI projects must comply with data privacy regulations including GDPR, CCPA, and industry-specific requirements.

Key Requirements:
1. Data Minimization: Collect only necessary data for the AI use case
2. Encryption: All data must be encrypted at rest and in transit
3. Access Controls: Implement role-based access control (RBAC)
4. Data Retention: Define and enforce data retention policies
5. Privacy Impact Assessment: Required for projects handling PII

Approval Process:
- Projects with PII require Data Protection Officer review
- High-risk projects require executive approval
- All projects must complete privacy questionnaire
""",
                'source': 'AI_Governance_Policy_v2.1.pdf',
                'metadata': {'category': 'governance', 'version': '2.1'}
            },
            {
                'content': """AI Risk Assessment Framework

Risk Dimensions:
1. Data Privacy & Security (0-10 scale)
   - Handling of PII/sensitive data
   - Data encryption and access controls
   - Compliance with regulations

2. Bias & Fairness (0-10 scale)
   - Training data representativeness
   - Model fairness across demographics
   - Bias testing and mitigation

3. Transparency & Explainability (0-10 scale)
   - Model interpretability
   - Decision explanation capability
   - Documentation completeness

4. Regulatory Compliance (0-10 scale)
   - Industry regulation adherence
   - Legal requirements compliance
   - Audit trail completeness

5. Operational Risk (0-10 scale)
   - System reliability and availability
   - Error handling and fallbacks
   - Monitoring and alerting

Risk Levels:
- Low (0-3): Standard approval process
- Medium (4-6): Additional review required
- High (7-10): Executive approval and enhanced monitoring
""",
                'source': 'Risk_Assessment_Framework_v1.5.pdf',
                'metadata': {'category': 'risk', 'version': '1.5'}
            },
            {
                'content': """Generative AI Best Practices

Implementation Guidelines:
1. Prompt Engineering
   - Use clear, specific prompts
   - Implement few-shot learning when applicable
   - Test prompts thoroughly before deployment

2. Safety Guardrails
   - Content filtering for harmful outputs
   - Input validation and sanitization
   - Output verification and human review

3. Cost Management
   - Monitor token usage and costs
   - Implement caching for common queries
   - Use appropriate model sizes

4. Performance Optimization
   - Batch requests when possible
   - Implement retry logic with exponential backoff
   - Cache embeddings for frequently accessed documents

5. Monitoring & Logging
   - Log all AI interactions for audit
   - Track performance metrics
   - Set up alerts for anomalies
""",
                'source': 'GenAI_Best_Practices_v1.0.pdf',
                'metadata': {'category': 'technical', 'version': '1.0'}
            }
        ]
        
        # Add synchronously for seeding
        import asyncio
        asyncio.run(self.add_documents(sample_docs))
        logger.info("Sample data seeded successfully")
