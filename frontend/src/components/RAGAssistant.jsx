import { useState } from 'react';
import { Send, Bot, User } from 'lucide-react';
import { ragQuery } from '../services/api';

function RAGAssistant() {
    const [messages, setMessages] = useState([
        {
            role: 'assistant',
            content: 'Hello! I\'m your AI Governance Assistant. I can help you with questions about AI policies, compliance requirements, and best practices. What would you like to know?'
        }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMessage = { role: 'user', content: input };
        setMessages([...messages, userMessage]);
        setInput('');
        setLoading(true);

        try {
            const response = await ragQuery(input);
            const assistantMessage = {
                role: 'assistant',
                content: response.answer,
                sources: response.sources
            };
            setMessages(prev => [...prev, assistantMessage]);
        } catch (error) {
            console.error('Error querying RAG:', error);
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: 'Sorry, I encountered an error. Please try again.'
            }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-3xl font-bold text-white">AI Governance Assistant</h2>
                <p className="text-slate-400 mt-1">Ask questions about AI policies and governance</p>
            </div>

            <div className="card h-[600px] flex flex-col">
                {/* Messages */}
                <div className="flex-1 overflow-y-auto space-y-4 mb-4">
                    {messages.map((message, index) => (
                        <div
                            key={index}
                            className={`flex items-start space-x-3 ${message.role === 'user' ? 'justify-end' : ''
                                }`}
                        >
                            {message.role === 'assistant' && (
                                <div className="bg-purple-500/20 p-2 rounded-lg">
                                    <Bot className="w-5 h-5 text-purple-400" />
                                </div>
                            )}

                            <div
                                className={`max-w-[70%] ${message.role === 'user'
                                        ? 'bg-blue-600 text-white'
                                        : 'bg-slate-700 text-slate-100'
                                    } rounded-lg p-4`}
                            >
                                <p className="whitespace-pre-wrap">{message.content}</p>

                                {message.sources && message.sources.length > 0 && (
                                    <div className="mt-3 pt-3 border-t border-slate-600">
                                        <p className="text-xs text-slate-400 mb-2">Sources:</p>
                                        {message.sources.map((source, idx) => (
                                            <div key={idx} className="text-xs text-slate-400 mb-1">
                                                • {source.source}
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>

                            {message.role === 'user' && (
                                <div className="bg-blue-500/20 p-2 rounded-lg">
                                    <User className="w-5 h-5 text-blue-400" />
                                </div>
                            )}
                        </div>
                    ))}

                    {loading && (
                        <div className="flex items-start space-x-3">
                            <div className="bg-purple-500/20 p-2 rounded-lg">
                                <Bot className="w-5 h-5 text-purple-400" />
                            </div>
                            <div className="bg-slate-700 rounded-lg p-4">
                                <div className="flex space-x-2">
                                    <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                                    <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                                    <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                                </div>
                            </div>
                        </div>
                    )}
                </div>

                {/* Input */}
                <form onSubmit={handleSubmit} className="flex space-x-2">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask about AI governance policies..."
                        className="input-field flex-1"
                        disabled={loading}
                    />
                    <button
                        type="submit"
                        disabled={loading || !input.trim()}
                        className="btn-primary flex items-center space-x-2"
                    >
                        <Send className="w-4 h-4" />
                        <span>Send</span>
                    </button>
                </form>
            </div>

            {/* Suggested Questions */}
            <div className="card">
                <h3 className="text-lg font-semibold text-white mb-3">Suggested Questions</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {[
                        'What are the data privacy requirements for AI projects?',
                        'How do I assess bias and fairness in my AI model?',
                        'What compliance requirements apply to healthcare AI?',
                        'What security measures are required for AI systems?'
                    ].map((question, index) => (
                        <button
                            key={index}
                            onClick={() => setInput(question)}
                            className="text-left p-3 bg-slate-700/50 hover:bg-slate-700 rounded-lg text-slate-300 text-sm transition-colors"
                        >
                            {question}
                        </button>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default RAGAssistant;
