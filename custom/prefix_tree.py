import pickle
import uuid

from setup import *

path_color = Purple


# config.pixel_height = 1920
# config.pixel_width = 1080
# config.frame_height = 16.0
# config.frame_width = 9.0


class TrieNode:
    def __init__(self, label=None):
        self.children = {}
        self.is_word = False
        self.id = str(uuid.uuid4())
        self.label = label


class Trie(Scene):
    def custom_vertex(self, node: TrieNode):
        circle = Circle(radius=0.4, color=Red if node.is_word else Green, fill_opacity=1)
        label = Text(str(node.label), font="Courier")
        label.move_to(circle.get_center())
        vgroup = VGroup(circle, label)

        vgroup.z_index = 10
        return vgroup

    def search_word(self, word, word_text=None):
        if not word_text:
            word_text = Text(word, font="Courier").to_edge(UP).to_edge(LEFT)
            self.play(Write(word_text))

        cur = self.root
        pointer = SurroundingRectangle(self.graph[self.root.id], color=path_color)
        letter_pointer = SurroundingRectangle(word_text[0], color=path_color)
        self.play(Create(pointer), Create(letter_pointer), run_time=0.1)
        path = VGroup()
        for i, c in enumerate(word):
            self.play(letter_pointer.animate.move_to(word_text[i].get_center()))
            if c not in cur.children:
                return
            child = cur.children[c]

            self.play(pointer.animate.move_to(self.graph[child.id].get_center()),
                      letter_pointer.animate.move_to(word_text[i].get_center()),
                      self.graph.edges[(cur.id, child.id)].animate.set_color(path_color),
                      self.graph.vertices[child.id][0].animate.set_color(path_color), run_time=0.1)

            path.add(self.graph.vertices[child.id])
            cur = child
        self.remove(pointer)
        self.remove(letter_pointer)
        if cur.is_word:
            self.play(Indicate(VGroup(path), color=None), Indicate(word_text, color=path_color), run_time=0.1)
        self.reset_graph_state()
        # self.remove(word_text)

    def autocomplete(self, query: str):
        cur = self.root
        self.reset_graph_state()
        text = Text(query, font="Courier").to_edge(LEFT + UP)

        cursor = Rectangle(
            color=GREY_A,
            fill_color=GREY_A,
            fill_opacity=1.0,
            height=text.height * 1.2,
            width=text[0].width / 2,
        ).move_to(text[0], aligned_edge=DOWN)  # Position the cursor

        self.play(TypeWithCursor(text, cursor))
        self.play(Blink(cursor, blinks=2))
        path = VGroup()

        def dfs(node: TrieNode):
            path.add(self.graph.vertices[node.id])
            for node_child in node.children.values():
                self.play(self.graph.edges[(node.id, node_child.id)].animate.set_color(path_color),
                          self.graph.vertices[node_child.id][0].animate.set_color(path_color),
                          self.graph.vertices[node_child.id][1].animate.set_color(WHITE),
                          run_time=0.1)
                dfs(node_child)

        for c in query:
            if c in cur.children:
                self.play(self.graph.edges[(cur.id, cur.children[c].id)].animate.set_color(path_color),
                          self.graph.vertices[cur.id][0].animate.set_color(path_color),
                          self.graph.vertices[cur.id][1].animate.set_color(WHITE),
                          run_time=0.1)
                path.add(self.graph.vertices[cur.id])
                cur = cur.children[c]
        self.play(self.graph.vertices[cur.id][0].animate.set_color(path_color),
                  self.graph.vertices[cur.id][1].animate.set_color(WHITE), run_time=0.1)
        path.add(self.graph.vertices[cur.id])
        dfs(cur)

        self.play(Indicate(VGroup(path), color=None, scale_factor=1.05))
        self.remove(cursor)
        text.fade(1)
        self.remove(text)

    def add_word_without_animation(self, word):
        cur = self.root
        for i, c in enumerate(word):
            if c not in cur.children:
                child = TrieNode(c)
                child.is_word = i == len(word) - 1
                cur.children[c] = child
                self.graph._labels.update({child.id: child.label})
                destination = self.graph[cur.id].get_center()
                self.graph.add_vertices(child.id,
                                        vertex_mobjects={
                                            child.id: self.custom_vertex(child)},
                                        positions={child.id: destination})
                self.graph.add_edges((cur.id, child.id))

            else:
                child = cur.children[c]
            self.node_map[(word, i)] = child.id

            cur = child
        self.update_graph()

    def add_word(self, word):
        word_text = Text(word, font="Courier").to_edge(UP).to_edge(LEFT)
        self.play(Write(word_text), run_time=0.1)

        cur = self.root
        pointer = SurroundingRectangle(self.graph[self.root.id], color=path_color)
        letter_pointer = SurroundingRectangle(word_text[0], color=path_color)
        pointer.add_updater(lambda r: r.move_to(self.graph[self.root.id].get_center()))
        self.play(Create(pointer), Create(letter_pointer), run_time=0.1)
        for i, c in enumerate(word):
            self.play(letter_pointer.animate.move_to(word_text[i].get_center()), run_time=0.1)

            if c not in cur.children:
                letter_copy = word_text[i].copy()
                self.play(letter_copy.animate.move_to(self.graph[cur.id].get_center()), run_time=0.1)
                self.remove(letter_copy)
                child = TrieNode(c)
                child.is_word = i == len(word) - 1
                cur.children[c] = child
                self.graph._labels.update({child.id: child.label})

                destination = self.graph[cur.id].get_center()

                # self.remove(letter_copy)
                self.graph.add_vertices(child.id,
                                        vertex_mobjects={
                                            child.id: self.custom_vertex(child)},
                                        positions={child.id: destination})

                self.graph.add_edges((cur.id, child.id))
                self.graph.edges[(cur.id, child.id)].set_color(path_color)
                self.graph.vertices[cur.id][0].set_color(path_color)
                self.update_graph()


            else:
                child = cur.children[c]
            self.node_map[(word, i)] = child.id
            pointer.clear_updaters()

            self.play(pointer.animate.move_to(self.graph[child.id].get_center()),
                      letter_pointer.animate.move_to(word_text[i].get_center()),
                      self.graph.edges[(cur.id, child.id)].animate.set_color(path_color),
                      self.graph.vertices[cur.id][0].animate.set_color(path_color), run_time=0.1)
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

    def update_graph(self):

        self.play(self.graph.animate.change_layout('tree', root_vertex=self.root.id,
                                                   layout_config={"vertex_spacing": (1, 1)}), run_time=0.1)
        if self.graph.height > config.frame_height:
            scale_factor = min(config.frame_width / self.graph.width, config.frame_height / self.graph.height)
            self.graph.scale(scale_factor)

    def construct(self):
        self.root = TrieNode('.')
        self.graph = Graph(vertices=[self.root.id], edges=[],
                           vertex_mobjects={self.root.id: self.custom_vertex(self.root)})
        self.play(Create(self.graph), run_time=0.1)
        self.node_map = {}
        self.words = [
            "car",
            "card",
            "carpet",
            "cat",
            "catalog",
            "castle",
            # "box",
            # "body",
            # "band",
            # "bank",
            # "banner",
            # "backend",
            # "banking",
        ]
        for word in self.words:
            self.add_word_without_animation(word)

        self.clear()

        # words_texts = self.create_graph_from_words()
        # for mob in words_texts:
        #     self.remove(mob)

        self.autocomplete_demo()

    def autocomplete_demo(self):
        target = "card"
        for i in range(1, len(target) + 1):
            self.autocomplete(target[:i])
            self.reset_graph_state()
        self.wait()

    def create_graph_from_words(self):
        prev_text = Text(self.words[0], font="Courier").to_edge(LEFT + UP)
        words_texts = [prev_text]
        writing_animation = [Write(prev_text)]
        for i in range(1, len(self.words)):
            text = Text(self.words[i], font="Courier").next_to(prev_text, direction=DOWN, buff=0.1, aligned_edge=LEFT)
            words_texts.append(text)
            writing_animation.append(Write(text))
            prev_text = text
        self.play(AnimationGroup(writing_animation))
        self.graph.next_to(VGroup(words_texts), direction=RIGHT, buff=0.2)
        animations = []
        for wi, word in enumerate(self.words):
            for i, c in enumerate(word):
                animations.append(words_texts[wi][i].copy().animate.become(self.graph[self.node_map[(word, i)]]))
        for edge in self.graph.edges:
            animations.append(Create(self.graph.edges[edge]))
        animations.append(Create(self.graph.vertices[self.root.id]))
        self.play(AnimationGroup(animations))
        self.reset_graph_state()
        # self.search_words(words, words_texts)
        self.wait()
        return words_texts

    def search_words(self, words, words_texts):
        for word, words_text in zip(words, words_texts):
            self.search_word(word, words_text)


if __name__ == "__main__":
    scene = Trie()
    scene.construct()
