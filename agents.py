from mcplib import BaseAgent
from rag_pipeline import RAGPipeline
from knowledge_graph import SimpleKnowledgeGraph
from langchain_google_genai import ChatGoogleGenerativeAI
from config import GOOGLE_API_KEY,GEMINI_MODEL,GEMINI_TEMPERATURE,GEMINI_MAX_TOKENS
import os

#initialize resources once
rag=RAGPipeline()
kg=SimpleKnowledgeGraph()


# Initialize Gemini LLM via LangChain
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY # Ensure API key is set in env

llm = ChatGoogleGenerativeAI(
    model= GEMINI_MODEL,
    temperature=GEMINI_TEMPERATURE
)



class QueryRouterAgent(BaseAgent):
    def on_message(self, message):
        query = message.payload
        #classify query type
        if "refund" in query.lower() or "return" in query.lower():
            classification = "refund"
        elif "shipping" in query.lower() or "delivery" in query.lower():
            classification = "shipping"
        elif "warranty" in query.lower():
            classification = "warranty"
        else:
            classification = "general"
        #Forward to RAG agent
        self.send('rag', 'classified_query', {'query': query, 'classification': classification})

class RAGAgent(BaseAgent):
    # Retrieves relevant context from knowledge base
    def on_message(self, message):
        query= message.payload['query']
        #retrieve relevant docs
        docs=rag.retrieve(query)
        context=rag.format_context(docs)
        # Forward to Responder with retrieved context
        self.send('responder', 'context_ready', {'query': query, 'context': context, 'classification': message.payload.get('classification','general')})
        

class KGAgent(BaseAgent):
    # Queries the knowledge graph for domain reasoning
    def on_message(self, message):
        entity = message.payload
        kg_data = kg.query_entity(entity)
        self.send('responder', 'kg_context', kg_data)

class ResponderAgent(BaseAgent):
    """Generates final response using Gemini API"""
    def on_message(self, msg):
        query = msg.payload.get('query', '')
        context = msg.payload.get('context', '')
        classification = msg.payload.get('classification', 'general') 
        
        # Construct prompt for Gemini
        system_prompt = f"""You are a helpful customer support agent.
        classification: {classification}
        Use the provided context to answer the customer's question accurately and professionally.
        If information is missing or not available in the context, respond with "I'm sorry, I don't have that information right now."""
        
        user_prompt = f"""Customer Question: {query}
        Available context: {context}
        Provide a concise and accurate answer based on the context."""

        try:
            # Generate response using Gemini LLM
            response = llm.invoke(
                f"System: {system_prompt}\n\nUser: {user_prompt}"
            )

            #  Gemini responses differ by SDK version — handle both cases
            if hasattr(response, "content"):
                final_response = response.content
            elif isinstance(response, dict) and "content" in response:
                final_response = response["content"]
            else:
                final_response = str(response)

        except Exception as e:        
            final_response = f"Error generating response: {str(e)}"

        # Print for logging
        print(f"\n[Responder] Generated Response:\n{final_response}\n")

        # Optionally send to evaluator
        self.send('evaluator', 'response_generated', {
            'query': query,
            'response': final_response
        })

        #  Return final response to Streamlit app
        return final_response
