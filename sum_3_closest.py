from manim import *

from custom.array import Array
from custom.array_pointer import ArrayPointer


class Sum3Closest(Scene):
    def __init__(self):
        self.a = sorted([-1, 2, 1, -4])
        self.i = 0
        self.j = self.i + 1
        self.k = len(self.a) - 1
        super().__init__()

    def sum(self):
        return self.a[self.i] + self.a[self.j] + self.a[self.k]

    def construct(self):
        target = Text("target = 1").to_edge(UL)
        self.add(target)
        varray = Array([str(n) for n in self.a])
        self.add(varray)
        ip = ArrayPointer(varray, "n", color=RED, direction=UP, index=self.i)
        jp = ArrayPointer(varray, "n", color=GREEN, direction=DOWN, index=self.j)
        kp = ArrayPointer(varray, "n", color=BLUE, direction=UP, index=self.k)
        sum = self.sum()
        sum_t = Text(f"sum = {sum}").to_edge(UP)
        self.add(sum_t)
        self.add(ip, jp, kp)
