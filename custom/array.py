from manim import Table, VGroup, GREEN, BackgroundRectangle


class Array(Table):

    def __init__(self, array: []):
        self._array = array
        super().__init__([array], include_outer_lines=True)
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
