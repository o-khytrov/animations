from manim import *
import numpy as np

from custom.array import Array
from custom.array_pointer import ArrayPointer


class MergeSort(Scene):

    def __init__(self):
        super().__init__()
        self.original_array = []
        self.m_original_array = None
        self.m_original_array_divisor = None

    def display_array_divisor(self, m):
        self.remove(self.m_original_array_divisor)
        lines = self.m_original_array.vertical_lines
        self.m_original_array_divisor = lines[m + 1].copy().scale(2).set_color(RED)
        self.play(Create(self.m_original_array_divisor))

    def copy(self, dest: Array, i1: int, source: Array, i2: int):
        dest_el = dest.mob_table[0][i1]
        copied_el = source.mob_table[0][i2].copy()
        dest_el.set_color(GREEN)
        copied_el.set_color(GREEN)
        dest_loc = dest_el.get_center()
        dest.mob_table[0][i1] = copied_el
        self.remove(dest_el)
        anim = Succession(
            AnimationGroup(copied_el.animate.move_to(dest_loc)))
        self.play(anim)
        dest_el.set_color(WHITE)
        dest.mob_table[0][i1] = copied_el
        dest.elements.add(copied_el)
        copied_el.set_color(WHITE)

    def merge_sort(self, arr, m_array):

        if len(arr) > 1:

            # Finding the mid of the array
            mid = len(arr) // 2
            # self.display_array_divisor(mid)
            # Dividing the array elements

            L = arr[:mid]

            # Into 2 halves
            R = arr[mid:]

            m_l = Array(L).move_to(m_array, aligned_edge=LEFT)
            m_divisor = Line(m_l.get_edge_center(UR), m_l.get_edge_center(DR), color=RED)
            self.add(m_divisor)

            r_l = Array(R).move_to(m_array, aligned_edge=RIGHT)
            self.play(m_l.animate.next_to(m_array, DOWN, aligned_edge=LEFT).shift(LEFT * 0.35),
                      r_l.animate.next_to(m_array, DOWN, aligned_edge=RIGHT).shift(RIGHT * 0.35))

            # Sorting the first half
            self.merge_sort(L, m_l)

            # Sorting the second half
            self.merge_sort(R, r_l)

            i = j = k = 0

            arr_pointer = ArrayPointer(m_array, "k", color=YELLOW)
            l_pointer = ArrayPointer(m_l, "i", direction=DOWN, color=TEAL)
            r_pointer = ArrayPointer(r_l, "j", direction=DOWN, color=BLUE)
            self.add(arr_pointer)
            self.add(l_pointer)
            self.add(r_pointer)
            # Copy data to temp arrays L[] and R[]
            while i < len(L) and j < len(R):
                if L[i] <= R[j]:
                    arr[k] = L[i]
                    self.play(r_pointer.wiggle(), Circumscribe(l_pointer._select_box, color=GREEN))
                    self.play(l_pointer.move_to_index(i))
                    self.copy(m_array, k, m_l, i)
                    i += 1

                else:
                    arr[k] = R[j]
                    self.play(l_pointer.wiggle(), Circumscribe(r_pointer._select_box, color=GREEN))
                    self.play(r_pointer.move_to_index(j))
                    self.copy(m_array, k, r_l, j)
                    j += 1
                self.add(m_array.highlight_element(k, GREEN))
                k += 1
                self.play(arr_pointer.move_to_index(k))

            # Checking if any element was left
            while i < len(L):
                arr[k] = L[i]
                self.play(l_pointer.move_to_index(i), arr_pointer.move_to_index(k))
                self.copy(m_array, k, m_l, i)
                self.add(m_array.highlight_element(k, GREEN))
                i += 1
                k += 1

            while j < len(R):
                arr[k] = R[j]
                self.play(r_pointer.move_to_index(j), arr_pointer.move_to_index(k))
                self.copy(m_array, k, r_l, j)
                self.add(m_array.highlight_element(k, GREEN))
                j += 1
                k += 1

            self.remove(arr_pointer._select_box, arr_pointer._arrow, arr_pointer._label)
            self.remove(l_pointer._select_box, l_pointer._arrow, l_pointer._label)
            self.remove(r_pointer._select_box, r_pointer._arrow, r_pointer._label)
            self.play(Uncreate(m_l.highlighted_elements), Uncreate(r_l.highlighted_elements), Uncreate(m_l),
                      Uncreate(r_l),
                      Uncreate(m_divisor), )

    def construct(self):
        # self.original_array = np.random.randint(1, 100, 7).tolist()
        self.original_array = [9, 8, 6, 7, 1, 4, 3, 2, 5]
        self.m_original_array = Array(self.original_array).to_edge(UP)
        self.add(self.m_original_array)

        self.merge_sort(self.original_array, self.m_original_array)
        self.wait()


if __name__ == "__main__":
    with tempconfig({"quality": "low_quality"}):
        scene = MergeSort()
        scene.render()
