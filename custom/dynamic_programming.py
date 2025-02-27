from setup import *


class BubbleSort(Scene):
    def construct(self):

        linspace_array = np.linspace(1, 10, num=10, dtype=float)

        array = list(linspace_array)
        rectangles = []
        for i in range(len(array)):
            rectangles.append(Rectangle(width=1, stroke_width=0.5, height=array[i]).scale(0.5).set_fill(Green, opacity=1 / len(array) * array[i]))

        row = VGroup(rectangles).arrange(RIGHT, buff=0.02, aligned_edge=DOWN)
        self.play(Create(row))

        def dfs(i):
            if i == len(rectangles):
                return 0
            if i > len(rectangles):
                return 1
            if i + 1 < len(rectangles):
                curve_start = rectangles[i].get_top()
                curve_end = rectangles[i + 1].get_top()
                curve = CurvedArrow(curve_start, curve_end, radius=-0.4, tip_length=0.15)
                self.play(Create(curve), run_time=0.3)
            if i + 2 < len(rectangles):
                curve_start = rectangles[i].get_top()
                curve_end = rectangles[i + 2].get_top()
                curve = CurvedArrow(curve_start, curve_end, radius=-0.8, tip_length=0.15)
                self.play(Create(curve), run_time=0.3)

            return dfs(i + 1) + dfs(i + 2)

        dfs(0)
        self.wait()
