from manim import *

from custom.array import Array
from custom.array_pointer import ArrayPointer


class Quicksort(Scene):
    def __init__(self):
        super().__init__()
        self.m_array = None
        self.m_l_pointer = None
        self.m_h_pointer = None
        self.m_p_pointer = None
        self.m_text = None

    def swap(self, arr, i1, i2):
        tmp = arr[i1]
        arr[i1] = arr[i2]
        arr[i2] = tmp
        if i1 != i2:
            self.play(self.m_array.swap(i1, i2))

    def partition(self, arr, low, high):
        # area = VGroup()
        #
        # for i in range(low - 1, high):
        #     area.add(self.m_array.get_element_by_index(i))
        # select_box = SurroundingRectangle(area)
        # self.add(select_box)
        pivot = arr[high]
        self.play(self.m_p_pointer.move_to_index(high))
        i = low - 1
        for j in range(low, high):
            self.play(self.m_l_pointer.move_to_index(j))
            text = f"{arr[j]} {'<' if pivot > arr[j] else '>='} {pivot}"
            if self.m_text:
                self.play(self.m_text.animate.become(Text(text).to_edge(UP)))
            else:
                self.m_text = Text(text).to_edge(UP)
                self.play(Write(self.m_text))
            self.wait()
            if arr[j] < pivot:
                i += 1
                self.swap(arr, i, j)
        self.swap(arr, i + 1, high)
        # self.remove(select_box)
        return i + 1

    def quicksort(self, arr: [], low: int, high: int):
        if low < high:
            pi = self.partition(arr, low, high)
            self.quicksort(arr, low, pi - 1)
            self.quicksort(arr, pi + 1, high)

    def construct(self):
        array = [10, 80, 30, 90, 40]
        self.m_array = Array(array)
        self.add(self.m_array)
        low = 0
        high = len(array) - 1
        self.m_l_pointer = ArrayPointer(self.m_array, "l", color=YELLOW)
        self.m_h_pointer = ArrayPointer(self.m_array, "h", index=high, direction=DOWN)
        self.m_p_pointer = ArrayPointer(self.m_array, "p", color=GREEN, index=high, direction=UP)
        self.add(self.m_l_pointer, self.m_p_pointer)
        self.quicksort(array, low, high)
        self.wait()


if __name__ == "__main__":
    # with tempconfig({"quality": "low_quality"}):
    #     scene = Quicksort()
    #     scene.render()
    print()
