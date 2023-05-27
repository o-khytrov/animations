from manim import *

from custom.array import Array
from custom.array_pointer import ArrayPointer


class IsSubsequence(Scene):
    def construct(self):
        t = "ahbgdc"
        s = "abc"
        s_array = Array([c for c in s])
        t_array = Array([c for c in t]).next_to(s_array, DOWN)
        self.add(s_array)
        self.add(t_array)
        s_pointer = ArrayPointer(s_array, "j", color=BLUE, direction=UP)
        t_pointer = ArrayPointer(t_array, "i", color=YELLOW, direction=DOWN)
        self.add(s_pointer)
        self.add(t_pointer)
        i = 0
        s_index = 0
        counter = 0
        while i < len(t):

            self.play(t_pointer.move_to_index(i))

            if s_index > len(s) - 1:
                break
            if s[s_index] == t[i]:
                self.add(t_array.highlight_element(i))

                s_index += 1
                if s_index < len(s):
                    self.play(s_pointer.move_to_index(s_index))

                counter += 1

            i += 1
            self.wait()