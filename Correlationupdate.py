import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import pandas as pd

# ---------------------
# Streamlit config
# ---------------------
st.set_page_config(page_title="🎯 Guess the Correlation!", layout="centered")
st.title(" Correlation Guessing Game \n FAMU-FSU College of Engineering 🎓")
st.markdown("#### 🚀 **Welcome to the most fun way to learn correlations!** 🌟")

# ---------------------
# Define correlation structure for 6 rounds
# ---------------------
CORRELATION_STRUCTURE = [
    {"type": "Strong Positive", "target": 0.95, "emoji": "🚀📈", "color": "#FF6B6B",
     "desc": "Super Strong Upward Trend!"},
    {"type": "Strong Negative", "target": -0.95, "emoji": "⚡📉", "color": "#4ECDC4",
     "desc": "Super Strong Downward Trend!"},
    {"type": "No Correlation", "target": 0.0, "emoji": "🌪️🔄", "color": "#45B7D1", "desc": "Random Chaos Mode!"},
    {"type": "Strong Positive", "target": 0.90, "emoji": "🔥📈", "color": "#96CEB4", "desc": "Blazing Upward Pattern!"},
    {"type": "Strong Negative", "target": -0.90, "emoji": "❄️📉", "color": "#FFEAA7", "desc": "Icy Downward Slide!"},
    {"type": "No Correlation", "target": 0.0, "emoji": "🎲🔄", "color": "#DDA0DD", "desc": "Pure Randomness!"}
]

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
if "round_results" not in st.session_state:
    st.session_state.round_results = []
if "game_completed" not in st.session_state:
    st.session_state.game_completed = False

# ---------------------
# Show correlation examples before the game starts
# ---------------------
if st.session_state.student_name == "":
    st.markdown("---")
    st.markdown("### 📚 **Quick Visual Guide to Correlation** ")
    st.markdown("#### 🎨 Learn the patterns before you play!")

    col1, col2, col3 = st.columns(3)


    def plot_example(corr, title, col, color):
        np.random.seed(42)  # Consistent examples
        x = np.linspace(0, 1, 1000)
        if corr == 1:
            y = x + np.random.normal(0, 0.05, 1000)
        elif corr == -1:
            y = -x + 1 + np.random.normal(0, 0.05, 1000)
        else:
            y = np.random.rand(1000)

        fig, ax = plt.subplots(figsize=(5, 4))
        ax.scatter(x, y, c=color, edgecolors='white', s=50, alpha=0.8)
        ax.set_title(title, fontsize=14, fontweight='bold', color='#2E4057')
        ax.set_xlabel("X Variable", fontsize=11, color='#2E4057')
        ax.set_ylabel("Y Variable", fontsize=11, color='#2E4057')
        ax.tick_params(axis='both', labelsize=9)
        ax.grid(True, alpha=0.3, color='gray')
        ax.set_facecolor('#F8F9FA')
        fig.patch.set_facecolor('white')
        col.pyplot(fig)


    with col1:
        plot_example(1, "🚀 +0.9 to +1.0: Strong Positive", col1, '#FF6B6B')
        st.markdown("**⬆️ As X increases, Y increases strongly!**")

    with col2:
        plot_example(-1, "⚡ -0.9 to -1.0: Strong Negative", col2, '#4ECDC4')
        st.markdown("**⬇️ As X increases, Y decreases strongly!**")

    with col3:
        plot_example(0, " 0: No Correlation", col3, '#45B7D1')
        st.markdown("**🔄 No clear pattern - pure randomness!**")

    st.markdown("---")
    st.markdown("### **Ready to test your skills?** Let's play! 🎮")

# ---------------------
# Name input (once)
# ---------------------
if st.session_state.student_name == "":
    st.markdown("##### **Enter your name to start your correlation adventure!**")
    name_input = st.text_input("✏️ Your Name Here 👇", placeholder="Type your awesome name...")
    if name_input:
        st.session_state.student_name = name_input.strip()
        # Reset game state for new student
        st.session_state.round = 1
        st.session_state.score = 0
        st.session_state.round_results = []
        st.session_state.game_completed = False
        st.session_state.show_result = False
        st.success(f"🎉🎊 Welcome to the game, **{st.session_state.student_name}**! 🎊🎉")
        st.balloons()
        st.rerun()

