
import dash
from dash import dcc, html
import dash_daq as daq
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from dash.dependencies import Input, Output
import json

app = dash.Dash(__name__)

# Load configuration
with open('./data/building_config.json') as f:
    config = json.load(f)

# Setup graph
G = nx.Graph()
for room_id, coord in config['doors'].items():
    G.add_node(f"door-{room_id}", pos=(coord['x'], coord['y']))
for stair_id, coord in config['stairs'].items():
    G.add_node(stair_id, pos=(coord['x'], coord['y']))

# Layout
app.layout = html.Div([
    html.H1("Navigator Simulation"),
    dcc.Graph(id="graph"),
    daq.LEDDisplay(id="correct-count", label="Correct Paths", value="0"),
    daq.LEDDisplay(id="wrong-count", label="Wrong Paths", value="0"),
])

@app.callback(
    Output("graph", "figure"),
    Input("graph", "id")
)
def update_graph(_):
    pos = nx.get_node_attributes(G, 'pos')
    fig, ax = plt.subplots(figsize=(6, 6))
    nx.draw(G, pos, ax=ax, with_labels=True, node_color="lightblue", node_size=300)
    return {"data": [], "layout": {"title": "Navigation Graph"}}

if __name__ == "__main__":
    app.run_server(debug=True)
