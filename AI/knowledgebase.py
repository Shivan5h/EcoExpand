from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import networkx as nx
import matplotlib.pyplot as plt
import io
from fastapi.responses import StreamingResponse

# Initialize FastAPI app and NetworkX graph
app = FastAPI(title="Compliance Knowledge Graph API")
knowledge_graph = nx.DiGraph()

# Pydantic models for API requests
class Entity(BaseModel):
    name: str
    type: str

class Relation(BaseModel):
    source: str
    target: str
    relation: str

class GraphData(BaseModel):
    entities: List[Entity]
    relations: List[Relation]

# API Endpoints

@app.post("/add_entities/")
def add_entities(entities: List[Entity]):
    """Add entities to the knowledge graph."""
    for entity in entities:
        knowledge_graph.add_node(entity.name, type=entity.type)
    return {"message": f"{len(entities)} entities added successfully."}

@app.post("/add_relations/")
def add_relations(relations: List[Relation]):
    """Add relations to the knowledge graph."""
    for relation in relations:
        if not knowledge_graph.has_node(relation.source) or not knowledge_graph.has_node(relation.target):
            raise HTTPException(status_code=404, detail="Source or target entity not found.")
        knowledge_graph.add_edge(relation.source, relation.target, relation=relation.relation)
    return {"message": f"{len(relations)} relations added successfully."}

@app.get("/get_graph/")
def get_graph():
    """Retrieve the knowledge graph as a dictionary."""
    nodes = [{"name": node, **data} for node, data in knowledge_graph.nodes(data=True)]
    edges = [{"source": u, "target": v, "relation": data["relation"]} for u, v, data in knowledge_graph.edges(data=True)]
    return {"nodes": nodes, "edges": edges}

@app.get("/visualize_graph/")
def visualize_graph():
    """Visualize the knowledge graph as an image."""
    pos = nx.spring_layout(knowledge_graph)
    plt.figure(figsize=(12, 8))
    nx.draw_networkx_nodes(knowledge_graph, pos, node_size=1500, node_color="lightblue")
    nx.draw_networkx_labels(knowledge_graph, pos, font_size=10)
    nx.draw_networkx_edges(knowledge_graph, pos, arrowstyle="->", arrowsize=20, edge_color="gray")
    edge_labels = nx.get_edge_attributes(knowledge_graph, "relation")
    nx.draw_networkx_edge_labels(knowledge_graph, pos, edge_labels=edge_labels, font_size=8)
    plt.title("Knowledge Graph Visualization")
    plt.axis("off")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return StreamingResponse(buf, media_type="image/png")

@app.post("/bulk_upload/")
def bulk_upload(graph_data: GraphData):
    """Add entities and relations in bulk."""
    add_entities(graph_data.entities)
    add_relations(graph_data.relations)
    return {"message": "Graph data uploaded successfully."}

@app.delete("/clear_graph/")
def clear_graph():
    """Clear the entire knowledge graph."""
    knowledge_graph.clear()
    return {"message": "Knowledge graph cleared successfully."}

