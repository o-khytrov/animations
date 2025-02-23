from manim import *


class Queue(Scene):
    def enqueue(self, value):
        rect = Rectangle().scale(0.3).to_edge(LEFT)
        label = Text(str(value)).move_to(rect)
        enqueued = VGroup(rect, label)
        self.play(Create(enqueued))
        if self.queue_end:
            self.play(enqueued.animate.next_to(self.queue_end, direction=LEFT, buff=0.1))
        self.queue.append(enqueued)
        self.play(VGroup(self.queue).animate.move_to(ORIGIN))
        self.queue_end = enqueued

    def dequeue(self):
        first_out = self.queue.pop(0)
        self.play(first_out.animate.to_edge(RIGHT).fade(1))
        self.play(VGroup(self.queue).animate.move_to(ORIGIN))

    def construct(self):
        self.array = [1, 2, 3, 4, 5, 6]
        self.queue_end = None
        self.queue = []

        self.queue_end = Rectangle().scale(0.3)
        self.play(Create(self.queue_end))
        self.queue.append(self.queue_end)
        for i in reversed(range(5)):
            self.enqueue(i)

        for j in range(4):
            self.dequeue()
