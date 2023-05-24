from manim import *


class ArrayPointer(VGroup):
    def __init__(self, table: Table, text: str, color=WHITE, direction=UP):
        super().__init__()
        self._table = table
        self._direction = direction
        target_cell = self._table.get_cell((1, 1))

        self._text = Text(text, color=color, font_size=25)

        self._arrow = Triangle(color=color, fill_color=color, fill_opacity=1).scale(0.1).rotate(
            -60 * DEGREES).next_to(self._text, self._direction * -1, buff=0.1)

        self._select_box = target_cell.copy().scale(1.05).set_color(color)
        self._pointer = VGroup(self._text, self._arrow).next_to(target_cell, direction, buff=0.2)
        super().add(self._pointer, self._select_box)

    def MoveTo(self, cell_index):
        next_cell = self._table.get_cell(cell_index)
        return AnimationGroup(self._pointer.animate.next_to(next_cell, self._direction),
                              self._select_box.animate.move_to(next_cell))


class NeedleInHaystack(Scene):
    def construct(self):
        haystack = "mississippi"
        needle = "ssip"
        haystack_table = Table([[c for c in haystack]], include_outer_lines=True).scale(0.8)
        needle_table = Table([[c for c in needle]], include_outer_lines=True).scale(0.8).next_to(haystack_table, UP)
        self.add(haystack_table)
        self.add(needle_table)

        needle_pointer = ArrayPointer(needle_table, "i=0", color=RED, direction=UP)
        haystack_pointer = ArrayPointer(haystack_table, "i=0", color=YELLOW, direction=DOWN)
        self.add(needle_pointer)
        self.add(haystack_pointer)

        highlighted_cells = VGroup()
        i = 0
        n_index = 0
        while i < len(haystack):
            self.play(haystack_pointer.MoveTo((1, 1 + i)))
            self.play(needle_pointer.MoveTo((1, 1 + n_index)))
            if haystack[i] == needle[n_index]:

                cell = needle_table.get_cell((1, 1 + n_index))
                bg_cell = BackgroundRectangle(cell, color=YELLOW)

                self.add(bg_cell)
                highlighted_cells.add(bg_cell)

                cell = haystack_table.get_cell((1, 1 + i))
                bg_cell = BackgroundRectangle(cell, color=YELLOW)

                self.add(bg_cell)
                highlighted_cells.add(bg_cell)

                n_index += 1
            else:
                i = i - n_index
                n_index = 0
                for bg_cell in highlighted_cells:
                    self.remove(bg_cell)

            if n_index == len(needle):
                result = i - len(needle) + 1
                break
            i += 1
        self.wait()


if __name__ == "__main__":
    with tempconfig({"quality": "low_quality"}):
        scene = NeedleInHaystack()
        scene.render()
