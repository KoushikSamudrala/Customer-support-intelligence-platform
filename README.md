---
title: Agentic AI Customer Support
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: 1.51.0
app_file: app.py
pinned: false
---



# Agentic AI Customer Support Intelligence Platform

## Overview

A production-ready multi-agent system where agents communicate exclusively via explicit mcp

## Architecture


User Input (Streamlit)
↓
QueryRouterAgent (classifies query)
↓ [MCPMessage]
RAGAgent (retrieves context)
↓ [MCPMessage]
ResponderAgent (Gemini API → generates response)
↓
User Output

## Quick Start

### Local Development

1. **Clone and setup:** 

```bash 
git clone your-repo; 
cd customer-support-ai 
python -m venv venv 
source venv/bin/activate # or venv\Scripts\activate on Windows 
pip install -r requirements.txt
```

2. Get Gemini API Key:


      .Visit:https://aistudio.google.com
  
      .Click "Get API Key"
  
      .Copy and save in .env file


3. Run locally:
  '''
    streamlit run app.py
  '''

4. Test:

  ''' python tests/test_system.py '''

# Project structure

├── mcplib.py # MCP message bus &amp; base agent

├── config.py # Configuration &amp; credentials

├── rag_pipeline.py # Retrieval system

├── knowledge_graph.py # Domain knowledge graph

├── agents.py # Agent implementations (with Gemini)

├── evaluation.py # Response evaluation

├── app.py # Streamlit UI

├── requirements.txt # Dependencies

├── .env.example # Environment template

├── tests/ # Test suite

└── docs/README.md # This file