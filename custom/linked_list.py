from collections import defaultdict

from manim import *


class ListNode:
    def __init__(self, label, val, next_node=None, ):
        self.label = label
        self.val = val
        self.next_node = next_node


class LinkedList(Scene):
    def __init__(self):
        super().__init__()
        self.nodes = []
        self.circle_scale = 0.4

    def play_create_node(self):
        pass

    def add_pointer(self, points_to, label, color=RED):
        pointer = Circle(color=color, stroke_width=10).scale(self.circle_scale).scale(1.1).move_to(points_to.get_center())
        self.play(Create(pointer))
        #icon = Text(label).next_to(pointer, direction=DOWN)

        return pointer

    def connect_nodes(self, node, next_node, direction):
        curve_start = node.get_right()
        curve_end = next_node.get_left()
        if direction == 'right':
            curve_start = node.get_right()
            curve_end = next_node.get_left()
        if direction == 'down':
            curve_start = node.get_bottom()
            curve_end = next_node.get_top()
        if direction == 'left':
            curve_start = node.get_left()
            curve_end = next_node.get_right()
        if direction == 'top':
            curve_start = node.get_top()
            curve_end = next_node.get_bottom()
        curve = CurvedArrow(curve_start, curve_end, radius=-1.5, tip_length=0.25)
        self.play(Create(curve), run_time=0.3)
        return curve

    def add_next(self, node, text, direction='right', origin=LEFT):
        directions = {
            "right": RIGHT,
            "down": DOWN,
            "left": LEFT
        }
        next_node = Circle(color=WHITE).scale(self.circle_scale).next_to(node, directions[direction], buff=0.5)
        t = Text(text).move_to(next_node)
        curve = self.connect_nodes(node, next_node, direction)

        self.play(Create(next_node), Write(t), run_time=0.1)

        self.current.next_node = ListNode(t, next_node)
        self.current = self.current.next_node
        self.nodes.append(self.current)
        return next_node

    def construct(self):
        head = Circle(color=WHITE).scale(self.circle_scale).to_edge(LEFT)
        head_label = "0"
        t = Text(head_label).move_to(head)

        self.head = ListNode(head_label, head)
        self.nodes.append(self.head)
        self.current = self.head

        self.play(Create(head), Write(t), run_time=0.1)

        node = head
        for i in range(1, 10):
            node = self.add_next(node, f"{i}")
        node = self.add_next(node, "10", "down")
        for i in range(10, 17):
            node = self.add_next(node, f"{i}", "left")

        self.connect_nodes(node, self.nodes[2].val, "top")
        self.current.next_node = self.nodes[2]

        self.wait()
        slow_pointer = self.add_pointer(self.head.val, "🐢", GREEN)
        fast_pointer = self.add_pointer(self.head.val, "🐇",YELLOW)
        slow_position = self.head
        fast_position = self.head
        node_visits = defaultdict(int)

        while True:
            node_visits[slow_position.label] += 1
            node_visits[fast_position.label] += 1
            if fast_position.next_node and fast_position.next_node.next_node:
                self.play(fast_pointer.animate.move_to(fast_position.next_node.val.get_center()), run_time=0.25)
                self.play(fast_pointer.animate.move_to(fast_position.next_node.next_node.val.get_center()), run_time=0.25)
                fast_position = fast_position.next_node.next_node
            if fast_position.label == slow_position.label:
                self.play(FocusOn(fast_pointer))
                break

            if slow_position.next_node:
                self.play(slow_pointer.animate.move_to(slow_position.next_node.val.get_center()), run_time=0.25)
                slow_position = slow_position.next_node

        self.wait()
