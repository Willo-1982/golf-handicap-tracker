import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime

# File to store player data
DATA_FILE = "golf_scores.json"

# Sample UK golf courses with ratings
uk_courses = {
    "St Andrews": {
        "White": {"course_rating": 72.0, "slope_rating": 123},
        "Yellow": {"course_rating": 70.5, "slope_rating": 120},
        "Red": {"course_rating": 68.0, "slope_rating": 115}
    },
    "Royal Birkdale": {
        "White": {"course_rating": 73.2, "slope_rating": 130},
        "Yellow": {"course_rating": 71.0, "slope_rating": 125},
        "Red": {"course_rating": 69.0, "slope_rating": 118}
    },
    "Sunningdale": {
        "White": {"course_rating": 72.8, "slope_rating": 128},
        "Yellow": {"course_rating": 71.2, "slope_rating": 124},
        "Red": {"course_rating": 69.5, "slope_rating": 119}
    }
}

# Load data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

# Save data
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Calculate handicap index
def calculate_handicap_index(scores):
    if len(scores) < 8:
        return None
    differentials = [
        (s['score'] - s['course_rating']) * 113 / s['slope_rating']
        for s in scores
    ]
    differentials.sort()
    best_8 = differentials[:8]
    return round(sum(best_8) / len(best_8), 2)

# Calculate course handicap
def calculate_course_handicap(handicap_index, course_rating, slope_rating):
    return round(handicap_index * slope_rating / 113, 2)

# Streamlit UI
st.title("Golf Handicap Tracker")

data = load_data()

# Sidebar for player management
st.sidebar.header("Player Management")
new_player = st.sidebar.text_input("Add New Player")
if st.sidebar.button("Add Player") and new_player:
    if new_player not in data:
        data[new_player] = []
        save_data(data)
        st.sidebar.success(f"Player '{new_player}' added.")

remove_player = st.sidebar.selectbox("Remove Player", [""] + list(data.keys()))
if st.sidebar.button("Remove Selected Player") and remove_player:
    if remove_player in data:
        del data[remove_player]
        save_data(data)
        st.sidebar.success(f"Player '{remove_player}' removed.")

# Select player
player = st.selectbox("Select Player", list(data.keys()))
if player:
    st.subheader(f"{player}'s Score History")
    scores = data[player]
    if scores:
        df = pd.DataFrame(scores)
        df.index.name = "Index"
        st.dataframe(df)

        # Delete score
        delete_index = st.number_input("Enter index to delete", min_value=0, max_value=len(df)-1, step=1)
        if st.button("Delete Score"):
            data[player].pop(delete_index)
            save_data(data)
            st.success("Score deleted.")
            st.experimental_rerun()
    else:
        st.info("No scores yet.")

    # Handicap calculation
    handicap_index = calculate_handicap_index(data[player])
    if handicap_index is not None:
        st.write(f"**Handicap Index:** {handicap_index}")
        latest = data[player][-1]
        course_handicap = calculate_course_handicap(handicap_index, latest['course_rating'], latest['slope_rating'])
        st.write(f"**Course Handicap:** {course_handicap}")
    else:
        st.info("At least 8 scores are required to calculate handicap index.")

    # Add new score
    st.subheader("Add New Score")
    date = st.date_input("Date", datetime.today())
    course_input = st.text_input("Course Name")
    matching_courses = [c for c in uk_courses.keys() if course_input.lower() in c.lower()]
    selected_course = st.selectbox("Matching Courses", matching_courses) if matching_courses else None
    tee = st.selectbox("Tee", ["White", "Yellow", "Red"])
    score = st.number_input("Score", min_value=40, max_value=150, step=1)

    if selected_course:
        course_rating = uk_courses[selected_course][tee]["course_rating"]
        slope_rating = uk_courses[selected_course][tee]["slope_rating"]
        st.write(f"Course Rating: {course_rating}, Slope Rating: {slope_rating}")
    else:
        course_rating = st.number_input("Course Rating", min_value=60.0, max_value=80.0, step=0.1)
        slope_rating = st.number_input("Slope Rating", min_value=55, max_value=155, step=1)

    if st.button("Add Score"):
        new_score = {
            "date": date.strftime("%Y-%m-%d"),
            "course": selected_course if selected_course else course_input,
            "tee": tee,
            "score": score,
            "course_rating": course_rating,
            "slope_rating": slope_rating
        }
        data[player].append(new_score)
        save_data(data)
        st.success("Score added.")
        st.experimental_rerun()

