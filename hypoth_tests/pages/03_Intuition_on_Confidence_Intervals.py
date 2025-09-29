import streamlit as st  
import numpy as np 
from utils import *

st.title("Confidence Interval Coverage Explorer")

# --- Controls ---
colA, colB, colC = st.columns([1,1,1])
with colA:
    n = st.slider("Sample size (n)", 10, 400, 30, step=1)
    conf = st.slider("Confidence level (%)", 80, 99, 95, step=1)
with colB:
    reps = st.slider("Number of intervals", 10, 300, 80, step=5)
    speed = st.slider("Animation speed (sec/frame)", 0.02, 0.5, 0.12)
with colC:
    seed = st.number_input("Resampling seed", min_value=0, value=206, step=1)
    sample_mean = st.number_input("Population mean (μ)", value=75.0)

# session_state for dataset seed + animation state
if "dataset_seed" not in st.session_state: st.session_state.dataset_seed = 123456
if "ci_data" not in st.session_state: st.session_state.ci_data = None
if "k" not in st.session_state: st.session_state.k = 0
if "playing" not in st.session_state: st.session_state.playing = False

c1, c2, c3 = st.columns(3)
if c1.button("🎲 Generate / Reset"):
    # bump dataset seed -> new population
    st.session_state.dataset_seed = int(time.time() * 1_000_000) % (2**32 - 1)
    st.session_state.ci_data = None
    st.session_state.k = 0
    st.session_state.playing = False

if c2.button("▶️ Play"):
    if st.session_state.ci_data is None:
        pop = make_pop(sample_mean, 10, 30_000, st.session_state.dataset_seed)
        st.session_state.ci_data = compute_intervals(pop, n, reps, conf, seed=seed)
        st.session_state.k = 0
    st.session_state.playing = True

if c3.button("⏸️ Pause"):
    st.session_state.playing = False

# always compute current population from seed + mean
pop = make_pop(sample_mean, 10, 30_000, st.session_state.dataset_seed)

# if intervals not built yet (e.g., first render), build once
if st.session_state.ci_data is None:
    st.session_state.ci_data = compute_intervals(pop, n, reps, conf, seed=seed)

placeholder = st.empty()
prog = st.progress(0)

# animate or render static
if st.session_state.playing:
    while st.session_state.k < reps and st.session_state.playing:
        st.session_state.k += 1
        fig = draw_frame(st.session_state.ci_data, st.session_state.k, conf, n, reps)
        placeholder.pyplot(fig)
        prog.progress(st.session_state.k / reps)
        plt.close(fig)
        time.sleep(float(speed))
    st.session_state.playing = False
else:
    k = max(1, st.session_state.k)
    fig = draw_frame(st.session_state.ci_data, k, conf, n, reps)
    placeholder.pyplot(fig)
    plt.close(fig)
    prog.progress(k / reps)

# summary
data = st.session_state.ci_data
final_cov = (data["hit"][:max(1, st.session_state.k)].mean() * 100).round(1)
st.info(f"Coverage so far: **{final_cov}%**  |  Target: **{conf}%**")