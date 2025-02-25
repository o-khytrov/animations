from manim import *
from custom.array import Array
from custom.array_pointer import ArrayPointer

from manim.opengl import *


class OpenGLIntro(Scene):
    def construct(self):
        input_t = [73, 74, 75, 71, 69, 72, 76, 73]
        res = [0] * len(input_t)
        cell_width = 2.5
        stack_position = DOWN * (config.frame_height / 2 - 0.5)
        mobject_stak = []
        stack = []

        temperatures = Array(input_t).to_edge(UP, buff=0.35)
        res_array = Array(res).next_to(temperatures, DOWN, buff=0.35)

        pointer = ArrayPointer(temperatures, "i", color=BLUE, direction=DOWN)
        self.add(temperatures)
        self.add(pointer)
        self.add(res_array)

        def stack_push(val, parent=None):

            rect = Rectangle(width=cell_width, height=1, color=WHITE).next_to(parent)
            t = Text(str(val)).move_to(rect)
            stack_item = VGroup(rect, t)
            # stack_item.rotate(angle=0.25 * PI)
            moving_animation = stack_item.animate.move_to(stack_position)  # .rotate(angle=-0.25 * PI)
            if mobject_stak:
                moving_animation = (stack_item.animate
                                    # .rotate(angle=-0.25 * PI)
                                    .next_to(mobject_stak[-1], direction=UP,
                                             buff=0))
            self.play(
                AnimationGroup(
                    FadeIn(stack_item),  # Fade in the object
                    moving_animation,

                )
            )
            mobject_stak.append(stack_item)

        def stack_pop():
            r = mobject_stak.pop()

            self.play(
                r.animate.move_to(UP * 3 + RIGHT * 3).rotate(angle=-0.20 * PI).set_opacity(0)
            )

        for i, t in enumerate(input_t):
            self.play(pointer.move_to_index(i))
            el = temperatures.get_element_by_index(i)
            while stack and t > stack[-1][1]:
                stack_i, _ = stack.pop(-1)
                stack_pop()
                res[stack_i] = i - stack_i
                res_array.get_cell()
            stack.append((i, t))
            stack_push((i, t), el)

        self.wait()
