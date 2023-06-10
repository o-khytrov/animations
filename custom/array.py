from manim import *


class Array(Table):

    def __init__(self, array: [], **kwargs):
        self._array = array
        super().__init__([[str(e) for e in array]], include_outer_lines=True, **kwargs)
        self.scale(0.8)
        self._highlighted_elements = VGroup()

    def get_element_by_index(self, index: int):
        return self.get_cell((1, 1 + index))

    def highlight_element(self, index: int, highlight_color=GREEN):
        element = self.get_element_by_index(index)
        bg_cell = BackgroundRectangle(element, color=highlight_color)
        self._highlighted_elements.add(bg_cell)
        return bg_cell

    def clear_highlighted_elements(self):
        self._highlighted_elements = VGroup()

    @property
    def highlighted_elements(self):
        return self._highlighted_elements

    def swap(self, i1, i2):
        el1 = self.mob_table[0][i1]
        el2 = self.mob_table[0][i2]
        loc1 = el1.get_center()
        loc2 = el2.get_center()
        self.mob_table[0][i1] = el2
        self.mob_table[0][i2] = el1
        return Succession(AnimationGroup(el1.animate.shift(UP * 2),
                                         el2.animate.shift(UP * 2)),
                          AnimationGroup(el1.animate.move_to(loc2),
                                         el2.animate.move_to(loc1)))

    def get_subarray_elements(self, left, right):
        group = VGroup()
        for i in range(left, right + 1):
            try:
                group.add(self.mob_table[0][i])
            except:
                pass
        return group

    def get_subarray_surrounding_rectangle(self, start, end):
        subarray = self.get_subarray_group(start, end)
        return SurroundingRectangle(subarray)

    def get_subarray_group(self, start, end):
        subarray = VGroup()
        for i in range(start, end):
            subarray.add(self.get_element_by_index(i))
        return subarray
