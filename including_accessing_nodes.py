import networkx as nx
import plotly.graph_objects as go
from collections import defaultdict
import heapq

class Graph:
    def __init__(self):
        self.large_graph = nx.Graph()
        self.small_graphs = defaultdict(nx.Graph)

    def add_vertex(self, vertex, **properties):
        self.large_graph.add_node(vertex, **properties)

        matching_vertices = self.find_matching_vertices(vertex)
        if matching_vertices:
            for matching_vertex in matching_vertices:
                self.large_graph.add_edge(matching_vertex, vertex)
        else:
            tags = properties.get("tag")
            if isinstance(tags, list):
                for tag in tags:
                    if self.large_graph.has_node(tag):
                        self.large_graph.add_edge(tag, vertex)
                    else:
                        self.large_graph.add_edge("Brain", vertex)
            else:
                if tags is not None:
                    if self.large_graph.has_node(tags):
                        self.large_graph.add_edge(tags, vertex)
                    else:
                        self.large_graph.add_edge("Brain", vertex)
                else:
                    self.large_graph.add_edge("Brain", vertex)

    def find_matching_vertices(self, vertex):
        if vertex not in self.large_graph.nodes:
            return []  # Return an empty list if the vertex does not exist in the graph

        vertex_tags = self.large_graph.nodes[vertex].get("tag")
        # vertex_names = list(self.large_graph.nodes())
        matching_vertices = []
        for v, data in self.large_graph.nodes(data=True):
            if v != vertex and data.get("tag") is not None and vertex_tags is not None and (
                    isinstance(vertex_tags, list) and (data.get("tag") in vertex_tags or data.get("tag") == v)
                    or (isinstance(vertex_tags, str) and (data.get("tag") == vertex_tags or data.get("tag") == v))):
                matching_vertices.append(v)
        return matching_vertices

    def connect_last_nodes_to_brain(self):
        last_nodes = []
        for small_graph in self.small_graphs.values():
            last_node = list(small_graph.nodes)[-1]
            last_nodes.append(last_node)

        for last_node in last_nodes:
            if last_node != "Brain":
                self.large_graph.add_edge(last_node, "Brain")

    def print_graph(self):
        self.connect_last_nodes_to_brain()

        fig = go.Figure()

        # Calculate the positions of the nodes using the spring layout algorithm
        pos = nx.spring_layout(self.large_graph)

        # Add nodes to the figure
        for node, position in pos.items():
            # Get the tags of the node
            tags = self.large_graph.nodes[node].get("tag")

            # Determine the color based on the tags
            color = generate_color(tags, self.large_graph)

            # Determine the text color based on the background color
            text_color = "white" if is_color_dark(color) else "black"

            # Set the size, color, and text color of the node
            fig.add_trace(go.Scatter(x=[position[0]], y=[position[1]], mode='markers', name=node,
                                     marker=dict(size=50, color=color, symbol='circle'),
                                     textfont=dict(color=text_color)))
            # Add the node label
            fig.add_annotation(x=position[0], y=position[1], text=node, showarrow=False,
                               font=dict(size=14, color=text_color))

        # Add edges to the figure
        for edge in self.large_graph.edges:
            x0, y0 = pos[edge[0]][0], pos[edge[0]][1]
            x1, y1 = pos[edge[1]][0], pos[edge[1]][1]
            fig.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1], mode='lines'))

        # Set layout options for a better visualization
        fig.update_layout(showlegend=False, hovermode='closest', title='Graph Visualization')

        # Display the graph
        fig.show()

