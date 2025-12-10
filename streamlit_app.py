import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
import os

st.set_page_config(page_title="Daily Habit Tracker", layout="centered")

# Names
NAMES = ["Theju", "Udaya", "Teju", "Tushara", "Kavya"]

# CSV file to store all data
DATA_FILE = "scores.csv"

# Start date for weekly/monthly cycles
START_DATE = date(2025, 1, 2)  # All calculations begin from Jan 2

# ---------------------------------------
# LOAD OR CREATE CSV STORAGE
# ---------------------------------------
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["name", "date", "diet", "workout", "social", "diet_penalty", "score"])
    df.to_csv(DATA_FILE, index=False)

st.title("🏆 Daily Habit Score Tracker")

# ---------------------------------------
# INPUT SECTION
# ---------------------------------------
st.header("Submit Today's Update")

name = st.selectbox("Name", NAMES)
diet = st.selectbox("Diet", ["Yes", "No"])
workout = st.selectbox("Workout", ["Yes", "No"])
social = st.selectbox("Social Media", ["Yes", "No"])

diet_penalty = 1
if diet == "No":
    diet_penalty = st.number_input("How many diet mistakes?", min_value=1, max_value=10, value=1)

# ---------------------------------------
# SCORING LOGIC
# ---------------------------------------
score = 0
score += 1 if diet == "Yes" else -diet_penalty
score += 1 if workout == "Yes" else -1
score += 1 if social == "Yes" else 0

st.subheader(f"Today's Score: ⭐ {score}")

# ---------------------------------------
# SUBMIT LOGIC (Update instead of duplicate)
# ---------------------------------------
if st.button("Submit"):
    today = str(date.today())

    # Remove existing entry for same person + date
    df = df[~((df["name"] == name) & (df["date"] == today))]

    # Add new updated row
    new_row = {
        "name": name,
        "date": today,
        "diet": diet,
        "workout": workout,
        "social": social,
        "diet_penalty": diet_penalty,
        "score": score
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # Save CSV
    df.to_csv(DATA_FILE, index=False)

    st.success("✅ Entry submitted and updated for today!")

# ---------------------------------------
# DAILY SUMMARY
# ---------------------------------------
st.header("📅 Daily Summary")

today = str(date.today())
today_df = df[df["date"] == today]

if len(today_df) == 0:
    st.info("No entries submitted today yet.")
else:
    st.dataframe(today_df[["name", "diet", "workout", "social", "score"]])

# Convert date column
df["date"] = pd.to_datetime(df["date"]).dt.date

# ---------------------------------------
# WEEKLY SUMMARY (Custom cycle starting Jan 2)
# ---------------------------------------
st.header("📅 Weekly Summary (Custom 7-day Cycle)")

# Compute week number from start date
df["days_since_start"] = (df["date"] - START_DATE).apply(lambda x: x.days)
df = df[df["days_since_start"] >= 0]  # Ignore dates before Jan 2

df["week_number"] = df["days_since_start"] // 7
current_week = (date.today() - START_DATE).days // 7

weekly_df = df[df["week_number"] == current_week]
weekly_scores = weekly_df.groupby("name")["score"].sum().reset_index()
weekly_scores = weekly_scores.sort_values("score", ascending=False)

if len(weekly_scores) == 0:
    st.info("No entries for this week yet.")
else:
    st.subheader(f"Week {current_week + 1} Summary")
    st.dataframe(weekly_scores)

    winner = weekly_scores.iloc[0]
    st.success(
        f"🏆 **Weekly Winner:** {winner['name']} with **{winner['score']}** points!"
    )

# ---------------------------------------
# MONTHLY SUMMARY (4-week cycles)
# ---------------------------------------
st.header("📆 Monthly Summary (4-Week Cycle)")

df["month_number"] = df["week_number"] // 4
current_month = current_week // 4

monthly_df = df[df["month_number"] == current_month]
monthly_scores = monthly_df.groupby("name")["score"].sum().reset_index()
monthly_scores = monthly_scores.sort_values("score", ascending=False)

if len(monthly_scores) == 0:
    st.info("No entries for this month yet.")
else:
    st.subheader(f"Month {current_month + 1} Summary")
    st.dataframe(monthly_scores)

    month_winner = monthly_scores.iloc[0]
    st.success(
        f"🏆 **Monthly Winner:** {month_winner['name']} with **{month_winner['score']}** points!"
    )
