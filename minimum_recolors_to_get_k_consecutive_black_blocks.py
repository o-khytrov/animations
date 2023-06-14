from manim import *

from custom.array import Array
from custom.array_pointer import ArrayPointer


class MinimumRecolors(Scene):

    def build_table(self, hash_map):
        data = []
        for key in hash_map.keys():
            data.append([key, str(hash_map[key])])
        return Table(data, include_outer_lines=True).to_edge(UP)

    def get_min_steps(self, hash_map):
        min_steps = min((hash_map["W"], hash_map["B"]))
        return Text(f"min_steps = {min_steps}")

    def construct(self):
        # s = "WBBWWBBWBW"
        # k = 7
        s = "BWWWBB"
        k = 6
        hash_map = {"W": 0, "B": 0}
        m_array = Array(s).scale(0.7)
        self.add(m_array)
        m_hash_map = self.build_table(hash_map)
        self.add(m_hash_map)
        l_pointer = ArrayPointer(m_array, "l", direction=UP, color=YELLOW)
        r_pointer = ArrayPointer(m_array, "r", direction=DOWN, color=RED)
        self.add(l_pointer)
        self.add(r_pointer)
        l = 0
        r = 0
        m_select_box = m_array.get_subarray_surrounding_rectangle(l, r + 1)
        m_min_steps = self.get_min_steps(hash_map).next_to(m_hash_map)
        self.add(m_select_box)
        self.add(m_min_steps)
        for r in range(len(s)):
            c = s[r]
            if c == "W":
                m_array.mob_table[0][r].set_color(RED)
            hash_map[c] += 1
            if r - l + 1 >= k:
                hash_map[s[l]] -= 1
                l += 1
            self.play(r_pointer.move_to_index(r), l_pointer.move_to_index(l),
                      m_select_box.animate.become(m_array.get_subarray_surrounding_rectangle(l, r + 1)))
            if c == "W":
                m_array.mob_table[0][r].set_color(ORANGE)
            if c == "B":
                m_array.mob_table[0][r].set_color(BLUE)
            if l > 0:
                m_array.mob_table[0][l - 1].set_color(WHITE)
            self.play(m_hash_map.animate.become(self.build_table(hash_map)))
            if r - l + 1 >= k:
                self.play(m_min_steps.animate.become(self.get_min_steps(hash_map).next_to(m_hash_map)))


if __name__ == "__main__":
    with tempconfig({"quality": "low_quality"}):
        scene = MinimumRecolors()
        scene.render()
