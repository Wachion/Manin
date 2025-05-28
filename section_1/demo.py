from manim import *


class Chapter_5(Scene):
    def construct(self):
        #数轴
        axis = NumberLine(x_range=[-2,2,1],include_ticks=True,include_tip=True,include_numbers=True).shift(LEFT*3)
        self.add(axis)
