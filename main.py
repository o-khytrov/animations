import math

from manim import *

hex_digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]


class DecimalSystem(Scene):

    def construct(self):
        # self.decimal_system_exmpained()
        # self.decimal2binary(325)
        self.decimal2hex(1024)

    def decimal2hex(self, number: int):
        self.clear()
        title = Text("Decimal2Hex conversion")
        self.play(Write(title))
        self.play(FadeOut(title))
        number_tex = Tex(str(number))
        self.play(Write(number_tex))
        self.play(number_tex.animate.to_edge(UL))
        tmp = number
        current_mobject = number_tex;
        bin_group = VGroup()
        while tmp > 0:
            modulo = tmp % 16
            step = Tex(f"$ {str(tmp)} \mod 16 = {modulo}$").next_to(current_mobject, DOWN).align_to(LEFT, LEFT)
            result = Tex(f"{hex_digits[modulo]}").next_to(step, RIGHT)
            bin_group.add(result)
            self.play(Write(step))
            self.play(Write(result))
            current_mobject = step
            tmp = int(tmp / 16)
        for i, b in enumerate(bin_group):
            copy = b.copy()
            if i == 0:
                self.play(copy.animate.to_edge(DL))
            else:
                self.play(copy.animate.next_to(prev_place, RIGHT))
            prev_place = copy

    def decimal2binary(self, numer: int):
        title = Text("Decimal2Binary conversion")
        self.play(Write(title))
        self.play(FadeOut(title))
        number_tex = Tex(str(numer))
        self.play(Write(number_tex))
        self.play(number_tex.animate.to_edge(UL))
        tmp = numer
        current_mobject = number_tex;
        bin_group = VGroup()
        while tmp > 0:
            step = Tex(f"$ {str(tmp)} \mod 2 = $").next_to(current_mobject, DOWN).align_to(LEFT, LEFT)
            result = Tex(f"{str(tmp % 2)}").next_to(step, RIGHT)
            bin_group.add(result)
            self.play(Write(step))
            self.play(Write(result))
            current_mobject = step
            tmp = int(tmp / 2)
        for i, b in enumerate(bin_group):
            copy = b.copy()
            if i == 0:
                self.play(copy.animate.to_edge(DL))
            else:
                self.play(copy.animate.next_to(prev_place, RIGHT))
            prev_place = copy

    def decimal_system_exmpained(self):
        number = 325
        composed_number = self.vgroup_from_number(number)
        self.add(composed_number)
        # decimal_places = self.get_decimal_places(number).next_to(composed_number, DOWN)
        # self.add(decimal_places)
        # for digit in composed_number:
        # self.play(Indicate(digit))
        # self.decimal_system()
        # self.binary_system()
        for i, digit in enumerate(composed_number):
            copy = composed_number[i].copy()
            if i == 0:
                self.play(copy.animate.to_edge(UP))
            else:
                self.play(copy.animate.next_to(prv, DOWN))
            prv = copy
            power = len(composed_number) - i - 1
            digit = str(number)[i]
            power_of_ten_formula = Tex(f"$  10^{power} * {digit}  $").next_to(copy)
            self.play(Write(power_of_ten_formula))
            power_of_ten = int(math.pow(10, power))
            total = Tex(f"$ = {power_of_ten} *  {digit} = {power_of_ten * int(digit)}$") \
                .next_to(power_of_ten_formula,
                         RIGHT)
            self.play(Write(total))
        self.wait()

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
