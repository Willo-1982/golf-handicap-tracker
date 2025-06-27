
import streamlit as st
import pandas as pd
import numpy as np
import datetime

# Sample data for players
players_data = {
    'Alice': [
        {'date': '2023-01-01', 'course': 'St Andrews', 'tee': 'White', 'score': 85, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-01-15', 'course': 'St Andrews', 'tee': 'White', 'score': 88, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-02-01', 'course': 'St Andrews', 'tee': 'White', 'score': 82, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-02-15', 'course': 'St Andrews', 'tee': 'White', 'score': 90, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-03-01', 'course': 'St Andrews', 'tee': 'White', 'score': 84, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-03-15', 'course': 'St Andrews', 'tee': 'White', 'score': 87, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-04-01', 'course': 'St Andrews', 'tee': 'White', 'score': 83, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-04-15', 'course': 'St Andrews', 'tee': 'White', 'score': 86, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-05-01', 'course': 'St Andrews', 'tee': 'White', 'score': 81, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-05-15', 'course': 'St Andrews', 'tee': 'White', 'score': 89, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-06-01', 'course': 'St Andrews', 'tee': 'White', 'score': 80, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-06-15', 'course': 'St Andrews', 'tee': 'White', 'score': 91, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-07-01', 'course': 'St Andrews', 'tee': 'White', 'score': 79, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-07-15', 'course': 'St Andrews', 'tee': 'White', 'score': 92, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-08-01', 'course': 'St Andrews', 'tee': 'White', 'score': 78, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-08-15', 'course': 'St Andrews', 'tee': 'White', 'score': 93, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-09-01', 'course': 'St Andrews', 'tee': 'White', 'score': 77, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-09-15', 'course': 'St Andrews', 'tee': 'White', 'score': 94, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-10-01', 'course': 'St Andrews', 'tee': 'White', 'score': 76, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-10-15', 'course': 'St Andrews', 'tee': 'White', 'score': 95, 'course_rating': 72.0, 'slope_rating': 123},
    ],
    'Bob': [
        {'date': '2023-01-01', 'course': 'St Andrews', 'tee': 'White', 'score': 90, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-01-15', 'course': 'St Andrews', 'tee': 'White', 'score': 92, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-02-01', 'course': 'St Andrews', 'tee': 'White', 'score': 91, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-02-15', 'course': 'St Andrews', 'tee': 'White', 'score': 93, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-03-01', 'course': 'St Andrews', 'tee': 'White', 'score': 89, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-03-15', 'course': 'St Andrews', 'tee': 'White', 'score': 94, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-04-01', 'course': 'St Andrews', 'tee': 'White', 'score': 88, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-04-15', 'course': 'St Andrews', 'tee': 'White', 'score': 95, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-05-01', 'course': 'St Andrews', 'tee': 'White', 'score': 87, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-05-15', 'course': 'St Andrews', 'tee': 'White', 'score': 96, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-06-01', 'course': 'St Andrews', 'tee': 'White', 'score': 86, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-06-15', 'course': 'St Andrews', 'tee': 'White', 'score': 97, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-07-01', 'course': 'St Andrews', 'tee': 'White', 'score': 85, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-07-15', 'course': 'St Andrews', 'tee': 'White', 'score': 98, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-08-01', 'course': 'St Andrews', 'tee': 'White', 'score': 84, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-08-15', 'course': 'St Andrews', 'tee': 'White', 'score': 99, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-09-01', 'course': 'St Andrews', 'tee': 'White', 'score': 83, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-09-15', 'course': 'St Andrews', 'tee': 'White', 'score': 100, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-10-01', 'course': 'St Andrews', 'tee': 'White', 'score': 82, 'course_rating': 72.0, 'slope_rating': 123},
        {'date': '2023-10-15', 'course': 'St Andrews', 'tee': 'White', 'score': 101, 'course_rating': 72.0, 'slope_rating': 123},
    ]
}

# Function to calculate handicap index
def calculate_handicap_index(scores):
    differentials = []
    for score in scores:
        differential = (score['score'] - score['course_rating']) * 113 / score['slope_rating']
        differentials.append(differential)
    differentials.sort()
    best_8_differentials = differentials[:8]
    handicap_index = sum(best_8_differentials) / len(best_8_differentials)
    return handicap_index

# Function to display player data
def display_player_data(player_name, scores):
    st.write(f"### {player_name}'s Scores")
    df = pd.DataFrame(scores)
    st.dataframe(df)
    handicap_index = calculate_handicap_index(scores)
    st.write(f"**Handicap Index:** {handicap_index:.2f}")

# Streamlit app layout
st.title("Golf Handicap Tracker")
st.write("Track and calculate golf handicaps based on the World Handicap System (WHS).")

# Player selection
player_name = st.selectbox("Select Player", list(players_data.keys()))

# Display player data
if player_name:
    display_player_data(player_name, players_data[player_name])

# Add new score
st.write("### Add New Score")
new_date = st.date_input("Date", datetime.date.today())
new_course = st.text_input("Course", "St Andrews")
new_tee = st.selectbox("Tee", ["White", "Yellow", "Red"])
new_score = st.number_input("Score", min_value=0, max_value=200, value=80)
new_course_rating = st.number_input("Course Rating", min_value=0.0, max_value=100.0, value=72.0)
new_slope_rating = st.number_input("Slope Rating", min_value=55, max_value=155, value=123)

if st.button("Add Score"):
    new_score_entry = {
        'date': new_date.strftime('%Y-%m-%d'),
        'course': new_course,
        'tee': new_tee,
        'score': new_score,
        'course_rating': new_course_rating,
        'slope_rating': new_slope_rating
    }
    players_data[player_name].append(new_score_entry)
    st.success("New score added successfully!")
    display_player_data(player_name, players_data[player_name])

# Export to Excel
if st.button("Export to Excel"):
    with pd.ExcelWriter("golf_handicap_tracker.xlsx") as writer:
        for player, scores in players_data.items():
            df = pd.DataFrame(scores)
            df.to_excel(writer, sheet_name=player, index=False)
    st.success("Data exported to golf_handicap_tracker.xlsx")
