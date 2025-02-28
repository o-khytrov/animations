from setup import *

tree_val = 0


def build_tree(levels, level=0):
    global tree_val
    root = {
        "val": tree_val,
        "children": []
    }
    tree_val += 1
    if levels == level:
        return root

    root["left"] = build_tree(levels, level + 1)
    root["right"] = build_tree(levels, level + 1)

    return root


class Tree(Scene):
    def dfs_visualization(self):
        g, tree = self.builld_graph()

        self.play(Create(g))

        def dfs(node, parent=None):
            if not node:
                return
            if parent:
                g.edges[(parent["val"], node["val"])].set_color(RED)
            g[node["val"]].set_color(RED)
            g._labels[node["val"]].set_color(WHITE)

            self.wait(0.4)
            if "left" in node:
                dfs(node["left"], node)
            if "right" in node:
                dfs(node["right"], node)

        dfs(tree)
        self.wait()

    def bfs_visualization(self):
        g, root = self.builld_graph()
        self.play(Create(g))

        stack = [(root, None)]
        while stack:
            node, parent = stack.pop(0)
            if parent:
                g.edges[(parent["val"], node["val"])].set_color(RED)
                self.wait(0.1)
            g[node["val"]].set_color(RED)
            g._labels[node["val"]].set_color(WHITE)
            self.wait(0.4)
            if "left" in node:
                stack.append((node["left"], node))
            if "right" in node:
                stack.append((node["right"], node))
        self.wait()

    def construct(self):
        self.bfs_visualization()

    def builld_graph(self):
        tree = build_tree(4)
        vertices = []
        edges = []

        def dfs(node):
            if not node:
                return
            vertices.append(node["val"])
            if "right" in node:
                edges.append((node["val"], node["right"]["val"]))
                dfs(node["right"])
            if "left" in node:
                edges.append((node["val"], node["left"]["val"]))
                dfs(node["left"])

        dfs(tree)
        g = Graph(vertices, edges, layout="tree", root_vertex=0, labels=True, layout_config={"vertex_spacing": (0.8, 1)}, label_fill_color=Green)
        return g, tree
