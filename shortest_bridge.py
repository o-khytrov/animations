from manim import *
import numpy as np


class ShortestBridge(Scene):
    def construct(self):
        input_array = np.array([[1, 1, 1, 1, 1], [1, 0, 0, 0, 1], [1, 0, 1, 0, 1], [1, 0, 0, 0, 1], [1, 1, 1, 1, 1]])
        input_text = Text(str(input_array)).scale(0.5).to_edge(UL)
        self.play(Write(input_text))
        grid = IntegerTable(input_array, include_outer_lines=True)
        """
        for i, row in enumerate(input_array):
            for j, val in enumerate(row):
                x = i + 1
                y = j + 1
                if val:
                    color = GREEN
                else:
                    color = BLUE
                grid.add_highlighted_cell((x, y), color=color)

        """
        self.play(Create(grid))

        def fill(x: int, y: int, val=None):
            if x > input_array.shape[0] - 1:
                return
            if y > input_array.shape[1] - 1:
                return
            if x < 0:
                return
            if y < 0:
                return

            if input_array[x][y] != 1:
                return

            self.wait(0.3)

            # grid.add(grid.get_cell((x + 1, y + 1), color=RED))
            grid.add_highlighted_cell((x + 1, y + 1), color=GREEN)

            fill(x + 1, y)
            # fill(x - 1, y)
            fill(x, y + 1)
            # fill(x, y - 1)

        fill(0, 0)

        self.wait()
