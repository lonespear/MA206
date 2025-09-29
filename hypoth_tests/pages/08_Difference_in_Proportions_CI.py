# pages/08_Diff_in_Proportions_CI.py
import math
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from scipy.stats import norm

st.set_page_config(page_title="Difference in Proportions Confidence Interval", layout="centered")
st.title("Difference in Proportions Confidence Interval")

# -----------------
# Explanation
# -----------------
st.write(
    "A confidence interval gives a range of plausible values for the **difference between two population "
    "proportions**, $\\pi_1 - \\pi_2$. This is useful when comparing two groups."
)

st.write("Suppose group 1 has $X_1$ successes out of $n_1$ trials, and group 2 has $X_2$ successes out of $n_2$ trials.")

st.latex(r"""
\hat{p}_1 = \frac{X_1}{n_1}, \quad \hat{p}_2 = \frac{X_2}{n_2}
""")

st.write("The point estimate of the difference in population proportions is:")

st.latex(r"""
\hat{p}_1 - \hat{p}_2
""")

st.write("The **standard error** is:")

st.latex(r"""
SE = \sqrt{ \frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2} }
""")

st.write("So the $(1-\\alpha)100\\%$ confidence interval is:")

st.latex(r"""
(\hat{p}_1 - \hat{p}_2) \;\pm\; z^* \times SE
""")

st.caption("Here $z^*$ is the critical value from the Standard Normal distribution, such as 1.96 for 95% confidence.")

# -----------------
# Example
# -----------------
st.divider()
st.subheader("Example")

st.write("""
Suppose we want to compare the rate of Cadets who skip breakfast between males and females:
- Male Cadets: 30 out of 100 skip breakfast ($\\hat{p}_1 = 0.30$).  
- Female Cadets: 20 out of 120 skip breakfast ($\\hat{p}_2 \\approx 0.167$).  
""")

n1, x1 = 100, 30
n2, x2 = 120, 20
p1_hat, p2_hat = x1/n1, x2/n2
diff = p1_hat - p2_hat
conf = 95
alpha = 1 - conf/100
z_star = norm.ppf(1 - alpha/2)
SE = math.sqrt(p1_hat*(1-p1_hat)/n1 + p2_hat*(1-p2_hat)/n2)
lo = diff - z_star * SE
hi = diff + z_star * SE

st.latex(
    r"\hat{p}_1 = 0.30, \quad \hat{p}_2 \approx 0.167, \quad "
    r"\hat{p}_1 - \hat{p}_2 \approx 0.133"
)

st.latex(
    r"CI = ("
    + f"{lo:.3f}, {hi:.3f}"
    + r")"
)

# Visualization
fig, ax = plt.subplots(figsize=(6, 1.6))
ax.hlines(1, lo, hi, color="tab:red", linewidth=4)
ax.plot([lo, hi], [1, 1], "o", color="tab:red")
ax.plot(diff, 1, "o", color="tab:blue")
ax.axvline(0, color="black", linestyle="--", alpha=0.7)  # line at 0
ax.set_xlim(-0.5, 0.5)
ax.set_yticks([])
ax.set_xlabel("Difference in proportions")
ax.set_title(f"{conf}% CI for difference in proportions")
ax.grid(axis="x", alpha=0.25)
st.pyplot(fig)

st.info(
    f"We are {conf}% confident that the true difference "
    f"(male minus female breakfast skipping rate) lies between {lo:.3f} and {hi:.3f}. "
    f"Since the interval does {'not ' if lo*hi>0 else ''}include 0, "
    f"we {'do' if lo*hi>0 else 'do not'} have evidence of a difference."
)

# -----------------
# Practice
# -----------------
st.divider()
st.subheader("Practice: Difference in Proportions CI")

col1, col2 = st.columns(2)
with col1:
    n1 = st.number_input("Sample size group 1 (n₁)", min_value=1, value=100)
    x1 = st.number_input("Successes group 1 (X₁)", min_value=0, value=30)
    n2 = st.number_input("Sample size group 2 (n₂)", min_value=1, value=120)
    x2 = st.number_input("Successes group 2 (X₂)", min_value=0, value=20)
with col2:
    conf = st.slider("Confidence level (%)", 80, 99, 95, step=1)

p1_hat, p2_hat = x1/n1, x2/n2
diff = p1_hat - p2_hat
alpha = 1 - conf/100
z_star = norm.ppf(1 - alpha/2)
SE = math.sqrt(p1_hat*(1-p1_hat)/n1 + p2_hat*(1-p2_hat)/n2)
lo = diff - z_star*SE
hi = diff + z_star*SE

st.latex(
    f"\\hat p_1 = {p1_hat:.3f},\\ "
    f"\\hat p_2 = {p2_hat:.3f},\\ "
    f"\\hat p_1 - \\hat p_2 = {diff:.3f},\\ "
    f"CI = ({lo:.3f}, {hi:.3f})"
)

# Visualize
fig2, ax2 = plt.subplots(figsize=(6, 1.6))
ax2.hlines(1, lo, hi, color="tab:red", linewidth=4)
ax2.plot([lo, hi], [1, 1], "o", color="tab:red")
ax2.plot(diff, 1, "o", color="tab:blue")
ax2.axvline(0, color="black", linestyle="--", alpha=0.7)
ax2.set_xlim(-0.5, 0.5)
ax2.set_yticks([])
ax2.set_xlabel("Difference in proportions")
ax2.set_title(f"{conf}% CI for difference in proportions")
ax2.grid(axis="x", alpha=0.25)
st.pyplot(fig2)
