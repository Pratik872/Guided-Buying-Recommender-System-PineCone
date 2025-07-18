# Guided Buying Recommender (GBR) System from Concept to Production with CI-CD

<b>AI-powered procurement recommendation system demonstrating vector search and multi-agent architecture for enterprise purchasing decisions.</b>
- Semantic Search
- Named Entity Recognition powered search
- Personalized Recommendations
- Business Logic/ (Rules for employee levels)
- Contextual Buying Suggestions.

![Worflow](https://github.com/Pratik872/Guided-Buying-Recommender-System-PineCone/blob/main/readme_resources/workflow_diagram.svg)

## MODULAR Project Structure
![structure](https://github.com/Pratik872/Guided-Buying-System-PineCone/blob/main/readme_resources/structure.png)

## Scalability
- Data Sources: Data Lake for historical data and training, Apache Kafka stream for real-time data and inference
- <b>100M+ products vs current 50K</b>: Pinecone Enterprise Performance Tier, Graph Databases
- <b>100,000+ concurrent users</b>: Horizontal scaling, Multi-region deployment, Load balancing at multiple levels (global → regional → application)
- <b>Model Real-time Inference Optimization</b>: Model Quantization, Model Pruning, Knowledge Diastillation, Model Caching
- <b>Multi-agent orchestration</b>: LangChain / AutoGen orchestration
- <b>Azure Cloud Platform</b>: Database Services, Machine Learning and Container Platform


## Recommendation Quality
- <b>Bundle Recommendations</b>: 3 intelligent bundles per search
- <b>Alternative Products</b>: Similar items within budget
- <b>Cost Optimization</b>: Average 5% bundle savings
- <b>Business Compliance</b>: 100% budget adherence

## Business Capabilities
- <b>Budget Optimization</b>: Role-based filtering and recommendations
- <b>Bundle Intelligence</b>: Automatic accessory suggestions with savings calculation
- <b>Alternative Discovery</b>: Similar product recommendations

## Business Impact
- <b>Faster Procurement</b>: 139ms search vs traditional catalog browsing
- <b>Cost Savings</b>: Automated bundle recommendations
- <b>Compliance</b>: Built-in budget and policy enforcement
- <b>User Adoption</b>: Intuitive chat-like interface
- <b>Production Ready</b>: Containerized deployment with automated testing
- <b>Scalability</b>: Cloud deployment supporting enterprise workloads

## MLOPs & Production
- <b>Container Startup</b>: ~15 seconds including model loading
- <b>CI/CD Runtime</b>: ~2 minutes for full test and build cycle
- <b>Health Monitoring</b>: Automated status validation
- <b>Production Ready</b>: Dockerized with automated testing
- <b>Production URL</b>: Live accessible endpoint with health checks


## Production Infrastructure
- <b>Docker Containerization</b>: Optimized single-stage build reducing image from 10GB to 3GB
- <b>Automated Testing</b>: Pytest integration with module validation
- <b>Continuous Deployment</b>: Automated Railway deployment on main branch pushes
- <b>Health Monitoring</b>: Streamlit health endpoint checks with Railway integration

<!-- ## Business Applications -->
<!-- ### SAP Ariba Context
- <b>Procurement Intelligence</b>: Automated buying suggestions
- <b>Cost Optimization</b>: Bundle deals and budget compliance
- <b>User Experience</b>: Natural language search interface
- <b>Scalability</b>: Vector database handles millions of products
- <b>Integration Ready</b>: API-first architecture for enterprise systems -->


<!-- ### SAP Ariba Alignment
- <b>Vector Search</b>: Next-generation catalog search using semantic understanding
- <b>AI Recommendations</b>: Intelligent buying suggestions based on user context
- <b>Business Logic</b>: Enterprise-grade policy enforcement and budget controls
- <b>Multi-Agent Architecture</b>: Scalable, maintainable AI system design
- <b>Performance</b>: Production-ready latency for enterprise deployment -->

## Tech Stack
- Dataset: Amazon Products Dataset
- Database: Pinecone Serverless (AWS us-east-1)
- Embedding Model: all-mpnet-base-v2 (768 dimensions)
- NER Model: Babelscape/wikineural-multilingual-ner
- Framework: Streamlit 1.29+
- Python: 3.12
- Container: Docker with health checks
- CI/CD: GitHub Actions with automated testing
- Deployment: Railway cloud platform with continuous deployment

## Challenges Faced and Solutions
### Docker Image Optimization

<b>Challenge</b>: Initial Docker image size of 10GB causing slow deployments and high resource usage

<b>Solution</b>:
- Switched to CPU-only PyTorch (--index-url https://download.pytorch.org/whl/cpu)
- Added comprehensive cache cleanup (pip cache purge, removed /root/.cache/pip)
- Optimized layer structure and added .dockerignore
<b>Result</b>: Reduced image size to 3GB (70% reduction)


### Production Latency Issues

<b>Challenge</b>: 70-second response times in production due to model reloading

<b>Solution</b>:
- Implemented @st.cache_resource for model caching
- Added Pinecone connection caching
- Cached NER pipeline initialization

<b>Result</b>: First request ~35s, subsequent requests ~5-10s

### CI/CD Pipeline Failures

<b>Challenge</b>: Railway CLI deployment failures in GitHub Actions

<b>Solution</b>:
- Removed manual Railway deployment from CI/CD
- Leveraged Railway's native GitHub integration for auto-deployment

<b>Result</b>: Streamlined pipeline with automatic deployments on main branch pushes