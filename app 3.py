import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

DATA_FILE = "golf_data.json"
FAVOURITES_FILE = "favourites.json"

# Load data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def load_favourites():
    if os.path.exists(FAVOURITES_FILE):
        with open(FAVOURITES_FILE, "r") as f:
            return json.load(f)
    return []

def save_favourites(favs):
    with open(FAVOURITES_FILE, "w") as f:
        json.dump(favs, f)

# Handicap calculation
def calculate_handicap_index(scores):
    differentials = []
    for score in scores:
        differential = (score['score'] - score['course_rating']) * 113 / score['slope_rating']
        differentials.append(differential)
    differentials.sort()
    best_8 = differentials[:8]
    return round(sum(best_8) / len(best_8), 2) if best_8 else None

# App
st.title("Golf Handicap Tracker")

data = load_data()
favourites = load_favourites()

# Sidebar: Player management
st.sidebar.header("Player Management")
new_player = st.sidebar.text_input("Add New Player")
if st.sidebar.button("Add Player") and new_player:
    if new_player not in data:
        data[new_player] = []
        save_data(data)
        st.sidebar.success(f"Player '{new_player}' added.")

remove_player = st.sidebar.selectbox("Remove Player", list(data.keys()))
if st.sidebar.button("Remove Selected Player"):
    if remove_player in data:
        del data[remove_player]
        save_data(data)
        st.sidebar.success(f"Player '{remove_player}' removed.")

# Main: Select player
player = st.selectbox("Select Player", list(data.keys()))
if player:
    st.subheader(f"{player}'s Scores")
    scores = data[player]
    df = pd.DataFrame(scores)
    if not df.empty:
        st.dataframe(df)
        handicap_index = calculate_handicap_index(scores)
        if handicap_index is not None:
            st.write(f"**Handicap Index:** {handicap_index}")
    else:
        st.write("No scores yet.")

    # Delete score
    if scores:
        delete_index = st.selectbox("Select score to delete", range(len(scores)))
        if st.button("Delete Selected Score"):
            scores.pop(delete_index)
            data[player] = scores
            save_data(data)
            st.success("Score deleted.")

# Add score section
st.subheader("Add New Score")

course_input = st.text_input("Search Course")
matching_courses = [c for c in uk_courses.keys() if course_input.lower() in c.lower()]
selected_course = st.selectbox("Select Course", matching_courses)

if selected_course:
    if st.button("Add to Favourites") and selected_course not in favourites:
        favourites.append(selected_course)
        save_favourites(favourites)
        st.success(f"Added '{selected_course}' to favourites.")

    tee = st.selectbox("Tee", ["White", "Yellow", "Red"])
    course_rating, slope_rating = uk_courses[selected_course][tee]
    st.write(f"Course Rating: {course_rating}, Slope Rating: {slope_rating}")

    score = st.number_input("Score", min_value=40, max_value=150, value=85)
    date = st.date_input("Date", datetime.today())

    if st.button("Add Score") and player:
        new_score = {
            "date": date.strftime("%Y-%m-%d"),
            "course": selected_course,
            "tee": tee,
            "score": score,
            "course_rating": course_rating,
            "slope_rating": slope_rating
        }
        data[player].append(new_score)
        save_data(data)
        st.success("Score added.")
