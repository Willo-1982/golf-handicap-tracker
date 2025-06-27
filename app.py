
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import openpyxl

# Initialize session state for players and scores
if 'players' not in st.session_state:
    st.session_state.players = {}
if 'scores' not in st.session_state:
    st.session_state.scores = []

# Function to calculate handicap index
def calculate_handicap_index(scores):
    if len(scores) < 8:
        return None
    scores = sorted(scores)[:8]
    return np.mean(scores)

# Function to calculate course handicap
def calculate_course_handicap(handicap_index, course_rating, slope_rating):
    return (handicap_index - course_rating) * 113 / slope_rating

# Title
st.title('Golf Handicap Tracker')

# Add new player
with st.form(key='add_player'):
    st.header('Add New Player')
    player_name = st.text_input('Player Name')
    submit_player = st.form_submit_button('Add Player')
    if submit_player and player_name:
        st.session_state.players[player_name] = []
        st.success(f'Player {player_name} added!')

# Select player
player = st.selectbox('Select Player', list(st.session_state.players.keys()))

# Add new score
with st.form(key='add_score'):
    st.header('Add New Score')
    score = st.number_input('Score', min_value=0)
    course_rating = st.number_input('Course Rating', min_value=0.0)
    slope_rating = st.number_input('Slope Rating', min_value=0)
    date = st.date_input('Date', value=datetime.date.today())
    submit_score = st.form_submit_button('Add Score')
    if submit_score and player:
        st.session_state.scores.append({
            'Player': player,
            'Score': score,
            'Course Rating': course_rating,
            'Slope Rating': slope_rating,
            'Date': date
        })
        st.success(f'Score added for {player}!')

# Display scores
st.header('Scores')
if player:
    player_scores = [s for s in st.session_state.scores if s['Player'] == player]
    if player_scores:
        df = pd.DataFrame(player_scores)
        st.dataframe(df)
        handicap_index = calculate_handicap_index(df['Score'].tolist())
        if handicap_index is not None:
            st.write(f'Handicap Index: {handicap_index:.2f}')
            course_handicap = calculate_course_handicap(handicap_index, course_rating, slope_rating)
            st.write(f'Course Handicap: {course_handicap:.2f}')
        else:
            st.write('Not enough scores to calculate handicap index.')
    else:
        st.write('No scores available for this player.')

# Export to Excel
if st.button('Export to Excel'):
    with pd.ExcelWriter('golf_handicap_tracker.xlsx', engine='openpyxl') as writer:
        for player in st.session_state.players.keys():
            player_scores = [s for s in st.session_state.scores if s['Player'] == player]
            if player_scores:
                df = pd.DataFrame(player_scores)
                df.to_excel(writer, sheet_name=player, index=False)
    st.success('Data exported to golf_handicap_tracker.xlsx')
