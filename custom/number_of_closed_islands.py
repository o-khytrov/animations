from collections import defaultdict

from networkx.classes import neighbors

from setup import *


class MaxAreaOfIsland(Scene):

    def show_directions(self, mobject, r, c):

        directions = VGroup()
        arrow_kwargs = {

            "stroke_width": 0.8,
            "buff": 0,
        }
        if r + 1 < len(self.grid):
            down_neighbour = self.matrix.get_cell((r + 2, c + 1))
            down_arrow = Arrow(start=mobject.get_center(), end=down_neighbour.get_center(), **arrow_kwargs)
            directions.add(down_arrow)
            self.arrows[(r + 1, c)].append(down_arrow)
        if r - 1 >= 0:
            up_neighbour = self.matrix.get_cell((r, c + 1))
            up_arrow = Arrow(start=mobject.get_center(), end=up_neighbour.get_center(), **arrow_kwargs)
            directions.add(up_arrow)
            self.arrows[(r - 1, c)].append(up_arrow)
        if c + 1 < len(self.grid[r]):
            right_neighbour = self.matrix.get_cell((r + 1, c + 2))
            right_arrow = Arrow(start=mobject.get_center(), end=right_neighbour.get_center(), **arrow_kwargs)
            directions.add(right_arrow)
            self.arrows[(r, c + 1)].append(right_arrow)
        if c - 1 >= 0:
            left_neighbour = self.matrix.get_cell((r + 1, c))
            left_arrow = Arrow(start=mobject.get_center(), end=left_neighbour.get_center(), **arrow_kwargs)
            directions.add(left_arrow)
            self.arrows[(r, c - 1)].append(left_arrow)

        self.play(Create(directions), run_time=0.4)

    def init(self):
        self.grid = [[1, 1, 1, 1, 1, 1, 1, 0], [1, 0, 0, 0, 0, 1, 1, 0], [1, 0, 1, 0, 1, 1, 1, 0],
                     [1, 0, 0, 0, 0, 1, 0, 1], [1, 1, 1, 1, 1, 1, 1, 0]]
        # self.grid = [[0, 0, 1, 1, 0, 1, 0, 0, 1, 0], [1, 1, 0, 1, 1, 0, 1, 1, 1, 0], [1, 0, 1, 1, 1, 0, 0, 1, 1, 0],
        #              [0, 1, 1, 0, 0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 1, 1, 1, 0], [0, 1, 0, 1, 0, 1, 0, 1, 1, 1],
        #              [1, 0, 1, 0, 1, 1, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 0, 0, 1, 0, 1, 0, 1],
        #              [1, 1, 1, 0, 1, 1, 0, 1, 1, 0]]
        self.matrix = IntegerTable(
            np.array(self.grid),
            include_outer_lines=True
        ).scale(0.6)
        self.visit = set()
        self.arrows = defaultdict(list)
        self.path = []
        self.play(Create(self.matrix))
        self.wait()
        self.borders = []

    def visit_cell(self, r, c):
        self.play(self.pointer.animate.move_to(self.matrix.get_cell((r + 1, c + 1))), run_time=0.4)
        if not (r, c) in self.visit:
            if self.grid[r][c] == 0:
                self.borders.clear()
                is_closed = self.dfs(r, c)
                if is_closed:
                    self.result += 1
                    self.play(self.on_screen_max_area.animate.become(
                        Text(f"result = {self.result}").next_to(self.matrix, UP)), run_time=0.4)
                    self.play(Circumscribe(VGroup(self.borders)))
                    self.borders.clear()

                return
            else:
                self.highlight(r, c)
                self.visit.add((r, c))

    def count_closed_islands(self):
        self.result = 0
        self.on_screen_max_area = Text("result = 0").next_to(self.matrix, UP)
        self.add(self.on_screen_max_area)
        self.pointer = self.matrix.get_cell((1, 1), color=Red)

        self.add(self.pointer)

        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                self.visit_cell(r, c)

        self.wait()

    def highlight(self, r, c):
        if (r, c) in self.visit:
            return
        color = Green if self.grid[r][c] == 0 else Blue
        self.matrix.add_highlighted_cell((r + 1, c + 1), color=color, fill_opacity=1)
        self.wait(0.1)

    def draw_border(self, r, c, parent):
        pr, pc = parent
        parent_cell = self.matrix.get_cell((pr + 1, pc + 1))
        top_left, top_right, bottom_right, bottom_left = parent_cell.get_vertices()
        border = None
        if c > pc:  # right
            border = Line(top_right, bottom_right, color=Red, stroke_width=6)
        elif c < pc:  # left
            border = Line(top_left, bottom_left, color=Red, stroke_width=6)
        elif r > pr:  # down
            border = Line(bottom_right, bottom_left, color=Red, stroke_width=6)
        elif r < pr:  # up
            border = Line(top_left, top_right, color=Red, stroke_width=6)
        if border:
            self.add(border)
            self.borders.append(border)

    def dfs(self, r, c, parent=None):
        if r < 0 or r >= len(self.grid) or c < 0 or c >= len(self.grid[r]):
            self.remove_arrows(r, c)
            return False
        next_cell = self.matrix.get_cell((r + 1, c + 1))

        line = Line(start=self.pointer.get_center(), end=next_cell.get_center(), color=Red)
        self.path.append(line)
        path_len = len(self.path)
        animations = AnimationGroup(self.pointer.animate.move_to(next_cell), Create(line))
        for arrow in self.arrows[(r, c)]:
            animations = AnimationGroup(animations, Uncreate(arrow))
        self.play(animations, run_time=0.4)
        self.highlight(r, c)

        if (r, c) in self.visit:
            self.remove_arrows(r, c)
            if self.grid[r][c] == 1:
                self.draw_border(r, c, parent)
            return True

        self.visit.add((r, c))

        if self.grid[r][c] == 1:
            self.draw_border(r, c, parent)
            return True
        self.show_directions(self.pointer, r, c)
        neighbours = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
        res = True
        for nr, nc in neighbours:
            if not self.dfs(nr, nc, (r, c)):
                res = False
            self.play(self.pointer.animate.move_to(next_cell), run_time=0.4)
            while len(self.path) > path_len:
                self.remove(self.path.pop(-1))

        return res

    def remove_arrows(self, r, c):
        for arrow in self.arrows[(r, c)]:
            self.play(Uncreate(arrow), run_time=0.4)
            self.remove(arrow)
        self.arrows[(r, c)].clear()

    def highlight_islands(self):
        ROWS = len(self.grid)
        COLS = len(self.grid[0])
        visit = set()

        def dfs(r, c, land):
            if r < 0 or r == ROWS or c < 0 or c == COLS or self.grid[r][c] == 0:
                return
            if (r, c) in visit:
                return

            land.append(self.matrix.get_cell((r + 1, c + 1)))
            visit.add((r, c))
            neighbours = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
            for nr, nc in neighbours:
                dfs(nr, nc, land)

        for r in range(ROWS):
            for c in range(COLS):
                if self.grid[r][c] == 1:
                    land = []
                    dfs(r, c, land)
                    self.matrix.add_highlighted_cell((r + 1, c + 1), color=Blue, fill_opacity=1)
                else:
                    self.matrix.add_highlighted_cell((r + 1, c + 1), color=Green, fill_opacity=1)

    def construct(self):
        self.init()
        self.count_closed_islands()
        # self.highlight_islands()
        self.remove(self.pointer)
        self.wait()


if __name__ == "__main__":
    scene = MaxAreaOfIsland()
    scene.construct()
