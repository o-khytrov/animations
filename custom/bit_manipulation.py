from manim import *


class BitManipulation(Scene):

    def bitwise_operation(self, a: int, b: int, operation, sign, start_point):
        a_txt = MathTex(str(a)).move_to(start_point)
        res = operation(a, b)
        sign_txt = MathTex(sign).next_to(a_txt, direction=RIGHT)
        b_txt = MathTex(str(b)).next_to(sign_txt, direction=RIGHT)
        eq_txt = MathTex("=").next_to(b_txt, direction=RIGHT)
        res_txt = MathTex(res).next_to(eq_txt, direction=RIGHT)

        expression_left_side = VGroup(a_txt, sign_txt, b_txt)

        self.play(Write(a_txt), Write(sign_txt), Write(b_txt), Write(eq_txt))

        bin_a_text = MathTex(f"{a:04b}").next_to(expression_left_side, direction=DOWN)
        bin_b_text = MathTex(f"{b:04b}").next_to(bin_a_text, direction=DOWN)
        bin_res_txt = MathTex(f"{res:04b}").next_to(bin_b_text, direction=DOWN)

        a_txt_copy = a_txt.copy()
        b_txt_copy = b_txt.copy()
        self.play(a_txt_copy.animate.become(bin_a_text))
        self.play(b_txt_copy.animate.become(bin_b_text))

        self.play(Write(bin_res_txt))
        bin_xor_txt_copy = bin_res_txt.copy()
        self.play(bin_xor_txt_copy.animate.become(res_txt))

        expression_group = VGroup(a_txt, sign_txt, b_txt, eq_txt, res_txt, bin_a_text, bin_b_text, bin_res_txt, a_txt_copy, b_txt_copy, bin_xor_txt_copy)
        self.play(FadeOut(expression_group))

    def bitwise_xor(self, a, b, start_point):
        self.bitwise_operation(a, b, lambda x, y: x ^ y, "\oplus", start_point)

    def bitwise_and(self, a, b, start_point):
        self.bitwise_operation(a, b, lambda x, y: x & y, "\land", start_point)

    def bitwise_or(self, a, b, start_point):
        self.bitwise_operation(a, b, lambda x, y: x | y, "\lor", start_point)

    def construct(self):

        previous = None
        for number in range(1, 10):
            decimal_text = MathTex(str(number))
            if previous:
                decimal_text.next_to(previous, direction=DOWN)
            else:
                decimal_text.to_edge(LEFT + UP)
            self.play(Write(decimal_text), run_time=0.3)

            binary_string = f"{number:04b}"
            self.play(decimal_text.copy().animate.become(MathTex(binary_string).next_to(decimal_text, direction=RIGHT)), run_time=0.3)

            previous = decimal_text

        self.bitwise_or(5, 7, ORIGIN)
        self.bitwise_and(5, 7, ORIGIN)
        self.bitwise_xor(5, 7, ORIGIN)
        self.wait()
