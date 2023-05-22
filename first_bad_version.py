from manim import *
import numpy as np


class CodeText(Text):
    def __init__(self, text: str):
        super().__init__(text, font="JetBrains Mono", color=YELLOW, font_size=20)


class FirstBadVersion(Scene):

    def is_bad_version(self, n):
        return n >= self._first_bad

    def construct(self):
        num = 11
        self._first_bad = 5
        code_font = register_font("JetBrains Mono")

        array = ["?" for a in range(num)]
        table = Table([array], include_outer_lines=True).scale(0.7).to_edge(DOWN, buff=1)

        self.play(Create(table))
        indices = VGroup()
        for i, cell in enumerate(table.mob_table[0]):
            index = Text(f"{i+1}", color=YELLOW, font_size=12).next_to(cell, DOWN, buff=0.3)
            indices.add(index)
        self.play(Write(indices))
        """
        for i, n in enumerate(array):
            table.add_highlighted_cell((1, i + 1), color=GREEN if n else RED)
            self.wait(0.3)

        """

        first_line = CodeText(f"int n = {num}").to_edge(UL)
        self.play(Write(first_line))

        code_text = """
        int r = n;
        int l = 0;
        int result = n;
        """
        code = VGroup()
        prev_line = None
        for line in code_text.split("\n"):
            print(line)
            code_line = CodeText(line)
            if prev_line:
                code_line.next_to(prev_line, DOWN, buff=0.1, aligned_edge=LEFT)
            else:
                code_line.next_to(first_line, DOWN, buff=0.1, aligned_edge=LEFT)
            prev_line = code_line
            code.add(code_line)
            self.play(Write(code_line))

        l = 0
        r = num
        m = l + (r - l) // 2

        left_pointer = Text(f"l = 0", color=BLUE).next_to(table.get_cell((1, 1)), UP)
        self.play(Write(left_pointer))
        right_pointer = Text(f"r = {num}", color=RED).next_to(table.get_cell((1, num)), DOWN)
        self.play(Write(right_pointer))

        mid_text = Text(f"m = {m}", color=YELLOW).next_to(table.get_cell((1, m + 1)), UP)
        self.play(Write(mid_text))

        while l < r:
            m = l + (r - l) // 2
            self.play(mid_text.animate.next_to(table.get_cell((1, m + 1)), UP))

            table.add_highlighted_cell((1, m + 1), color=YELLOW)
            self.wait(0.1)
            if self.is_bad_version(m):
                next_cell = table.get_cell((1, m + 1))
                for c in range(m, r):
                    table.add_highlighted_cell((1, c + 1), color=RED)

                    self.wait(0.1)
                self.play(right_pointer.animate.next_to(next_cell, DOWN),
                          Transform(right_pointer, Text(f"r = {m + 1}", color=RED).next_to(next_cell, DOWN)))
                r = m
                result = m
            else:

                for c in range(l, m):
                    table.add_highlighted_cell((1, c + 1), color=GREEN)
                    self.wait(0.1)
                l = m + 1
                next_cell = table.get_cell((1, l + 1))

                self.play(left_pointer.animate.next_to(next_cell, UP),
                          Transform(left_pointer, Text(f"l = {l + 1}", color=BLUE).next_to(next_cell, UP)))
            self.wait()

        self.wait()


if __name__ == "__main__":
    with tempconfig({"quality": "low_quality"}):
        scene = FirstBadVersion()
        scene.render()
