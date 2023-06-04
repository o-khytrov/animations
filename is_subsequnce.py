from manim import *

from custom.array import Array
from custom.array_pointer import ArrayPointer


class IsSubsequence(Scene):
    def intro(self):
        t = "ahbgdc"
        s = "abc"
        s_array = Array([c for c in s])
        t_array = Array([c for c in t]).next_to(s_array, DOWN)
        self.add(s_array)
        self.add(t_array)
        self.wait()
        self.add(s_array.highlight_element(0, highlight_color=YELLOW))
        self.wait()
        self.add(t_array.highlight_element(0))
        self.wait()
        self.add(s_array.highlight_element(1, highlight_color=YELLOW))
        self.wait()
        self.add(t_array.highlight_element(2))
        self.wait()
        self.add(s_array.highlight_element(2, highlight_color=YELLOW))
        self.wait()
        self.add(t_array.highlight_element(5))
        self.wait()

    def construct(self):
        t = "ahbgdc"
        s = "abc"
        s_array = Array([c for c in s])
        t_array = Array([c for c in t]).next_to(s_array, DOWN)
        self.add(s_array)
        self.add(t_array)
        self.wait()
        s_pointer = ArrayPointer(s_array, "j", color=BLUE, direction=UP)
        t_pointer = ArrayPointer(t_array, "i", color=YELLOW, direction=DOWN)
        self.add(s_pointer)
        self.add(t_pointer)
        i = 0
        s_index = 0
        counter = 0
        counter_text = Text("counter = 0").next_to(s_array, UP, buff=2)
        self.play(Write(counter_text))
        while i < len(t):

            self.play(t_pointer.move_to_index(i))

            if s_index > len(s) - 1:
                break
            if s[s_index] == t[i]:
                self.add(t_array.highlight_element(i))
                counter += 1
                self.play(Transform(counter_text, (Text(f"counter = {counter}").next_to(s_array, UP, buff=2))))

                s_index += 1
                if s_index < len(s):
                    self.play(s_pointer.move_to_index(s_index))
            else:
                self.play(t_pointer.wiggle())

            i += 1
            self.wait()
