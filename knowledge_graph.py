import networkx as nx

class SimpleKnowledgeGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self._build_graph()

    def _build_graph(self):
        #nodes
        nodes= [("Product", {"type":"entity"}), ("Refund Policy", {"type":"policy"}),
                ("Shipping Info", {"type":"policy"}), ("Warranty", {"type":"service"}),("Support_Team", {"type":"department"})]
        #edges(Relationships)
        edges = [("Product", "Refund Policy", {"relation":"covered_by"}),
                 ("Product", "Warranty", {"relation":"has"}),
                 ("Refund_Policy", "Support_Team", {"relation":"managed_by"}),
                 ("Shipping_Policy", "Support_Team", {"relation":"managed_by"})]
        
        
        
        # Example structure
        self.graph.add_nodes_from(nodes)
        self.graph.add_edges_from(edges)
        

    def query_entity(self, entity):
        if entity in self.graph:
            return {"entity": entity,
                    "attributes": dict(self.graph.nodes[entity]),
                    "relations": list(self.graph.neighbors(entity))
                   }
        return {"error":f"Entity '{entity}' not found"}