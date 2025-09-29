import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, t, beta
import math

# Vectorized interval generator (fast)
def compute_intervals(pop, n, reps, conf, seed=None):
    if seed is not None:
        rng = np.random.default_rng(seed)
    else:
        rng = np.random.default_rng()
    true_mean = float(np.mean(pop))
    alpha = 1 - conf/100
    t_star = t.ppf(1 - alpha/2, df=n-1)

    # vectorized bootstrap
    idx = rng.integers(0, pop.size, size=(reps, n))
    samples = pop[idx]
    xbar = samples.mean(axis=1)
    se = samples.std(axis=1, ddof=1) / np.sqrt(n)
    lo = xbar - t_star*se
    hi = xbar + t_star*se
    hit = (lo <= true_mean) & (true_mean <= hi)
    return dict(true_mean=true_mean, xbar=xbar, lo=lo, hi=hi, hit=hit)

def draw_frame(data, k, conf, n, reps, height_px=900):
    """Draw first k intervals. Returns a matplotlib fig for st.pyplot."""
    true_mean = data["true_mean"]
    lo, hi, xbar, hit = data["lo"][:k], data["hi"][:k], data["xbar"][:k], data["hit"][:k]
    y = np.arange(1, k+1)

    # scale fig height to #reps (taller window)
    height_in = max(6, min(20, 0.22 * reps))  # 0.22in per interval, capped
    fig, ax = plt.subplots(figsize=(7, height_in))

    colors = np.where(hit, "green", "red")
    ax.hlines(y, lo, hi, colors=colors, linewidth=2)
    ax.scatter(xbar, y, c=colors, s=18, zorder=3)

    ax.axvline(true_mean, color="blue", ls="--")
    ax.set_ylim(0, reps + 1)
    ax.set_xlabel("Value")
    ax.set_ylabel("Sample #")
    cov_so_far = hit.mean() * 100 if k > 0 else 0.0
    ax.set_title(f"{conf}% Confidence Intervals (n={n}, reps={reps})  |  Coverage so far: {cov_so_far:0.1f}%")
    ax.grid(alpha=0.2, axis="x")
    return fig

def plot_normal_test(z_obs, alpha, tail):
    x = np.linspace(-3.8, 3.8, 600)
    y = norm.pdf(x)

    fig, ax = plt.subplots()
    ax.plot(x, y, label="Standard Normal PDF")

    if tail == "right":
        zcrit = norm.ppf(1 - alpha)
        xx = np.linspace(zcrit, x.max(), 300)
        ax.fill_between(xx, norm.pdf(xx), alpha=0.4, label=f"Rejection (z ≥ {zcrit:.2f})")
    elif tail == "left":
        zcrit = norm.ppf(alpha)
        xx = np.linspace(x.min(), zcrit, 300)
        ax.fill_between(xx, norm.pdf(xx), alpha=0.4, label=f"Rejection (z ≤ {zcrit:.2f})")
    else:  # two
        zcrit = norm.ppf(1 - alpha/2)
        xx = np.linspace(zcrit, x.max(), 300)
        ax.fill_between(xx, norm.pdf(xx), alpha=0.4, label=f"Rejection (|z| ≥ {zcrit:.2f})")
        xx = np.linspace(x.min(), -zcrit, 300)
        ax.fill_between(xx, norm.pdf(xx), alpha=0.4)

    ax.axvline(z_obs, color="green", linestyle="--", label=f"Observed z = {z_obs:.3f}")
    if tail == "two":
        ax.axvline(-z_obs, color="green", linestyle="--")

    if tail == "two":
        ax.axvline(zcrit, color="pink", linestyle="--", label=f"Critical ±{zcrit:.2f}")
        ax.axvline(-zcrit, color="pink", linestyle="--")
    else:
        ax.axvline(zcrit, color="pink", linestyle="--", label=f"Critical {zcrit:.2f}")

    ax.set_xlabel("z")
    ax.set_ylabel("Density")
    ax.set_title(
        "Normal model — Right tail" if tail=="right" else
        "Normal model — Left tail" if tail=="left" else
        "Normal model — Two tails"
    )
    ax.legend(loc="upper right", bbox_to_anchor=(1,1))
    st.pyplot(fig)

