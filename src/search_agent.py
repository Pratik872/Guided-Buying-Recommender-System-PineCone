from dataclasses import dataclass
import time
from config.constants import top_k


class SearchAgent:

    def __init__(self, pinecone_index, retriever_model, ner_engine):
        self.index = pinecone_index
        self.retriever = retriever_model
        self.ner = ner_engine

    def search(self, query: str, user_profile: dict):
        """Execute search with business logic"""
        #Generate Embedding for Query
        emb_query = self.retriever.encode(query).tolist()
        

        #Extract entities
        entities = self._extract_entities(query)
        

        #Apply business logic filters
        filters = self._apply_business_rules(user_profile, entities)
        
        #Measure search latency
        start_time = time.time()

        #Vector Search
        results = self.index.query(
            vector = emb_query,
            top_k = top_k,
            include_metadata = True,
            filter = filters
        )

        end_time = time.time()
        search_latency = (end_time - start_time) * 1000  # Convert to milliseconds

        search_results = []
        for match in results['matches']:
            result = {
                "id" : match['id'],
                "title":match['metadata']['title'],
                "price" : float(match['metadata']['price']),
                "stars" : float(match['metadata']['stars']),
                "reviews" : int(match['metadata']['reviews']),
                "isBestSeller" : match['metadata']['isBestSeller'],
                "boughtinLastMonth" : int(match['metadata']['boughtInLastMonth']),
                "productURL" : match['metadata']['productURL']
            }

            search_results.append(result)
        print(search_results)

        return search_results

    
    def _apply_business_rules(self, user_profile, entities):
        """Apply business logic for filtering"""
        filters ={}

        #Budget constraint
        if 'budget' in user_profile and user_profile['budget']:
            filters['price'] = {'$lte': user_profile['budget']}

        #Entity-based filtering
        if entities:
            filters['ner'] = {'$in': entities}

        #Role-based category filtering
        if 'categories' in user_profile:
            category_ids = self._get_category_ids(user_profile['categories'])
            if category_ids:
                filters['category_id'] = {'$in': category_ids}

        return filters
    
    
    def _get_category_ids(self, categories: list[str]) -> list[int]:
        """Map category names into IDs based on dataset"""

        category_mapping = {
            'electronics': [68, 69, 72, 73, 75],
            'computers': [57, 81],
            'accessories': [55, 56, 60, 63, 64, 65, 66, 71, 76]
        }

        ids = []

        for cat in categories:
            if cat.lower() in category_mapping:
                ids.extend(category_mapping[cat.lower()])

        return [int(id) for id in ids]

    
    def _extract_entities(self, text_query: str):
        """Extract named entities from query"""

        entities = []
        for item in self.ner(text_query):
            entities.append(item['word'])
        return list(set(entities)) if entities else []
    


    
