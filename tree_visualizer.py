from graphviz import Digraph


def visualize_tree(root, filename="tree"):
    """
    Visualize the tree structure using graphviz.

    Args:
        root: The root node of the tree
        filename: Name of the output file (without extension)
    """
    dot = Digraph(comment="Tree Visualization")
    dot.attr(rankdir="TB")  # Top to Bottom direction

    # Set default node and edge styles
    dot.attr("node", shape="circle", style="filled", fillcolor="lightblue")
    dot.attr("edge", color="gray50")

    def add_nodes_edges(node, node_id="0", parent_char=""):
        # Add current node
        if node_id == "0":
            node_label = "ROOT"
            fillcolor = "lightgreen"
        else:
            node_label = parent_char
            fillcolor = "lightpink" if node.is_terminal else "lightblue"

        dot.node(node_id, node_label, fillcolor=fillcolor)

        # Add children
        for i, (key, child) in enumerate(node.childrens.items()):
            child_id = f"{node_id}_{i}"
            add_nodes_edges(child, child_id, key)
            dot.edge(node_id, child_id, label=key)

    add_nodes_edges(root)
    dot.render(filename, view=True, format="png")
