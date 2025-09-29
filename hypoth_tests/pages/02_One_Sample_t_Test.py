# pages/05_One_Sample_t_Test.py
import streamlit as st
import numpy as np
from scipy.stats import t
from utils import *

st.title("One-Sample t-Test")

st.write("This test is used to determine if the mean of a quantitative variable equals some specific value.")

st.divider()
st.subheader("1. Write your hypothesis statements.")

st.write("""
        Hypothesis testing always begins with an assumption about the population mean $\\mu$. 
        For example, is the average number of push-ups a Cadet can do equal to the Army’s fitness standard? 
        Or is the average amount of sleep less than 7 hours per night?
        """)

st.latex(r"""
    \begin{align*}
        H_0 &: \mu = \text{Any value of interest (a parameter)} \\
        H_A &: \mu >, <, \text{ or } \neq \text{ that same value}
    \end{align*}
""")

st.write(r"""
    We write $\mu$ because hypotheses always refer to the **population mean**. Our sample will give us $\bar{x}$, 
    the sample mean, and we’ll compare that to the hypothesized population mean.
    """)

st.subheader("2. Gather your data related to your research question.")

st.write(r""" 
    Suppose I believe Cadets sleep less than 7 hours per night. To test this, I randomly survey 20 Cadets 
    and find that their average sleep was $\bar{x} = 6.5$ hours with sample standard deviation $s = 0.8$.
    
    My hypothesis statements are:
    """)

st.latex(r"""\begin{align*}
H_0:& \mu = 7.0 \text{ hours} \\
H_A:& \mu < 7.0 \text{ hours}
\end{align*}""")

st.write(""" 
    Now we can compute our standardized statistic. For means, we use the **t-statistic**:
""")

st.latex(r"""
    t = \frac{\bar{x} - \mu_0}{s / \sqrt{n}}, \quad \text{ where } \mu_0 \text{ is the null hypothesis mean.}
""")

st.write(""" 
    In our example:
""")

st.latex(r"""
    n = 20, \quad \bar{x} = 6.5, \quad s = 0.8, \quad \mu_0 = 7.0
""")

st.latex(r"""
    t = \frac{6.5 - 7.0}{0.8 / \sqrt{20}} \approx -2.80
""")

# Compute test statistic, critical value, p-value
n, xbar, s, mu0 = 20, 6.5, 0.8, 7.0
t_obs = (xbar - mu0) / (s / np.sqrt(n))
df = n - 1
alpha = 0.05
p_value = t.cdf(t_obs, df)  # left-tailed
t_crit = t.ppf(alpha, df)

# Plot
import matplotlib.pyplot as plt
x = np.linspace(-4, 4, 400)
y = t.pdf(x, df)

fig, ax = plt.subplots()
ax.plot(x, y, 'b', label=f"t-dist (df={df})")

# Shade rejection region
xx = np.linspace(-4, t_crit, 200)
ax.fill_between(xx, t.pdf(xx, df), alpha=0.4, color='red', label="Rejection Region")

# Draw observed t
ax.axvline(t_obs, color='green', linestyle='--', label=f"Observed t = {t_obs:.2f}")
ax.axvline(t_crit, color='pink', linestyle='--', label=f"Critical t = {t_crit:.2f}")

# Annotate
ax.annotate(
    f"P-value = {p_value:.3f}",
    xy=(t_obs, t.pdf(t_obs, df)),
    xytext=(-3, 0.05),
    arrowprops=dict(facecolor="black", shrink=0.05, width=1, headwidth=8)
)

ax.set_title("Left-Tailed t-Test Example")
ax.set_xlabel("t")
ax.set_ylabel("Density")
ax.legend(loc="upper right")
st.pyplot(fig)

st.write(f"""
    Based on our standardized statistic ($t = {t_obs:.2f}$ with df={df}), the p-value is about {p_value:.3f}.
    Since this p-value is **less than α = 0.05**, we would **reject the null hypothesis**.
    
    This means our data provides evidence that Cadets sleep less than 7 hours per night.
""")

