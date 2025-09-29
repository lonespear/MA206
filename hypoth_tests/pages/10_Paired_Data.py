# pages/10_Paired_Data.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t
from utils import *

st.title("Working with Paired Data")

st.subheader("Paired t-Test")

st.write("This test is used to determine if the **mean difference** between two related groups is equal to some value (usually 0).")

st.divider()
st.subheader("1. Write your hypothesis statements.")

st.write("""
Paired data arises when each subject has two linked measurements — for example, before and after training, or left and right foot strength.  
We define the difference for each subject as $d_i = x_{1i} - x_{2i}$.
""")

st.latex(r"""
\begin{align*}
    H_0 &: \mu_d = 0 \\
    H_A &: \mu_d > 0,\ \mu_d < 0,\ \text{or } \mu_d \neq 0
\end{align*}
""")

st.write("Here $\\mu_d$ is the **population mean of the differences**. The hypotheses always refer to the population, not the sample.")

st.subheader("2. Gather your data.")

st.write("""
Suppose we test whether a new sleep program helps Cadets.  
We record hours of sleep **before and after** the program for 10 Cadets.  
We compute differences (After − Before). The sample mean of differences is $\\bar{d} = 0.6$, with $s_d = 0.5$.
""")

st.latex(r"""
n = 10, \quad \bar{d} = 0.6, \quad s_d = 0.5
""")

st.subheader("3. Compute the test statistic.")

st.write("""
For paired data, we reduce the problem to a **one-sample t-test on the differences**:
""")

st.latex(r"""
t = \frac{\bar{d} - \mu_{d,0}}{s_d/\sqrt{n}}, \quad df = n-1
""")

st.write("In our example, testing $H_0: \mu_d = 0$:")

# Example calc
n = 10
dbar = 0.6
sd = 0.5
mu_d0 = 0
df = n - 1
t_obs = (dbar - mu_d0) / (sd / np.sqrt(n))
alpha = 0.05
p_value = 1 - t.cdf(t_obs, df)  # right-tailed
tcrit = t.ppf(1 - alpha, df)

st.latex(
    r"t = \frac{0.6 - 0}{0.5/\sqrt{10}} \approx "
    + f"{t_obs:.2f}"
)

# Plot
x = np.linspace(-4, 4, 400)
y = t.pdf(x, df)

fig, ax = plt.subplots()
ax.plot(x, y, 'b', label=f"t-dist (df={df})")

# Shade rejection region
xx = np.linspace(tcrit, 4, 200)
ax.fill_between(xx, t.pdf(xx, df), alpha=0.4, color='red', label="Rejection Region")

# Draw observed t
ax.axvline(t_obs, color='green', linestyle='--', label=f"Observed t = {t_obs:.2f}")
ax.axvline(tcrit, color='pink', linestyle='--', label=f"Critical t = {tcrit:.2f}")

# Annotate
ax.annotate(
    f"P-value = {p_value:.3f}",
    xy=(t_obs, t.pdf(t_obs, df)),
    xytext=(t_obs+0.5, 0.05),
    arrowprops=dict(facecolor="black", shrink=0.05, width=1, headwidth=8)
)

ax.set_title("Right-Tailed Paired t-Test Example")
ax.set_xlabel("t")
ax.set_ylabel("Density")
ax.legend(loc="upper right")
st.pyplot(fig)

st.write(f"""
Based on our standardized statistic ($t = {t_obs:.2f}$ with df={df}), the p-value is about {p_value:.3f}.  
Since the p-value is {"less" if p_value < alpha else "greater"} than $\\alpha=0.05$, we 
{"reject" if p_value < alpha else "fail to reject"} the null hypothesis.  
""")

st.divider()
st.subheader("Two-Sided Example")

st.write("""
Suppose instead we want to test whether the sleep program changes sleep in *either direction* (more or less sleep).  
Then the hypotheses are:
""")

st.latex(r"""\begin{align*}
    H_0 &: \mu_d = 0 \\
    H_A &: \mu_d \neq 0
\end{align*}""")

p_value_two = 2*(1 - t.cdf(abs(t_obs), df))
tcrit_two = t.ppf(1 - alpha/2, df)

# Plot
x = np.linspace(-4, 4, 400)
y = t.pdf(x, df)
fig, ax = plt.subplots()
ax.plot(x, y, 'b', label=f"t-dist (df={df})")

xx = np.linspace(tcrit_two, 4, 200)
ax.fill_between(xx, t.pdf(xx, df), alpha=0.4, color='red', label="Rejection Regions")
xx = np.linspace(-4, -tcrit_two, 200)
ax.fill_between(xx, t.pdf(xx, df), alpha=0.4, color='red')

ax.axvline(t_obs, color='green', linestyle='--', label=f"Observed t = {t_obs:.2f}")
ax.axvline(tcrit_two, color='pink', linestyle='--', label=f"Critical t = ±{tcrit_two:.2f}")
ax.axvline(-tcrit_two, color='pink', linestyle='--')

ax.set_title("Two-Sided Paired t-Test Example")
ax.set_xlabel("t")
ax.set_ylabel("Density")
ax.legend(loc="upper right")
st.pyplot(fig)

st.write(f"""
For a two-sided test, the p-value is about {p_value_two:.3f}.  
We would {"reject" if p_value_two < alpha else "fail to reject"} $H_0$ at $\\alpha=0.05$.
""")

# -----------------
# Practice
# -----------------
st.divider()
st.subheader("Practice: Paired t-Test")

