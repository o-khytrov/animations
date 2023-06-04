from manim import *


class RangeSumQuery(Scene):
    def construct(self):
        matrix = [[3, 0, 1, 4, 2],
                  [5, 6, 3, 2, 1],
                  [1, 2, 0, 1, 5],
                  [4, 1, 0, 1, 7],
                  [1, 0, 3, 0, 5]];
        t = IntegerTable(matrix, include_outer_lines=True).scale(0.7).to_edge(LEFT)

        copy = [row[:] for row in matrix]

        for r in range(len(matrix)):
            prefix = 0
            for c in range(len(matrix[r])):
                prefix += matrix[r][c]
                above = copy[r - 1][c] if r > 0 else 0
                copy[r][c] = prefix + above

        t_sum = IntegerTable(copy, include_outer_lines=True).scale(0.7).next_to(t, RIGHT)

        for c in range(1, 3):
            for r in range(1, 3):
                t.add_highlighted_cell((r + 1, c + 1))
                t_sum.add_highlighted_cell((r + 1, c + 1))

        self.add(t)

        self.add(t_sum)
