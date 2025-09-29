# pages/06_Two_Proportion_Z_Test.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from utils import *

st.title("Two-Proportion Z-Test")

st.write("This test is used to determine if **two population proportions** are equal or different.")

st.divider()
st.subheader("1. Write your hypothesis statements.")

st.write("""
        Hypothesis testing always begins with assumptions about the population proportions. 
        For two groups, we’ll call them $\\pi_1$ and $\\pi_2$.  
        Example: Do male and female Cadets skip breakfast at the same rate?
        """)

st.latex(r"""
    \begin{align*}
        H_0 &: \pi_1 = \pi_2 \\
        H_A &: \pi_1 > \pi_2, \ \pi_1 < \pi_2, \ \text{or } \pi_1 \neq \pi_2
    \end{align*}
""")

st.write("""
    Notice: hypotheses are always written about the **parameters** ($\\pi_1, \\pi_2$), 
    not about the observed sample statistics ($\\hat{p}_1, \\hat{p}_2$).
    """)

st.subheader("2. Gather your data.")

st.write("""
    Suppose we want to test if **male Cadets are more likely to skip breakfast than female Cadets**.
    - Out of 100 male Cadets surveyed, 30 say they skip breakfast.  
    - Out of 120 female Cadets surveyed, 20 say they skip breakfast.  

    Our hypotheses would be:
""")

st.latex(r"""\begin{align*}
    H_0 &: \pi_1 = \pi_2 \\
    H_A &: \pi_1 > \pi_2
\end{align*}""")

st.write("""
    First, calculate the observed proportions:
""")

st.latex(r"""
    \hat{p}_1 = \frac{30}{100} = 0.30, \quad 
    \hat{p}_2 = \frac{20}{120} \approx 0.167
""")

st.write("""
    Next, compute the **pooled proportion** under $H_0$ (because we assume $\\pi_1 = \\pi_2$):
""")

st.latex(r"""
    \hat{p} = \frac{X_1 + X_2}{n_1 + n_2}
             = \frac{30 + 20}{100 + 120}
             = \frac{50}{220} \approx 0.227
""")

st.write("The standard error for the difference in proportions is:")

st.latex(r"""
    SE = \sqrt{ \hat{p}(1-\hat{p})\left(\frac{1}{n_1} + \frac{1}{n_2}\right) }
""")

st.write("So the test statistic is:")

st.latex(r"""
    Z = \frac{\hat{p}_1 - \hat{p}_2}{SE}
""")

# Example calculation
n1, x1 = 100, 30
n2, x2 = 120, 20
p1_hat, p2_hat = x1/n1, x2/n2
p_pool = (x1 + x2) / (n1 + n2)
SE = np.sqrt(p_pool*(1-p_pool)*(1/n1 + 1/n2))
z_obs = (p1_hat - p2_hat)/SE
p_value = 1 - norm.cdf(z_obs)  # right-tailed
alpha = 0.05

# Plot
x = np.linspace(-4, 4, 400)
y = norm.pdf(x)

fig, ax = plt.subplots()
ax.plot(x, y, 'b', label="Standard Normal PDF")

# Shade rejection region
xx = np.linspace(z_obs, 4, 200)
ax.fill_between(xx, norm.pdf(xx), alpha=0.4, color='red', label="Rejection Region")

ax.axvline(z_obs, color='green', linestyle='--', label=f"Observed Z = {z_obs:.2f}")

ax.set_title("Right-Tailed Two-Proportion Z-Test")
ax.set_xlabel("z")
ax.set_ylabel("Density")
ax.legend(loc="upper right")
st.pyplot(fig)

st.write(f"""
Based on our standardized statistic ($Z = {z_obs:.2f}$), the p-value is about {p_value:.3f}.  
Since the p-value is {"less" if p_value < alpha else "greater"} than $\\alpha = 0.05$, we 
{"reject" if p_value < alpha else "fail to reject"} the null hypothesis.  
This means our data {"provides evidence that male Cadets skip breakfast at a higher rate" if p_value < alpha else "does not provide strong evidence of a difference"}.
""")

st.divider()
st.subheader("Two-Sided Example")

st.write("""
    Suppose instead we don’t care which group is larger — we just want to know if there is *any* difference.  
    Then we would use a **two-sided test**:
""")

st.latex(r"""\begin{align*}
    H_0 &: \pi_1 = \pi_2 \\
    H_A &: \pi_1 \neq \pi_2
\end{align*}""")

p_value_two = 2*(1 - norm.cdf(abs(z_obs)))
z_crit = norm.ppf(1 - alpha/2)

x = np.linspace(-4, 4, 400)
y = norm.pdf(x)

fig, ax = plt.subplots()
ax.plot(x, y, 'b', label="Standard Normal PDF")

# Shade both tails
xx = np.linspace(z_crit, 4, 200)
ax.fill_between(xx, norm.pdf(xx), alpha=0.4, color='red', label="Rejection Regions")
xx = np.linspace(-4, -z_crit, 200)
ax.fill_between(xx, norm.pdf(xx), alpha=0.4, color='red')

ax.axvline(z_obs, color='green', linestyle='--', label=f"Observed Z = {z_obs:.2f}")
ax.axvline(z_crit, color='pink', linestyle='--', label=f"Critical Z = ±{z_crit:.2f}")
ax.axvline(-z_crit, color='pink', linestyle='--')

ax.set_title("Two-Sided Two-Proportion Z-Test")
ax.set_xlabel("z")
ax.set_ylabel("Density")
ax.legend(loc="upper left", bbox_to_anchor=(1,1))
st.pyplot(fig)

st.write(f"""
For a two-sided test, the p-value is about {p_value_two:.3f}.  
We would {"reject" if p_value_two < alpha else "fail to reject"} $H_0$ at $\\alpha=0.05$.
""")

st.divider()
st.subheader("Practice: Two-Proportion Z-Test")

col1, col2 = st.columns(2)
with col1:
    n1 = st.number_input("Sample size group 1 (n₁)", min_value=1, value=100)
    x1 = st.number_input("Successes group 1 (X₁)", min_value=0, value=30)
    n2 = st.number_input("Sample size group 2 (n₂)", min_value=1, value=120)
    x2 = st.number_input("Successes group 2 (X₂)", min_value=0, value=20)
with col2:
    tail = tail_choice()
    alpha_percent = st.slider("α (%)", 1, 20, value=5)
    alpha = alpha_percent/100

p1_hat, p2_hat = x1/n1, x2/n2
p_pool = (x1 + x2) / (n1 + n2)
SE = np.sqrt(p_pool*(1-p_pool)*(1/n1 + 1/n2))
z_obs = (p1_hat - p2_hat)/SE

if tail == "right":
    pval = 1 - norm.cdf(z_obs)
elif tail == "left":
    pval = norm.cdf(z_obs)
else:
    pval = 2*min(norm.cdf(z_obs), 1 - norm.cdf(z_obs))

st.latex(
    f"\\hat p_1 = {p1_hat:.3f},\\quad "
    f"\\hat p_2 = {p2_hat:.3f},\\quad "
    f"Z={z_obs:.3f},\\quad "
    f"\\text{{p-value}}={pval:.3f}"
)
plot_normal_test(z_obs, alpha, tail)
(st.success if pval < alpha else st.warning)("Reject H₀" if pval < alpha else "Fail to reject H₀")
