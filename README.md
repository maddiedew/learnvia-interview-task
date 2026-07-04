# learnvia-interview-task
# Limit Practice App

A small Streamlit app for practicing limits of the form:

$$\lim_{x \to -1} \sqrt{\dfrac{x+1}{x^2+cx+b}} = \dfrac{1}{a}$$

`b` and `c` are randomized (via a random integer `a`) each time a new
problem is generated, and the app evaluates the student's answer against the
correct value `1/a`.

## How the problem is generated

Two conditions from the task directions drive the problem generator:

1. **The expression under the root must be a `0/0` form at `x = -1`.**
   The numerator `x+1` is already `0` there, so the denominator must be
   `0` at `x = -1` as well:
   `1 - c + b = 0  →  c = b + 1`.
   So, `x² + cx + b` factors as `(x+1)(x+b)`, and the fraction simplifies
   to `1/(x+b)` for `x =/= -1`.

3. **The limit must simplify to `1/a` for an integer `a`.**
   Taking the limit of the simplified expression:
   `lim_{x→-1} √(1/(x+b)) = √(1/(b-1))`.
   We will focus on the positive solution, this only equals `1/a` when `a`
   is a **positive** integer and `b - 1 = a²`. So:
   - `a` is randomly chosen from `1` to `8`
   - `b = a² + 1`
   - `c = b + 1 = a² + 2`

This guarantees every generated problem is a valid `0/0` limit that
simplifies to a clean `1/a`.

## Features

- New random problem on every page load, plus a "New Problem" button to
  generate a new problem without refreshing.
- Accepts answers as integers, fractions, or decimals.
- Clear success/error feedback after submitting.
- A collapsible, step-by-step explanation shown after each
  submission, whether the answer was correct or incorrect.

## File overview

- `app.py` — the full app: problem generation, UI, answer parsing/correctness,
  and explanation.
