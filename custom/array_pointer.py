from manim import VGroup, WHITE, UP, Triangle, DEGREES, DOWN, Text, AnimationGroup, RED, Wiggle, Succession, \
    DEFAULT_MOBJECT_TO_MOBJECT_BUFFER

from custom.array import Array
import numpy as np


class ArrayPointer(VGroup):

    def __init__(self, array: Array, name: str, color=WHITE, direction=UP, index=0, hide_name=False,
                 label_buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER):
        super().__init__()
        self._array = array
        self._direction = direction
        self._index = index
        self._name = name
        self._target_element = self._array.get_element_by_index(index)
        self._color = color
        self._select_box = self._target_element.copy().scale(1.05).set_color(self._color)

        self._arrow = Triangle(color=self._color, fill_color=self._color, fill_opacity=1).scale(0.1).rotate(
            -self.get_arrow_rotation_degree() * DEGREES).next_to(self._target_element, self._direction, buff=0.15)

        self._label = self.get_label()
        self._label.next_to(self._arrow, self._direction, buff=label_buff)

        def label_text_updater(label):
            label.become(self.get_label())
            self._label.next_to(self._arrow, self._direction, buff=label_buff)

        self._label.add_updater(label_text_updater)
        self._pointer = VGroup(self._label, self._arrow)
        super().add(self._pointer, self._select_box)

    def get_arrow_rotation_degree(self):
        if np.array_equal(self._direction, UP):
            return 60
        if np.array_equal(self._direction, DOWN):
            return 120

    def get_text(self):
        return f"{self._name}={self._index}"

    def get_label(self):
        return Text(self.get_text(), color=self._color, font_size=25)

    def move_to_index(self, index):
        self._select_box.set_color(self._color)
        self._index = index
        self._target_element = self._array.get_element_by_index(self._index)

        return AnimationGroup(self._arrow.animate.next_to(self._target_element, self._direction, buff=0.15),
                              self._select_box.animate.move_to(self._target_element).become(
                                  self._target_element.copy().scale(1.05).set_color(self._color)))

    def wiggle(self):
        self._select_box.set_color(RED)
        return Succession(AnimationGroup(Wiggle(self._select_box)),
                          AnimationGroup(self._select_box.animate.set_color(self._color)))
