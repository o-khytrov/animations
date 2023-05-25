from manim import *


class Array(Table):

    def __init__(self, array: []):
        self._array = array
        super().__init__([array], include_outer_lines=True)
        self.scale(0.8)
        self._highlighted_elements = VGroup()

    def get_element_by_index(self, index: int):
        return self.get_cell((1, 1 + index))

    def highlight_element(self, index: int):
        element = self.get_element_by_index(index)
        bg_cell = BackgroundRectangle(element, color=YELLOW)
        self._highlighted_elements.add(bg_cell)
        return bg_cell

    @property
    def highlighted_elements(self):
        return self._highlighted_elements


class ArrayPointer(VGroup):

    def __init__(self, array: Array, name: str, color=WHITE, direction=UP, index=0):
        super().__init__()
        self._array = array
        self._direction = direction
        self._index = index
        self._name = name
        self._target_element = self._array.get_element_by_index(index)
        self._color = color

        self._text = Text(self.get_text(), color=self._color, font_size=25)

        self._arrow = Triangle(color=self._color, fill_color=self._color, fill_opacity=1).scale(0.1).rotate(
            -60 * DEGREES).next_to(self._text, self._direction * -1, buff=0.1)

        self._select_box = self._target_element.copy().scale(1.05).set_color(self._color)
        self._pointer = VGroup(self._text, self._arrow).next_to(self._target_element, direction, buff=0.2)
        super().add(self._pointer, self._select_box)

    def get_text(self):
        return f"{self._name}={self._index}"

    def move_to_index(self, index):
        self._index = index
        self._target_element = self._array.get_element_by_index(self._index)
        return AnimationGroup(self._pointer.animate.next_to(self._target_element, self._direction),
                              self._select_box.animate.move_to(self._target_element),
                              Transform(self._text,
                                        Text(self.get_text(), color=self._color, font_size=25).move_to(self._arrow,
                                                                                                       self._direction)))


class NeedleInHaystack(Scene):
    def construct(self):
        haystack = "mississippi"
        needle = "ssip"
        haystack_table = Array([c for c in haystack])
        needle_table = Array([c for c in needle]).next_to(haystack_table, UP)
        self.add(haystack_table)
        self.add(needle_table)

        needle_pointer = ArrayPointer(needle_table, "n", color=RED, direction=UP)
        haystack_pointer = ArrayPointer(haystack_table, "h", color=YELLOW, direction=DOWN)
        self.add(needle_pointer)
        self.add(haystack_pointer)

        i = 0
        n_index = 0
        while i < len(haystack):
            self.play(haystack_pointer.move_to_index(i))
            self.play(needle_pointer.move_to_index(n_index))

            if haystack[i] == needle[n_index]:
                self.add(needle_table.highlight_element(n_index))
                self.add(haystack_table.highlight_element(i))
                n_index += 1
            else:
                i = i - n_index
                n_index = 0
                for element in needle_table.highlighted_elements:
                    self.remove(element)
                for element in haystack_table.highlighted_elements:
                    self.remove(element)

            if n_index == len(needle):
                result = i - len(needle) + 1
                break
            i += 1

        self.wait()


if __name__ == "__main__":
    with tempconfig({"quality": "low_quality"}):
        scene = NeedleInHaystack()
        scene.render()
