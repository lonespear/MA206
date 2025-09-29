# pages/04_One_Proportion_CI.py
import math
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from scipy.stats import norm

from utils import *

st.set_page_config(page_title="One-Proportion Confidence Interval", layout="centered")
st.title("One-Proportion Confidence Interval")

# -----------------
# Explanation
# -----------------
st.write(
    "A confidence interval gives a range of plausible values for the true population proportion $(\\pi)$. "
    "For a sample with $X$ successes out of $n$ trials, the sample proportion is:"
)
st.latex(r"\hat{p} = \frac{X}{n}")

st.write(
    "The **standard error (SE)** measures sampling variability:"
)
st.latex(r"SE = \sqrt{\frac{\hat{p}(1-\hat{p})}{n}}")

st.write(
    "Then a $(1-\alpha)100\%$ confidence interval is given by:"
)
st.latex(r"\hat{p} \;\pm\; z^* \times SE")

st.caption("Here $z^*$ is the critical value from the Standard Normal distribution, such as 1.96 for 95% confidence.")

# -----------------
# Inputs
# -----------------
st.divider()
st.subheader("Inputs")

col1, col2, col3 = st.columns(3)
with col1:
    n = st.number_input("Sample size (n)", min_value=1, value=100, step=1)
with col2:
    X = st.number_input("Successes (X)", min_value=0, max_value=int(n), value=56, step=1)
with col3:
    conf = st.slider("Confidence level (%)", 80, 99, 95, step=1)

# -----------------
# Compute CI (Wald / textbook)
# -----------------
phat = X / n
alpha = 1 - conf / 100
z_star = norm.ppf(1 - alpha / 2)
SE = math.sqrt(phat * (1 - phat) / n)
lo = phat - z_star * SE
hi = phat + z_star * SE

# -----------------
# Display results
# -----------------
st.subheader("Result")

st.latex(
    r"\hat{p} = \frac{X}{n} = "
    + f"{phat:.3f}"
    + r"\quad \Rightarrow \quad CI = \left("
    + f"{lo:.3f},\ {hi:.3f}"
    + r"\right)"
)

# -----------------
# Visualization
# -----------------
fig, ax = plt.subplots(figsize=(6, 1.6))
ax.hlines(1, lo, hi, color="tab:red", linewidth=4)
ax.plot([lo, hi], [1, 1], "o", color="tab:red")
ax.plot(phat, 1, "o", color="tab:blue")
ax.set_xlim(-0.05, 1.05)
ax.set_yticks([])
ax.set_xlabel("Proportion")
ax.set_title(f"{conf}% CI for one proportion (n={n}, X={X})")
ax.grid(axis="x", alpha=0.25)
st.pyplot(fig)

# -----------------
# Interpretation
# -----------------
st.info(
    f"We are {conf}% confident that the true population proportion lies between "
    f"{lo:.3f} and {hi:.3f}."
)