st.divider()

st.subheader("Two-Sided Test Example")

st.write("""
    Suppose I believe the average number of push-ups Cadets can do is **different from 50**, 
    but I don’t care if it’s higher or lower. I sample 15 Cadets, who average $\\bar{x} = 47$ push-ups with $s = 5$.
""")

st.latex(r"""\begin{align*}
    H_0 &: \mu = 50 \\
    H_A &: \mu \neq 50
\end{align*}""")

n, xbar, s, mu0 = 15, 47, 5, 50
t_obs = (xbar - mu0) / (s / np.sqrt(n))
df = n - 1
alpha = 0.05
p_value = 2 * (1 - t.cdf(abs(t_obs), df))
t_crit = t.ppf(1 - alpha/2, df)

st.latex(r"""
    t = \frac{47 - 50}{5/\sqrt{15}} \approx """ + f"{t_obs:.2f}"
)

# Plot
x = np.linspace(-4, 4, 400)
y = t.pdf(x, df)

fig, ax = plt.subplots()
ax.plot(x, y, 'b', label=f"t-dist (df={df})")

# Shade rejection regions
xx = np.linspace(t_crit, 4, 200)
ax.fill_between(xx, t.pdf(xx, df), alpha=0.4, color='red', label="Rejection Regions")
xx = np.linspace(-4, -t_crit, 200)
ax.fill_between(xx, t.pdf(xx, df), alpha=0.4, color='red')

# Draw observed t and criticals
ax.axvline(t_obs, color='green', linestyle='--', label=f"Observed t = {t_obs:.2f}")
ax.axvline(-t_obs, color='green', linestyle='--')
ax.axvline(t_crit, color='pink', linestyle='--', label=f"Critical t = ±{t_crit:.2f}")
ax.axvline(-t_crit, color='pink', linestyle='--')

# Annotate
ax.annotate(
    f"P-value = {p_value:.3f}",
    xy=(t_obs, t.pdf(t_obs, df)),
    xytext=(-2.5, 0.1),
    arrowprops=dict(facecolor="black", shrink=0.05, width=1, headwidth=8)
)

ax.set_title("Two-Sided t-Test Example")
ax.set_xlabel("t")
ax.set_ylabel("Density")
ax.legend(loc="upper right")
st.pyplot(fig)

st.write(f"""
    Based on our standardized statistic ($t = {t_obs:.2f}$ with df={df}), the two-sided p-value is about {p_value:.3f}.
    Since this p-value is {'less' if p_value < alpha else 'greater'} than α = 0.05, we would 
    {"reject" if p_value < alpha else "fail to reject"} the null hypothesis.
""")

st.divider()

st.subheader("Practice: One-Sample t-Test")
col1, col2 = st.columns(2)
with col1:
    n = st.number_input("Sample size (n)", min_value=2, value=20)
    xbar = st.number_input("Sample mean (x̄)", value=6.5)
    s = st.number_input("Sample standard deviation (s)", value=0.8)
    mu0 = st.number_input("Null mean (μ₀)", value=7.0)
with col2:
    tail = tail_choice()
    alpha_percent = st.slider("α (%)", 1, 20, value=5)
    alpha = alpha_percent/100

t_obs = (xbar - mu0) / (s / np.sqrt(n))
df = n - 1

if tail == "right":
    pval = 1 - t.cdf(t_obs, df)
elif tail == "left":
    pval = t.cdf(t_obs, df)
else:
    pval = 2*min(t.cdf(t_obs, df), 1 - t.cdf(t_obs, df))

st.latex(f"\\bar x = {xbar:.3f},\\quad t={t_obs:.3f},\\quad df={df},\\quad \\text{{p-value}}={pval:.3f}")
plot_t_test(t_obs, alpha, tail, df)
(st.success if pval < alpha else st.warning)("Reject H₀" if pval < alpha else "Fail to reject H₀")
