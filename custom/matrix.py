from setup import *

import numpy as np
import random


def generate_islands(shape, num_islands, max_size):
    matrix = np.zeros(shape, dtype=int)

    for _ in range(num_islands):
        # Randomly select a starting point for the island
        x, y = random.randint(0, shape[0] - 1), random.randint(0, shape[1] - 1)

        # Generate a random island within the max_size constraint
        for _ in range(random.randint(1, max_size)):
            dx, dy = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])  # Random movement
            x, y = np.clip(x + dx, 0, shape[0] - 1), np.clip(y + dy, 0, shape[1] - 1)
            matrix[x, y] = 1

    return matrix


# Example usage

class Matrix(Scene):
    def construct(self):
        grid = [[0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0],
                [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]]

        matrix = IntegerTable(
            np.array(grid),
            include_outer_lines=True
        ).scale(0.5)
        self.play(Create(matrix))
        self.wait()
        visit = set()

        def show_directions(mobject, r, c):
            arrow_scale = 0.5
            directions = VGroup()


            if r + 1 < len(grid) and (r + 1, c) not in visit:
                down_arrow = Arrow(start=mobject.get_bottom(), end=mobject.get_bottom() + DOWN, buff=0.05).scale(arrow_scale)
                directions.add(down_arrow)
            if r - 1 >= 0 and (r - 1, c) not in visit:
                up_arrow = Arrow(start=mobject.get_top(), end=mobject.get_top() + UP, buff=0.05).scale(arrow_scale)
                directions.add(up_arrow)
            if c + 1 < len(grid[r]) and (r, c + 1) not in visit:
                right_arrow = Arrow(start=mobject.get_right(), end=mobject.get_right() + RIGHT, buff=0.05).scale(arrow_scale)
                directions.add(right_arrow)
            if c - 1 >= 0 and (r, c - 1) not in visit:
                left_arrow = Arrow(start=mobject.get_left(), end=mobject.get_left() + LEFT, buff=0.05).scale(arrow_scale)
                directions.add(left_arrow)

            self.play(Create(directions), run_time=0.5)

            self.remove(directions)

        max_area = 0
        on_max_area = Variable(max_area, Text("max_area"), num_decimal_places=0).next_to(matrix, direction=UP)
        self.add(on_max_area)

        def highlight(r, c):
            if (r, c) in visit:
                return
            color = ManimColor("#03045e") if grid[r][c] == 0 else ManimColor("#006400")
            matrix.add_highlighted_cell((r + 1, c + 1), color=color, fill_opacity=1)
            self.wait(0.1)

        path = []

        def dfs(r, c):
            if (r, c) in visit:
                return 0
            if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[r]):
                return 0

            next_cell = matrix.get_cell((r + 1, c + 1))

            line = Line(start=pointer.get_center(), end=next_cell.get_center(), color=RED)
            path.append(line)
            path_len = len(path)

            self.play(pointer.animate.move_to(next_cell), Create(line), run_time=0.4)
            highlight(r, c)
            visit.add((r, c))

            if grid[r][c] == 0:
                return 0
            show_directions(pointer, r, c)
            neighbours = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
            res = 1
            for nr, nc in neighbours:
                res + dfs(nr, nc)
                self.play(pointer.animate.move_to(next_cell), run_time=0.4)
                while len(path) > path_len:
                    self.remove(path.pop(-1))

            return res

        pointer = matrix.get_cell((1, 1), color=RED)
        self.add(pointer)
        max_area_tracker = on_max_area.tracker
        for r in range(len(grid)):
            for c in range(len(grid[r])):
                self.play(pointer.animate.move_to(matrix.get_cell((r + 1, c + 1))), run_time=0.4)
                if not (r, c) in visit:
                    if grid[r][c] == 1:
                        area = dfs(r, c)
                        max_area = max(max_area, area)
                        self.play(max_area_tracker.animate.set_value(max_area))
                    else:
                        highlight(r, c)
                        visit.add((r, c))

        self.wait()
