# Home.py
import time
import secrets
import streamlit as st

st.set_page_config(
    page_title="MA206 • Statistical Inference",
    page_icon="📈",
    layout="centered"
)

st.title("MA206: Probability & Statistics")
st.subheader("Hypothesis Testing and Confidence Intervals")

st.markdown(
    """
This app provides interactive walkthroughs of the most common hypothesis tests and
confidence intervals in introductory statistics.  
Instead of just formulas, each page is designed to **build intuition** with
step-by-step explanations, visualizations, and practice blocks.
"""
)

# -------------------------
# Core Vocabulary
# -------------------------
st.divider()
st.subheader("Core Vocabulary")

with st.expander("Population"):
    st.markdown(
        """
The **entire group** we want to study or draw conclusions about.  
- Example: *All Cadets at West Point*.
"""
    )

with st.expander("Sample"):
    st.markdown(
        """
A **subset of the population** that we actually collect data from.  
- Example: *A random 200 Cadets surveyed*.  
- We use the sample to estimate what is true about the whole population.
"""
    )

with st.expander("Random Sampling"):
    st.markdown(
        """
Every member of the population has an equal chance of being selected.  
- Strength: Supports **generalization** of results to the population.  
- Example: Drawing cadet names randomly from the roster.
"""
    )

with st.expander("Convenience Sample"):
    st.markdown(
        """
A sample chosen because it is **easy to collect**, not random.  
- Example: Surveying only Cadets in your company.  
- Risk: May not represent the population, weakens **generalization**.
"""
    )

with st.expander("Generalization"):
    st.markdown(
        """
The ability to extend results from a **sample** to the **population**.  
- Strongest when sampling is **random**.
"""
    )

with st.expander("Significance Level (α)"):
    st.markdown(
        """
The **threshold for evidence** against the null hypothesis.  
- Commonly $\\alpha = 0.05$ (5%).  
- If the p-value is less than α, we reject $H_0$.
"""
    )

with st.expander("p-value"):
    st.markdown(
        """
The probability of observing a result as extreme (or more extreme) as your data, **if $H_0$ were true**.  
- Small p-values mean the data would be unlikely under $H_0$, giving evidence against it.
"""
    )

with st.expander("Observed Statistic"):
    st.markdown(
        """
The quantity we calculate from the **sample** (e.g., $\\hat{p}, \\bar{x}, \\bar{d}$).  
It is the “realized” version of a population parameter based on our data.
"""
    )

with st.expander("Standardized Statistic"):
    st.markdown(
        """
The observed statistic, converted into a **standard scale** (z or t).  
- Formula: $\\text{(statistic − hypothesized value)} / SE$.  
- Allows comparison to a reference distribution (Normal or t).
"""
    )

with st.expander("Random Assignment"):
    st.markdown(
        """
Assigning individuals to treatment or control groups **at random**.  
- Strength: Supports **causal conclusions**.  
- Example: Randomly assigning Cadets to a new PT program vs. the standard PT program.
"""
    )

with st.expander("Causation"):
    st.markdown(
        """
A claim that one variable **directly influences** another.  
- Requires both **random sampling** (to generalize) and **random assignment** (to justify cause-and-effect).
"""
    )

st.divider()
st.subheader("Glossary of Inference Tools")

with st.expander("One-Proportion Z-Test"):
    st.markdown(
        """
Tests whether a **population proportion** ($\\pi$) is equal to some hypothesized value $\\pi_0$.  
- **Typical use:** “Is more than 5% of Americans smokers?”  
- **Statistic:** $\\hat{p} = X/n$  
- **Test statistic:**  
  $$
  Z = \\frac{\\hat{p} - \\pi_0}{\\sqrt{\\pi_0(1-\\pi_0)/n}}
  $$  
- Requires $n\\pi_0$ and $n(1-\\pi_0)$ to be reasonably large (10+).
"""
    )

with st.expander("One-Sample t-Test"):
    st.markdown(
        """
Tests whether a **population mean** ($\\mu$) equals a hypothesized value $\\mu_0$.  
- **Typical use:** “Do Cadets sleep fewer than 7 hours on average?”  
- **Statistic:** $\\bar{x}$ (sample mean)  
- **Test statistic:**  
  $$
  t = \\frac{\\bar{x} - \\mu_0}{s/\\sqrt{n}}, \\quad df = n-1
  $$  
- Uses the **t-distribution** because $\\sigma$ is unknown.
"""
    )

