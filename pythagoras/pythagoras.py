
from manim import *
import numpy as np

class PythagoreanTheoremProof(Scene):
    def construct(self):
        # --- Configuration ---
        a_len = 3  # Length of side 'a'
        b_len = 4  # Length of side 'b'
        c_len = np.sqrt(a_len**2 + b_len**2) # Length of hypotenuse 'c' (will be 5 for 3-4-5 triangle)

        triangle_color = BLUE_A
        square_a_color = GREEN_A
        square_b_color = RED_A
        square_c_color = YELLOW_A

        # --- Part 1: Draw the Right Triangle and Squares ---

        # Define vertices of the right triangle (right angle at origin)
        p1 = ORIGIN
        p2 = b_len * RIGHT
        p3 = a_len * UP

        # Create the triangle
        triangle = Polygon(p1, p2, p3, color=triangle_color, fill_opacity=0.5)
        self.play(Create(triangle))
        self.wait(0.5)

        # Indicate the right angle at p1
       # Indicate the right angle at p1
        line1 = Line(p1, p2)
        line2 = Line(p1, p3)

        right_angle = RightAngle(
        line1,
        line2,
        length=0.4,
        quadrant=(1, 1)
)

        self.play(Create(right_angle))
        self.wait(0.5)

        # Label sides a, b, c with numerical values
        # Labels are positioned near the midpoint of each side
        label_a_val = MathTex(f"a={a_len:.0f}").next_to(Line(p1,p3).get_center(), LEFT, buff=0.1)
        label_b_val = MathTex(f"b={b_len:.0f}").next_to(Line(p1,p2).get_center(), DOWN, buff=0.1)
        label_c_val = MathTex(f"c={c_len:.0f}").next_to(Line(p2,p3).get_center(), UP + RIGHT, buff=0.1)
        self.play(Write(label_a_val), Write(label_b_val), Write(label_c_val))
        self.wait(1)

        # Draw square on side 'a'
        sq_a = Square(side_length=a_len, color=square_a_color, fill_opacity=0.7)
        # Position square 'a' to the left of the vertical leg
        sq_a.move_to(p1 + a_len/2 * UP + a_len/2 * LEFT)
        self.play(Create(sq_a))

        # Draw square on side 'b'
        sq_b = Square(side_length=b_len, color=square_b_color, fill_opacity=0.7)
        # Position square 'b' below the horizontal leg
        sq_b.move_to(p1 + b_len/2 * RIGHT + b_len/2 * DOWN)
        self.play(Create(sq_b))

        # Draw square on side 'c' (hypotenuse)
        # Calculate vector for side 'c' (from p2 to p3)
        vec_c = p3 - p2
        # Calculate a perpendicular vector to side 'c', pointing outwards from the triangle
        vec_c_perp = rotate_vector(vec_c, PI/2) # Rotate by 90 degrees counter-clockwise
        # Define the other two vertices of the square on 'c'
        p4 = p3 + vec_c_perp
        p5 = p2 + vec_c_perp
        sq_c = Polygon(p2, p3, p4, p5, color=square_c_color, fill_opacity=0.7)
        self.play(Create(sq_c))
        self.wait(1)

        # --- Part 2: Display Areas and Equation ---
        # Labels for the areas of the squares
        text_a2 = MathTex("a^2 = ", f"{a_len**2:.0f}", color=square_a_color).move_to(sq_a.get_center()).scale(0.8)
        text_b2 = MathTex("b^2 = ", f"{b_len**2:.0f}", color=square_b_color).move_to(sq_b.get_center()).scale(0.8)
        text_c2 = MathTex("c^2 = ", f"{c_len**2:.0f}", color=square_c_color).move_to(sq_c.get_center()).scale(0.8)

        self.play(FadeIn(text_a2, shift=UP), FadeIn(text_b2, shift=DOWN), FadeIn(text_c2, shift=RIGHT))
        self.wait(1.5)

        # Pythagorean Theorem Equation
        equation_text = MathTex("a^2 + b^2 = c^2").to_edge(UP, buff=0.5).scale(1.2)
        equation_values = MathTex(f"{a_len**2:.0f} + {b_len**2:.0f} = {c_len**2:.0f}").next_to(equation_text, DOWN)

        # Animate the individual area texts fading out and the main equation appearing
        self.play(
            FadeOut(text_a2, text_b2, text_c2),
            triangle.animate.shift(UP * 1.5), # Shift triangle up slightly for better visibility
            VGroup(sq_a, sq_b, sq_c).animate.shift(UP * 1.5)
        )
        self.play(Write(equation_text))
        self.wait(0.5)
        self.play(Write(equation_values))
        self.wait(2)

        # --- Part 3: Conceptual Area Transformation (Visual Metaphor for a^2 + b^2 = c^2) ---
        # Group all current elements to shift them left, making space for the demonstration
        all_elements = VGroup(
            triangle, right_angle, label_a_val, label_b_val, label_c_val,
            sq_a, sq_b, sq_c, equation_text, equation_values
        )
        self.play(all_elements.animate.shift(LEFT * 3))

        # Create a blank target square of side c on the right to visualize the combined area
        target_sq_c = Square(side_length=c_len, color=square_c_color, fill_opacity=0.3)
        target_sq_c.move_to(RIGHT * 3) # Position it on the right
        self.play(Create(target_sq_c))
        self.wait(0.5)

        # Create copies of squares 'a' and 'b' for the animation
        sq_a_clone = sq_a.copy().set_opacity(0.8).set_color(square_a_color)
        sq_b_clone = sq_b.copy().set_opacity(0.8).set_color(square_b_color)

        # Animate the clones shrinking and moving towards the center of target_sq_c
        # This visually suggests their areas are being collected or combined
        self.play(
            sq_a_clone.animate.scale(0.3).move_to(target_sq_c.get_center() + UP * 0.5),
            sq_b_clone.animate.scale(0.3).move_to(target_sq_c.get_center() + DOWN * 0.5),
            run_time=1.5
        )
        self.wait(0.5)

        # Combine the two scaled clones into a single VGroup
        combined_clones = VGroup(sq_a_clone, sq_b_clone)

        # Transform the combined clones into the target_sq_c,
        # visually representing a^2 + b^2 filling c^2
        self.play(
            Transform(combined_clones, target_sq_c.copy().set_opacity(1).set_fill(color=square_c_color, opacity=1)),
            run_time=2
        )
        self.wait(2)

        # Final message or confirmation
        final_text = Text("Q.E.D.", font_size=50, color=WHITE).next_to(combined_clones, DOWN, buff=1)
        self.play(Write(final_text))
        self.wait(3)