# ANUSWETHAA ##
    def heuristic(self,node1, node2):
        pos = nx.spring_layout(self.large_graph)
        # Calculate the heuristic value as the Euclidean distance between the nodes
        x1, y1 = pos[node1]
        x2, y2 = pos[node2]
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def a_star(self, start, goal):
        # Initialize the open and closed sets
        open_set = []
        closed_set = set()

        # Create a dictionary to keep track of the parent of each node
        parent = {}

        # Create a dictionary to keep track of the cost of each node
        cost = {}
        cost[start] = 0

        # Calculate the heuristic value for the start node
        h = self.heuristic(start, goal)

        # Add the start node to the open set
        heapq.heappush(open_set, (h, start))

        while open_set:
            # Pop the node with the lowest f score from the open set
            current = heapq.heappop(open_set)[1]

            # If we have reached the goal node, reconstruct the path and return it
            if current == goal:
                path = [current]
                while current in parent:
                    current = parent[current]
                    path.append(current)
                path.reverse()
                return path

            # Add the current node to the closed set
            closed_set.add(current)

            # Explore the neighbors of the current node
            for neighbor in graph.large_graph.neighbors(current):
                # If the neighbor is already in the closed set, skip it
                if neighbor in closed_set:
                    continue

                # Calculate the tentative cost to reach the neighbor from the start node
                tentative_cost = cost[current] + graph.large_graph[current][neighbor].get("weight", 1)

                # If the neighbor is not in the open set, add it
                if neighbor not in [node[1] for node in open_set]:
                    heapq.heappush(open_set, (tentative_cost + self.heuristic(neighbor, goal), neighbor))

                # If the neighbor is in the open set but the tentative cost is greater than the current cost, skip it
                elif tentative_cost >= cost[neighbor]:
                    continue

                # Update the parent and cost dictionaries
                parent[neighbor] = current
                cost[neighbor] = tentative_cost

        # If we have explored all the nodes and haven't found the goal node, return None
        return None

# SHESHU ##

    def access_vertex_by_name(self, vertex_name):
        visited = set()

        def dfs(node):
            visited.add(node)
            if node == vertex_name:
                return True
            for neighbor in self.large_graph.neighbors(node):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
            return False

        for node in self.large_graph.nodes:
            if node not in visited:
                if dfs(node):
                    return True

        return False




def generate_color(tags, graph):
    # Map tags to colors
    color_map = {
        "Sense": "rgb(144, 238, 144)",  # lightgreen
        "Motor": "rgb(255, 215, 0)",  # gold
        "Cognitive": "rgb(255, 192, 203)",  # pink
        "Work": "rgb(255, 165, 0)"  # orange
        # Add more tag-color mappings here
    }

    # Check if tags is None
    if isinstance(tags, list):
        # Initialize the color to white
        mixed_color = "rgb(255, 255, 255)"

        # Iterate over the tags and mix the colors
        for tag in tags:
            if tag in color_map.keys():
                color = color_map[tag]
                mixed_color = mix_colors(mixed_color, color)

        return mixed_color
    elif isinstance(tags, str):
        # Check if the tag matches with any tag in the graph
        if tags in color_map.keys():
            return color_map[tags]

        # Check if the tag is the name of a vertex in the graph
        if graph.has_node(tags):
            node_tags = graph.nodes[tags].get("tag")
            if isinstance(node_tags, list):
                # Initialize the color to white
                mixed_color = "rgb(255, 255, 255)"

                # Iterate over the tags of the node and mix the colors
                for tag in node_tags:
                    if tag in color_map.keys():
                        color = color_map[tag]
                        mixed_color = mix_colors(mixed_color, color)

                return mixed_color
            elif node_tags in color_map.keys():
                return color_map[node_tags]

    return "rgb(173, 216, 230)"  # lightblue


def mix_colors(color1, color2):
    # Extract the RGB values from the colors
    r1, g1, b1 = color1[4:-1].split(",")
    r2, g2, b2 = color2[4:-1].split(",")

    # Calculate the average of the RGB values
    r = (int(r1) + int(r2)) // 2
    g = (int(g1) + int(g2)) // 2
    b = (int(b1) + int(b2)) // 2

    # Return the mixed color
    return f"rgb({r}, {g}, {b})"


def is_color_dark(color):
    # Extract the RGB values from the color
    r, g, b = color[4:-1].split(",")

    # Convert the RGB values to integers
    r, g, b = int(r), int(g), int(b)

    # Calculate the relative luminance of the color
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255

    # Return True if the color is dark, False otherwise
    return luminance < 0.5


graph = Graph()

graph.add_vertex("HEARING", tag="Sense")
graph.add_vertex("TASTE", tag="Sense")
graph.add_vertex("LOCOMOTION", tag="Motor")
graph.add_vertex("SMELL", tag="Sense")
graph.add_vertex("TOUCH", tag="Sense")
graph.add_vertex("SPEECH", tag="Motor")
graph.add_vertex("THINKING", tag="Cognitive")
graph.add_vertex("EMOTIONS", tag="Cognitive")
# graph.add_vertex("My vertex", tag="SPEECH")
graph.add_vertex("Singing", tag=["SPEECH", "HEARING"])
# desired_vertex_name = "Singing"
# desired_vertex = graph.access_vertex_by_name(desired_vertex_name)

# print(desired_vertex_name)
# print(desired_vertex)
# graph.print_graph()
