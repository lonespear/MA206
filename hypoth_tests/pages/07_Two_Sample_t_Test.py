# pages/07_Two_Sample_t_Test.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t
from utils import *

st.title("Two-Sample t-Test")

st.write("This test is used to determine if **two population means** are equal or different.")

st.divider()
st.subheader("1. Write your hypothesis statements.")

st.write("""
        We now have two groups, each with their own population mean: $\\mu_1$ and $\\mu_2$.  
        Example: Do male and female Cadets get the same average hours of sleep per night?
        """)

st.latex(r"""
    \begin{align*}
        H_0 &: \mu_1 = \mu_2 \\
        H_A &: \mu_1 > \mu_2,\ \mu_1 < \mu_2,\ \text{or } \mu_1 \neq \mu_2
    \end{align*}
""")

st.write("""
    As always, hypotheses are written about the **parameters** ($\\mu_1, \\mu_2$), 
    not the observed sample means.
    """)

st.subheader("2. Gather your data.")

st.write("""
    Suppose we want to test whether **male and female Cadets get the same average sleep**.  
    - From 15 male Cadets, the sample mean is $\\bar{x}_1 = 6.2$ hours with $s_1 = 0.9$.  
    - From 18 female Cadets, the sample mean is $\\bar{x}_2 = 6.8$ hours with $s_2 = 0.7$.  
""")

st.latex(r"""\begin{align*}
    H_0 &: \mu_1 = \mu_2 \\
    H_A &: \mu_1 \neq \mu_2
\end{align*}""")

st.write("We calculate the **standard error** using the pooled variance formula:")

st.latex(r"""
    SE = \sqrt{ \frac{s_1^2}{n_1} + \frac{s_2^2}{n_2} }
""")

st.write("Then the test statistic is:")

st.latex(r"""
    t = \frac{\bar{x}_1 - \bar{x}_2}{SE}
""")

# Example calculation
n1, xbar1, s1 = 15, 6.2, 0.9
n2, xbar2, s2 = 18, 6.8, 0.7

SE = np.sqrt((s1**2)/n1 + (s2**2)/n2)
t_obs = (xbar1 - xbar2)/SE

# Welch–Satterthwaite df
df = ((s1**2/n1 + s2**2/n2)**2) / ((s1**2/n1)**2/(n1-1) + (s2**2/n2)**2/(n2-1))
alpha = 0.05
p_value = 2*(1 - t.cdf(abs(t_obs), df))
tcrit = t.ppf(1 - alpha/2, df)

# Plot
x = np.linspace(-4, 4, 400)
y = t.pdf(x, df)

fig, ax = plt.subplots()
ax.plot(x, y, 'b', label=f"t-dist (df≈{df:.1f})")

xx = np.linspace(tcrit, 4, 200)
ax.fill_between(xx, t.pdf(xx, df), alpha=0.4, color='red', label="Rejection Regions")
xx = np.linspace(-4, -tcrit, 200)
ax.fill_between(xx, t.pdf(xx, df), alpha=0.4, color='red')

ax.axvline(t_obs, color='green', linestyle='--', label=f"Observed t = {t_obs:.2f}")
ax.axvline(tcrit, color='pink', linestyle='--', label=f"Critical t = ±{tcrit:.2f}")
ax.axvline(-tcrit, color='pink', linestyle='--')

ax.set_title("Two-Sided Two-Sample t-Test Example")
ax.set_xlabel("t")
ax.set_ylabel("Density")
ax.legend(loc="upper right")
st.pyplot(fig)

st.write(f"""
Based on our standardized statistic ($t = {t_obs:.2f}$ with df≈{df:.1f}), the p-value is about {p_value:.3f}.  
Since the p-value is {"less" if p_value < alpha else "greater"} than $\\alpha=0.05$, we 
{"reject" if p_value < alpha else "fail to reject"} the null hypothesis.  
This means our data {"suggests a difference in sleep hours" if p_value < alpha else "does not provide strong evidence of a difference"} between male and female Cadets.
""")

st.divider()
st.subheader("Practice: Two-Sample t-Test")

col1, col2 = st.columns(2)
with col1:
    n1 = st.number_input("Sample size group 1 (n₁)", min_value=2, value=15)
    xbar1 = st.number_input("Sample mean group 1 (x̄₁)", value=6.2)
    s1 = st.number_input("Sample std dev group 1 (s₁)", value=0.9)
    n2 = st.number_input("Sample size group 2 (n₂)", min_value=2, value=18)
with col2:
    xbar2 = st.number_input("Sample mean group 2 (x̄₂)", value=6.8)
    s2 = st.number_input("Sample std dev group 2 (s₂)", value=0.7)
    tail = tail_choice()
    alpha_percent = st.slider("α (%)", 1, 20, value=5)
    alpha = alpha_percent/100

SE = np.sqrt((s1**2)/n1 + (s2**2)/n2)
t_obs = (xbar1 - xbar2)/SE
df = ((s1**2/n1 + s2**2/n2)**2) / ((s1**2/n1)**2/(n1-1) + (s2**2/n2)**2/(n2-1))

if tail == "right":
    pval = 1 - t.cdf(t_obs, df)
elif tail == "left":
    pval = t.cdf(t_obs, df)
else:
    pval = 2*min(t.cdf(t_obs, df), 1 - t.cdf(t_obs, df))

st.latex(
    f"\\bar x_1 = {xbar1:.3f},\\ "
    f"\\bar x_2 = {xbar2:.3f},\\ "
    f"t = {t_obs:.3f},\\ "
    f"df≈{df:.1f},\\ "
    f"\\text{{p-value}}={pval:.3f}"
)

plot_t_test(t_obs, alpha, tail, round(df,2))
(st.success if pval < alpha else st.warning)("Reject H₀" if pval < alpha else "Fail to reject H₀")
