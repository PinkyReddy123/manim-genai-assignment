Here's the complete Manim Community Edition code to prove the Pythagorean theorem using a visual dissection method.

The scene will:
1.  Draw a right triangle and label its sides `a`, `b`, and `c`.
2.  Draw squares on each side of the triangle, colored distinctly.
3.  Introduce the theorem statement `a^2 + b^2 = c^2`.
4.  Transition to a visual proof by rearrangement (often attributed to Bhaskara or a common Euclidean dissection). This involves:
    *   Constructing a large square of side `a+b`.
    *   Arranging four copies of the original right triangle inside this large square to form a central square of side `c` (area `c^2`).
    *   Constructing an identical large square.
    *   Rearranging the same four triangles inside this second large square to leave two empty squares, one of side `a` (area `a^2`) and one of side `b` (area `b^2`).
    *   Comparing the empty areas in both large squares to conclude `a^2 + b^2 = c^2`.
5.  Display the final theorem prominently.

```python
from manim import *

class PythagoreanTheoremProof(Scene):
    def construct(self):
        # 0. Configuration and Constants
        # Define the side lengths for our demonstration triangle.
        # We'll use a 3-4-5 right triangle for clarity.
        a_len = 3  # Length of the vertical leg
        b_len = 4  # Length of the horizontal leg
        c_len = np.sqrt(a_len**2 + b_len**2) # Length of the hypotenuse (will be 5)

        # Colors for better visualization
        color_a = BLUE_B
        color_b = RED_B
        color_c = GREEN_B
        color_triangle = GREY_C
        
        # Adjusting the scene for initial placement
        self.camera.frame.scale(1.2)
        
        # 1. Draw the Right Triangle
        # Let's place the right angle at the origin (0,0) for easier calculations.
        C_origin = Dot(ORIGIN).set_color(WHITE) # Right angle vertex
        B_right = Dot(RIGHT * b_len).set_color(WHITE) # Vertex on the x-axis
        A_up = Dot(UP * a_len).set_color(WHITE) # Vertex on the y-axis

        triangle = Polygon(
            C_origin.get_center(), B_right.get_center(), A_up.get_center(),
            color=color_triangle, fill_opacity=0.7, stroke_width=2
        )
        
        self.play(Create(triangle))
        self.wait(0.5)

        # 2. Label Sides a, b, c
        # Side 'a' is opposite vertex A_up (side CB, length b_len)
        # Side 'b' is opposite vertex B_right (side CA, length a_len)
        # Side 'c' is opposite vertex C_origin (side AB, length c_len)
        # Common convention for legs a, b, and hypotenuse c.
        
        # Label 'a' (leg along x-axis)
        label_side_a = MathTex("a").next_to(Line(C_origin.get_center(), B_right.get_center()).get_center(), DOWN, buff=0.1)
        # Label 'b' (leg along y-axis)
        label_side_b = MathTex("b").next_to(Line(C_origin.get_center(), A_up.get_center()).get_center(), LEFT, buff=0.1)
        # Label 'c' (hypotenuse)
        label_side_c = MathTex("c").next_to(Line(A_up.get_center(), B_right.get_center()).get_center(), UP + RIGHT, buff=0.1)

        side_labels = VGroup(label_side_a, label_side_b, label_side_c)
        self.play(Write(side_labels))
        self.wait(1)

        # 3. Draw Squares on Each Side
        
        # Square on side 'a' (horizontal leg CB)
        sq_a = Polygon(
            C_origin.get_center(),
            B_right.get_center(),
            B_right.get_center() + DOWN * a_len,
            C_origin.get_center() + DOWN * a_len,
            color=color_a, fill_opacity=0.6, stroke_width=2
        )
        
        # Square on side 'b' (vertical leg CA)
        sq_b = Polygon(
            C_origin.get_center(),
            A_up.get_center(),
            A_up.get_center() + LEFT * b_len,
            C_origin.get_center() + LEFT * b_len,
            color=color_b, fill_opacity=0.6, stroke_width=2
        )

        # Square on side 'c' (hypotenuse AB)
        # To make the square point outwards from the triangle, we find the vector for the hypotenuse
        # and rotate it by -90 degrees (clockwise) to get the direction for the square's other sides.
        vec_AB = B_right.get_center() - A_up.get_center()
        perp_vec_AB_outward = rotate_vector(vec_AB, -PI/2)

        sq_c = Polygon(
            A_up.get_center(),
            B_right.get_center(),
            B_right.get_center() + perp_vec_AB_outward,
            A_up.get_center() + perp_vec_AB_outward,
            color=color_c, fill_opacity=0.6, stroke_width=2
        )
        
        squares = VGroup(sq_a, sq_b, sq_c)

        self.play(
            Create(sq_a),
            Create(sq_b),
            Create(sq_c),
            run_time=2
        )
        self.wait(1)

        # 5. Show a²+b²=c²
        theorem_statement = MathTex("a^2 + b^2 = c^2").to_edge(UP).shift(LEFT * 3)
        self.play(Write(theorem_statement))
        self.wait(2)

        # Fade out the initial setup to make way for the dissection proof
        self.play(
            FadeOut(triangle, side_labels, squares, theorem_statement),
            run_time=2
        )
        self.wait(1)

        # -----------------------------------------------------------
        # Part 4: Visual Dissection Proof (Euclidean / Bhaskara's method)
        # This method uses two large squares of side length (a+b).
        # In one, four right triangles leave a central square c^2.
        # In the other, four identical right triangles leave two squares a^2 and b^2.
        # -----------------------------------------------------------

        # Base triangle for the dissection (right angle at origin)
        base_triangle_points = [
            ORIGIN,
            RIGHT * b_len,
            UP * a_len
        ]
        base_triangle = Polygon(*base_triangle_points, color=color_triangle, fill_opacity=0.7, stroke_width=1)
        
        side_large_sq = a_len + b_len

        # --- Arrangement 1: Shows c^2 ---
        # A large square of side (a+b)
        large_sq1 = Square(side_length=side_large_sq, color=LIGHT_GREY, fill_opacity=0.1, stroke_width=2)
        large_sq1.move_to(LEFT * 3) # Position it on the left
        self.play(Create(large_sq1))

        # Create 4 copies of the base triangle
        triangles1 = VGroup()
        t1_orig = base_triangle.copy() # Base on X, Height on Y
        t2_rot = base_triangle.copy().rotate(-PI/2) # Base on -Y, Height on X
        t3_rot = base_triangle.copy().rotate(PI) # Base on -X, Height on -Y
        t4_rot = base_triangle.copy().rotate(PI/2) # Base on Y, Height on -X
        
        # Position these triangles such that their right angles form the corners of the inner c^2 square.
        # Each triangle's right angle (ORIGIN) is placed at a specific point relative to the bottom-left of large_sq1.
        large_sq1_bl = large_sq1.get_corner(BL)
        
        # T1: Right angle at (a_len, 0) relative to large_sq1_bl
        t1_orig.move_to(large_sq1_bl + RIGHT * a_len)
        
        # T2: Right angle at (a_len + b_len, a_len) relative to large_sq1_bl
        t2_rot.move_to(large_sq1_bl + RIGHT * side_large_sq + UP * a_len)
        
        # T3: Right angle at (b_len, a_len + b_len) relative to large_sq1_bl
        t3_rot.move_to(large_sq1_bl + RIGHT * b_len + UP * side_large_sq)
        
        # T4: Right angle at (0, b_len) relative to large_sq1_bl
        t4_rot.move_to(large_sq1_bl + UP * b_len)
        
        triangles1.add(t1_orig, t2_rot, t3_rot, t4_rot)

        self.play(Create(triangles1), run_time=2)
        self.wait(0.5)
        
        # Draw the central c^2 square
        inner_sq_c_proof = Square(side_length=c_len, color=color_c, fill_opacity=0.8, stroke_width=2)
        inner_sq_c_proof.move_to(large_sq1.get_center()) # For this arrangement, it's centered
        
        self.play(Create(inner_sq_c_proof))
        self.wait(1)

        label_arrangement_1 = MathTex("(a+b)^2 = c^2 + 4 \\cdot \\text{Area(Triangle)}")
        label_arrangement_1.next_to(large_sq1, DOWN, buff=0.5).scale(0.8)
        self.play(Write(label_arrangement_1))
        self.wait(2)

        # --- Arrangement 2: Shows a^2 + b^2 ---
        # An identical large square of side (a+b)
        large_sq2 = Square(side_length=side_large_sq, color=LIGHT_GREY, fill_opacity=0.1, stroke_width=2)
        large_sq2.move_to(RIGHT * 3) # Position it on the right
        self.play(Create(large_sq2))

        # Create 4 *new* copies of triangles for transformation
        triangles2 = VGroup()
        t1_arr2 = base_triangle.copy()
        t2_arr2 = base_triangle.copy().rotate(PI) # Rotated 180 degrees
        t3_arr2 = base_triangle.copy().rotate(-PI/2) # Rotated -90 degrees (clockwise)
        t4_arr2 = base_triangle.copy().rotate(PI/2) # Rotated 90 degrees (counter-clockwise)
        
        # Place triangles such that they fill the corners, leaving a^2 and b^2 squares.
        # Each triangle's right angle (ORIGIN) is placed at a specific corner of large_sq2.
        
        # T1 (bottom-left): Right angle at large_sq2.get_corner(BL)
        t1_arr2.move_to(large_sq2.get_corner(BL))
        
        # T2 (top-right): Right angle at large_sq2.get_corner(UR)
        t2_arr2.move_to(large_sq2.get_corner(UR))
        
        # T3 (top-left): Right angle at large_sq2.get_corner(UL)
        t3_arr2.move_to(large_sq2.get_corner(UL))
        
        # T4 (bottom-right): Right angle at large_sq2.get_corner(BR)
        t4_arr2.move_to(large_sq2.get_corner(BR))

        triangles2.add(t1_arr2, t2_arr2, t3_arr2, t4_arr2)

        # Animate the transformation of the triangles from the first arrangement to the second
        # Also fade out the c^2 square as it's not present in this arrangement
        self.play(Transform(triangles1, triangles2), FadeOut(inner_sq_c_proof), run_time=3)
        self.wait(0.5)

        # Draw the inner squares a^2 and b^2
        sq_a_prime = Square(side_length=a_len, color=color_a, fill_opacity=0.8, stroke_width=2)
        sq_b_prime = Square(side_length=b_len, color=color_b, fill_opacity=0.8, stroke_width=2)

        # Positioning the squares
        # sq_a_prime (bottom-left area)
        sq_a_prime.move_to(large_sq2.get_corner(BL) + RIGHT * a_len/2 + UP * a_len/2)
        
        # sq_b_prime (top-right area)
        sq_b_prime.move_to(large_sq2.get_corner(UR) + LEFT * b_len/2 + DOWN * b_len/2)
        
        self.play(
            Create(sq_a_prime),
            Create(sq_b_prime)
        )
        self.wait(1)

        label_arrangement_2 = MathTex("(a+b)^2 = a^2 + b^2 + 4 \\cdot \\text{Area(Triangle)}")
        label_arrangement_2.next_to(large_sq2, DOWN, buff=0.5).scale(0.8)
        self.play(Write(label_arrangement_2))
        self.wait(2)

        # 5. Conclusion
        # Group all elements of the dissection proof for slight repositioning
        all_proof_elements = VGroup(
            large_sq1, triangles1, inner_sq_c_proof, label_arrangement_1, # inner_sq_c_proof is faded, but still in VGroup
            large_sq2, triangles2, sq_a_prime, sq_b_prime, label_arrangement_2
        )
        self.play(all_proof_elements.animate.shift(UP * 1.5), run_time=1.5)
        
        # Display the two area equations
        eq_c_sq_area = MathTex("c^2 + 4 \\cdot \\text{Area(Triangle)}").move_to(LEFT * 3)
        eq_ab_sq_area = MathTex("a^2 + b^2 + 4 \\cdot \\text{Area(Triangle)}").move_to(RIGHT * 3)
        equal_sign_comp = MathTex("=").next_to(eq_c_sq_area, RIGHT)
        
        self.play(
            FadeOut(label_arrangement_1, label_arrangement_2), # Fade out local labels
            Write(eq_c_sq_area),
            Write(eq_ab_sq_area),
            Write(equal_sign_comp)
        )
        self.wait(1)

        # Explain the deduction
        explanation_text = MathTex(
            "\\text{Since both large squares are identical, their total areas are equal.}",
            "\\text{Subtracting the area of the four identical triangles from both sides, we get:}"
        ).scale(0.7).next_to(equal_sign_comp, DOWN, buff=1.0)
        
        self.play(Write(explanation_text[0]))
        self.wait(2)
        self.play(Write(explanation_text[1]))
        self.wait(2)
        
        # Show the final deduction
        final_deduction = MathTex("c^2 = a^2 + b^2").scale(1.2).next_to(explanation_text, DOWN, buff=0.5)
        self.play(Write(final_deduction))
        self.wait(3)

        self.play(FadeOut(all_proof_elements, eq_c_sq_area, eq_ab_sq_area, equal_sign_comp, explanation_text, final_deduction))

        # Final display of the theorem
        final_theorem_display = MathTex("a^2 + b^2 = c^2").scale(2)
        self.play(Write(final_theorem_display))
        self.wait(3)

```