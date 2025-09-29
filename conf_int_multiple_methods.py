# pages/04_One_Proportion_CI.py
import math
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from scipy.stats import norm

from utils import *

st.set_page_config(page_title="One-Proportion Confidence Interval", layout="centered")
st.title("One-Proportion Confidence Interval")

st.write(
    "Many times in addition to running an hypothesis test, a reliability estimate of where the true population" \
    "parameter may lie is also important to determine. These are called confidence intervals, and are calculated " \
    "with a reliability tolerance $\alpha$, not to be confused with significance level."
    "To compute a confidence interval for a single population proportion $(\pi)$ " \
    "from a sample with $X$ successes out of $n$ trials, the generic formula is:")

st.latex("CI_{\\alpha} = \\hat{p} \\pm SE \\times z^*")

st.write("where $ SE = \\sqrt{\\frac{\\hat{p}(1-\\hat{p})}{n}} $ and $ z^* $ is the inverse CDF of the Standard Normal distribution at quantile $ \\alpha / 2 $")

st.write("For a walkthrough of choose a method and confidence level below."
)



METHODS = {
    "Wald (textbook)": wald_ci,
    "Wilson (score)": wilson_ci,
    "Agresti–Coull": agresti_coull_ci,
    "Clopper–Pearson (exact)": clopper_pearson_ci,
}

def plot_interval(phat, lo, hi, conf, n, X, method_label):
    fig, ax = plt.subplots(figsize=(7, 1.8))
    ax.hlines(1, lo, hi, color="tab:red", linewidth=4)
    ax.plot([lo, hi], [1, 1], "o", color="tab:red")
    ax.plot(phat, 1, "o", color="tab:blue")
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(0.8, 1.2)
    ax.set_yticks([])
    ax.set_xlabel("Proportion")
    ax.set_title(f"{conf:.0f}% CI for one proportion  |  n={n}, X={X}  |  {method_label}")
    ax.grid(axis="x", alpha=0.25)
    # Labels
    ax.text(lo, 1.12, f"{lo:.3f}", ha="center")
    ax.text(hi, 1.12, f"{hi:.3f}", ha="center")
    ax.text(phat, 0.88, f"p̂={phat:.3f}", ha="center", color="tab:blue")
    return fig

def validity_warning(X, n, method):
    # Textbook rule-of-thumb for Wald
    if method == "Wald (textbook)":
        ok = (X >= 10) and ((n - X) >= 10)
        if not ok:
            st.warning(
                "Wald CI validity condition not met: need at least **10 successes and 10 failures** "
                f"(X={X}, n−X={n-X}). Consider **Wilson** or **Clopper–Pearson**."
            )

# -----------------
# Inputs
# -----------------
st.divider()
st.subheader("Inputs")

col1, col2, col3 = st.columns(3)
with col1:
    n = st.number_input("Sample size (n)", min_value=1, value=100, step=1)
    X = st.number_input("Successes (X)", min_value=0, max_value=int(n), value=min(56, int(n)), step=1)
with col2:
    conf = st.slider("Confidence level (%)", 80, 99, 95, step=1)
    method = st.selectbox("Method", list(METHODS.keys()), index=1)
with col3:
    show_compare = st.checkbox("Compare all methods", value=False)
    check_hypo = st.checkbox("Check if a hypothesized π₀ is inside the CI", value=False)
    if check_hypo:
        p0 = st.number_input("Hypothesized π₀", min_value=0.0, max_value=1.0, value=0.50, step=0.01)

if n <= 0:
    st.stop()

# -----------------
# Compute & display
# -----------------
phat, lo, hi = METHODS[method](int(X), int(n), float(conf))
validity_warning(int(X), int(n), method)

st.subheader("Result")
st.latex(
    r"\hat{p}=\frac{X}{n}="
    + f"{phat:.3f}"
    + r"\quad\Rightarrow\quad \text{CI} = \left("
    + f"{lo:.3f},\ {hi:.3f}"
    + r"\right)"
)

fig = plot_interval(phat, lo, hi, conf, n, X, method)
st.pyplot(fig)

# Interpretation / hypothesis relation
if check_hypo:
    inside = (lo <= p0 <= hi)
    if inside:
        st.info(
            f"Since $\pi_0={p0:.3f}$ lies **inside** the {conf:.0f}% CI, a two-sided z-test at "
            f"α={1-conf/100:.2f} would **fail to reject** $H_0: \pi=\pi_0$."
        )
    else:
        st.success(
            f"Since $\pi_0={p0:.3f}$ lies **outside** the {conf:.0f}% CI, a two-sided z-test at "
            f"α={1-conf/100:.2f} would **reject** \(H_0: \\pi=\\pi_0\)."
        )

st.caption(
    "Rule-of-thumb validity for Wald: at least 10 successes and 10 failures. "
    "Wilson and Clopper–Pearson perform better for small samples or extreme proportions."
)

# -----------------
# Compare methods (optional)
# -----------------
if show_compare:
    st.divider()
    st.subheader("Method comparison")

    rows = []
    for name, fn in METHODS.items():
        p, l, h = fn(int(X), int(n), float(conf))
        rows.append((name, p, l, h, h - l))
    # Simple table
    import pandas as pd
    df = pd.DataFrame(rows, columns=["Method", "p̂", "Lower", "Upper", "Width"])
    st.dataframe(df.style.format({"p̂": "{:.3f}", "Lower": "{:.3f}", "Upper": "{:.3f}", "Width": "{:.3f}"}), use_container_width=True)

    # Stacked plot of all intervals
    fig2, ax2 = plt.subplots(figsize=(7, 2 + 0.6 * len(METHODS)))
    y = np.arange(len(METHODS)) + 1
    for i, (name, p, l, h, w) in enumerate(rows, start=1):
        color = "tab:red" if name == method else "tab:gray"
        ax2.hlines(i, l, h, color=color, linewidth=4)
        ax2.plot([l, h], [i, i], "o", color=color)
        ax2.plot(p, i, "o", color="tab:blue")
        ax2.text(h + 0.01, i, name, va="center", fontsize=10)
    ax2.axvline(phat, color="tab:blue", ls="--", alpha=0.5)
    ax2.set_yticks([])
    ax2.set_xlim(-0.05, 1.05)
    ax2.set_xlabel("Proportion")
    ax2.set_title(f"All methods at {conf:.0f}% (n={n}, X={X})")
    ax2.grid(axis="x", alpha=0.25)
    st.pyplot(fig2)

# -----------------
# Sample size planner (bonus)
# -----------------
st.divider()
with st.expander("Sample size planner (margin of error)"):
    st.write(
        "Solve $ n \ge \dfrac{z^2 p^*(1-p^*)}{m^2} $ for a desired margin of error $(m)$."
        "If $(p^*)$ is unknown, use the conservative $(p^*=0.5)$."
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        conf2 = st.slider("Confidence (%)", 80, 99, value=int(conf), key="ss_conf")
    with c2:
        m = st.number_input("Margin of error (m)", min_value=0.001, max_value=0.25, value=0.05, step=0.005)
    with c3:
        p_star = st.number_input("Planning value p*", min_value=0.0, max_value=1.0, value=float(phat), step=0.01)

    alpha2 = 1 - conf2 / 100
    z2 = norm.ppf(1 - alpha2 / 2)
    n_req = math.ceil((z2**2) * p_star * (1 - p_star) / (m**2))
    st.info(f"Required sample size: **n ≥ {n_req}**")
