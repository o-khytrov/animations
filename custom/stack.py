from manim import *

# config.frame_height = 6
# config.frame_width = 8
class Stack(Scene):
    def shift(self):
        self.play(VGroup(self.stack).animate.move_to(ORIGIN))

    def push(self, value):
        rect = Rectangle().scale(0.3).to_edge(LEFT + UP)
        label = Text(str(value)).move_to(rect)
        group = VGroup(rect, label).rotate(PI / 8)

        if self.stack:
            self.play(group.animate.fade(0).rotate(-PI / 8).next_to(self.stack[-1], direction=UP, buff=0.15))
        else:
            self.play(group.animate.fade(0).rotate(-PI / 8).move_to(ORIGIN))
        self.stack.append(group)
        self.shift()

    def pop(self):
        top = self.stack.pop(-1)
        self.play(top.animate.to_edge(RIGHT).to_edge(UP).rotate(-PI / 8).fade(1))
        self.shift()

    def construct(self):
        self.stack = []
        self.push(5)
        self.push(3)
        self.push(4)
        self.pop()

        self.pop()
        self.push(8)
        self.push(9)
        self.push(10)