col1, col2 = st.columns(2)
with col1:
    n = st.number_input("Number of pairs (n)", min_value=2, value=10)
    dbar = st.number_input("Sample mean difference (d̄)", value=0.6)
    sd = st.number_input("Sample std dev of differences (s_d)", value=0.5)
    mu_d0 = st.number_input("Null mean difference (μ_d₀)", value=0.0)
with col2:
    tail = tail_choice()
    alpha_percent = st.slider("α (%)", 1, 20, value=5)
    alpha = alpha_percent/100

df = n - 1
t_obs = (dbar - mu_d0) / (sd / np.sqrt(n))

if tail == "right":
    pval = 1 - t.cdf(t_obs, df)
elif tail == "left":
    pval = t.cdf(t_obs, df)
else:
    pval = 2*min(t.cdf(t_obs, df), 1 - t.cdf(t_obs, df))

st.latex(
    f"\\bar d = {dbar:.3f},\\ "
    f"s_d = {sd:.3f},\\ "
    f"n = {n},\\ "
    f"t = {t_obs:.3f},\\ "
    f"df = {df},\\ "
    f"\\text{{p-value}}={pval:.3f}"
)

plot_t_test(t_obs, alpha, tail, df)
(st.success if pval < alpha else st.warning)("Reject H₀" if pval < alpha else "Fail to reject H₀")


st.divider()

st.subheader("Paired Data Confidence Interval")

# -----------------
# Explanation
# -----------------
st.write(
    "When we collect **paired data**, each observation in group 1 is naturally linked with an "
    "observation in group 2. Examples: before/after measurements, or matched Cadets in two conditions. "
    "The key idea: analyze the *differences* between pairs."
)

st.write("If $d_i = x_{1i} - x_{2i}$ is the difference for pair $i$, then we reduce the problem to a one-sample CI:")

st.latex(r"""
\bar{d} = \frac{1}{n}\sum_{i=1}^n d_i, \quad s_d = \text{stdev of the differences}
""")

st.write("The standard error is:")

st.latex(r"""
SE = \frac{s_d}{\sqrt{n}}
""")

st.write("So the $(1-\\alpha)100\\%$ confidence interval is:")

st.latex(r"""
\bar{d} \;\pm\; t^* \times SE
""")

st.caption("Here $t^*$ is the critical value from the t-distribution with $n-1$ degrees of freedom.")

# -----------------
# Example
# -----------------
st.divider()
st.subheader("Example")

st.write("""
Suppose we want to test if a new sleep program helps Cadets get more rest.  
We survey 10 Cadets before and after the program. The average difference (After − Before) is  
$\\bar{d} = 0.6$ hours with standard deviation $s_d = 0.5$.
""")

n = 10
dbar = 0.6
sd = 0.5
df = n - 1
conf = 95
alpha = 1 - conf/100
t_star = t.ppf(1 - alpha/2, df)
SE = sd / math.sqrt(n)
lo = dbar - t_star*SE
hi = dbar + t_star*SE

st.latex(
    r"\bar{d} = 0.6, \quad s_d = 0.5, \quad n=10"
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
ax.plot(dbar, 1, "o", color="tab:blue")
ax.axvline(0, color="black", linestyle="--", alpha=0.7)  # line at 0
ax.set_xlim(-0.5, 1.5)
ax.set_yticks([])
ax.set_xlabel("Mean difference (After − Before)")
ax.set_title(f"{conf}% CI for paired mean difference (df={df})")
ax.grid(axis="x", alpha=0.25)
st.pyplot(fig)

st.info(
    f"We are {conf}% confident that the true mean difference lies between {lo:.3f} and {hi:.3f}. "
    f"Since the interval does {'not ' if lo*hi>0 else ''}include 0, "
    f"we {'do' if lo*hi>0 else 'do not'} have evidence of a change."
)

# -----------------
# Practice
# -----------------
st.divider()
st.subheader("Practice: Paired Data CI")

col1, col2 = st.columns(2)
with col1:
    n = st.number_input("Number of pairs (n)", min_value=2, value=10, key="ci_n")
    dbar = st.number_input("Sample mean of differences (d̄)", value=0.6, step=0.1, key="ci_dbar")
with col2:
    sd = st.number_input("Sample std dev of differences (s_d)", value=0.5, step=0.1, key="ci_sd")
    conf = st.slider("Confidence level (%)", 80, 99, 95, step=1, key="ci_conf")

df = n - 1
alpha = 1 - conf/100
t_star = t.ppf(1 - alpha/2, df)
SE = sd / math.sqrt(n)
lo = dbar - t_star*SE
hi = dbar + t_star*SE

st.latex(
    f"\\bar d = {dbar:.3f},\\ "
    f"s_d = {sd:.3f},\\ "
    f"n = {n},\\ "
    f"df = {df},\\ "
    f"CI = ({lo:.3f}, {hi:.3f})"
)

# Visualize
fig2, ax2 = plt.subplots(figsize=(6, 1.6))
ax2.hlines(1, lo, hi, color="tab:red", linewidth=4)
ax2.plot([lo, hi], [1, 1], "o", color="tab:red")
ax2.plot(dbar, 1, "o", color="tab:blue")
ax2.axvline(0, color="black", linestyle="--", alpha=0.7)
ax2.set_xlim(lo-0.5, hi+0.5)
ax2.set_yticks([])
ax2.set_xlabel("Mean difference (After − Before)")
ax2.set_title(f"{conf}% CI for paired mean difference (df={df})")
ax2.grid(axis="x", alpha=0.25)
st.pyplot(fig2)
