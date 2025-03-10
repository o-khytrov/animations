from setup import *

config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 16.0
config.frame_width = 9.0


class BitManipulation(Scene):
    def math_per_character(self, expression: str, **kwargs):

        # Convert the string into individual characters while keeping LaTeX intact
        math_chars = [char for char in expression]  # Split into characters
        return MathTex(*math_chars, **kwargs)

    def bitwise_operation(self, a: int, b: int, operation, sign, start_point, title, code_sign):

        code_str = f"{a} {code_sign} {b}"
        a_txt = MathTex(str(a))
        res = operation(a, b)
        sign_txt = MathTex(sign).next_to(a_txt, direction=RIGHT)
        b_txt = MathTex(str(b)).next_to(sign_txt, direction=RIGHT)
        eq_txt = MathTex("=").next_to(b_txt, direction=RIGHT)
        res_txt = MathTex(res).next_to(eq_txt, direction=RIGHT)
        expression_left_side = VGroup(a_txt, sign_txt, b_txt)
        a_bin_str = f"{a:04b}"
        b_bin_str = f"{b:04b}"
        res_bin_str = f"{res:04b}"

        bin_a_text = self.math_per_character(a_bin_str).next_to(expression_left_side, direction=DOWN)
        bin_b_text = self.math_per_character(b_bin_str).next_to(bin_a_text, direction=DOWN)

        underline = Line().next_to(bin_b_text, direction=DOWN, buff=0.1)
        bin_res_txt = self.math_per_character(res_bin_str).next_to(underline, direction=DOWN)
        bin_xor_txt_copy = bin_res_txt.copy()

        a_txt_copy = a_txt.copy()
        b_txt_copy = b_txt.copy()
        code_background_config = {
            "corner_radius": 0
        }
        code = Code(code_string=code_str, language="python", add_line_numbers=False, background="rectangle",
                    background_config=code_background_config).next_to(expression_left_side,
                                                                      direction=UP)
        title_txt = Text(title).next_to(code, direction=UP)
        expression_group = VGroup(title_txt, a_txt, sign_txt, b_txt, eq_txt, res_txt, bin_a_text, bin_b_text,
                                  bin_res_txt, a_txt_copy, b_txt_copy, bin_xor_txt_copy, underline, code)
        expression_group.move_to(start_point)
        expression_group.scale(2)

        self.play(Write(title_txt))
        self.play(Create(code))
        self.play(Write(a_txt), Write(sign_txt), Write(b_txt), Write(eq_txt))
        self.play(a_txt_copy.animate.become(bin_a_text))
        self.play(b_txt_copy.animate.become(bin_b_text))
        self.play(Create(underline))
        for i in reversed(range(len(res_bin_str))):
            indication_color = Green if res_bin_str[i] == '1' else Red
            self.remove(b_txt_copy[i])
            self.remove(a_txt_copy[i])
            ba = bin_a_text[i]
            bb = bin_b_text[i]

            br = bin_res_txt[i]
            self.play(Indicate(ba, color=indication_color), Indicate(bb, color=indication_color))
            ba.set_color(indication_color)
            bb.set_color(indication_color)
            self.play(Write(br))

        self.play(bin_xor_txt_copy.animate.become(res_txt))

        self.play(FadeOut(expression_group))

    def bitwise_xor(self, a, b, start_point):
        self.bitwise_operation(a, b, lambda x, y: x ^ y, "\oplus", start_point, "XOR", "^")

    def bitwise_and(self, a, b, start_point):
        self.bitwise_operation(a, b, lambda x, y: x & y, "\land", start_point, "AND", "&")

    def bitwise_or(self, a, b, start_point):
        self.bitwise_operation(a, b, lambda x, y: x | y, "\lor", start_point, "OR", "|")

    def bitwise_shift_right(self, a, b, start_point):
        self.bitwise_operation(a, b, lambda x, y: x >> y, "\gg", start_point, "Right Shifting ", ">>")

    def decimal_to_binary_conversion(self):
        previous = None
        for number in range(1, 10):
            decimal_text = MathTex(str(number))
            if previous:
                decimal_text.next_to(previous, direction=DOWN)
            else:
                decimal_text.to_edge(LEFT + UP)
            self.play(Write(decimal_text), run_time=0.3)

            binary_string = f"{number:04b}"
            self.play(decimal_text.copy().animate.become(MathTex(binary_string).next_to(decimal_text, direction=RIGHT)),
                      run_time=0.3)

            previous = decimal_text

    def construct(self):

        # self.decimal_to_binary_conversion()
        #text = Text("101010", font="Monaco").scale(2)
        # self.play(Write(text))
        self.bitwise_or(5, 7, ORIGIN)
        self.bitwise_and(5, 7, ORIGIN)
        self.bitwise_xor(5, 7, ORIGIN)
        # self.bitwise_shift_right(3, 1, ORIGIN)
        self.wait()
