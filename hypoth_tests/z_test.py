import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

st.title("Executing a One-Proportion Z-Test on Categorical Data")

st.write("This app will build intuitition on the big ideas behind hypothesis testing!")

st.divider()

tab1, tab2 = st.tabs(["📖 Explanation", "🎮 Playground"])

# -----------------
# Page 1: Explanation
# -----------------
with tab1:
    st.subheader("1. Write your hypothesis statements.")

    st.write("""
            Hypothesis testing always begins with some underlying assumption that you will be testing using the sampled data. 
            It can arise from any question, ie 'What percentage of Americans currently smoke?' or 'Is this a fair-sided die?' or
            'Does the mess hall waste more than 30% of the food it produces?'
            These are all valid questions that you could then test once you have appropriate data. 
            """)

    st.latex(r"""
        \begin{align*}
            H_0 &: \pi = \text{Any value of interest (a parameter)} \\
            H_A &: \pi >, <, \text{ or } \neq \text{ that same value}
        \end{align*}
    """)

    st.write("""
        We write $\pi$ because the hypothesis statements always refer to the population parameter. In the next section when we gather data
        and find the statistic for that sample. We will then compare the statistic to the parameter to see if we have a statistically significant result.
        """)

    st.subheader("2. Gather your data related to your research question.")

    st.write(""" 
        So let's use the example that I think more than 5\% of Americans smoke. This would be insanely hard to actually find the 
        exact percentage of all +350 million Americans that smoke right? So in practice, I would attempt to RANDOMLY sample the population.
        Say I randomly dialed 200 American phone numbers and all of them answered, with only 12 of them answering 'yes' that they smoke.
        My hypothesis statements for this example would be:
        """)

    st.latex(r"""\begin{align*}
    H_0:& \pi = 0.05 \text{, or "The percentage of Americans that smoke is 5\%"} \\
    H_A:& \pi > 0.05 \text{, or "The percentage of Americans that smoke is greater than 5\%"}
            \end{align*}
    """)

    st.write(""" 
        Now that we've organized ourselves around this research question and sampled some data, we can calculate our statistic. With categorical data
            the research question must always be able to simplify around a 'yes' or 'no' type of question, ie (Do they smoke?, Is the Cadet a Corps Squad athlete?, 
            Was the outcome of the At-Bat a Home-Run?). We deal with proportions of the number of 'yes' responses in our data to test for categorical data.
            We only need the number of correct responses, out of the total number of responses (our sample size), and call that ratio our observed statistic. 
    """)

    st.latex(r"""
        n = 200 \quad \text{ (Sample Size) }\\
        \hat{p} = \frac{12}{200} = 0.06 \quad \text{ (Observed Statistic) }
    """)

    st.write("""
        Now that we've found our observed statistic, we need a way for this statistic to be able to be compared to the Standard Normal Distribution,
            (A bell curve with mean 0 and variance 1). For this to happen we need to create a standardized statistc (denoted Z) as follows:
    """)

    st.latex(r"""
        Z = \frac{\hat{p} - \pi_0}{\sqrt{\frac{\pi_0(1-\pi_0)}{n}}}, \quad \text{ Where } \pi_0 \text{ is the value in our null hypothesis. }
    """)

    st.write(""" Okay, hold the phone, where did this complicated equation come from for standardizing? Great question! We can standardize any dataset
            so that the sample mean is zero and the variance is 1 by z-scoring the data: """)

    st.latex(r"""
        z_i = \frac{x_i - \bar{x}}{s_x} \quad \text{ Where } \bar{x} \text{ is the sample mean and } s_x \text{ is the sample standard deviation. }
    """)

    st.write(
        "For our observed statistic: $\\tfrac{X}{n}$, the only random part of this quantity is the numerator, X. This random variable is in fact a "
        "Binomial Random Variable with sample size n, and probability $\pi_0$. Our observed statistic, $\\tfrac{X}{n}$ is really a linear transformation "
        "by the scalar $\\tfrac{1}{n}$. From our random variable rules, we know the variance of a linear transformation to be $ Var Y = a^2 Var X $,"
        " and the formula for the  variance of a binomial random variable is $np(1-p)$. So the overall standard deviation for our observed statistic is:" 
    )
    st.latex(r"""\begin{align*}
            Var(Y) &= Var \left(\frac{X}{n} \right) \qquad \text{ The linear transformation of the Binomial RV to our observed statistic} \\
                    &= \frac{1}{n^2} Var(X) \qquad \text{ Random Variable Rule for Variance } \\
                    &= \frac{n \pi_0 (1 - \pi_0)}{n^2} \qquad \text{ Formula for Variance of a Binomial RV} \\
                    &= \frac{\pi_0 (1 - \pi_0)}{n} \qquad \text{ Simplify } \\
            STD(Y) = \sqrt{Var(Y)} &= \sqrt{\frac{\pi_0 (1-\pi_0)}{n}} \qquad \text{ Solve for Standard Deviation }
        \end{align*}""")

    st.write(
        "So the solved standardized statistic in our percentage of Americans smoking test is:"
    )
    st.latex(r"Z = \frac{\hat{p} - \pi_0}{\sqrt{\frac{\pi_0(1-\pi_0)}{n}}} = \frac{0.06 - 0.05}{\sqrt{\frac{0.05(1-0.05)}{200}}} = 0.649" ) 

    # Critical value
    z_crit = 0.649
    z_rej = norm.ppf(0.95)

    # X-axis for normal distribution
    x = np.linspace(-3.5, 3.5, 400)
    y = norm.pdf(x, 0, 1)
    p_value = 1 - norm.cdf(z_crit)

    fig, ax = plt.subplots()

    # Plot the normal curve
    ax.plot(x, y, 'b', label="Standard Normal PDF")

    # Shade the rejection region (greater than z_crit)
    x_fill = np.linspace(z_crit, 3.5, 200)
    y_fill = norm.pdf(x_fill, 0, 1)
    ax.fill_between(x_fill, y_fill, alpha=0.4, color='red', label="Rejection Region")

    # Draw vertical line at critical value
    ax.axvline(z_crit, color='green', linestyle='--')
    ax.text(z_crit+0.05, 0.05, f"z = {z_crit}", color='red')
    ax.annotate(
        f"P-value: {np.round(p_value,3)}",
        xy = (1.5*z_crit, .5*norm.pdf(z_crit)),
        xytext = (1.5, 0.25),
        arrowprops = dict(facecolor="black", shrink=0.05, width=1, headwidth=8)
    )

    # Labels
    ax.set_title("Right-Tailed Hypothesis Test")
    ax.set_xlabel("z")
    ax.set_ylabel("Density")
    ax.legend()

    st.pyplot(fig)

    st.write("""
        Here is where we arrive at our evaluating the strength of our argument. Based on our standardized statistic, 
        a p-value of 0.258 is calculated. Remembering our definition of p-value to be:
        ***The probability of rejecting the null hypothesis when it is actually true,*** we should *fail to reject* 
        the null hypothesis in this example. A p-value of 0.258 means: If the null hypothesis were true, there is about a 26% chance of seeing data this extreme (or more extreme) just by random variation.
Put another way, about 1 in 4 times we’d see evidence that looks as “convincing” against the null as what we just observed, even though the null is actually true.
        This is how you should think about assessing p-values, yes traditionally we use the significance level $\\alpha=0.05$,
        meaning we will **reject the null hypothesis** when we have a p-value less than 0.05, however it is entirely dependent on
        the given field of study and what weight the decision brings.    
    """)

    st.divider()

    st.subheader("Left-Tailed Test Example")

    st.write("""
        Let's try a different scenario. Suppose I believe that **fewer than 20% of Cadets skip breakfast**.
        Just like before, it would be extremely hard to ask every single Cadet, so I instead take a random
        sample. Let's say I ask 150 Cadets, and 20 of them report that they skip breakfast.
        
        What are my hypothesis statements for this question?
    """)

    st.latex(r"""\begin{align*}
        H_0 &: \pi = 0.20 \\
        H_A &: \pi < 0.20
    \end{align*}""")

    st.write(""" 
        Now that we’ve written our hypotheses, let’s calculate our sample proportion and standardized statistic.
    """)

    st.latex(r"""
        n = 150 \quad \text{ (Sample Size) }\\
        \hat{p} = \frac{20}{150} \approx 0.133 \quad \text{ (Observed Statistic) }
    """)

    st.latex(r"""
        Z = \frac{\hat{p} - \pi_0}{\sqrt{\frac{\pi_0(1-\pi_0)}{n}}}
          = \frac{0.133 - 0.20}{\sqrt{\frac{0.20(1-0.20)}{150}}}
          \approx -2.31
    """)

    st.write("""
        Notice that this test is **left-tailed**, so the rejection region is in the **left side** of the
        distribution. The p-value is the probability of observing a standardized statistic this low
        (or lower) if the null hypothesis were true.
    """)

    # Critical values and p-value
    z_obs = -2.31
    p_value = norm.cdf(z_obs)   # left-tail probability
    z_crit = norm.ppf(0.05)     # critical cutoff at alpha = 0.05

    # Plot
    x = np.linspace(-3.5, 3.5, 400)
    y = norm.pdf(x)

    fig, ax = plt.subplots()
    ax.plot(x, y, 'b', label="Standard Normal PDF")

    # Shade rejection region
    xx = np.linspace(-3.5, z_crit, 200)
    ax.fill_between(xx, norm.pdf(xx), alpha=0.4, color='red', label="Rejection Region")

    # Draw observed Z and critical line
    ax.axvline(z_obs, color='green', linestyle='--', label=f"Observed Z = {z_obs:.2f}")
    ax.axvline(z_crit, color='pink', linestyle='--', label=f"Critical Z = {z_crit:.2f}")

    # Annotate p-value
    ax.annotate(
        f"P-value = {p_value:.3f}",
        xy=(z_obs, norm.pdf(z_obs)),
        xytext=(-1, 0.05),
        arrowprops=dict(facecolor="black", shrink=0.05, width=1, headwidth=8)
    )

    ax.set_title("Left-Tailed Hypothesis Test")
    ax.set_xlabel("z")
    ax.set_ylabel("Density")
    ax.legend(loc="upper right")

    st.pyplot(fig)

    st.write(f"""
        Based on our standardized statistic ($Z = {z_obs:.2f}$), the p-value is about {p_value:.3f}.
        Since this p-value is **less than our α = 0.05**, we would **reject the null hypothesis**.
        
        This means our data provides evidence that fewer than 20% of Cadets skip breakfast.
    """)

    st.subheader("Two-Sided Test Example")

    st.write("""
        Sometimes we care about whether a proportion is **different from some benchmark in either direction**.
        Suppose I believe that *exactly half of all Cadets would prefer to attend an AIAD over Air-Assault School*.
        Any difference above or below 50% would be interesting.
        
        To test this, I take a random sample of 120 Cadets, and 70 of them say they would prefer AIAD.
    """)

    st.latex(r"""\begin{align*}
        H_0 &: \pi = 0.50 \\
        H_A &: \pi \neq 0.50
    \end{align*}""")

    st.write(""" 
        Now let’s calculate the sample proportion and standardized statistic.
    """)

    st.latex(r"""
        n = 120 \quad \text{ (Sample Size) }\\
        \hat{p} = \frac{70}{120} \approx 0.583 \quad \text{ (Observed Statistic) }
    """)

    st.latex(r"""
        Z = \frac{\hat{p} - \pi_0}{\sqrt{\frac{\pi_0(1-\pi_0)}{n}}}
          = \frac{0.583 - 0.50}{\sqrt{\frac{0.50(1-0.50)}{120}}}
          \approx 1.80
    """)

    st.write("""
        Because this test is **two-sided**, the rejection regions are in **both tails** of the distribution.
        The p-value is the probability of being this far or farther from the null in *either direction*.
    """)

    # Observed Z and p-value
    z_obs = 1.80
    p_value = 2 * (1 - norm.cdf(abs(z_obs)))  # two-tailed
    z_crit = norm.ppf(1 - 0.05/2)             # critical cutoff at alpha = 0.05

    # Plot
    x = np.linspace(-3.5, 3.5, 400)
    y = norm.pdf(x)

    fig, ax = plt.subplots()
    ax.plot(x, y, 'b', label="Standard Normal PDF")

    # Shade rejection regions
    xx = np.linspace(z_crit, 3.5, 200)
    ax.fill_between(xx, norm.pdf(xx), alpha=0.4, color='red', label="Rejection Regions")
    xx = np.linspace(-3.5, -z_crit, 200)
    ax.fill_between(xx, norm.pdf(xx), alpha=0.4, color='red')

    # Draw observed Z and critical lines
    ax.axvline(z_obs, color='green', linestyle='--', label=f"Observed Z = {z_obs:.2f}")
    ax.axvline(-z_obs, color='green', linestyle='--')
    ax.axvline(z_crit, color='pink', linestyle='--', label=f"Critical Z = ±{z_crit:.2f}")
    ax.axvline(-z_crit, color='pink', linestyle='--')

    # Annotate p-value
    ax.annotate(
        f"P-value = {p_value:.3f}",
        xy=(-z_obs, norm.pdf(z_obs)),
        xytext=(-1.0, 0.1),
        arrowprops=dict(facecolor="black", shrink=0.05, width=1, headwidth=8)
    )
    ax.annotate(
        f"P-value = {p_value:.3f}",
        xy=(z_obs, norm.pdf(-z_obs)),
        xytext=(-1.0, 0.1),
        arrowprops=dict(facecolor="black", shrink=0.05, width=1, headwidth=8)
    )

    ax.set_title("Two-Sided Hypothesis Test")
    ax.set_xlabel("z")
    ax.set_ylabel("Density")
    ax.legend(loc="upper left", bbox_to_anchor=(1, 1))

    st.pyplot(fig)

    st.write(f"""
        Based on our standardized statistic ($Z = {z_obs:.2f}$), the two-sided p-value is about {p_value:.3f}.
        Since this p-value is **greater than our α = 0.05**, we would *fail to reject* the null hypothesis.
        
        In other words, our sample does not provide strong evidence that the proportion of Cadets who prefer 
        AIADs to Air Assault school differs from exactly 50%.
    """)

