import streamlit as st
import pandas as pd
import datetime
import os

# Initialize session state
if 'players' not in st.session_state:
    st.session_state.players = {
        'Alice': [],
        'Bob': []
    }

st.title("🏌️ Golf Handicap Tracker (WHS)")

# Select player
player_names = list(st.session_state.players.keys())
selected_player = st.selectbox("Select Player", player_names)

# Display score history
st.subheader(f"Score History for {selected_player}")
scores = st.session_state.players[selected_player]
if scores:
    df = pd.DataFrame(scores)
    st.dataframe(df)
else:
    st.info("No scores yet for this player.")

# Add new score
st.subheader("Add New Score")
with st.form("score_form"):
    date = st.date_input("Date", datetime.date.today())
    course = st.text_input("Course Name")
    tee = st.selectbox("Tee Color", ["White", "Yellow", "Red"])
    score = st.number_input("Score", min_value=50, max_value=150, value=90)
    course_rating = st.number_input("Course Rating", min_value=60.0, max_value=80.0, value=72.0)
    slope_rating = st.number_input("Slope Rating", min_value=55, max_value=155, value=113)
    submitted = st.form_submit_button("Add Score")

    if submitted:
        differential = (score - course_rating) * 113 / slope_rating
        st.session_state.players[selected_player].append({
            "Date": date,
            "Course": course,
            "Tee": tee,
            "Score": score,
            "Course Rating": course_rating,
            "Slope Rating": slope_rating,
            "Differential": round(differential, 2)
        })
        st.success("Score added!")

# Calculate Handicap Index
st.subheader("Handicap Index")
if len(scores) >= 8:
    differentials = sorted([s["Differential"] for s in scores])[:8]
    handicap_index = round(sum(differentials) / 8, 2)
    st.write(f"Handicap Index: **{handicap_index}**")

    # Use latest course rating and slope rating for course handicap
    latest = scores[-1]
    course_handicap = round((handicap_index * latest["Slope Rating"]) / 113 + (latest["Course Rating"] - latest["Course Rating"]), 2)
    st.write(f"Course Handicap (latest course): **{course_handicap}**")
else:
    st.info("At least 8 scores are required to calculate a handicap index.")