class EvaluationFramework:
    def __init__(self):
        self.history = []
    def evaluate(self, query, response):
        relevance = 1 if any(w in response.lower() for w in query.lower().split()) else 0
        
        #Hallucination check (simple keyword absence check)
        has_sources= any(phrase in response.lower() for phrase in ["based on", "according to", "our policy", "from","in the"])
        result= {
            'query': query,
            'response': response,
            'relevance': relevance,
            'has_sources': has_sources,
            'quality' : 'good' if relevance and has_sources else 'needs_improvement'
        }
        self.history.append(result)
        return result
