# learnvia-interview-task
# Limit Practice App

A small Streamlit app for practicing limits of the form:

$$\lim_{x \to -1} \sqrt{\dfrac{x+1}{x^2+cx+b}} = \dfrac{1}{a}$$

`b` and `c` are generated (via a random integer `a`) each time a new
problem is generated, and the app evaluates the student's answer against the
correct value `1/a`.

## How the problem is generated

Two conditions from the task directions drive the problem generator:

1. **The expression under the root must be a `0/0` form at `x = -1`.**
   
   The numerator `x+1` is already `0` at `x = -1`, so the denominator must be
   `0` at `x = -1` as well:
   `1 - c + b = 0  →  c = b + 1`.
   So, `x² + cx + b` factors as `(x+1)(x+b)`, and the fraction simplifies
   to `1/(x+b)` for `x =/= -1`.

2. **The limit must simplify to `1/a` for an integer `a`.**
   
   Taking the limit of the simplified expression:
   `lim_{x→-1} √(1/(x+b)) = √(1/(b-1))`.
   Since we will focus on the positive solution, this only equals `1/a` when `a`
   is a **positive** integer and `b - 1 = a²`. So:
   - `a` is randomly chosen from `1` to `25` (for the sake of reasonable coeff/constants, but this upper bound could be changed)
   - `b = a² + 1`
   - `c = b + 1 = a² + 2`

This guarantees every generated problem is a valid, indeterminate limit of the form `0/0` that simplifies to `1/a` for some positive integer `a`. The value of a determines the value of `b` and `c`. With the current range of random integers for `a`, there are 25 unique problems that can be generated.

## Features

- New random problem on every page load, plus a "New Problem" button to
  generate a new problem without refreshing.
- Accepts answers as integers, fractions, or decimals.
- Clear success/error feedback after submitting.
- A collapsible, step-by-step explanation is shown after each
  submission, whether the answer was correct or incorrect.

## File overview

- `app.py` — the full app: problem generation, UI, answer parsing/correctness,
  and explanation.
