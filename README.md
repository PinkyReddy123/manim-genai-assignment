# Manim GenAI Assignment

## Project Overview

This project demonstrates the use of the Google Gemini API to automatically generate Manim animations for mathematical concepts and critically evaluate the generated code.

The assignment contains two parts:

1. Pythagorean Theorem Visualization
2. Fourier Series Decomposition Visualization

The generated Manim code was executed, tested, and analyzed to identify limitations and areas for improvement.

---

## Project Structure

```text
manim-genai-assignment
│
├── README.md
├── requirements.txt
│
├── pythagoras
│   ├── gemini_pythagoras.py
│   ├── pythagoras.py
│   ├── pythagoras_output.png
│   └── pythagoras_critique.md
│
├── fourier
│   ├── gemini_fourier.py
│   ├── fourier_series.py
│   ├── fourier_output.png
│   └── fourier_critique.md
│
└── media
```

---

## Installation

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Required Packages

* Manim Community Edition
* Google Generative AI SDK
* NumPy
* MiKTeX (for LaTeX rendering)

---

## Running the Pythagorean Theorem Scene

Generate code using Gemini:

```bash
python pythagoras/gemini_pythagoras.py
```

Render animation:

```bash
manim -pqh pythagoras/pythagoras.py PythagoreanTheoremProof
```

---

## Running the Fourier Series Scene

Generate code using Gemini:

```bash
python fourier/gemini_fourier.py
```

Render animation:

```bash
manim -pqh fourier/fourier_series.py FourierSeriesSquareWave
```

---

## Findings from Critical Analysis

### Pythagorean Theorem

* Gemini generated explanatory text along with code.
* Markdown formatting had to be removed manually.
* Incorrect usage of the RightAngle API caused rendering errors.
* Generated labels required modification.
* The code assumed LaTeX dependencies were already installed.

### Fourier Series

* Gemini used deprecated Manim APIs.
* Generated code required compatibility fixes.
* Harmonic labels disappeared too quickly.
* Mathematical explanations were limited.
* Dependency requirements were not documented.

---

## Conclusion

The Gemini API successfully generated Manim animations for both mathematical concepts. However, manual debugging and compatibility fixes were required before the scenes could be rendered successfully. This demonstrates both the strengths and limitations of AI-generated code for technical animation tasks.
