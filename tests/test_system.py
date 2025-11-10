import sys
sys.path.insert(0, '..')

from mcplib import MCPBus
from agents import QueryRouterAgent, RAGAgent, KGAgent, ResponderAgent
from rag_pipeline import RAGPipeline

def test_basic_flow():
    print("\n=== Testing Basic MCP Message Flow ===")
    bus = MCPBus()
    router = QueryRouterAgent('router', bus)
    rag = RAGAgent('rag', bus)
    kg = KGAgent('kg', bus)
    responder = ResponderAgent('responder', bus)
    test_query = "How do I return a product?"
    #Simulate Message passing
    router.send('router', 'customer_query', test_query)
    m1 = router.receive()
    assert m1 is not None, "Router should receive message"
    router.on_message(m1)
    m2 = rag.receive()
    assert m2 is not None, "RAG Agent should receive classified query"
    rag.on_message(m2)
    m3 = responder.receive()
    assert m3 is not None, "Responder should receive context ready message" 

    print(" === Basic MCP Message Flow Test Passed ===")

def test_rag_retrieval():
    print("\n=== Testing RAG Retrieval ===")
    rag= RAGPipeline()
    docs = rag.retrieve("refund policy")
    assert len(docs) > 0, "RAG should retrieve at least one document"
    assert any("refund" in doc.lower() or "return" in doc.lower() for doc in docs), "Retrieved docs should contain relevant information"
    print(" === RAG Retrieval Test Passed ===")

def test_kg_query():
    print("\n=== Testing Knowledge Graph Query ===")
    from knowledge_graph import SimpleKnowledgeGraph
    kg = SimpleKnowledgeGraph()
    result = kg.query_entity("product")
    assert "attributes" in result, "KG should return entity attributes"
    print(" === Knowledge Graph Query Test Passed ===")

if __name__ == "__main__":
    test_basic_flow()
    test_rag_retrieval()
    test_kg_query()
    print("\nAll tests passed successfully.")     