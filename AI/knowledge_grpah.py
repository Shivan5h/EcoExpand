import spacy
import networkx as nx
from typing import List, Tuple
import matplotlib.pyplot as plt

# Load a pre-trained NLP model (spaCy's English model for Named Entity Recognition)
nlp = spacy.load("en_core_web_sm")

# Example dataset: Regulations, incentives, and compliance information
data = [
    {
        "text": "The RoDTEP scheme provides duty drawback incentives for exporters in India.",
        "entities": [("RoDTEP scheme", "Scheme"), ("duty drawback", "Incentive"), ("India", "Country")],
        "relations": [("RoDTEP scheme", "provides", "duty drawback"), ("duty drawback", "applies to", "India")],
    },
    {
        "text": "Exporters to Europe must comply with CE marking regulations.",
        "entities": [("Europe", "Region"), ("CE marking regulations", "Regulation")],
        "relations": [("CE marking regulations", "applies to", "Europe")],
    },
    {
        "text": "The US offers tax incentives for green energy products.",
        "entities": [("US", "Country"), ("tax incentives", "Incentive"), ("green energy products", "Product")],
        "relations": [("US", "offers", "tax incentives"), ("tax incentives", "targets", "green energy products")],
    },
]

# Function to create a knowledge graph
def build_knowledge_graph(data: List[dict]) -> nx.DiGraph:
    graph = nx.DiGraph()  # Directed graph
    for item in data:
        # Add entities as nodes
        for entity, entity_type in item["entities"]:
            graph.add_node(entity, type=entity_type)
        # Add relationships as edges
        for source, relation, target in item["relations"]:
            graph.add_edge(source, target, relation=relation)
    return graph

# Function to visualize the knowledge graph
def visualize_knowledge_graph(graph: nx.DiGraph):
    pos = nx.spring_layout(graph)  # Layout for graph visualization
    plt.figure(figsize=(12, 8))
    # Draw nodes with labels
    nx.draw_networkx_nodes(graph, pos, node_size=1500, node_color="lightblue")
    nx.draw_networkx_labels(graph, pos, font_size=10)
    # Draw edges with labels
    nx.draw_networkx_edges(graph, pos, arrowstyle="->", arrowsize=20, edge_color="gray")
    edge_labels = nx.get_edge_attributes(graph, "relation")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8)
    plt.title("Knowledge Graph for Compliance Data")
    plt.axis("off")
    plt.show()

# Build and visualize the knowledge graph
knowledge_graph = build_knowledge_graph(data)
visualize_knowledge_graph(knowledge_graph)
