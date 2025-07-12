# Guided Buying Recommender (GBR) System

<b>AI-powered procurement recommendation system demonstrating vector search and multi-agent architecture for enterprise purchasing decisions.</b>

![enterprise-grade-search]()

## Demo Results
### Search Performance
- <b>50,000 products</b> indexed and searchable
- <b>Sub-200ms</b> query response time
- <b>Semantic Similarity</b> scoring

### Recommendation Quality
- <b>Bundle Recommendations</b>: 3 intelligent bundles per search
- <b>Alternative Products</b>: Similar items within budget
- <b>Cost Optimization</b>: Average 5% bundle savings
- <b>Business Compliance</b>: 100% budget adherence

## Performance Metrics
### Search Latency
- <b>Average Query Time</b>: 139ms (vector search + NER + filtering)
- <b>Index Size</b>: 50K products with metadata
- <b>Embedding Generation</b>: less 50ms per query
- <b>Business Logic Processing</b>: less than 10ms

### Business Capabilities
- <b>Budget Optimization</b>: Role-based filtering and recommendations
- <b>Bundle Intelligence</b>: Automatic accessory suggestions with savings calculation
- <b>Alternative Discovery</b>: Similar product recommendations

## MODULAR Project Structure
![structure](https://github.com/Pratik872/NER_based_Semantic_Search/blob/main/readme%20resources/results.png)

## Project Overview
Next-generation procurement capabilities using:
- Semantic Search
- Named Entity Recognition powered search
- Personalized Recommendations
- Business Logic/ (Rules for employee levels)
- Contextual Buying Suggestions.

## Architecture
### Multi-Agent System
- <b>Search Agent</b>: Vector-based product discovery with NER entity extraction
- <b>Recommendation Agent</b>: Bundle generation and alternative product suggestions
- <b>GBR Orchestrator</b>: Coordinates agent workflows and business logic

## Business Applications
<!-- ### SAP Ariba Context
- <b>Procurement Intelligence</b>: Automated buying suggestions
- <b>Cost Optimization</b>: Bundle deals and budget compliance
- <b>User Experience</b>: Natural language search interface
- <b>Scalability</b>: Vector database handles millions of products
- <b>Integration Ready</b>: API-first architecture for enterprise systems -->

### Business Impact
- <b>Faster Procurement</b>: 139ms search vs traditional catalog browsing
- <b>Cost Savings</b>: Automated bundle recommendations
- <b>Compliance</b>: Built-in budget and policy enforcement
- <b>User Adoption</b>: Intuitive chat-like interface

<!-- ## SAP Ariba Alignment
- <b>Vector Search</b>: Next-generation catalog search using semantic understanding
- <b>AI Recommendations</b>: Intelligent buying suggestions based on user context
- <b>Business Logic</b>: Enterprise-grade policy enforcement and budget controls
- <b>Multi-Agent Architecture</b>: Scalable, maintainable AI system design
- <b>Performance</b>: Production-ready latency for enterprise deployment -->

## Tech Stack
- Database: Pinecone Serverless (AWS us-east-1)
- Embedding Model: all-mpnet-base-v2 (768 dimensions)
- NER Model: Babelscape/wikineural-multilingual-ner
- Framework: Streamlit 1.29+
- Python: 3.8+
- Response Time: <200ms average
- Scalability: 1M+ products supported


## Key Components
### NER Engine (ner_engine.py)
- BERT-based token classification
- Aggregation strategy for entity extraction
- CPU/GPU device management

### Retriever (retriever.py)
- Sentence transformer encoding
- Batch processing support
- Query embedding generation


## Performance
- Latency: ~0.8 seconds average search time
- Dataset: 10k indexed articles
- Precision: Entity filtering improves relevance
