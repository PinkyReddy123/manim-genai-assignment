import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

model = genai.GenerativeModel("gemini-2.5-flash")

prompt = """
Write complete Manim Community Edition code.

Create a scene proving the Pythagorean theorem.

Requirements:
- Draw a right triangle
- Label sides a,b,c
- Draw squares on each side
- Color the squares
- Show a²+b²=c²
- Include animations
- Output only Python code
"""

response = model.generate_content(prompt)

print(response.text)

with open("pythagoras.py", "w", encoding="utf-8") as f:
    f.write(response.text)