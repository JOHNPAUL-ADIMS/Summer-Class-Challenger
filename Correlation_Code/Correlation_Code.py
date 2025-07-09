import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import pandas as pd
import random

# Streamlit page config
st.set_page_config(page_title="Guess the Correlation", layout="centered")
st.title("🚦 Guess the Correlation – Transportation Data Challenge")

# Session state setup
for var in [
    "x", "y", "corr", "round", "score", "student_name", "scoreboard", "phase", "scenario",
    "direction_submitted", "direction_correct", "direction_guess", "direction_score",
    "value_submitted", "value_guess", "value_actual", "value_diff", "value_score",
    "used_scenarios", "xlabel", "ylabel", "difficulty_level"
]:
    if var not in st.session_state:
        if var == "scoreboard":
            st.session_state[var] = pd.DataFrame(columns=["Name", "Total Score"])
        elif var == "round":
            st.session_state[var] = 1
        elif var == "score":
            st.session_state[var] = 0
        elif var == "phase":
            st.session_state[var] = 1
        elif var == "used_scenarios":
            st.session_state[var] = []
        else:
            st.session_state[var] = None

# Define scenarios by difficulty level
scenarios_by_difficulty = {
    1: [  # Very Easy - Strong, obvious correlations
        {"x_label": "Number of Vehicles", "y_label": "Traffic Delay (min)", "direction": "positive", "base_corr": 0.85},
        {"x_label": "Public Transit Usage", "y_label": "Traffic Congestion Level", "direction": "negative",
         "base_corr": -0.80},
        {"x_label": "Gas Prices ($)", "y_label": "Vehicle Miles Traveled", "direction": "negative", "base_corr": -0.75},
    ],
    2: [  # Easy - Moderate correlations
        {"x_label": "Daily Bike Rentals", "y_label": "Air Pollution Index", "direction": "negative",
         "base_corr": -0.65},
        {"x_label": "Speed Limit (mph)", "y_label": "Crash Count", "direction": "positive", "base_corr": 0.60},
        {"x_label": "Road Width (ft)", "y_label": "Vehicle Throughput", "direction": "positive", "base_corr": 0.55},
    ],
    3: [  # Medium - Weaker correlations
        {"x_label": "Hours of Rain", "y_label": "Average Traffic Speed", "direction": "negative", "base_corr": -0.45},
        {"x_label": "Distance to Downtown (mi)", "y_label": "Bus Ridership", "direction": "negative",
         "base_corr": -0.40},
        {"x_label": "Bike Lane Coverage (%)", "y_label": "Bicycle Crash Rate", "direction": "negative",
         "base_corr": -0.35},
    ],
    4: [  # Hard - Very weak correlations
        {"x_label": "Number of Stop Signs", "y_label": "Average Speed", "direction": "negative", "base_corr": -0.25},
        {"x_label": "Parking Availability", "y_label": "Traffic Circulation Time", "direction": "negative",
         "base_corr": -0.20},
        {"x_label": "Number of Intersections", "y_label": "Signal Delay (sec)", "direction": "positive",
         "base_corr": 0.15},
    ],
    5: [  # Very Hard - Near-zero or tricky correlations
        {"x_label": "Number of Street Lights", "y_label": "Number of Red Cars", "direction": "zero", "base_corr": 0.05},
        {"x_label": "Bridge Height (ft)", "y_label": "Average Vehicle Color Brightness", "direction": "zero",
         "base_corr": -0.03},
        {"x_label": "Speed Cameras Installed", "y_label": "Crash Count", "direction": "zero", "base_corr": 0.08},
    ]
}

# Difficulty settings for each round
difficulty_settings = {
    1: {"noise_factor": 0.1, "sample_size": 60, "label": "🟢 EASY"},
    2: {"noise_factor": 0.3, "sample_size": 55, "label": "🟡 MEDIUM-EASY"},
    3: {"noise_factor": 0.5, "sample_size": 50, "label": "🟠 MEDIUM"},
    4: {"noise_factor": 0.7, "sample_size": 45, "label": "🔴 HARD"},
    5: {"noise_factor": 0.9, "sample_size": 40, "label": "🟣 VERY HARD"}
}


