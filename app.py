import streamlit as st
import pandas as pd
import datetime

# File to store scores
DATA_FILE = "golf_scores.csv"

# Sample course data with tee-specific ratings
COURSES = {
    "St Andrews": {
        "White": {"course_rating": 72.0, "slope_rating": 123},
        "Yellow": {"course_rating": 70.5, "slope_rating": 118},
        "Red": {"course_rating": 68.0, "slope_rating": 115}
    },
    "Royal Birkdale": {
        "White": {"course_rating": 73.2, "slope_rating": 130},
        "Yellow": {"course_rating": 71.0, "slope_rating": 125},
        "Red": {"course_rating": 69.0, "slope_rating": 120}
    }
}

# Load or initialize data
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE, parse_dates=["Date"])
    else:
        return pd.DataFrame(columns=["Player", "Date", "Course", "Tee", "Score", "Course Rating", "Slope Rating"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Calculate score differential
def calculate_differential(score, course_rating, slope_rating):
    return round((score - course_rating) * 113 / slope_rating, 1)

# Calculate handicap index from best 8 of last 20 differentials
def calculate_handicap_index(differentials):
    if len(differentials) < 8:
        return None
    best_8 = sorted(differentials)[0:8]
    return round(sum(best_8) / 8, 1)

# Calculate course handicap
def calculate_course_handicap(handicap_index, course_rating, slope_rating):
    return round(handicap_index * slope_rating / 113, 1)

# App layout
st.title("🏌️ Golf Handicap Tracker (WHS)")

# Load data
df = load_data()

# Sidebar: Add or remove players
st.sidebar.header("Player Management")
player_list = sorted(df["Player"].unique())
new_player = st.sidebar.text_input("Add New Player")
if st.sidebar.button("Add Player") and new_player:
    if new_player not in player_list:
        player_list.append(new_player)
        st.sidebar.success(f"Added player: {new_player}")
selected_player = st.sidebar.selectbox("Select Player", player_list)
if st.sidebar.button("Remove Player") and selected_player:
    df = df[df["Player"] != selected_player]
    save_data(df)
    st.sidebar.success(f"Removed player: {selected_player}")
    st.experimental_rerun()

# Display scores for selected player
player_scores = df[df["Player"] == selected_player].sort_values("Date", ascending=False)
st.subheader(f"Score History for {selected_player}")
st.dataframe(player_scores)

# Calculate and display handicap
if len(player_scores) >= 8:
    diffs = player_scores["Score"].astype(float).combine(
        player_scores["Course Rating"].astype(float), lambda s, cr: s - cr
    ).combine(
        player_scores["Slope Rating"].astype(float), lambda d, sr: round(d * 113 / sr, 1)
    )
    handicap_index = calculate_handicap_index(diffs.tolist())
    latest = player_scores.iloc[0]
    course_handicap = calculate_course_handicap(handicap_index, latest["Course Rating"], latest["Slope Rating"])
    st.success(f"Handicap Index: {handicap_index} | Course Handicap: {course_handicap}")
else:
    st.info("At least 8 scores are required to calculate a handicap index.")

# Score entry form at the bottom
st.markdown("---")
st.subheader("➕ Add New Score")
with st.form("score_form"):
    date = st.date_input("Date", datetime.date.today())
    course = st.selectbox("Course", list(COURSES.keys()))
    tee = st.selectbox("Tee", list(COURSES[course].keys()))
    course_rating = COURSES[course][tee]["course_rating"]
    slope_rating = COURSES[course][tee]["slope_rating"]
    score = st.number_input("Score", min_value=50, max_value=150, step=1)
    submitted = st.form_submit_button("Submit Score")
    if submitted:
        new_entry = {
            "Player": selected_player,
            "Date": pd.to_datetime(date),
            "Course": course,
            "Tee": tee,
            "Score": score,
            "Course Rating": course_rating,
            "Slope Rating": slope_rating
        }
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        save_data(df)
        st.success("Score added successfully!")
        st.experimental_rerun()
