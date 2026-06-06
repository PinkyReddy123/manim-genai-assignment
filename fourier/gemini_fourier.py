import google.generativeai as genai

# Replace with your Gemini API key
genai.configure(api_key="YOUR_API_KEY")

model = genai.GenerativeModel("gemini-2.5-flash")

prompt = """
Generate a complete Manim Community Edition Python script.

Requirements:
1. Create a scene showing how a square wave is approximated using Fourier Series.
2. Show the first 5 harmonics.
3. Draw each harmonic in a different color.
4. Display the cumulative sum after adding each harmonic.
5. Show the final square wave approximation.
6. Include a title: 'Fourier Series Decomposition'.
7. Add labels for each harmonic.
8. Use only Manim Community Edition syntax.
9. Include all imports.
10. Output ONLY executable Python code.
11. Do not include explanations.
12. Do not include markdown code fences.
"""

response = model.generate_content(prompt)

with open("fourier_series.py", "w", encoding="utf-8") as f:
    f.write(response.text)

print("Fourier code saved to fourier_series.py")