with tab2:
    st.subheader("Practice with the One-Proportion Z-Test")

    st.write("""Below is a developed application where you can choose your own parameter of the null distribution,
    sample size, observed statistic, and type of test.""")

    col1, col2 = st.columns(2)
    with col1:
        n = st.number_input("Sample size (n)", min_value=1, value=200)
        x = st.number_input("Number of successes (X)", min_value=0, value=12)
        p0 = st.number_input("Null hypothesis proportion (π₀)", min_value=0.0, max_value=1.0, value=0.05, step=0.01)

    with col2:
        tail = st.radio("Choose test type:", ["One-Sided (Right-Tailed, >)", "One-Sided (Left-Tailed <)", "Two-Sided (≠)"])
        alpha_percent = st.slider("Confidence Threshold α (%):", 1, 20, value=5, step=1)
        alpha = alpha_percent / 100

    st.divider()

    _, col3, _ = st.columns([1.5,1,1])
    with col3:
        if "Right" in tail:
            st.write(f"""
                    $H_0$ : $\pi =$ {p0} \\
                    $H_A$ : $\pi >$ {p0}
            """)

        elif "Left" in tail:
            st.write(f"""
                    $H_0$ : $\pi =$ {p0} \\
                    $H_A$ : $\pi <$ {p0}
            """)

        else:  # Two-tailed
            st.write(f"""
                    $H_0$ : $\pi =$ {p0} \\
                    $H_A$ : $\pi \\neq$ {p0}
            """)

    # Statistic
    phat = x / n
    z = (phat - p0) / np.sqrt(p0*(1-p0)/n)

    # P-value depending on test
    if "Right" in tail:
        p_value = 1 - norm.cdf(z)
    elif "Left" in tail:
        p_value = norm.cdf(z)
    else:  # Two-tailed
        p_value = 2 * min(norm.cdf(z), 1 - norm.cdf(z))

    st.latex(rf"\hat p = {phat:.3f}, \quad Z = {z:.3f}, \quad p\text{{-value}} = {p_value:.3f}")

    # Plot
    x_axis = np.linspace(-3.5, 3.5, 400)
    y_axis = norm.pdf(x_axis)

    fig, ax = plt.subplots()
    ax.plot(x_axis, y_axis, 'b')

    if "Right" in tail:
        z_crit = norm.ppf(1 - alpha)
        xx = np.linspace(z_crit, 3.5, 200)
        yy = norm.pdf(xx)
        ax.fill_between(xx, yy, alpha=0.4, color='red')
        ax.axvline(z, color="green", linestyle="--", label="Observed Z")
        ax.axvline(z_crit, color='pink', linestyle="--", label=f"Z*={z_crit:.2f}")

    elif "Left" in tail:
        z_crit = norm.ppf(alpha)
        xx = np.linspace(-3.5, z_crit, 200)
        yy = norm.pdf(xx)
        ax.fill_between(xx, yy, alpha=0.4, color='red')
        ax.axvline(z, color="green", linestyle="--", label="Observed Z")
        ax.axvline(z_crit, color='pink', linestyle="--", label=f"Z*={z_crit:.2f}")

    else:  # Two-tailed
        z_crit = norm.ppf(1 - alpha/2)
        # Shade right tail
        xx = np.linspace(z_crit, 3.5, 200)
        ax.fill_between(xx, norm.pdf(xx), alpha=0.4, color='red')
        # Shade left tail
        xx = np.linspace(-3.5, -z_crit, 200)
        ax.fill_between(xx, norm.pdf(xx), alpha=0.4, color='red')
        ax.axvline(z, color="green", linestyle="--", label="Observed Z")
        ax.axvline(z_crit, color='pink', linestyle="--", label=f"Z*={z_crit:.2f}")
        ax.axvline(-z_crit, color='pink', linestyle="--")

    ax.legend()
    ax.set_title(f"{tail} Test")
    ax.set_xlabel("z")
    ax.set_ylabel("Density")
    st.pyplot(fig)

    # Interpretation
    if p_value < alpha:
        st.success(f"Reject H₀ at α = {alpha}")
    else:
        st.warning(f"Fail to reject H₀ at α = {alpha}")