def generate_correlated_data(scenario, difficulty):
    """Generate data with controlled correlation and difficulty"""
    settings = difficulty_settings[difficulty]
    n = settings["sample_size"]
    noise_factor = settings["noise_factor"]
    target_corr = scenario["base_corr"]

    # Generate base data
    x = np.random.uniform(10, 100, n)

    if scenario["direction"] == "positive":
        # Start with perfect correlation, then add noise
        y = x * abs(target_corr) + np.random.normal(0, noise_factor * 50, n)
    elif scenario["direction"] == "negative":
        # Negative correlation
        y = -x * abs(target_corr) + 100 + np.random.normal(0, noise_factor * 50, n)
    else:  # zero correlation
        # Random data with minimal correlation
        y = np.random.normal(50, 15, n) + target_corr * x + np.random.normal(0, noise_factor * 30, n)

    # Add extra noise for higher difficulties
    if difficulty >= 4:
        x += np.random.normal(0, noise_factor * 10, n)
        y += np.random.normal(0, noise_factor * 15, n)

    return x, y


# Show intro if no name yet
if not st.session_state.student_name:
    st.subheader("📚 Quick Guide to Correlation")
    st.markdown("""
Correlation measures how two variables relate to each other.

- **+1**: Strong positive correlation (⬆️⬆️)
- **0**: No correlation (🔄)
- **-1**: Strong negative correlation (⬆️⬇️)

**🎯 Progressive Challenge:** The game gets harder with each round!
- Round 1-2: Clear, strong patterns
- Round 3: Moderate relationships  
- Round 4-5: Weak or tricky correlations with more noise

You'll see transport-related variable pairs. First, guess the **direction** (positive, negative, zero), then estimate the **correlation value**.
    """)
    col1, col2, col3 = st.columns(3)


    def plot_example(corr, col):
        x = np.linspace(0, 10, 100)
        if corr == 1:
            y = x + np.random.normal(0, 0.5, 100)
        elif corr == -1:
            y = -x + np.random.normal(0, 0.5, 100)
        else:
            y = np.random.normal(0, 2, 100)
        fig, ax = plt.subplots(figsize=(3, 2))
        ax.scatter(x, y, alpha=0.6)
        ax.set_xticks([])
        ax.set_yticks([])
        col.pyplot(fig)


    with col1:
        plot_example(1, col1)
        st.caption("⬆️ **Positive**")
    with col2:
        plot_example(-1, col2)
        st.caption("⬇️ **Negative**")
    with col3:
        plot_example(0, col3)
        st.caption("🔄 **No Correlation**")

    st.markdown("---")
    st.subheader("🎮 Enter your name to start")
    name_input = st.text_input("Student Name:")
    if name_input:
        st.session_state.student_name = name_input.strip()
        st.session_state.used_scenarios = []
        st.rerun()

