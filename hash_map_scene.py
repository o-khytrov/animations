from manim import *

from custom.hash_map import HashMap


class HashMapDemo(Scene):
    def construct(self):
        hash_map = HashMap()
        self.add(hash_map)
        key_mobject = Text("Bob").to_edge(UP)
        value_mobject = Text("1").to_edge(UP)
        group = VGroup(key_mobject, value_mobject)
        group.arrange(RIGHT).to_edge(UP)
        self.play(Write(key_mobject))
        self.play(Write(value_mobject))

        hash_map.add_entry("Bob", "1", key_mobject.copy(), value_mobject.copy(), self)

        key_mobject2 = Text("Alice").to_edge(UP)
        value_mobject2 = Text("2").to_edge(UP)
        group2 = VGroup(key_mobject2, value_mobject2)
        group2.arrange(RIGHT).next_to(group)
        self.play(Write(key_mobject2))
        self.play(Write(value_mobject2))

        hash_map.add_entry("Alice", "2", key_mobject2.copy(), value_mobject2.copy(), self)
        self.wait()
