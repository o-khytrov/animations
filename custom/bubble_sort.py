from setup import *


class BubbleSort(Scene):
    def construct(self):

        linspace_array = np.linspace(1, 15, num=20, dtype=float)

        # Shuffle the array randomly
        np.random.shuffle(linspace_array)
        array = list(linspace_array)
        rectangles = []
        for i in range(len(array)):
            rectangles.append(Rectangle(width=1, stroke_width=0.5, height=array[i]).scale(0.5).set_fill(Green, opacity=1 / len(array) * array[i]))

        row = VGroup(rectangles).arrange(RIGHT, buff=0.02, aligned_edge=DOWN)
        self.play(Create(row))

        def bubble_sort():
            while True:
                swapped = False
                for i in range(1, len(array)):
                    if array[i - 1] > array[i]:
                        self.play(rectangles[i].animate.move_to(rectangles[i - 1], aligned_edge=DOWN), rectangles[i - 1].animate.move_to(rectangles[i], aligned_edge=DOWN), run_time=0.3)
                        rectangles[i - 1], rectangles[i] = rectangles[i], rectangles[i - 1]
                        array[i - 1], array[i] = array[i], array[i - 1]
                        swapped = True
                if not swapped:
                    break

        bubble_sort()

        self.wait()