else:
    # 🛑 Check if all rounds are completed
    if st.session_state.round > len(CORRELATION_STRUCTURE) and not st.session_state.game_completed:
        st.session_state.game_completed = True
        # Update scoreboard
        new_row = pd.DataFrame([[st.session_state.student_name, st.session_state.score]],
                               columns=["Name", "Total Score"])
        st.session_state.scoreboard = pd.concat([st.session_state.scoreboard, new_row], ignore_index=True)
        st.rerun()

    # Show final results screen
    elif st.session_state.game_completed:
        st.markdown("---")
        st.markdown("# **GAME COMPLETED!** 🏆🎉")
        st.balloons()

        # Student's final score with visual styling
        score_percentage = (st.session_state.score / 600) * 100

        if score_percentage >= 90:
            grade_emoji = "🌟🏆"
            grade_color = "#FFD700"
            grade_text = "OUTSTANDING!"
        elif score_percentage >= 80:
            grade_emoji = "🔥💪"
            grade_color = "#28a745"
            grade_text = "EXCELLENT!"
        elif score_percentage >= 70:
            grade_emoji = "👍✨"
            grade_color = "#17a2b8"
            grade_text = "GREAT JOB!"
        elif score_percentage >= 60:
            grade_emoji = "🎯📈"
            grade_color = "#ffc107"
            grade_text = "GOOD WORK!"
        else:
            grade_emoji = "💡🎮"
            grade_color = "#6c757d"
            grade_text = "KEEP PRACTICING!"

        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {grade_color}22, {grade_color}44);
                    padding: 30px;
                    border-radius: 20px;
                    border-left: 8px solid {grade_color};
                    margin: 20px 0;
                    text-align: center;">
            <h1 style="color: {grade_color}; margin: 0;">{st.session_state.student_name}</h1>
            <h2 style="color: {grade_color}; margin: 10px 0;">{grade_text}</h2>
            <h1 style="color: {grade_color}; margin: 15px 0; font-size: 3em;">{st.session_state.score}/600</h1>
            <h3 style="color: {grade_color}; margin: 10px 0;">Final Score: {score_percentage:.1f}%</h3>
        </div>
        """, unsafe_allow_html=True)

        # Round-by-round summary
        st.markdown("### 📊 **Round-by-Round Performance Summary**")

        summary_data = []
        for result in st.session_state.round_results:
            status = "✅ Correct" if result['correct'] else "❌ Incorrect" if result[
                                                                                'guess'] != "I Don't Know" else "🤷 Didn't Know"
            summary_data.append({
                "Round": f"Round {result['round']}",
                "Type": result['type'],
                "Target": f"{result['target']:+.2f}",
                "Your Guess": result['guess'],
                "Status": status,
                "Score": f"{result['score']}/100"
            })

        summary_df = pd.DataFrame(summary_data)
        st.dataframe(
            summary_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Round": st.column_config.TextColumn("🎮 Round", width="small"),
                "Type": st.column_config.TextColumn("📊 Correlation Type", width="medium"),
                "Target": st.column_config.TextColumn("🎯 Target", width="small"),
                "Your Guess": st.column_config.TextColumn("💭 Your Answer", width="medium"),
                "Status": st.column_config.TextColumn("✅ Result", width="small"),
                "Score": st.column_config.TextColumn("🏅 Points", width="small")
            }
        )

        # Performance analysis
        correct_answers = sum(1 for result in st.session_state.round_results if result['correct'])
        incorrect_answers = sum(1 for result in st.session_state.round_results if
                                not result['correct'] and result['guess'] != "I Don't Know")
        unknown_answers = sum(1 for result in st.session_state.round_results if result['guess'] == "I Don't Know")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("✅ Correct Answers", correct_answers, f"{(correct_answers / 6) * 100:.1f}%")
        with col2:
            st.metric("❌ Incorrect Answers", incorrect_answers, f"{(incorrect_answers / 6) * 100:.1f}%")
        with col3:
            st.metric("🤷 'I Don't Know'", unknown_answers, f"{(unknown_answers / 6) * 100:.1f}%")

        # Insights and tips
        st.markdown("### 💡 **Insights & Tips for Next Time**")
        insights = []

        if correct_answers >= 5:
            insights.append("🌟 **Excellent!** You have a strong understanding of correlation patterns!")
        elif correct_answers >= 3:
            insights.append("👍 **Good job!** You're getting the hang of recognizing correlations.")
        else:
            insights.append("💪 **Keep practicing!** Correlation recognition improves with experience.")

        if unknown_answers > 2:
            insights.append("🎯 **Tip:** When unsure, look for the general trend - upward, downward, or scattered.")

        # Check specific correlation types performance
        strong_pos_correct = sum(1 for r in st.session_state.round_results if "Positive" in r['type'] and r['correct'])
        strong_neg_correct = sum(1 for r in st.session_state.round_results if "Negative" in r['type'] and r['correct'])
        no_corr_correct = sum(
            1 for r in st.session_state.round_results if "No Correlation" in r['type'] and r['correct'])

        if strong_pos_correct == 0:
            insights.append("📈 **Focus area:** Practice identifying strong positive correlations (upward trends).")
        if strong_neg_correct == 0:
            insights.append("📉 **Focus area:** Practice identifying strong negative correlations (downward trends).")
        if no_corr_correct == 0:
            insights.append("🔄 **Focus area:** Practice recognizing when there's no clear pattern (random scatter).")

        for insight in insights:
            st.markdown(f"- {insight}")

        # Buttons to proceed
        col1, col2 = st.columns(2)

        with col1:
            if st.button("🎮 **Start New Game** (Next Student)", type="primary", use_container_width=True):
                # Reset for next student
                st.session_state.student_name = ""
                st.session_state.round = 1
                st.session_state.score = 0
                st.session_state.x = None
                st.session_state.y = None
                st.session_state.corr = None
                st.session_state.show_result = False
                st.session_state.round_results = []
                st.session_state.game_completed = False
                st.rerun()

        with col2:
            if st.button("📊 **View Leaderboard**", type="secondary", use_container_width=True):
                st.markdown("👇 **Scroll down to see the Hall of Fame!** 👇")

    # Regular game flow continues here
    elif st.session_state.round <= len(CORRELATION_STRUCTURE):
        # Show current round info with style - MOVED INSIDE ELSE BLOCK
        current_round_info = CORRELATION_STRUCTURE[st.session_state.round - 1]

        # Create a colorful header
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(
                f"######  **Hey {st.session_state.student_name}**!, welcome to round {st.session_state.round} of "
                f"6  🎮")
            # st.markdown(f"### **Round {st.session_state.round} of 6** 🎮")

        # Round info with colorful styling
        st.markdown(f"""
        <div style="
            background: linear-gradient(90deg, {current_round_info['color']}22, {current_round_info['color']}44);
            padding: 10px;
            border-radius: 10px;
            border-left: 5px solid {current_round_info['color']};
            margin: 10px 0;
        ">
            <h3 style="color: #2E4057; margin: 0;">
                {current_round_info['emoji']} <strong>{current_round_info['type']}</strong>
            </h3>
            <p style="color: #5A6C7D; margin: 5px 0 0 0; font-size: 16px;">
                🎯 {current_round_info['desc']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # ---------------------
        # Generate new plot with structured correlation
        # ---------------------
        if st.button("**Generate New Awesome Plot!** ✨🎲", type="primary"):
            # Get the target correlation for this round
            target_corr = current_round_info['target']

            # Generate data based on correlation type
            np.random.seed()  # Ensure randomness in each generation
            x = np.random.rand(1000)

            if abs(target_corr) < 0.1:  # No correlation
                y = np.random.rand(1000)
            else:
                # Create very strong correlated data
                noise_factor = 0.1  # Very low noise for strong correlations (0.9-1.0)
                noise = np.random.normal(0, noise_factor, 1000)

                if target_corr > 0:
                    # Positive correlation
                    y = target_corr * x + noise
                else:
                    # Negative correlation
                    y = target_corr * x + noise

            # Normalize y to reasonable range
            y = (y - np.min(y)) / (np.max(y) - np.min(y))

            st.session_state.x = x
            st.session_state.y = y
            st.session_state.corr = pearsonr(x, y)[0]
            st.success("🎉 New plot generated! Time to make your guess! 🎯\n\n")

        # ---------------------
        # Show plot and guess input
        # ---------------------
        if st.session_state.x is not None:
            st.markdown("#####  **Instruction : You are to use the plot below to guess the correlation!**")

            # Plot
            fig, ax = plt.subplots(figsize=(10, 7))
            ax.scatter(st.session_state.x, st.session_state.y,
                       c=current_round_info['color'],
                       edgecolors='white',
                       s=80,
                       alpha=0.8,
                       linewidth=1.5)
            ax.set_title(f"Round {st.session_state.round}: Estimate the correlation!",
                         fontsize=18, fontweight='bold', color='black', pad=20)
            ax.set_xlabel("X Variable", fontsize=14, fontweight='bold')
            ax.set_ylabel("Y Variable", fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.1, linestyle='--')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_color('#CCCCCC')
            ax.spines['left'].set_color('#CCCCCC')
            ax.spines['bottom'].set_linewidth(1.5)
            ax.spines['left'].set_linewidth(1.5)
            fig.patch.set_facecolor('white')
            st.pyplot(fig)

            # Guess input
            st.markdown("### 💭 **What's your guess?**")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                guess = st.radio(
                    "🎯 Choose the best description of the correlation in the plot:",
                    [
                        "High Positive Correlation",
                        "Low Positive Correlation",
                        "No Correlation",
                        "Low Negative Correlation",
                        "High Negative Correlation",
                        "I Don't Know"
                    ],
                    key=f"guess_select_round_{st.session_state.round}"
                )

            if "show_result" not in st.session_state:
                st.session_state.show_result = False

            if st.button("**Click here to submit your awesome guess!** ✅",
                         type="primary") and not st.session_state.show_result:
                actual = st.session_state.corr


                def get_actual_label(corr_val):
                    if corr_val >= 0.90:
                        return "High Positive Correlation"
                    elif 0.30 <= corr_val < 0.90:
                        return "Low Positive Correlation"
                    elif -0.30 < corr_val < 0.30:
                        return "No Correlation"
                    elif -0.90 < corr_val <= -0.30:
                        return "Low Negative Correlation"
                    elif corr_val <= -0.90:
                        return "High Negative Correlation"
                    else:
                        return "Uncategorized"


                actual_label = get_actual_label(actual)

                if guess == "I Don't Know":
                    round_score = 0
                elif guess == actual_label:
                    round_score = 100
                else:
                    round_score = 50

                st.session_state.round_score = round_score
                st.session_state.actual_label = actual_label
                st.session_state.actual_corr = actual
                st.session_state.student_guess = guess
                st.session_state.score += round_score
                st.session_state.show_result = True

                # Store round results for final summary
                round_result = {
                    "round": st.session_state.round,
                    "type": current_round_info['type'],
                    "target": current_round_info['target'],
                    "actual": actual,
                    "guess": guess,
                    "correct": guess == actual_label,
                    "score": round_score
                }
                st.session_state.round_results.append(round_result)

            if st.session_state.show_result:
                # Show feedback/results
                round_score = st.session_state.round_score
                actual = st.session_state.actual_corr
                actual_label = st.session_state.actual_label
                guess = st.session_state.student_guess

                if round_score == 100:
                    result_emoji = "🏆🌟"
                    result_color = "#28a745"
                    result_msg = "Perfect! You nailed it!"
                elif round_score == 50:
                    result_emoji = "👍💪"
                    result_color = "#17a2b8"
                    result_msg = "Good try! You're close!"
                else:
                    result_emoji = "🤔💡"
                    result_color = "#6c757d"
                    result_msg = "Keep practicing!"

                st.markdown(f"""
                <div style="background: linear-gradient(135deg, {result_color}22, {result_color}44);
                            padding: 20px;
                            border-radius: 15px;
                            border-left: 5px solid {result_color};
                            margin: 10px 0;">
                    <h3 style="color: #2E4057;">{result_emoji} <strong>{result_msg}</strong></h3>
                    <p><strong>✅ Actual Correlation Value:</strong> <code>{actual:.2f}</code></p>
                    <p><strong>🏷️ Actual Category:</strong> <code>{actual_label}</code></p>
                    <p><strong>🎯 Your Guess:</strong> <code>{guess}</code></p>
                    <p><strong>🏅 Score This Round:</strong> <code>{round_score}/100</code></p>
                    <p><strong>🔥 Total Score:</strong> <code>{st.session_state.score}/600</code></p>
                </div>
                """, unsafe_allow_html=True)

                if st.button("➡️ Next Round"):
                    st.session_state.round += 1
                    st.session_state.x = None
                    st.session_state.y = None
                    st.session_state.show_result = False
                    if st.session_state.round > len(CORRELATION_STRUCTURE):
                        # Game is complete, will show final results on next rerun
                        pass
                    st.rerun()

# ---------------------
# Show scoreboard
# ---------------------
if not st.session_state.scoreboard.empty:
    st.markdown("---")
    st.markdown("### 🏆🌟 **Hall of Fame - Correlation Champions!** 🌟🏆")

    sorted_scoreboard = st.session_state.scoreboard.sort_values(by="Total Score", ascending=False).reset_index(
        drop=True)

    # Add ranking emojis
    ranking_emojis = ["🥇", "🥈", "🥉", "🏅", "⭐", "🌟", "💫", "✨", "🎯", "🎮"]

    # Create a copy for display
    display_scoreboard = sorted_scoreboard.copy()
    display_scoreboard.index += 1  # Start ranking from 1

    # Add emoji column
    display_scoreboard['Rank'] = [ranking_emojis[min(i, len(ranking_emojis) - 1)] for i in
                                  range(len(display_scoreboard))]

    # Reorder columns
    display_scoreboard = display_scoreboard[['Rank', 'Name', 'Total Score']]

    # Style the dataframe
    st.dataframe(
        display_scoreboard,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Rank": st.column_config.TextColumn("🏆 Rank", width="small"),
            "Name": st.column_config.TextColumn("👤 Player Name", width="medium"),
            "Total Score": st.column_config.NumberColumn("🎯 Score", width="small", format="%d/600")
        }
    )

