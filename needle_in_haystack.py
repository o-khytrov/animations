from manim import *


class NeedleInHaystack(Scene):
    def construct(self):
        haystack = "sadbutsad"
        needle = "sad"

        haystack_table = Table([[c for c in haystack]], include_outer_lines=True).scale(0.8)

        needle_table = Table([[c for c in needle]], include_outer_lines=True).scale(0.8).next_to(haystack_table, UP)
        self.add(haystack_table)
        self.add(needle_table)

        target_cell=needle_table.get_cell((1, 1))
        needle_pointer_text = Text(f"i=0", color=RED, font_size=25)
        needle_pointer_arrow = Triangle(color=RED, fill_color=RED, fill_opacity=1).scale(0.1).rotate(
            60 * DEGREES).next_to(
            needle_pointer_text, DOWN, buff=0.1)
        needle_pointer = VGroup(needle_pointer_text, needle_pointer_arrow)
        needle_pointer.next_to(target_cell, UP, buff=0.2)

        haystack_pointer_text = Text(f"j=0", color=YELLOW, font_size=25)
        haystack_pointer_arrow = Triangle(color=YELLOW, fill_color=YELLOW, fill_opacity=1).scale(0.1).next_to(
            haystack_pointer_text, UP, buff=0.1)
        haystack_pointer = VGroup(haystack_pointer_text, haystack_pointer_arrow)
        haystack_pointer.next_to(haystack_table.get_cell((1, 1)), DOWN, buff=0.2)

        self.add(needle_pointer)
        self.add(haystack_pointer)

        for i in range(1, len(needle)):
            next_cell = needle_table.get_cell((1, 1 + i))
            self.play(needle_pointer.animate.next_to(next_cell, UP))

        for i in range(1, len(haystack)):
            next_cell = haystack_table.get_cell((1, 1 + i))
            self.play(haystack_pointer.animate.next_to(next_cell, DOWN))
