from manim import *

#BV1om411k7Fv Tutorial Case
class Try(Scene):
    def construct(self):
        c = Circle(fill_opacity=1)
        s = Square(color=YELLOW, fill_opacity=1)
        self.play(FadeIn(c))
        self.wait()
        self.play(ReplacementTransform(c, s))
        self.wait()
        self.play(FadeOut(s))
        self.wait()

#BV1om411k7Fv Tutorial Section 2 Love Death Robot
class LDR(Scene):
    def construct(self):
        # Love
        s = Square(color=RED, fill_opacity=0.3)
        c1 = Circle(color=RED, fill_opacity=0.3).move_to(s.get_top())
        c2 = c1.copy().move_to(s.get_right())
        love = VGroup(s,c1,c2)
        self.play(Create(love))
        self.play(love.animate.rotate(45*DEGREES))
        self.play(love.animate.to_edge(LEFT, buff=1))
        # Death
        rt1 = Rectangle(color=RED, height=4, width=1, fill_opacity=0.3).rotate(45*DEGREES)
        rt2 = rt1.copy().rotate(90*DEGREES)
        death = VGroup(rt1,rt2)
        self.play(Create(death))
        # Robot
        eye_up = 0.5
        eye_side = 0.8
        r_s = Square(color=RED, side_length=3.5, fill_opacity=0.3)
        r_c1 = Circle(fill_color=BLACK, stroke_color=RED, radius=0.5, fill_opacity=0.3).move_to(LEFT*eye_side+UP*eye_up)
        r_c2 = r_c1.copy().move_to(RIGHT*eye_side+UP*eye_up)
        robot = VGroup(r_s,r_c1,r_c2).to_edge(RIGHT, buff=1)
        self.play(Create(robot))
        
        LDR = VGroup(love,death,robot)
        self.play(LDR.animate.set_opacity(1))
        self.wait()


#BV18gmAYSEHa Tutorial Section 1
class NameOfAnimation(Scene):
    def construct(self):
        plane = NumberPlane()
        box = Rectangle(stroke_color=GREEN_B, stroke_opacity=1, fill_color=GREEN_A, fill_opacity=1, height=1, width=1)
        
        axes = Axes(x_range=[-3,3,1], y_range=[-3,3,0.5], x_length=6, y_length=6)
        
        c = Circle(stroke_color=GREEN_C, stroke_opacity=1, fill_color=GREEN_D, fill_opacity=0.5, stroke_width=10)
        tri =Triangle(color=RED, stroke_width=10)

        self.add(plane)
        '''
        self.add(box)
        self.play(box.animate.shift(RIGHT*3), run_time=2)
        self.play(box.animate.shift(RIGHT*5), run_time=1)
        self.wait(1)

        self.play(Write(axes))
        self.play(DrawBorderThenFill(c))
        self.play(c.animate.set_width(1))
        self.play(Transform(c,tri))

        plane = self.add_plane(animate=True).add_coordinates()
        
        axes = Axes(x_range=[-5,5,1], y_range=[-4,4,1], x_length=10, y_length=8, axis_config = {"include_tip": True, "numbers_to_exclude": [0]})
        
        axes.to_edge(UR)
        axis_labels = axes.get_axis_labels(x_label = "x", y_label = "f(x)")
        
        graph = axes.get_graph(lambda x : x**0.5, x_range = [0,4], color =YELLOW)
        graphing_stuff = VGroup(axes,graph,axis_labels)
        self.play(DrawBorderThenFill(axes),Write(axis_labels))
        
        axes.add_coordinates()
        

        self.play(Create(graph))
        self.play(graphing_stuff.animate.shift(DOWN*4))
        self.play(axes.animate.shift*(LEFT*3))
        '''