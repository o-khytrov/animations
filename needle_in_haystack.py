from manim import *

from custom.array import Array
from custom.array_pointer import ArrayPointer


class NeedleInHaystack(Scene):
    def construct(self):
        haystack = "mississippi"
        needle = "ssip"
        haystack_table = Array([c for c in haystack])
        needle_table = Array([c for c in needle]).next_to(haystack_table, UP)
        self.add(haystack_table)
        self.add(needle_table)
        return
        self.play(Circumscribe(haystack_table))
        self.wait()
        self.play(Circumscribe(needle_table))

        needle_pointer = ArrayPointer(needle_table, "n", color=BLUE, direction=UP)
        haystack_pointer = ArrayPointer(haystack_table, "h", color=YELLOW, direction=DOWN)
        self.add(needle_pointer)
        self.add(haystack_pointer)

        h = 0
        n_index = 0
        while h < len(haystack):
            self.play(haystack_pointer.move_to_index(h))
            self.play(needle_pointer.move_to_index(n_index))

            if haystack[h] == needle[n_index]:
                self.add(needle_table.highlight_element(n_index))
                self.add(haystack_table.highlight_element(h))
                n_index += 1
            else:
                h = h - n_index
                n_index = 0
                self.play(haystack_pointer.wiggle(), needle_pointer.wiggle())
                for element in needle_table.highlighted_elements:
                    self.remove(element)
                needle_table.clear_highlighted_elements()
                for element in haystack_table.highlighted_elements:
                    self.remove(element)
                haystack_table.clear_highlighted_elements()

            if n_index == len(needle):
                result = h - len(needle) + 1
                self.play(Circumscribe(haystack_table.highlighted_elements, run_time=1.5))
                result_text = Text(f"r = h - strlen(needle) + 1 = {result}").next_to(haystack_table, DOWN, buff=2)
                self.play(Write(result_text))
                result_pointer = ArrayPointer(haystack_table, "r", color=GREEN, direction=DOWN, index=result)
                self.add(result_pointer)

                break
            h += 1

        self.wait()


if __name__ == "__main__":
    with tempconfig({"quality": "low_quality"}):
        scene = NeedleInHaystack()
        scene.render()
