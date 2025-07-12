from typing import List, Dict, Any
from src.search_agent import SearchAgent
from src.recommendation_agent import RecommendationAgent
from src.logging.logger import logging

class GBRSystem:
    
    def __init__(self, pinecone_index, retriever_model, ner_engine):

        self.search_agent = SearchAgent(pinecone_index, retriever_model, ner_engine)
        self.recommendation_agent = RecommendationAgent(pinecone_index, retriever_model)


    def process_query(self, query: str, user_profile: dict) -> dict:
        """Complete GBR workflow: search + recommendations"""

        #Step 1: Search for products
        search_results = self.search_agent.search(query, user_profile)
        logging.info(f"GBRSystem > process_query: Searching products finished")

        #Step2: Generate Recommendations
        bundles = self.recommendation_agent.recommend_bundles(search_results, user_profile)
        logging.info(f"GBRSystem > process_query: Recommendations achieved")

        #Step3: Find Alternatives for top product
        alternatives = []
        if search_results:
            alternatives = self.recommendation_agent.recommend_alternatives(search_results[0], user_profile)

        return {
            "search_results": search_results,
            "bundles": bundles,
            "alternatives": alternatives,
            "user_profile": user_profile
        }
        