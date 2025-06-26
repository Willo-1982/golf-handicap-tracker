
import streamlit as st
import pandas as pd
from datetime import datetime

# Load the Excel file
df = pd.read_excel('golf_handicap_tracker.xlsx')

# Function to calculate handicap index
def calculate_handicap_index(scores):
    scores = sorted(scores)[:8]
    return sum(scores) / len(scores)

# Function to calculate course handicap
def calculate_course_handicap(handicap_index, course_rating, slope_rating):
    return (handicap_index - course_rating) * (113 / slope_rating)

# Streamlit app
st.title('Golf Handicap Tracker')

# Player selection
player = st.selectbox('Select Player', df['Player'].unique())

# Filter data for the selected player
player_data = df[df['Player'] == player]

# Display player data
st.write('Player Data:')
st.dataframe(player_data)

# Calculate and display handicap
if len(player_data) >= 8:
    scores = player_data['Score'].tolist()
    handicap_index = calculate_handicap_index(scores)
    course_rating = player_data['Course Rating'].iloc[0]
    slope_rating = player_data['Slope Rating'].iloc[0]
    course_handicap = calculate_course_handicap(handicap_index, course_rating, slope_rating)
    st.write(f"{player}'s Handicap Index: {handicap_index:.2f}")
    st.write(f'{player}'s Course Handicap: {course_handicap:.2f}')
else:
    st.write('Not enough scores to calculate handicap.')

# Add new score
st.write('Add New Score:')
new_score = st.number_input('Score', min_value=0)
new_date = st.date_input('Date', value=datetime.now())
new_course = st.text_input('Course', value='St Andrews')
new_tee = st.selectbox('Tee', ['White', 'Yellow', 'Red'])
new_course_rating = st.number_input('Course Rating', value=72.0)
new_slope_rating = st.number_input('Slope Rating', value=123)

if st.button('Add Score'):
    new_data = {
        'Player': player,
        'Course': new_course,
        'Tee': new_tee,
        'Score': new_score,
        'Date': new_date,
        'Course Rating': new_course_rating,
        'Slope Rating': new_slope_rating
    }
    df = df.append(new_data, ignore_index=True)
    df.to_excel('golf_handicap_tracker.xlsx', index=False)
    st.success('Score added successfully!')
