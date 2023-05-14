from manim import *


class DecimalSystem(Scene):

    def construct(self):
        number = 325
        composed_number = self.vgroup_from_number(number)
        self.add(composed_number)
        decimal_places = self.get_decimal_places(number).next_to(composed_number, DOWN)
        self.add(decimal_places)
        # for digit in composed_number:
        # self.play(Indicate(digit))
        # self.decimal_system()
        # self.binary_system()

    def vgroup_from_number(self, number: int) -> Mobject:
        number_as_string = str(number)
        previous_digit = None

        digits = VGroup()
        for digit in number_as_string:
            if previous_digit:
                mobject = Tex(digit).next_to(previous_digit, RIGHT, buff=0.05)
            else:
                mobject = Tex(digit)
            previous_digit = mobject
            digits.add(mobject)

        return digits

    def get_decimal_places(self, number: int) -> Mobject:
        decimal_places = VGroup()
        previous_digit = None
        number_str = str(number)
        for i, str_digit in enumerate(number_str):
            power = len(number_str) - i - 1
            mobject = Tex(f"$ 10^{power} * {str_digit} +$")
            if previous_digit:
                mobject.next_to(previous_digit, RIGHT, buff=0.05)
            decimal_places.add(mobject)
            previous_digit = mobject
        return decimal_places

    def decimal_system(self):
        self.clear()
        decimal_number = Tex("325")
        formula2 = Tex("$= 10^{2} * 3 + 10^{1} * 2 + 10^{0} *5 $").next_to(decimal_number, RIGHT)
        group = VGroup(decimal_number, formula2).move_to(ORIGIN)
        self.play(Write(decimal_number))
        self.play(Write(formula2))

    def binary_system(self):
        self.clear()
        previous = None
        for i in range(10):
            number = Tex(f"{i}")
            if previous:
                number.next_to(previous, DOWN)
            else:
                number.to_edge(UL)
            self.play(Write(number))
            previous = number
            binary_number = Tex(f"{i:08b}").next_to(number, buff=3)
            self.play(Write(binary_number))
