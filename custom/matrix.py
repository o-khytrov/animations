from manim import *
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

        def highlight(r, c):
            if (r, c) in visit:
                return
            color = BLUE if grid[r][c] == 0 else GREEN
            matrix.add_highlighted_cell((r + 1, c + 1), color=color, fill_opacity=1)
            self.wait(0.1)

        def dfs(r, c):
            if (r, c) in visit:
                return
            if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[r]):
                return
            highlight(r, c)
            visit.add((r, c))
            if grid[r][c] == 0:
                return

            neighbours = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
            for nr, nc in neighbours:
                dfs(nr, nc)

        for r in range(len(grid)):
            for c in range(len(grid[r])):
                if not (r, c) in visit:
                    if grid[r][c] == 1:
                        dfs(r, c)
                    else:
                        highlight(r, c)
        dfs(0, 0)

        self.wait()
