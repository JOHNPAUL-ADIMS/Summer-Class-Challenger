import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import pandas as pd
import random

# ---------------------
# Streamlit config
# ---------------------
st.set_page_config(page_title="Guess the R²!", layout="centered")
st.title("🚦 Guess the R² – Transportation Data Challenge")

# ---------------------
# Session state setup
# ---------------------
if "x" not in st.session_state:
    st.session_state.x = None
if "y" not in st.session_state:
    st.session_state.y = None
if "r_squared" not in st.session_state:
    st.session_state.r_squared = None
if "round" not in st.session_state:
    st.session_state.round = 1
if "score" not in st.session_state:
    st.session_state.score = 0
if "scoreboard" not in st.session_state:
    st.session_state.scoreboard = pd.DataFrame(columns=["Name", "Total Score"])
if "student_name" not in st.session_state:
    st.session_state.student_name = ""

# ---------------------
# Show intro plots before starting
# ---------------------
def generate_transport_plot(corr_type):
    x = np.linspace(0, 100, 100)
    if corr_type == "positive":
        y = x + np.random.normal(0, 10, size=100)
        title = "More Bicycle Lanes vs. Fewer Accidents"
        xlabel = "Miles of Dedicated Bicycle Lanes"
        ylabel = "Number of Bicycle Accidents"
    elif corr_type == "negative":
        y = -x + np.random.normal(0, 10, size=100) + 100
        title = "Public Transit Usage vs. Traffic Congestion"
        xlabel = "Public Transit Usage (%)"
        ylabel = "Traffic Congestion Level"
    else:
        y = np.random.normal(50, 15, size=100)
        title = "Street Lights vs. Car Color"
        xlabel = "Number of Street Lights"
        ylabel = "Number of Red Cars"

    fig, ax = plt.subplots()
    ax.scatter(x, y, c='skyblue', edgecolors='black')
    ax.set_title(title, fontsize=14)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.tick_params(axis='both', labelsize=10)
    return fig

# Data generation rules
scenarios = [
    {
        "x_label": "Speed Limit (mph)",
        "y_label": "Crash Count",
        "direction": "positive"
    },
    {
        "x_label": "Number of Vehicles",
        "y_label": "Traffic Delay (min)",
        "direction": "positive"
    },
    {
        "x_label": "Public Transit Usage (%)",
        "y_label": "Traffic Congestion Level",
        "direction": "negative"
    },
    {
        "x_label": "Road Width (m)",
        "y_label": "Vehicle Throughput",
        "direction": "positive"
    },
    {
        "x_label": "Gas Prices ($/gallon)",
        "y_label": "Vehicle Miles Traveled",
        "direction": "negative"
    }
]

if st.session_state.student_name == "":
    st.subheader("📚 Quick Guide to R²")
    st.write("Before you begin, take a look at how transportation data can relate:")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.pyplot(generate_transport_plot("positive"))
        st.caption("🚲 More bike lanes = fewer accidents (strong **positive** correlation)")
    with col2:
        st.pyplot(generate_transport_plot("negative"))
        st.caption("🚌 More transit use = less congestion (strong **negative** correlation)")
    with col3:
        st.pyplot(generate_transport_plot("zero"))
        st.caption("💡 Street lights and car color = **no clear relation**")

    st.markdown("---")
    st.subheader("🎮 Enter your name to start")
    name_input = st.text_input("Student Name:")
    if name_input:
        st.session_state.student_name = name_input.strip()
        st.success(f"Welcome, {st.session_state.student_name}!")
        st.rerun()

# ---------------------
# Game begins here
# ---------------------
else:
    st.write(f"👋 Hello **{st.session_state.student_name}** – Round {st.session_state.round} of 5")

    if st.button("🎲 Generate New Plot"):
        scenario = random.choice(scenarios)
        x = np.random.uniform(10, 100, 100)

        if scenario["direction"] == "positive":
            y = x + np.random.normal(0, 10, size=100)
        elif scenario["direction"] == "negative":
            y = -x + np.random.normal(0, 10, size=100) + 100
        else:
            y = np.random.normal(50, 10, size=100)

        st.session_state.x = x
        st.session_state.y = y
        st.session_state.r_squared = round(pearsonr(x, y)[0] ** 2, 2)
        st.session_state.xlabel = scenario["x_label"]
        st.session_state.ylabel = scenario["y_label"]

    if st.session_state.x is not None:
        fig, ax = plt.subplots()
        ax.scatter(st.session_state.x, st.session_state.y, c='orange', edgecolors='black')
        ax.set_title("📊 Estimate the R² (How well does X predict Y?)")
        ax.set_xlabel(st.session_state.get("xlabel", "X"))
        ax.set_ylabel(st.session_state.get("ylabel", "Y"))
        st.pyplot(fig)

        guess_input = st.text_input(
            "🔢 Enter your guess for R² (between 0 and 1):",
            placeholder="e.g. 0.75",
            key=f"guess_{st.session_state.round}"
        )

        if st.button("✅ Submit Guess"):
            if guess_input.strip() == "":
                st.error("❗ Please enter a number.")
            else:
                try:
                    guess = float(guess_input)
                    if 0.0 <= guess <= 1.0:
                        actual = st.session_state.r_squared
                        diff = abs(guess - actual)
                        round_score = max(0, round((1 - diff) * 100))
                        st.session_state.score += round_score

                        st.markdown(f"**✅ Actual R²:** `{actual:.2f}`")
                        st.markdown(f"**🎯 Your Guess:** `{guess:.2f}`")
                        st.markdown(f"**🏅 Score This Round:** `{round_score}/100`")

                        st.session_state.round += 1
                        st.session_state.x = None
                        st.session_state.y = None

                        if st.session_state.round > 5:
                            st.success(f"🎉 Great job, {st.session_state.student_name}! Final Score: {st.session_state.score}/500")
                            new_row = pd.DataFrame([[st.session_state.student_name, st.session_state.score]], columns=["Name", "Total Score"])
                            st.session_state.scoreboard = pd.concat([st.session_state.scoreboard, new_row], ignore_index=True)
                            st.session_state.student_name = ""
                            st.session_state.round = 1
                            st.session_state.score = 0
                            st.rerun()
                    else:
                        st.error("❗ Number must be between 0 and 1.")
                except ValueError:
                    st.error("❗ Please enter a valid numeric value.")

# ---------------------
# Show scoreboard
# ---------------------
if not st.session_state.scoreboard.empty:
    st.subheader("📋 Scoreboard")
    st.dataframe(st.session_state.scoreboard.sort_values(by="Total Score", ascending=False).reset_index(drop=True))

# ---------------------
# Instructor reset button
# ---------------------
with st.expander("🔒 Instructor Panel"):
    admin_password = st.text_input("Enter instructor password to unlock reset", type="password")
    if admin_password == "letmein":
        if st.button("🚨 Reset Entire Scoreboard"):
            st.session_state.scoreboard = pd.DataFrame(columns=["Name", "Total Score"])
            st.success("Scoreboard has been reset.")
