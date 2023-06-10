from manim import *

from custom.array import Array


class RepeatedDna(Scene):
    def __init__(self):
        self.m_array = None
        super().__init__()

    def build_matrix(self, d):
        m = Matrix([d.keys(), d.values()],
                   v_buff=1.3,
                   h_buff=0.8,
                   bracket_h_buff=SMALL_BUFF,
                   bracket_v_buff=SMALL_BUFF,
                   left_bracket="\{",
                   right_bracket="\}")
        return m

    def construct(self):
        s = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"
        # s = "AAAAACCCCCAAAAACC"
        self.m_array = Array([c for c in s]).scale(0.3).to_edge(UP)

        self.add(self.m_array)

        window_box = self.m_array.get_subarray_surrounding_rectangle(0, 9)
        self.add(window_box)
        l = 0
        r = 9
        length = len(s)
        map = {}
        self.wait()
        hash_map_g = VGroup().next_to(self.m_array, DOWN).to_edge(LEFT)
        self.add(hash_map_g)
        subarray_mobject_map = {}
        lb = Brace(hash_map_g, LEFT)
        rb = Brace(hash_map_g, RIGHT)
        self.add(lb)
        self.add(rb)
        while r < length:
            subarray = self.m_array.get_subarray_group(l, r)
            self.play(window_box.animate.move_to(subarray).become(SurroundingRectangle(subarray)))
            substring = s[l:r + 1]
            if substring in map.keys():
                map[substring] += 1
                sur_rec = SurroundingRectangle(subarray_mobject_map[substring])
                self.add(sur_rec)
                subarray_mobject_map[substring].set_color(RED)
                self.wait()
                self.remove(sur_rec)
            else:
                map[substring] = 1
                new_subarray = self.m_array.get_subarray_elements(l, r).copy()
                self.play(new_subarray.animate.next_to(hash_map_g, DOWN).become(
                    Text(substring, font_size=14).next_to(hash_map_g, DOWN)))
                hash_map_g.add(new_subarray, Text(":", font_size=14), Text("1", font_size=14))
                subarray_mobject_map[substring] = new_subarray
                hash_map_g.arrange_in_grid(len(subarray_mobject_map), cols=3, buff=0.05)
                self.remove(lb)
                self.remove(rb)
                lb = Brace(hash_map_g, LEFT)
                rb = Brace(hash_map_g, RIGHT)
                self.add(lb)
                self.add(rb)

            r += 1
            l += 1
            self.play(Circumscribe(hash_map_g))


if __name__ == "__main__":
    with tempconfig({"quality": "low_quality"}):
        scene = RepeatedDna()
        scene.render()