def plot_t_test(t_obs, alpha, tail, df):
    alpha = float(alpha)
    x = np.linspace(-4.5, 4.5, 700)
    y = t.pdf(x, df)

    fig, ax = plt.subplots()
    ax.plot(x, y, label=f"t PDF (df={df})")

    if tail == "right":
        tcrit = t.ppf(1 - alpha, df)
        xx = np.linspace(tcrit, x.max(), 300)
        ax.fill_between(xx, t.pdf(xx, df), alpha=0.4, label=f"Rejection (t ≥ {tcrit:.2f})")
    elif tail == "left":
        tcrit = t.ppf(alpha, df)
        xx = np.linspace(x.min(), tcrit, 300)
        ax.fill_between(xx, t.pdf(xx, df), alpha=0.4, label=f"Rejection (t ≤ {tcrit:.2f})")
    else:  # two
        tcrit = t.ppf(1 - alpha/2, df)
        xx = np.linspace(tcrit, x.max(), 300)
        ax.fill_between(xx, t.pdf(xx, df), alpha=0.4, label=f"Rejection (|t| ≥ {tcrit:.2f})")
        xx = np.linspace(x.min(), -tcrit, 300)
        ax.fill_between(xx, t.pdf(xx, df), alpha=0.4)

    ax.axvline(t_obs, color="green", linestyle="--", label=f"Observed t = {t_obs:.3f}")
    if tail == "two":
        ax.axvline(-t_obs, color="green", linestyle="--")

    if tail == "two":
        ax.axvline(tcrit, color="pink", linestyle="--", label=f"Critical ±{tcrit:.2f}")
        ax.axvline(-tcrit, color="pink", linestyle="--")
    else:
        ax.axvline(tcrit, color="pink", linestyle="--", label=f"Critical {tcrit:.2f}")

    ax.set_xlabel("t")
    ax.set_ylabel("Density")
    ax.set_title(
        f"t model (df={df}) — Right tail" if tail=="right" else
        f"t model (df={df}) — Left tail" if tail=="left" else
        f"t model (df={df}) — Two tails"
    )
    ax.legend(loc="upper right")
    st.pyplot(fig)

def tail_choice(label_default="One-Sided (Right-Tailed, >)"):
    opt = st.radio(
        "Choose test type:",
        ["One-Sided (Right-Tailed, >)", "One-Sided (Left-Tailed, <)", "Two-Sided (≠)"],
        index=["One-Sided (Right-Tailed, >)", "One-Sided (Left-Tailed, <)", "Two-Sided (≠)"].index(label_default)
    )
    if "Right" in opt: return "right"
    if "Left" in opt:  return "left"
    return "two"

def wald_ci(X: int, n: int, conf: float):
    """Textbook Wald interval: phat ± z * sqrt(phat(1-phat)/n). Clip to [0,1]."""
    phat = X / n
    alpha = 1 - conf / 100
    z = norm.ppf(1 - alpha / 2)
    se = math.sqrt(max(phat * (1 - phat) / n, 0.0))
    lo = max(0.0, phat - z * se)
    hi = min(1.0, phat + z * se)
    return phat, lo, hi

def wilson_ci(X: int, n: int, conf: float):
    """Wilson score interval (without continuity correction)."""
    phat = X / n
    alpha = 1 - conf / 100
    z = norm.ppf(1 - alpha / 2)
    denom = 1 + z**2 / n
    center = (phat + z**2 / (2 * n)) / denom
    half = (z * math.sqrt((phat * (1 - phat) / n) + (z**2 / (4 * n**2)))) / denom
    lo, hi = center - half, center + half
    return phat, max(0.0, lo), min(1.0, hi)

def agresti_coull_ci(X: int, n: int, conf: float):
    """Agresti–Coull interval using adjusted counts."""
    alpha = 1 - conf / 100
    z = norm.ppf(1 - alpha / 2)
    n_tilde = n + z**2
    p_tilde = (X + z**2 / 2) / n_tilde
    se = math.sqrt(p_tilde * (1 - p_tilde) / n_tilde)
    lo, hi = p_tilde - z * se, p_tilde + z * se
    return X / n, max(0.0, lo), min(1.0, hi)

def clopper_pearson_ci(X: int, n: int, conf: float):
    """Exact (Clopper–Pearson) interval via Beta quantiles."""
    phat = X / n
    alpha = 1 - conf / 100
    if X == 0:
        lo = 0.0
    else:
        lo = beta.ppf(alpha / 2, X, n - X + 1)
    if X == n:
        hi = 1.0
    else:
        hi = beta.ppf(1 - alpha / 2, X + 1, n - X)
    return phat, lo, hi

METHODS = {
    "Wald (textbook)": wald_ci,
    "Wilson (score)": wilson_ci,
    "Agresti–Coull": agresti_coull_ci,
    "Clopper–Pearson (exact)": clopper_pearson_ci,
}

# cached population maker
@st.cache_data
def make_pop(mean: float, sd: float, size: int, dataset_seed: int):
    rng = np.random.default_rng(dataset_seed)
    return rng.normal(mean, sd, size).astype(float)
