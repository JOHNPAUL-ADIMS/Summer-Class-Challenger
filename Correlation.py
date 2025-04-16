import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import pandas as pd

# ---------------------
# Streamlit config
# ---------------------
st.set_page_config(page_title="Guess the Correlation!", layout="centered")
st.title("🎓 Correlation Guessing Game")

# ---------------------
# Session state setup
# ---------------------
if "x" not in st.session_state:
    st.session_state.x = None
if "y" not in st.session_state:
    st.session_state.y = None
if "corr" not in st.session_state:
    st.session_state.corr = None
if "round" not in st.session_state:
    st.session_state.round = 1
if "score" not in st.session_state:
    st.session_state.score = 0
if "scoreboard" not in st.session_state:
    st.session_state.scoreboard = pd.DataFrame(columns=["Name", "Total Score"])
if "student_name" not in st.session_state:
    st.session_state.student_name = ""

# ---------------------
# Show correlation examples before the game starts
# ---------------------
if st.session_state.student_name == "":
    st.subheader("📚 Quick Visual Guide to Correlation")

    col1, col2, col3 = st.columns(3)

    def plot_example(corr, title, col):
        x = np.linspace(0, 1, 100)
        if corr == 1:
            y = x
        elif corr == -1:
            y = -x
        else:
            y = np.random.rand(100)
        fig, ax = plt.subplots()
        ax.scatter(x, y, c='skyblue', edgecolors='black')
        ax.set_title(title, fontsize=14)
        ax.set_xlabel("X", fontsize=12)
        ax.set_ylabel("Y", fontsize=12)
        ax.tick_params(axis='both', labelsize=10)
        col.pyplot(fig)

    with col1:
        plot_example(1, "+1: Strong Positive", col1)
        st.caption("⬆️ As X increases, Y increases")

    with col2:
        plot_example(-1, "-1: Strong Negative", col2)
        st.caption("⬆️ As X increases, Y decreases")

    with col3:
        plot_example(0, "0: No Correlation", col3)
        st.caption("🔄 No clear pattern between X and Y")
# ---------------------
# Name input (once)
# ---------------------
if st.session_state.student_name == "":
    name_input = st.text_input("Enter your name to begin 👇")
    if name_input:
        st.session_state.student_name = name_input.strip()
        st.success(f"Welcome, {st.session_state.student_name}!")
        st.rerun()

else:
    st.write(f"👋 Hello **{st.session_state.student_name}** – Round {st.session_state.round} of 5")

    # ---------------------
    # Generate new plot
    # ---------------------
    if st.button("🎲 Generate New Plot"):
        x = np.random.rand(100)
        true_corr = np.random.uniform(-1, 1)
        noise = np.random.normal(0, 1 - abs(true_corr), size=100)
        y = true_corr * x + noise

        st.session_state.x = x
        st.session_state.y = y
        st.session_state.corr = pearsonr(x, y)[0]

    # ---------------------
    # Show plot and guess input
    # ---------------------
    if st.session_state.x is not None:
        fig, ax = plt.subplots()
        ax.scatter(st.session_state.x, st.session_state.y, c='orange', edgecolors='black')
        ax.set_title("📊 Estimate the correlation")
        st.pyplot(fig)

        guess = st.number_input("What is your guess for the correlation (-1 to 1)?", min_value=-1.0, max_value=1.0, step=0.01)

        if st.button("✅ Submit Guess"):
            actual = st.session_state.corr
            diff = abs(guess - actual)
            round_score = max(0, round((1 - diff) * 100))
            st.session_state.score += round_score

            st.markdown(f"**✅ Actual Correlation:** `{actual:.2f}`")
            st.markdown(f"**🎯 Your Guess:** `{guess:.2f}`")
            st.markdown(f"**🏅 Score This Round:** `{round_score}/100`")

            st.session_state.round += 1
            st.session_state.x = None  # Reset plot for next round
            st.session_state.y = None

            # Check if final round
            if st.session_state.round > 5:
                st.success(f"🎉 Great job, {st.session_state.student_name}! Final Score: {st.session_state.score}/500")
                # Update scoreboard
                new_row = pd.DataFrame([[st.session_state.student_name, st.session_state.score]], columns=["Name", "Total Score"])
                st.session_state.scoreboard = pd.concat([st.session_state.scoreboard, new_row], ignore_index=True)
                
                # Reset session vars for next student
                st.session_state.student_name = ""
                st.session_state.round = 1
                st.session_state.score = 0
                st.rerun()

# ---------------------
# Show scoreboard
# ---------------------
if not st.session_state.scoreboard.empty:
    st.subheader("📋 Scoreboard")
    st.dataframe(st.session_state.scoreboard.sort_values(by="Total Score", ascending=False).reset_index(drop=True))

# ---------------------
# Instructor reset button (hidden behind password)
# ---------------------
with st.expander("🔒 Instructor Panel"):
    admin_password = st.text_input("Enter instructor password to unlock reset", type="password")
    if admin_password == "letmein":  # Change to your secret
        if st.button("🚨 Reset Entire Scoreboard"):
            st.session_state.scoreboard = pd.DataFrame(columns=["Name", "Total Score"])
            st.success("Scoreboard has been reset.")
