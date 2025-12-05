import streamlit as st
from datetime import date, timedelta
import pandas as pd

st.set_page_config(page_title="Study Planner", layout="centered")
st.title("📚 Personal Study Planner")
st.caption("👨‍💻 Developed by Deepak Methre")

st.write("Create a simple day-wise study plan for your upcoming exam.")

# --- Inputs ---
today = date.today()
exam_date = st.date_input("📅 Exam date", min_value=today + timedelta(days=1))
hours_per_day = st.number_input("⏰ Hours you can study per day", min_value=1.0, max_value=16.0, value=3.0, step=0.5)

subjects_text = st.text_area(
    "📝 Enter your subjects (one per line)",
    value="Maths\nPhysics\nChemistry"
)

if st.button("Generate Study Plan"):
    subjects = [s.strip() for s in subjects_text.splitlines() if s.strip()]

    if not subjects:
        st.error("Please enter at least one subject.")
    else:
        days_left = (exam_date - today).days
        if days_left <= 0:
            st.error("Exam date must be in the future.")
        else:
            st.success(f"Days left: {days_left}")

            n_subj = len(subjects)
            total_hours = days_left * hours_per_day
            hours_per_subject = total_hours / n_subj

            # Summary per subject
            summary_rows = []
            for s in subjects:
                summary_rows.append({
                    "Subject": s,
                    "Total Hours (recommended)": round(hours_per_subject, 1),
                })
            summary_df = pd.DataFrame(summary_rows)

            st.subheader("📊 Recommended hours per subject")
            st.dataframe(summary_df, use_container_width=True)

            # Daily plan: rotate subjects each day
            plan_rows = []
            for i in range(days_left):
                day_date = today + timedelta(days=i + 1)
                subject_of_day = subjects[i % n_subj]
                plan_rows.append({
                    "Date": day_date.isoformat(),
                    "Main Subject": subject_of_day,
                    "Study Hours": hours_per_day
                })

            plan_df = pd.DataFrame(plan_rows)

            st.subheader("📅 Day-wise Study Plan")
            st.dataframe(plan_df, use_container_width=True)

            st.download_button(
                "⬇ Download plan as CSV",
                data=plan_df.to_csv(index=False),
                file_name="study_plan.csv",
                mime="text/csv"
            )

st.markdown("---")
st.info(
    "Tip: Change the exam date, daily hours, or subjects and click "
    "**Generate Study Plan** again to experiment with different schedules."
)
