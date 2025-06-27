import os
import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime


API_KEY = "JYFJIZ5QHLC6QLMFAO6FJFSVXM"

API_URL = "https://golfcourseapi.com/api/v1/courses/search"
DATA_FILE = "golf_scores.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

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

def calculate_course_handicap(handicap_index, slope_rating):
    return round(handicap_index * slope_rating / 113, 2)

def search_courses(query):
    headers = {"Authorization": f"Key {API_KEY}"}
    params = {"q": query, "country": "GB"}
    response = requests.get(API_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("courses", [])
    return []

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

        delete_index = st.number_input("Enter index to delete", min_value=0, max_value=len(df)-1, step=1)
        if st.button("Delete Score"):
            data[player].pop(delete_index)
            save_data(data)
            st.success("Score deleted.")
            st.experimental_rerun()
    else:
        st.info("No scores yet.")

    handicap_index = calculate_handicap_index(data[player])
    if handicap_index is not None:
        st.write(f"**Handicap Index:** {handicap_index}")
        latest = data[player][-1]
        course_handicap = calculate_course_handicap(handicap_index, latest['slope_rating'])
        st.write(f"**Course Handicap:** {course_handicap}")
    else:
        st.info("At least 8 scores are required to calculate handicap index.")

    st.subheader("Add New Score")

    course_query = st.text_input("Search UK Golf Course")
    selected_course_name = None
    selected_course = None

    if course_query and len(course_query) >= 3:
        course_options = search_courses(course_query)
        course_names = [c['name'] for c in course_options]
        selected_course_name = st.selectbox("Matching Courses", course_names) if course_names else None
        selected_course = next((c for c in course_options if c['name'] == selected_course_name), None)
    else:
        st.info("Start typing a course name (min 3 characters)...")

    tee_options = selected_course.get("tees", []) if selected_course else []
    tee_names = [t['name'] for t in tee_options]
    selected_tee = st.selectbox("Select Tee", tee_names) if tee_names else None

    selected_tee_data = next((t for t in tee_options if t['name'] == selected_tee), None)
    course_rating = selected_tee_data.get("course_rating", 72.0) if selected_tee_data else 72.0
    slope_rating = selected_tee_data.get("slope_rating", 113) if selected_tee_data else 113

    st.write(f"Course Rating: {course_rating}, Slope Rating: {slope_rating}")

    date = st.date_input("Date", datetime.today())
    score = st.number_input("Score", min_value=40, max_value=150, step=1)

    if st.button("Add Score"):
        new_score = {
            "date": date.strftime("%Y-%m-%d"),
            "course": selected_course_name,
            "tee": selected_tee,
            "score": score,
            "course_rating": course_rating,
            "slope_rating": slope_rating
        }
        data[player].append(new_score)
        save_data(data)
        st.success("Score added.")
        st.experimental_rerun()





