from typing import List, Dict, Any
import json
from config.constants import *


class RecommendationAgent:

    def __init__(self, pinecone_index, retriever_model):

        self.index = pinecone_index
        self.retriever = retriever_model

        # Product bundle rules
        self.bundle_rules = {
            'laptop': ['mouse', 'keyboard', 'monitor', 'headphones', 'usb', 'charger'],
            'monitor': ['cable', 'stand', 'keyboard', 'mouse'],
            'keyboard': ['mouse', 'pad', 'wrist'],
            'mouse': ['pad', 'keyboard'],
            'printer': ['paper', 'cartridge', 'cable'],
            'phone': ['case', 'charger', 'cable', 'headphones'],
            'tablet': ['case', 'stylus', 'keyboard', 'charger']
        }

        # Price thresholds for recommendations
        self.price_ranges = {
            'budget': (0, 100),
            'mid': (100, 500),
            'premium': (500, float('inf'))
        }

    def recommend_bundles(self, search_results: list[dict], user_profile: dict) -> list[dict]:
        """Generate bundle recommendation based on search results"""
        recommendations = []

        for product in search_results[:3]: #Top 3 products
            bundle = self._create_bundle(product, user_profile)
            if bundle:
                recommendations.append(bundle)

        return recommendations


    def _create_bundle(self, main_product:dict, user_profile:dict) -> dict:
        """Create bundle for main product"""
        #Detect product category
        category = self._detect_category(main_product['title'])

        if category not in self.bundle_rules:
            return None
        
        #Find accessories
        accessories = self._find_accessories(
            category,
            main_product,
            user_profile
        )

        if not accessories:
            return None
        
        #Calculate bundle price and savings
        total_price = main_product['price'] + sum(acc['price'] for acc in accessories)
        individual_price = total_price
        savings = individual_price * 0.05  #5% discount on bundle

        return {
            "main_product": main_product,
            "accessories": accessories,
            "total_price": total_price - savings,
            "savings": savings
            }


    def _detect_category(self, title:str) -> str:
        """Detect Product category from title"""
        title_lower = title.lower()
        
        categories = {
            'laptop': ['laptop', 'notebook', 'macbook'],
            'monitor': ['monitor', 'display', 'screen'],
            'keyboard': ['keyboard'],
            'mouse': ['mouse'],
            'printer': ['printer'],
            'phone': ['phone', 'iphone', 'smartphone'],
            'tablet': ['tablet', 'ipad']
        }
        
        for category, keywords in categories.items():
            if any(keyword in title_lower for keyword in keywords):
                return category
        
        return 'electronics'


    def _find_accessories(self, category: str, main_product: dict, user_profile: dict) -> list[dict]:
        """Find accessories for the main product"""
        accessory_keywords = self.bundle_rules.get(category, [])
        accessories = []
        
        budget_remaining = user_profile['budget'] - main_product['price']
        if budget_remaining <= 50:  # Need at least $50 for accessories
            return []
        
        for keyword in accessory_keywords[:3]:  # Limit to 3 accessories
            accessory = self._search_accessory(keyword, budget_remaining // 3)
            if accessory:
                accessories.append(accessory)
        
        return accessories
    
    def _search_accessory(self, keyword: str, max_price: float) -> Dict:
        """Search for specific accessory"""
        try:
            # Generate embedding for accessory search
            emb_query = self.retriever.encode(keyword).tolist()
            
            # Search with price constraint
            results = self.index.query(
                vector=emb_query,
                top_k=5,
                include_metadata=True,
                filter={'price': {'$lte': max_price, '$gt': 10}}
            )
            
            if results['matches']:
                match = results['matches'][0]['metadata']
                return {
                    'id': results['matches'][0]['id'],
                    'title': match['title'],
                    'price': float(match['price']),
                    'productURL': match['productURL']
                }
        except:
            pass
        
        return None
    
    def recommend_alternatives(self, product:dict, user_profile: dict) -> list[dict]:
        """Find alternative products in same category"""

        try:
            #Search for similar products
            emb_query = self.retriever.encode(product['title']).tolist()

            results = self.index.query(
                vector = emb_query,
                top_k = top_k,
                include_metadata = True,
                filter = {
                    'price': {
                        '$lte': user_profile['budget'],
                        '$gte': product['price'] * 0.7  #70% of original price
                    }
                }
            )

            alternatives = []
            for match in results['matches'][1:4]: #Skip first product as it is same one
                alternatives.append({
                    'id': match['id'],
                    'title': match['metadata']['title'],
                    'price': float(match['metadata']['price']),
                    'score': float(match['score']),
                    'productURL': match['metadata']['productURL']
                })

            return alternatives
        
        except:
            return []