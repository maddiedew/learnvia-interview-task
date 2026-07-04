import random
from fractions import Fraction

import streamlit as st

# Problem generation 
# -----------------------------------------------------------------
def generate_problem():
    """
    Generates a,b,c for new limit problem:

        lim_{x->-1} sqrt( (x+1) / (x^2 + c*x + b) ) = 1/a

    Quick rundown of the constraints:
      1. For (x+1)/(x^2+cx+b) to be a 0/0 form at x = -1, the denominator
         must vanish at x = -1 as well:
             1 - c + b = 0   =>   c = b + 1
         Since x^2 + cx + b = x^2 + (b + 1)x + b factors as (x+1)(x+b), 
         the fraction simplifies to 1/(x+b) for x != -1.
      2. Taking the limit of the simplified expression:
             lim_{x->-1} sqrt(1/(x+b)) = sqrt(1/(b-1))
         For this to equal 1/a for a positive integer a, we need:
             b - 1 = a^2   =>   b = a^2 + 1,   c = b + 1 = a^2 + 2

    To do this, we'll randomly generate a for each problem, and that 
    will determine the problem values of a,b,c.
    """
    # change upper bound here for greater number of unique problems
    # implemented with max of a = 25 to keep coefficients manageable
    a = random.randint(1, 25)
    b = a**2 + 1
    c = b + 1
    answer = Fraction(1, a)
    return b, c, a, answer


def term(coeff, var=""):
    """Format a signed term like '+ 4x', '- 3', '' (if coeff is 0)."""
    if coeff == 0:
        return ""
    sign = "+" if coeff > 0 else "-"
    return f" {sign} {abs(coeff)}{var}"


# Answer parsing
# ---------------------------------------------------------------------------
def parse_answer(raw):
    """Parse student's integer, fraction, or decimal answer string 
    into a fraction."""
    stripped_answer = raw.strip().replace(" ", "")
    if not stripped_answer:
        return None
    try:
        return Fraction(stripped_answer)
    except (ValueError, ZeroDivisionError):
        pass
    try:
        return Fraction(float(stripped_answer)).limit_denominator(10_000)
    except ValueError:
        return None


# Session state to manage re-runs/ try again
# ---------------------------------------------------------------------------

# initialize a new problem if no current problem exists
# only runs on initial load, otherwise problem generated below
if "a" not in st.session_state:
    (
        st.session_state.b,
        st.session_state.c,
        st.session_state.a,
        st.session_state.answer,
    ) = generate_problem()

    # store data from student interaction
    st.session_state.submitted = False
    st.session_state.correct = None
    st.session_state.answer_input = ""

# generates new problem
def new_problem():
    (
        st.session_state.b,
        st.session_state.c,
        st.session_state.a,
        st.session_state.answer,
    ) = generate_problem()

    # store data from student interaction
    st.session_state.submitted = False
    st.session_state.correct = None
    st.session_state.answer_input = ""


# UI
# ---------------------------------------------------------------------------

# variables for current problem
b, c, a = st.session_state.b, st.session_state.c, st.session_state.a
correct_answer = st.session_state.answer
denom = f"x^2{term(c, 'x')}{term(b)}"

# problem formatting and visuals
st.markdown("### Evaluate the limit:")
st.latex(rf"\lim_{{x \to -1}} \sqrt{{\dfrac{{x+1}}{{{denom}}}}}")
st.write(
    "Enter your answer below as a whole number, fraction, or decimal."
)

with st.form(key="answer_form", clear_on_submit=False):
    answer = st.text_input("Your answer:", key="answer_input", placeholder="e.g. 1/2 or 0.5")
    submitted = st.form_submit_button("Submit Answer", type="primary")

st.button("🔄 New Problem", on_click=new_problem)

if submitted:
    parsed = parse_answer(answer)
    if parsed is None:
        st.warning("Please only enter a whole number, fraction, or decimal.")
        st.session_state.submitted = False
    else:
        st.session_state.submitted = True
        st.session_state.correct = (parsed == correct_answer)

# responses based on student input
if st.session_state.submitted:
    if st.session_state.correct:
        st.success(f"🎉 Correct! The limit is **1/{a}**. Nice work.")
    else:
        st.error("Not quite right — give it another try, or check the explanation below for help.")

    with st.expander("📖 Show explanation"):
        st.markdown(
            rf"""
We evaluate:

$$\lim_{{x \to -1}} \sqrt{{\dfrac{{x+1}}{{{denom}}}}}$$

**Step 1 — Direct substitution.**

At $x=-1$, the numerator $x+1 = -1 + 1 = 0$. Substituting $x=-1$ into the denominator also gives $0$,
so this is a $\dfrac{{0}}{{0}}$ indeterminate form, which means $(x+1)$ is a factor of the denominator too.

**Step 2 — Simplify the expression.**

We can factor the expression as:

$${denom} = (x+1)(x+{b})$$

Next, cancel the common factor. For $x \neq -1$:

$$\frac{{x+1}}{{(x+1)(x+{b})}} = \frac{{1}}{{x+{b}}}$$

**Step 3 — Take the limit of the simplified expression.**

$$\lim_{{x \to -1}} \sqrt{{\frac{{1}}{{x+{b}}}}} = \sqrt{{\frac{{1}}{{-1+{b}}}}} = \sqrt{{\frac{{1}}{{{b-1}}}}} = \frac{{1}}{{{a}}}$$

"""
        )
