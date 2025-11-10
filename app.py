import streamlit as st
import time
from mcplib import MCPBus
from agents import QueryRouterAgent, RAGAgent, KGAgent, ResponderAgent
from evaluation import EvaluationFramework
import os, subprocess, sys
#subprocess.run([sys.executable, "-m", "pip", "install",
#                "huggingface-hub==0.23.2", "transformers==4.44.2",
#                "sentence-transformers==2.7.0", "--force-reinstall"])


#page config
st.set_page_config(page_title="Agentic AI Customer Support", layout="wide", initial_sidebar_state="expanded")
#set title
st.title("Agentic AI Customer Support Intelligence (with MCP Agents)")
st.markdown("Multi agent system with MCP Communication ,RAG retrieval and Gemini LLM for customer support.")
#sidebar info
with st.sidebar:
    st.header(" Configuration ")
    show_debug= st.checkbox("Debug Mode", value=False)
    show_metrics= st.checkbox("Show Evaluation Metrics", value=True)


# Instantiate the MCP bus and agents
@st.cache_resource
def initialize_system():
  bus = MCPBus()
  router = QueryRouterAgent('router', bus)
  rag = RAGAgent('rag', bus)
  kg = KGAgent('kg', bus)
  responder = ResponderAgent('responder', bus)
  evaluator = EvaluationFramework()
  return bus, router, rag, kg, responder, evaluator
bus, router, rag, kg, responder, evaluator = initialize_system()

# Main interface
col1, col2 = st.columns([2,1])

with col1:
    st.subheader(" Query Interface")
# User input
    user_query = st.text_area("Enter your customer support question:", height=100,
                              placeholder="E.g., can I return a product I bought last week?")
    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        process_query = st.button("Process Query",use_container_width=True)
    with col_btn2:
        clear_query = st.button("Clear Query",use_container_width=True)
        if clear_query:
           st.rerun()
with col2:
    st.subheader(" System Status")
    st.metric("status", "Active")
    st.metric("Model", "Gemini-2.5-Pro")
    st.metric("Agents", "4 active")
#process query if button clicked
if process_query and user_query.strip():
    st.divider()
    start_time = time.time()
    with st.spinner(" Processing query through agent system..."):
        #step 1: Router receives user query
        st.info("Step 1: Query Router classifying ...")
        router.send('router', 'customer_query', user_query)
        #step 2: Router processes
        m1= router.receive()
        if m1:
            router.on_message(m1)
        
        #step 3: RAG Agent retrieves context
        st.info("Step 2: RAG Agent retrieving context ...")
        m2= rag.receive()
        if m2:
            rag.on_message(m2)
        # Step 4: Responder generates final response
        st.info("Step 3: Responder generating response ...")
        response = None
        m3 = responder.receive()
        if m3:
            response = responder.on_message(m3)  # make sure on_message returns the text
        
        if response:
            st.subheader("Generated Response")
            st.write(response)
        else:
            st.warning("Responder did not generate a response. Check agent logs.")
        
        processing_time = time.time() - start_time
    st.success(f" Query processed in {processing_time:.2f} seconds.")

    #show metrics
    if show_metrics:
        
        st.subheader(" Performance Metrics ")
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("Processing Time (s)", f"{processing_time:.2f}")
        with col_m2:
            st.metric("Agents involved","4")
        with col_m3:
            st.metric("Messages passed","4")

    #Debug info
    if show_debug:
        st.divider()
        st.subheader(" Debug Information ")
        st.write(f"**original query:** {user_query}")
        st.write(f"**Processing Time:** {processing_time:.2f} seconds")
    
    # footer
    st.divider()
    st.markdown("""
    ---
    **Agentic AI Customer Support Platform** | Powered by Streamlit, LangChain, and Gemini LLM""")