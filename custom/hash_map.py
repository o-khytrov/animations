from manim import *


class HashMap(VGroup):
    def __init__(self):
        super().__init__()
        self._map = {}
        self._mobject_map = {}
        self._vgroup = VGroup().next_to(self.get_center())
        rec = Rectangle(height=2)
        self._lb = Brace(rec, LEFT)
        self._rb = Brace(rec, RIGHT)
        self.add(self._vgroup, self._lb, self._rb)

    def add_entry(self, key, value, mobject_key: Mobject, mobject_value: Mobject, scene: Scene):
        self._map[key] = value
        separator = Text(":")
        scene.play(
            mobject_key.animate.next_to(self._vgroup.get_point_mobject(DL), DOWN).become(
                Text(key).next_to(self._vgroup, DOWN)),
            mobject_value.animate.next_to(self._vgroup, DOWN).become(Text(key).next_to(self._vgroup, DOWN))

        )

        self._vgroup.add(mobject_key, separator, mobject_value)
        self._vgroup.arrange_in_grid(rows=len(self._map), cols=3)
        scene.play(
            self._lb.animate.become(Brace(self._vgroup, LEFT)),
            self._rb.animate.become(Brace(self._vgroup, RIGHT)))
