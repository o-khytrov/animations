import uuid

from setup import *

path_color = Purple

config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 16.0
config.frame_width = 9.0


class TrieNode:
    def __init__(self, label=None):
        self.children = {}
        self.is_word = False
        self.id = str(uuid.uuid4())
        self.label = label


class Trie(Scene):
    def custom_vertex(self, vertex, is_end=False):
        circle = Circle(radius=0.4, color=Red if is_end else Green, fill_opacity=1)
        label = vertex if type(vertex) is Text else Text(str(vertex), font="Courier")
        label.move_to(circle.get_center())
        vgroup = VGroup(circle, label)

        vgroup.z_index = 10
        return vgroup

    def search_word(self, word):
        word_text = Text(word, font="Courier").to_edge(UP).to_edge(LEFT)
        self.play(Write(word_text))
        cur = self.root
        pointer = SurroundingRectangle(self.graph[self.root.id], color=path_color)
        letter_pointer = SurroundingRectangle(word_text[0], color=path_color)
        self.play(Create(pointer), Create(letter_pointer))
        path = VGroup()
        for i, c in enumerate(word):
            self.play(letter_pointer.animate.move_to(word_text[i].get_center()))
            if c not in cur.children:
                return
            child = cur.children[c]

            self.play(pointer.animate.move_to(self.graph[child.id].get_center()),
                      letter_pointer.animate.move_to(word_text[i].get_center()),
                      self.graph.edges[(cur.id, child.id)].animate.set_color(path_color),
                      self.graph.vertices[child.id][0].animate.set_color(path_color))

            path.add(self.graph.vertices[child.id])
            cur = child
        self.remove(pointer)
        self.remove(letter_pointer)
        if cur.is_word:
            self.play(Indicate(VGroup(path), color=None))
        self.reset_graph_state()

    def add_word(self, word):

        word_text = Text(word, font="Courier").to_edge(UP).to_edge(LEFT)
        self.play(Write(word_text))
        cur = self.root
        pointer = SurroundingRectangle(self.graph[self.root.id], color=path_color)
        letter_pointer = SurroundingRectangle(word_text[0], color=path_color)
        pointer.add_updater(lambda r: r.move_to(self.graph[self.root.id].get_center()))
        self.play(Create(pointer), Create(letter_pointer))
        for i, c in enumerate(word):
            self.play(letter_pointer.animate.move_to(word_text[i].get_center()))
            letter_copy = word_text[i].copy()
            self.play(letter_copy.animate.move_to(self.graph[cur.id].get_center()))
            self.remove(letter_copy)
            if c not in cur.children:
                child = TrieNode(c)
                cur.children[c] = child
                self.graph._labels.update({child.id: child.label})

                destination = self.graph[cur.id].get_center()

                # self.remove(letter_copy)
                self.graph.add_vertices(child.id,
                                        vertex_mobjects={
                                            child.id: self.custom_vertex(child.label, is_end=i == len(word) - 1)},
                                        positions={child.id: destination})

                self.graph.add_edges((cur.id, child.id))
                self.graph.edges[(cur.id, child.id)].set_color(path_color)
                self.graph.vertices[cur.id][0].set_color(path_color)

                self.play(self.graph.animate.change_layout('tree', root_vertex=self.root.id,
                                                           layout_config={"vertex_spacing": (1, 1)}))


            else:
                child = cur.children[c]
            pointer.clear_updaters()
            self.graph.edges[(cur.id, child.id)].set_color(path_color)
            self.graph.vertices[cur.id][0].set_color(path_color)
            self.play(pointer.animate.move_to(self.graph[child.id].get_center()),
                      letter_pointer.animate.move_to(word_text[i].get_center()))
            pointer.add_updater(lambda r: r.move_to(self.graph[child.id].get_center()))

            cur = child
        cur.is_word = True
        self.remove(pointer)
        self.remove(word_text)
        self.remove(letter_pointer)
        self.reset_graph_state()

    def reset_graph_state(self):
        for edge in self.graph.edges:
            self.graph.edges[edge].set_color(WHITE)

        def reset_colors_dfs(node: TrieNode):
            self.graph[node.id][0].set_color(Red if node.is_word else Green)
            for child in node.children.values():
                reset_colors_dfs(child)

        reset_colors_dfs(self.root)

    def construct(self):
        self.root = TrieNode('.')
        self.graph = Graph(vertices=[self.root.id], edges=[],
                           vertex_mobjects={self.root.id: self.custom_vertex(Text(self.root.label))})
        self.play(Create(self.graph))
        self.add_word("apple")
        self.add_word("banana")
        self.add_word("box")
        self.add_word("body")
        self.add_word("application")
        self.add_word("band")

        self.search_word("band")
        self.wait()


if __name__ == "__main__":
    scene = Trie()
    scene.construct()
