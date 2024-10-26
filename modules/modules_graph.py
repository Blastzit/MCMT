import pandas as pd
import networkx as nx
from bokeh.io import show, save, output_file
from bokeh.plotting import figure, from_networkx
from bokeh.models import Range1d, MultiLine, Circle, NodesAndLinkedEdges
from bokeh.palettes import Spectral4, Spectral8
from .models import Module, Keyword
from .utils import get_short_module_code

# Parameters

edge_multiplier = 400 # larger means more repulsion
min_radius = 0.01
max_radius = 0.1
k = 2.1 # spring constant
size = 600

def generate_nx_graph():
    pre_modules = Module.objects.values_list('code', flat=True)
    
    modules = []
    modules_keywords = {}
    for module in pre_modules:
        keywords = Keyword.objects.filter(module_code=get_short_module_code(module)).values_list('keywords', flat=True)
        if keywords:
            modules.append(module)
            modules_keywords[module] = list(keywords)

    df = pd.DataFrame(0, index=modules, columns=modules, dtype=float)
    G = nx.Graph()

    for module1 in modules:
        G.add_node(module1)
        for module2 in modules:
            if module1 != module2:
                keywords1 = set(modules_keywords[module1])
                keywords2 = set(modules_keywords[module2])
                common_keywords = keywords1.intersection(keywords2)
                union_keywords = keywords1.union(keywords2)
                weight = len(common_keywords) / len(union_keywords) * edge_multiplier if len(union_keywords) > 0 else 0
                df.at[module1, module2] = weight

                if weight > 0:
                    G.add_edge(module1, module2, weight=weight)

    # Radius calculation

    weights = {node: [data['weight'] for _, _, data in G.edges(node, data=True)] for node in G.nodes()}
    mean_weights = {node: sum(w) / len(w) if len(w) > 0 else 0 for node, w in weights.items()}
    max_mean_weight = max(mean_weights.values())

    radius_scale = {node: min_radius + (max_radius - min_radius) * (mean_weight / max_mean_weight) for node, mean_weight in mean_weights.items()}

    # Community detection

    communities = nx.community.louvain_communities(G, seed=42)

    modularity_class = {}
    modularity_color = {}

    for community_number, community in enumerate(communities):
        for name in community: 
            modularity_class[name] = community_number
            modularity_color[name] = Spectral8[community_number]

    # Node attributes

    module_names = Module.objects.values_list('code', 'name')
    module_names = {code: name for code, name in module_names}
    names = {node: module_names[node] if node in module_names.keys() else '' for node in G.nodes()}

    nx.set_node_attributes(G, names, 'name')
    nx.set_node_attributes(G, mean_weights, 'weight')
    nx.set_node_attributes(G, radius_scale, 'radius')
    nx.set_node_attributes(G, modularity_class, 'modularity_class')
    nx.set_node_attributes(G, modularity_color, 'modularity_color')
    nx.set_node_attributes(G, 1, 'line_width')

    return G

def generate_bokeh_plot(G):
    HOVER_TOOLTIPS = [("Module", "@index"), ("Name", "@name"), ("Total Weight", "@weight")]

    plot = figure(tooltips=HOVER_TOOLTIPS,
                tools="pan,wheel_zoom", active_scroll='wheel_zoom', toolbar_location=None,
                x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1), width=size, height=size, sizing_mode='scale_width')
    plot.axis.visible=False

    graph_renderer = from_networkx(G, nx.spring_layout, scale=1, center=(0, 0), k=k)

    graph_renderer.node_renderer.glyph = Circle(radius='radius', fill_color='modularity_color', line_width='line_width')
    graph_renderer.node_renderer.hover_glyph = Circle(radius='radius', fill_color='modularity_color', line_width='line_width')

    graph_renderer.edge_renderer.glyph = MultiLine(line_color="#CCCCCC", line_alpha=0.8, line_width=1)
    graph_renderer.edge_renderer.selection_glyph = MultiLine(line_color=Spectral4[2], line_width=2)
    graph_renderer.edge_renderer.hover_glyph = MultiLine(line_color=Spectral4[1], line_width=2)

    graph_renderer.selection_policy = NodesAndLinkedEdges()
    graph_renderer.inspection_policy = NodesAndLinkedEdges()

    plot.renderers.append(graph_renderer)

    return plot, graph_renderer

def lighten_color(color, amount=0.5):
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return mc.to_hex(colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2]))

def highlight_modules(G, plot, graph_renderer, module_codes):
    if module_codes != []:
        node_color = [G.nodes[node]['modularity_color'] if node in module_codes else lighten_color(G.nodes[node]['modularity_color'], 0.2) for node in G.nodes()]
        line_width = [2 if node in module_codes else 1 for node in G.nodes()]
        graph_renderer.node_renderer.data_source.data['node_color'] = node_color
        graph_renderer.node_renderer.data_source.data['line_width'] = line_width
        graph_renderer.node_renderer.glyph = Circle(radius='radius', fill_color='node_color', line_width='line_width')
        graph_renderer.node_renderer.hover_glyph = Circle(radius='radius', fill_color='node_color', line_width='line_width')
    else:
        line_width = [1 for _ in G.nodes()]
        graph_renderer.node_renderer.glyph = Circle(radius='radius', fill_color='modularity_color')
        graph_renderer.node_renderer.hover_glyph = Circle(radius='radius', fill_color='modularity_color')
    plot.renderers = [graph_renderer]

    output_file("modules_network.html")
    save(plot)

G = generate_nx_graph()
plot, graph_renderer = generate_bokeh_plot(G)
output_file("modules_network.html")
save(plot)
# highlight_modules(G, plot, graph_renderer, ['MATH50008'])
# show(plot)