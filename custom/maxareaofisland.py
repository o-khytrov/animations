from collections import defaultdict

from setup import *


class MaxAreaOfIsland(Scene):

    def construct(self):
        self.init()
        self.find_max_area_of_island()

    def show_directions(self, mobject, r, c):

        directions = VGroup()
        arrow_kwargs = {

            "stroke_width": 0.8,
            "buff": 0,
        }
        if r + 1 < len(self.grid) and (r + 1, c) not in self.visit:
            down_neighbour = self.matrix.get_cell((r + 2, c + 1))
            down_arrow = Arrow(start=mobject.get_center(), end=down_neighbour.get_center(), **arrow_kwargs)
            directions.add(down_arrow)
            self.arrows[(r + 1, c)].append(down_arrow)
        if r - 1 >= 0 and (r - 1, c) not in self.visit:
            up_neighbour = self.matrix.get_cell((r, c + 1))
            up_arrow = Arrow(start=mobject.get_center(), end=up_neighbour.get_center(), **arrow_kwargs)
            directions.add(up_arrow)
            self.arrows[(r - 1, c)].append(up_arrow)
        if c + 1 < len(self.grid[r]) and (r, c + 1) not in self.visit:
            right_neighbour = self.matrix.get_cell((r + 1, c + 2))
            right_arrow = Arrow(start=mobject.get_center(), end=right_neighbour.get_center(), **arrow_kwargs)
            directions.add(right_arrow)
            self.arrows[(r, c + 1)].append(right_arrow)
        if c - 1 >= 0 and (r, c - 1) not in self.visit:
            left_neighbour = self.matrix.get_cell((r + 1, c))
            left_arrow = Arrow(start=mobject.get_center(), end=left_neighbour.get_center(), **arrow_kwargs)
            directions.add(left_arrow)
            self.arrows[(r, c - 1)].append(left_arrow)

        self.play(Create(directions), run_time=0.4)

    def init(self):
        self.grid = [[0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                     [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0],
                     [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]]
        self.matrix = IntegerTable(
            np.array(self.grid),
            include_outer_lines=True
        ).scale(0.5)
        self.visit = set()
        self.arrows = defaultdict(list)
        self.path = []
        self.play(Create(self.matrix))
        self.wait()

    def visit_cell(self, r, c):
        self.play(self.pointer.animate.move_to(self.matrix.get_cell((r + 1, c + 1))), run_time=0.4)
        if not (r, c) in self.visit:
            if self.grid[r][c] == 1:
                area = self.dfs(r, c)
                if area > self.max_area:
                    self.max_area = area
                    self.play(self.on_screen_max_area.animate.become(Text(f"max_area = {self.max_area}").next_to(self.matrix, UP)), run_time=0.4)
                return
            else:
                self.highlight(r, c)
                self.visit.add((r, c))

    def find_max_area_of_island(self):
        self.max_area = 0
        self.on_screen_max_area = Text("max_area = 0").next_to(self.matrix, UP)
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
        color = ManimColor("#03045e") if self.grid[r][c] == 0 else ManimColor("#006400")
        self.matrix.add_highlighted_cell((r + 1, c + 1), color=color, fill_opacity=1)
        self.wait(0.1)

    def dfs(self, r, c):
        if (r, c) in self.visit:
            self.remove_arrows(r, c)
            return 0
        if r < 0 or r >= len(self.grid) or c < 0 or c >= len(self.grid[r]):
            self.remove_arrows(r, c)
            return 0

        next_cell = self.matrix.get_cell((r + 1, c + 1))

        line = Line(start=self.pointer.get_center(), end=next_cell.get_center(), color=Red)
        self.path.append(line)
        path_len = len(self.path)
        animations = AnimationGroup(self.pointer.animate.move_to(next_cell), Create(line))
        for arrow in self.arrows[(r, c)]:
            animations = AnimationGroup(animations, Uncreate(arrow))
        self.play(animations, run_time=0.4)
        self.highlight(r, c)
        self.visit.add((r, c))

        if self.grid[r][c] == 0:
            return 0
        self.show_directions(self.pointer, r, c)
        neighbours = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
        res = 1
        for nr, nc in neighbours:
            res+=self.dfs(nr, nc)
            self.play(self.pointer.animate.move_to(next_cell), run_time=0.4)
            while len(self.path) > path_len:
                self.remove(self.path.pop(-1))

        return res

    def remove_arrows(self, r, c):
        for arrow in self.arrows[(r, c)]:
            self.play(Uncreate(arrow), run_time=0.4)
            self.remove(arrow)
        self.arrows[(r, c)].clear()


if __name__ == "__main__":
    scene = MaxAreaOfIsland()
    scene.construct()