# ---------------------
# Instructor reset button (hidden behind password)
# ---------------------
st.markdown("---")
with st.expander("🔐👨‍🏫 **Instructor Control Panel**"):
    st.markdown("### 🎓 **Teacher Zone** 🎓")
    admin_password = st.text_input("🔑 Enter instructor password to unlock magic powers", type="password")
    if admin_password == "letmein":  # Change to your secret
        st.success("🎉 Welcome, Teacher! You have admin powers! 🎉")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🚨💥 **Reset Entire Scoreboard** 💥🚨", type="secondary"):
                st.session_state.scoreboard = pd.DataFrame(columns=["Name", "Total Score"])
                st.success("✅ Scoreboard has been reset successfully! 🧹✨")
                st.balloons()

        with col2:
            st.info("🔥 **Quick Stats:** 🔥\n\n" +
                    f"📊 Total Players: **{len(st.session_state.scoreboard)}**\n\n" +
                    f"🎯 Rounds per Game: **6**\n\n" +
                    f"🏆 Max Possible Score: **600**")

        # Show correlation structure for instructor reference
        st.markdown("### 📋🎯 **Game Structure Reference:**")

        structure_df = pd.DataFrame([
            {
                "Round": f"Round {i + 1}",
                "Type": f"{info['emoji']} {info['type']}",
                "Target": f"{info['target']:+.2f}",
                "Description": info['desc']
            }
            for i, info in enumerate(CORRELATION_STRUCTURE)
        ])

        st.dataframe(
            structure_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Round": st.column_config.TextColumn("🎮 Round", width="small"),
                "Type": st.column_config.TextColumn("📊 Correlation Type", width="medium"),
                "Target": st.column_config.TextColumn("🎯 Target Value", width="small"),
                "Description": st.column_config.TextColumn("💭 Description", width="large")
            }
        )