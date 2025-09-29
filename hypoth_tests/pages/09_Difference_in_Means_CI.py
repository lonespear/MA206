# pages/09_Difference_in_Means_CI.py
import math
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from scipy.stats import t

st.set_page_config(page_title="Difference in Means Confidence Interval", layout="centered")
st.title("Difference in Means Confidence Interval")

# -----------------
# Explanation
# -----------------
st.write(
    "A confidence interval gives a range of plausible values for the **difference between two population means**, "
    "$\\mu_1 - \\mu_2$. This is useful when comparing averages across two groups."
)

st.write("Suppose group 1 has sample mean $\\bar{x}_1$, standard deviation $s_1$, and size $n_1$, "
         "and group 2 has $\\bar{x}_2, s_2, n_2$. The point estimate is:")

st.latex(r"""
\bar{x}_1 - \bar{x}_2
""")

st.write("The **standard error** (Welch’s formula) is:")

st.latex(r"""
SE = \sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}
""")

st.write("Then the $(1-\\alpha)100\\%$ confidence interval is:")

st.latex(r"""
(\bar{x}_1 - \bar{x}_2) \;\pm\; t^* \times SE
""")

st.caption("Here $t^*$ is the critical value from the t-distribution with approximate degrees of freedom (Welch–Satterthwaite).")

# -----------------
# Example
# -----------------
st.divider()
st.subheader("Example")

st.write("""
Suppose we compare average sleep hours between male and female Cadets:
- Male Cadets (group 1): $n_1 = 15$, $\\bar{x}_1 = 6.2$, $s_1 = 0.9$  
- Female Cadets (group 2): $n_2 = 18$, $\\bar{x}_2 = 6.8$, $s_2 = 0.7$
""")

n1, xbar1, s1 = 15, 6.2, 0.9
n2, xbar2, s2 = 18, 6.8, 0.7
diff = xbar1 - xbar2

SE = math.sqrt((s1**2)/n1 + (s2**2)/n2)
df = ((s1**2/n1 + s2**2/n2)**2) / ((s1**2/n1)**2/(n1-1) + (s2**2/n2)**2/(n2-1))
conf = 95
alpha = 1 - conf/100
t_star = t.ppf(1 - alpha/2, df)
lo = diff - t_star*SE
hi = diff + t_star*SE

st.latex(
    r"\bar{x}_1 = 6.2, \quad \bar{x}_2 = 6.8, \quad "
    r"\bar{x}_1 - \bar{x}_2 = -0.6"
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
ax.set_xlim(-2, 2)
ax.set_yticks([])
ax.set_xlabel("Difference in means")
ax.set_title(f"{conf}% CI for difference in means (df≈{df:.1f})")
ax.grid(axis="x", alpha=0.25)
st.pyplot(fig)

st.info(
    f"We are {conf}% confident that the true difference in means (male minus female sleep) "
    f"lies between {lo:.3f} and {hi:.3f}. "
    f"Since the interval does {'not ' if lo*hi>0 else ''}include 0, "
    f"we {'do' if lo*hi>0 else 'do not'} have evidence of a difference."
)

# -----------------
# Practice
# -----------------
st.divider()
st.subheader("Practice: Difference in Means CI")

col1, col2 = st.columns(2)
with col1:
    n1 = st.number_input("Sample size group 1 (n₁)", min_value=2, value=15)
    xbar1 = st.number_input("Sample mean group 1 (x̄₁)", value=6.2)
    s1 = st.number_input("Sample std dev group 1 (s₁)", value=0.9)
    n2 = st.number_input("Sample size group 2 (n₂)", min_value=2, value=18)
with col2:
    xbar2 = st.number_input("Sample mean group 2 (x̄₂)", value=6.8)
    s2 = st.number_input("Sample std dev group 2 (s₂)", value=0.7)
    conf = st.slider("Confidence level (%)", 80, 99, 95, step=1)

diff = xbar1 - xbar2
SE = math.sqrt((s1**2)/n1 + (s2**2)/n2)
df = ((s1**2/n1 + s2**2/n2)**2) / ((s1**2/n1)**2/(n1-1) + (s2**2/n2)**2/(n2-1))
alpha = 1 - conf/100
t_star = t.ppf(1 - alpha/2, df)
lo = diff - t_star*SE
hi = diff + t_star*SE

st.latex(
    f"\\bar x_1 = {xbar1:.3f},\\ "
    f"\\bar x_2 = {xbar2:.3f},\\ "
    f"\\bar x_1 - \\bar x_2 = {diff:.3f},\\ "
    f"df≈{df:.1f},\\ "
    f"CI = ({lo:.3f}, {hi:.3f})"
)

# Visualize
fig2, ax2 = plt.subplots(figsize=(6, 1.6))
ax2.hlines(1, lo, hi, color="tab:red", linewidth=4)
ax2.plot([lo, hi], [1, 1], "o", color="tab:red")
ax2.plot(diff, 1, "o", color="tab:blue")
ax2.axvline(0, color="black", linestyle="--", alpha=0.7)
ax2.set_xlim(-2, 2)
ax2.set_yticks([])
ax2.set_xlabel("Difference in means")
ax2.set_title(f"{conf}% CI for difference in means (df≈{df:.1f})")
ax2.grid(axis="x", alpha=0.25)
st.pyplot(fig2)
