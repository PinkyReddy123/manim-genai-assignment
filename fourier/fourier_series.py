from manim import *
import numpy as np

class FourierSeriesSquareWave(Scene):
    def construct(self):
        title = Text("Fourier Series Decomposition", font_size=50).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        plane = NumberPlane(
            x_range=[-PI - 0.5, PI + 0.5, PI/2],
            y_range=[-2.5, 2.5, 1],
            x_length=10,
            y_length=5,
            axis_config={"include_numbers": True, "font_size": 24},
            background_line_style={
                "stroke_color": GREY_B,
                "stroke_width": 1,
                "stroke_opacity": 0.6,
            }
        ).shift(DOWN * 0.5)
        plane.add_coordinates()

        x_label = MathTex("t").next_to(plane.x_axis, DR)
        y_label = MathTex("f(t)").next_to(plane.y_axis, UL)

        self.play(Create(plane), Write(x_label), Write(y_label))
        self.wait(0.5)

        num_harmonics = 5
        harmonic_colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
        approximation_color = WHITE
        
        def get_harmonic_term(n):
            return lambda x: (4 / PI) * (np.sin((2 * n - 1) * x) / (2 * n - 1))

        def get_sum_function(k):
            def func(x):
                s = 0
                for n_idx in range(1, k + 1):
                    s += get_harmonic_term(n_idx)(x)
                return s
            return func
            
        def get_zero_sum_function(x):
            return 0
            H
        current_sum_func = get_zero_sum_function
        current_approx_curve = plane.plot(current_sum_func, x_range=[-PI, PI], color=approximation_color)
        current_approx_label = Text("Sum: 0 Harmonics", font_size=24, color=approximation_color).to_corner(UL)
        
        self.play(Create(current_approx_curve), Write(current_approx_label))
        self.wait(1)

        for k in range(1, num_harmonics + 1):
            harmonic_func = get_harmonic_term(k)
            harmonic_graph = plane.plot(harmonic_func, x_range=[-PI, PI], color=harmonic_colors[k - 1])
            
            suffix = "th"
            if k == 1: suffix = "st"
            elif k == 2: suffix = "nd"
            elif k == 3: suffix = "rd"

            harmonic_label = Text(f"{k}{suffix} Harmonic", 
                                  font_size=28, 
                                  color=harmonic_colors[k - 1]).next_to(plane.x_axis, DOWN * 3.5).shift(RIGHT * 3)
            
            self.play(
                Create(harmonic_graph),
                Write(harmonic_label)
            )
            self.wait(0.5)

            new_sum_func = get_sum_function(k)
            new_approx_curve = plane.plot(new_sum_func, x_range=[-PI, PI], color=approximation_color)
            new_approx_label = Text(f"Sum: {k} Harmonics", font_size=24, color=approximation_color).to_corner(UL)
            
            self.play(
                Transform(current_approx_curve, new_approx_curve),
                Transform(current_approx_label, new_approx_label),
                FadeOut(harmonic_graph),
                FadeOut(harmonic_label)
            )
            self.wait(1)
        
        self.play(current_approx_curve.animate.set_stroke(width=5))
        self.wait(1)

        left_flat = plane.plot(lambda x: -1, x_range=[-PI, 0], color=GREY_D, stroke_width=4)
        right_flat = plane.plot(lambda x: 1, x_range=[0, PI], color=GREY_D, stroke_width=4)
        vertical_line_at_zero = Line(plane.coords_to_point(0, -1), plane.coords_to_point(0, 1), color=GREY_D, stroke_width=4)
        
        actual_square_wave = VGroup(left_flat, right_flat, vertical_line_at_zero)
        
        final_approx_text = Text("Final Approximation (5 Harmonics)", font_size=30, color=WHITE).to_corner(DR)
        ideal_wave_text = Text("Ideal Square Wave", font_size=30, color=GREY_D).next_to(final_approx_text, UP, buff=0.5)

        self.play(
            Write(final_approx_text),
            FadeIn(actual_square_wave),
            Write(ideal_wave_text),
            run_time=2
        )
        self.wait(3)

        self.play(
            FadeOut(title),
            FadeOut(plane),
            FadeOut(x_label),
            FadeOut(y_label),
            FadeOut(current_approx_curve),
            FadeOut(current_approx_label),
            FadeOut(actual_square_wave),
            FadeOut(final_approx_text),
            FadeOut(ideal_wave_text)
        )
        self.wait(1)