import streamlit as st
import pandas as pd
from datetime import date, timedelta
import os

st.set_page_config(page_title="Daily Habit Tracker", layout="centered")

NAMES = ["Theju", "Udaya", "Teju", "Tushara", "Kavya"]
DATA_FILE = "scores.csv"

# Load or create CSV
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["name", "date", "diet", "workout", "social", "diet_penalty", "score"])
    df.to_csv(DATA_FILE, index=False)

st.title("🏆 Daily Habit Score Tracker")

# Input
st.header("Submit Today's Update")

name = st.selectbox("Name", NAMES)
diet = st.selectbox("Diet", ["Yes", "No"])
workout = st.selectbox("Workout", ["Yes", "No"])
social = st.selectbox("Social Media", ["Yes", "No"])

diet_penalty = 1
if diet == "No":
    diet_penalty = st.number_input("How many diet mistakes?", min_value=1, max_value=10, value=1)

# Scoring logic
score = 0
score += 1 if diet == "Yes" else -diet_penalty
score += 1 if workout == "Yes" else -1
score += 1 if social == "Yes" else 0

st.subheader(f"Today's Score: {score}")

if st.button("Submit"):
    new_row = {
        "name": name,
        "date": str(date.today()),
        "diet": diet,
        "workout": workout,
        "social": social,
        "diet_penalty": diet_penalty,
        "score": score
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    st.success("Submitted!")

# Convert date column
df["date"] = pd.to_datetime(df["date"]).dt.date

# -------------------------
# DAILY SUMMARY
# -------------------------
st.header("📅 Daily Summary")

today = date.today()
daily_df = df[df["date"] == today]

if len(daily_df) == 0:
    st.info("No entries today yet.")
else:
    st.dataframe(daily_df[["name", "diet", "workout", "social", "score"]])

# -------------------------
# WEEKLY SUMMARY (Last 7 Days)
# -------------------------
st.header("📅 Weekly Summary (Last 7 Days)")

week_start = today - timedelta(days=6)
weekly_df = df[(df["date"] >= week_start) & (df["date"] <= today)]

weekly_scores = (
    weekly_df.groupby("name")["score"]
    .sum()
    .reset_index()
    .sort_values("score", ascending=False)
)

st.dataframe(weekly_scores)

if len(weekly_scores) > 0:
    winner = weekly_scores.iloc[0]
    st.success(f"🏆 Weekly Winner: {winner['name']} with {winner['score']} points")

# -------------------------
# MONTHLY SUMMARY (Last 28 Days)
# -------------------------
st.header("📆 Monthly Summary (Last 28 Days)")

month_start = today - timedelta(days=27)
monthly_df = df[(df["date"] >= month_start) & (df["date"] <= today)]

monthly_scores = (
    monthly_df.groupby("name")["score"]
    .sum()
    .reset_index()
    .sort_values("score", ascending=False)
)

st.dataframe(monthly_scores)

if len(monthly_scores) > 0:
    winner = monthly_scores.iloc[0]
    st.success(f"🏆 Monthly Winner: {winner['name']} with {winner['score']} points")
