from manim import *

from custom.array import Array
from custom.array_pointer import ArrayPointer


def combs(xs, i=0):
    if i == len(xs):
        yield ()
        return
    for c in combs(xs, i + 1):
        yield c
        yield c + (xs[i],)


def get_subsets(seq: []):
    """
    Returns all the subsets of this set. This is a generator.
    """
    if len(seq) <= 1:
        yield seq
        yield []
    else:
        for item in get_subsets(seq[1:]):
            yield [seq[0]] + item
            yield item


def count_chars(list_of_strings: [], char: str):
    count = 0
    for s in list_of_strings:
        for c in s:
            if c == char:
                count += 1
    return count


def divide_chunks(l: [], n: int):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


class OnesAndZeros(Scene):

    def __init__(self):
        self.m_strs = None
        super().__init__()

    def construct(self):
        strs = ["10", "0001", "111001", "1", "0"]

        m = 5
        n = 3
        self.m_strs = Array(strs).scale(0.5).to_edge(UP)
        m_mtex = Tex(f"m = {m}", color=YELLOW, font_size=28).next_to(self.m_strs, RIGHT)
        n_mtex = Tex(f"n = {m}", color=RED, font_size=28).next_to(m_mtex, RIGHT)
        self.add(self.m_strs)
        self.play(Write(m_mtex))
        self.play(Write(n_mtex))
        self.brute_force(strs)

    def brute_force(self, strs):
        combinations = list([c for c in get_subsets(strs) if c])
        chunks = divide_chunks(combinations, 16)
        vg_brute_force_solution = VGroup()
        paths = VGroup()
        for chunk in chunks:
            g = VGroup()

            for comb in chunk:
                m_subset = Table([comb], line_config={"stroke_width": 0.5}, include_outer_lines=True).scale(0.3)

                zeros = count_chars(comb, "0")
                ones = count_chars(comb, "1")
                t_zeros = Text(f"{zeros}", font_size=15, color=YELLOW)
                t_onex = Text(f"{ones}", font_size=14, color=RED)
                g.add(m_subset, t_zeros, t_onex)
                paths.add(VGroup(m_subset, t_zeros, t_onex))

            # g.arrange(DOWN, buff=0, center=False, aligned_edge=LEFT).to_edge(LEFT)
            g.arrange_in_grid(len(chunk), cols=3, buff=(0.2, 0.04,), col_alignments="lcc")
            vg_brute_force_solution.add(g)
        vg_brute_force_solution.arrange(aligned_edge=UP).next_to(self.m_strs, DOWN)
        self.add(vg_brute_force_solution)
        select_box = SurroundingRectangle(paths[0])
        self.add(select_box)

        for item in paths:
            self.play(select_box.animate.move_to(item).become(SurroundingRectangle(item)))

        self.wait()