# Game Begins
else:
    current_difficulty = st.session_state.round
    difficulty_label = difficulty_settings[current_difficulty]["label"]

    st.write(f"👋 Hello **{st.session_state.student_name}** – Round {st.session_state.round} of 5 {difficulty_label}")

    # Progress bar
    progress = (st.session_state.round - 1) / 5
    st.progress(progress)

    if st.session_state.phase == 1:  # Direction Guess Phase
        if st.session_state.x is None:
            # Select scenario for current difficulty level
            available_scenarios = [s for s in scenarios_by_difficulty[current_difficulty]
                                   if s not in st.session_state.used_scenarios]

            if not available_scenarios:
                available_scenarios = scenarios_by_difficulty[current_difficulty].copy()

            scenario = random.choice(available_scenarios)
            st.session_state.used_scenarios.append(scenario)

            # Generate data with progressive difficulty
            x, y = generate_correlated_data(scenario, current_difficulty)

            st.session_state.x = x
            st.session_state.y = y
            st.session_state.corr = round(pearsonr(x, y)[0], 2)
            st.session_state.xlabel = scenario["x_label"]
            st.session_state.ylabel = scenario["y_label"]
            st.session_state.scenario = scenario

        # Plot without points (just axes)
        fig, ax = plt.subplots(figsize=(8, 6))
        if st.session_state.xlabel:
            ax.set_xlabel(st.session_state.xlabel, fontsize=12)
        if st.session_state.ylabel:
            ax.set_ylabel(st.session_state.ylabel, fontsize=12)
        ax.set_title(f"🤔 What kind of relationship do you expect? {difficulty_label}", fontsize=14)
        st.pyplot(fig)

        direction_guess = st.radio(
            "Guess the correlation **direction**:",
            options=["Positive", "Negative", "No Correlation"],
            horizontal=True,
            key="direction_radio"
        )

        if st.button("✅ Submit Direction Guess") and not st.session_state.direction_submitted:
            correct = st.session_state.scenario["direction"]
            score_this = 20 if (
                    (correct == "positive" and direction_guess == "Positive") or
                    (correct == "negative" and direction_guess == "Negative") or
                    (correct == "zero" and direction_guess == "No Correlation")
            ) else 0

            st.session_state.score += score_this
            st.session_state.direction_correct = correct
            st.session_state.direction_guess = direction_guess
            st.session_state.direction_score = score_this
            st.session_state.direction_submitted = True

        if st.session_state.direction_submitted:
            st.markdown(f"**✅ Correct Direction:** `{st.session_state.direction_correct.capitalize()}`")
            st.markdown(f"**🎯 Your Guess:** `{st.session_state.direction_guess}`")
            st.markdown(f"**🏅 Score This Round (Direction):** `{st.session_state.direction_score}/20`")

            if st.button("➡️ Next: Guess Correlation Value"):
                st.session_state.phase = 2
                st.session_state.direction_submitted = False
                st.rerun()

    elif st.session_state.phase == 2:  # Correlation Value Guess Phase
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(st.session_state.x, st.session_state.y, color="orange", edgecolors="black", alpha=0.7)
        if st.session_state.xlabel:
            ax.set_xlabel(st.session_state.xlabel, fontsize=12)
        if st.session_state.ylabel:
            ax.set_ylabel(st.session_state.ylabel, fontsize=12)
        ax.set_title(f"📊 Now guess the actual correlation value! {difficulty_label}", fontsize=14)
        st.pyplot(fig)

        # Show correlation strength guide
        st.markdown("""
        **Correlation Strength Guide:**
        - 0.0 to ±0.2: Very weak
        - ±0.2 to ±0.4: Weak  
        - ±0.4 to ±0.6: Moderate
        - ±0.6 to ±0.8: Strong
        - ±0.8 to ±1.0: Very strong
        """)

        guess_input = st.text_input(
            "🔢 Your guess for correlation (between -1 and 1):",
            placeholder="e.g. 0.72",
            key=f"guess_{st.session_state.round}"
        )

        if st.button("✅ Submit Correlation Guess") and not st.session_state.value_submitted:
            if guess_input.strip() == "":
                st.error("❗ Please enter a number.")
            else:
                try:
                    guess = float(guess_input)
                    if -1.0 <= guess <= 1.0:
                        actual = st.session_state.corr
                        diff = abs(guess - actual)

                        # Adjust scoring based on difficulty (harder rounds are more forgiving)
                        max_score = 80
                        if current_difficulty >= 4:  # Hard rounds
                            round_score = max(0, round((1 - diff * 0.8) * max_score))
                        elif current_difficulty >= 3:  # Medium rounds
                            round_score = max(0, round((1 - diff * 0.9) * max_score))
                        else:  # Easy rounds
                            round_score = max(0, round((1 - diff) * max_score))

                        st.session_state.value_guess = guess
                        st.session_state.value_actual = actual
                        st.session_state.value_diff = diff
                        st.session_state.value_score = round_score
                        st.session_state.score += round_score
                        st.session_state.value_submitted = True
                    else:
                        st.error("❗ Number must be between -1 and 1.")
                except ValueError:
                    st.error("❗ Please enter a valid numeric value.")

        if st.session_state.value_submitted:
            st.markdown(f"**✅ Actual Correlation:** `{st.session_state.value_actual:.2f}`")
            st.markdown(f"**🎯 Your Guess:** `{st.session_state.value_guess:.2f}`")
            st.markdown(f"**📏 Difference:** `{st.session_state.value_diff:.2f}`")
            st.markdown(f"**🏅 Score This Round (Value):** `{st.session_state.value_score}/80`")

            if st.button("➡️ Next Round"):
                st.session_state.round += 1
                st.session_state.x = None
                st.session_state.y = None
                st.session_state.phase = 1
                st.session_state.value_submitted = False

                if st.session_state.round > 5:
                    st.success(f"🎉 Done! Final Score: {st.session_state.score}/500")
                    new_row = pd.DataFrame([[st.session_state.student_name, st.session_state.score]],
                                           columns=["Name", "Total Score"])
                    st.session_state.scoreboard = pd.concat([st.session_state.scoreboard, new_row], ignore_index=True)
                    st.session_state.student_name = ""
                    st.session_state.round = 1
                    st.session_state.score = 0
                    st.session_state.phase = 1
                    st.session_state.used_scenarios = []
                st.rerun()

# Scoreboard
if not st.session_state.scoreboard.empty:
    st.subheader("📋 Scoreboard")
    st.dataframe(st.session_state.scoreboard.sort_values(by="Total Score", ascending=False).reset_index(drop=True))

# Instructor Reset
with st.expander("🔒 Instructor Panel"):
    if st.text_input("Password", type="password") == "letmein":
        if st.button("🚨 Reset Entire Scoreboard"):
            st.session_state.scoreboard = pd.DataFrame(columns=["Name", "Total Score"])
            st.success("Scoreboard reset.")