# pages/05_One_Sample_Mean_CI.py
import math
import matplotlib.pyplot as plt
import streamlit as st
from scipy.stats import t

st.set_page_config(page_title="One-Sample Mean Confidence Interval", layout="centered")
st.title("One-Sample Mean Confidence Interval")

# -----------------
# Explanation
# -----------------
st.write(
    "A confidence interval gives a range of plausible values for the true population mean $(\\mu)$. "
    "For a sample with size $n$, mean $\\bar{x}$, and standard deviation $s$, the sample mean is:"
)
st.latex(r"\bar{x} = \frac{1}{n}\sum_{i=1}^n x_i")

st.write("The **standard error (SE)** is:")
st.latex(r"SE = \frac{s}{\sqrt{n}}")

st.write("Then a $(1-\\alpha)100\%$ confidence interval is given by:")
st.latex(r"\bar{x} \;\pm\; t^* \times SE")

st.caption("Here $t^*$ is the critical value from the Student t-distribution with $n-1$ degrees of freedom.")

# -----------------
# Inputs
# -----------------
st.divider()
st.subheader("Inputs")

col1, col2, col3 = st.columns(3)
with col1:
    n = st.number_input("Sample size (n)", min_value=2, value=25, step=1)
with col2:
    xbar = st.number_input("Sample mean (x̄)", value=50.0, step=0.5)
with col3:
    s = st.number_input("Sample standard deviation (s)", min_value=0.0001, value=10.0, step=0.5)

conf = st.slider("Confidence level (%)", 80, 99, 95, step=1)

# -----------------
# Compute CI (t-distribution)
# -----------------
alpha = 1 - conf / 100
df = n - 1
t_star = t.ppf(1 - alpha / 2, df)
SE = s / math.sqrt(n)
lo = xbar - t_star * SE
hi = xbar + t_star * SE

# -----------------
# Display results
# -----------------
st.subheader("Result")

st.latex(
    r"\bar{x} = "
    + f"{xbar:.3f}"
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
ax.plot(xbar, 1, "o", color="tab:blue")
ax.set_xlim(xbar - 4 * SE, xbar + 4 * SE)  # auto-scale around mean
ax.set_yticks([])
ax.set_xlabel("Mean")
ax.set_title(f"{conf}% CI for one mean (n={n}, df={df})")
ax.grid(axis="x", alpha=0.25)
st.pyplot(fig)

# -----------------
# Interpretation
# -----------------
st.info(
    f"We are {conf}% confident that the true population mean lies between "
    f"{lo:.3f} and {hi:.3f}."
)