with st.expander("Two-Proportion Z-Test"):
    st.markdown(
        """
Compares whether **two population proportions** ($\\pi_1, \\pi_2$) are equal.  
- **Typical use:** “Are male Cadets more likely than female Cadets to skip breakfast?”  
- **Statistic:** $\\hat{p}_1 - \\hat{p}_2$  
- **Pooled proportion:**  
  $$
  \\hat{p} = \\frac{X_1+X_2}{n_1+n_2}
  $$  
- **Test statistic:**  
  $$
  Z = \\frac{\\hat{p}_1 - \\hat{p}_2}{\\sqrt{\\hat{p}(1-\\hat{p})(1/n_1 + 1/n_2)}}
  $$
"""
    )

with st.expander("Two-Sample t-Test"):
    st.markdown(
        """
Compares whether **two population means** are equal.  
- **Typical use:** “Do male and female Cadets get the same average sleep?”  
- **Statistic:** $\\bar{x}_1 - \\bar{x}_2$  
- **Standard error:**  
  $$
  SE = \\sqrt{\\tfrac{s_1^2}{n_1} + \\tfrac{s_2^2}{n_2}}
  $$  
- **Test statistic:**  
  $$
  t = \\frac{\\bar{x}_1 - \\bar{x}_2}{SE}, \\quad df \\text{ (Welch’s approx.)}
  $$
"""
    )

with st.expander("Paired t-Test"):
    st.markdown(
        """
Tests whether the **mean of paired differences** is zero.  
- **Typical use:** “Do Cadets sleep more after a new training program?”  
- Reduce to a **one-sample t-test** on the differences $d_i = x_{1i} - x_{2i}$.  
- **Test statistic:**  
  $$
  t = \\frac{\\bar{d} - \\mu_{d,0}}{s_d/\\sqrt{n}}, \\quad df = n-1
  $$
"""
    )

st.divider()
st.subheader("Glossary of Confidence Intervals")

with st.expander("One-Proportion CI"):
    st.markdown(
        """
Estimates a **population proportion** $\\pi$.  
- Formula (Wald):  
  $$
  \\hat{p} \\pm z^* \\sqrt{\\hat{p}(1-\\hat{p})/n}
  $$  
- Better methods (Wilson, Clopper–Pearson) adjust for small samples.
"""
    )

with st.expander("One-Sample Mean CI"):
    st.markdown(
        """
Estimates a **population mean** $\\mu$.  
- Formula:  
  $$
  \\bar{x} \\pm t^* \\frac{s}{\\sqrt{n}}, \\quad df = n-1
  $$
"""
    )

with st.expander("Difference in Proportions CI"):
    st.markdown(
        """
Estimates $\\pi_1 - \\pi_2$.  
- Formula:  
  $$
  (\\hat{p}_1 - \\hat{p}_2) \\pm z^* \\sqrt{\\tfrac{\\hat{p}_1(1-\\hat{p}_1)}{n_1} + \\tfrac{\\hat{p}_2(1-\\hat{p}_2)}{n_2}}
  $$
"""
    )

with st.expander("Difference in Means CI"):
    st.markdown(
        """
Estimates $\\mu_1 - \\mu_2$.  
- Formula:  
  $$
  (\\bar{x}_1 - \\bar{x}_2) \\pm t^* \\sqrt{\\tfrac{s_1^2}{n_1} + \\tfrac{s_2^2}{n_2}}
  $$  
- Use Welch’s degrees of freedom.
"""
    )

with st.expander("Paired Data CI"):
    st.markdown(
        """
Estimates the **mean difference** $\\mu_d$.  
- Formula:  
  $$
  \\bar{d} \\pm t^* \\frac{s_d}{\\sqrt{n}}, \\quad df = n-1
  $$
"""
    )

# -------------------------
# Global controls / session init
# -------------------------
st.divider()
st.subheader("Global Controls")

col1, col2 = st.columns(2)

with col1:
    default_mean = st.number_input("Default population mean (μ) for demos", value=75.0, key="global_mean_input")
    if "global_mean" not in st.session_state:
        st.session_state.global_mean = default_mean
    if st.button("Apply default μ to all pages", key="apply_global_mean"):
        st.session_state.global_mean = default_mean
        st.success(f"Set global mean to μ = {default_mean:.2f}")

with col2:
    if st.button("🔄 Reset app state (new datasets on pages)", key="reset_state"):
        for k in list(st.session_state.keys()):
            if k != "global_mean":
                del st.session_state[k]
        st.session_state.dataset_seed = secrets.randbits(32)
        st.toast("State cleared. Pages will regenerate data.", icon="✅")
        time.sleep(0.2)

st.divider()
with st.expander("About this app"):
    st.markdown(
        """
- Built for **MA206** to help cadets practice inference with interactive visuals.  
- Each page is self-contained; shared utilities live in `utils.py`.  
- Use the **Reset** button above if a page’s datasets/animations should restart fresh.  
        """
    )