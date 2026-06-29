import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from io import StringIO

st.set_page_config(page_title="Student Management System", page_icon="🎓", layout="wide")

# ---------- DATABASE SETUP ----------
conn = sqlite3.connect("students.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    course TEXT
)
""")
conn.commit()

st.title("🎓 Student Management System")

# ---------- KPI CARDS (always visible) ----------
cursor.execute("SELECT * FROM students")
all_rows = cursor.fetchall()
all_df = pd.DataFrame(all_rows, columns=["ID", "Name", "Age", "Course"])

c1, c2, c3 = st.columns(3)
c1.metric("Total Students", len(all_df))
c2.metric("Total Courses", all_df["Course"].nunique() if not all_df.empty else 0)
c3.metric("Average Age", f"{all_df['Age'].mean():.1f}" if not all_df.empty else "—")

st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "➕ Add Student", "📋 View / Search", "✏️ Update", "🗑️ Delete", "📊 Insights & Import/Export"
])

# ---------- TAB 1: ADD ----------
with tab1:
    st.subheader("Add a New Student")

    with st.form("add_form", clear_on_submit=True):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=120, step=1)
        course = st.text_input("Course")
        submitted = st.form_submit_button("Add Student")

        if submitted:
            if name.strip() == "":
                st.error("❌ Name cannot be empty.")
            elif course.strip() == "":
                st.error("❌ Course cannot be empty.")
            else:
                # Duplicate check
                cursor.execute(
                    "SELECT * FROM students WHERE name = ? AND course = ?",
                    (name.strip(), course.strip())
                )
                if cursor.fetchone():
                    st.warning(f"⚠️ {name} is already enrolled in {course}. Added anyway as a new record.")

                cursor.execute(
                    "INSERT INTO students(name, age, course) VALUES (?, ?, ?)",
                    (name.strip(), int(age), course.strip())
                )
                conn.commit()
                st.success(f"✅ {name} added successfully.")
                st.rerun()

# ---------- TAB 2: VIEW / SEARCH ----------
with tab2:
    st.subheader("All Students")

    col1, col2, col3 = st.columns(3)
    with col1:
        search_name = st.text_input("Search by name")
    with col2:
        course_options = ["All"] + sorted(all_df["Course"].unique().tolist()) if not all_df.empty else ["All"]
        course_filter = st.selectbox("Filter by course", course_options)
    with col3:
        sort_by = st.selectbox("Sort by", ["ID", "Name", "Age", "Course"])

    query = "SELECT * FROM students WHERE 1=1"
    params = []

    if search_name.strip():
        query += " AND name LIKE ?"
        params.append(f"%{search_name.strip()}%")

    if course_filter != "All":
        query += " AND course = ?"
        params.append(course_filter)

    query += f" ORDER BY {sort_by}"

    cursor.execute(query, params)
    rows = cursor.fetchall()

    if not rows:
        st.info("No records found.")
    else:
        df = pd.DataFrame(rows, columns=["ID", "Name", "Age", "Course"])
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption(f"{len(df)} student(s) found")

# ---------- TAB 3: UPDATE ----------
with tab3:
    st.subheader("Update a Student Record")

    cursor.execute("SELECT id, name FROM students")
    all_students = cursor.fetchall()

    if not all_students:
        st.info("No students to update yet.")
    else:
        options = {f"{s[0]} - {s[1]}": s[0] for s in all_students}
        selected = st.selectbox("Select student", list(options.keys()))
        student_id = options[selected]

        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        current = cursor.fetchone()

        with st.form("update_form"):
            new_name = st.text_input("Name", value=current[1])
            new_age = st.number_input("Age", min_value=1, max_value=120, step=1, value=current[2])
            new_course = st.text_input("Course", value=current[3])
            update_btn = st.form_submit_button("Update Student")

            if update_btn:
                cursor.execute(
                    "UPDATE students SET name = ?, age = ?, course = ? WHERE id = ?",
                    (new_name.strip(), int(new_age), new_course.strip(), student_id)
                )
                conn.commit()
                st.success("✅ Student updated.")
                st.rerun()

# ---------- TAB 4: DELETE ----------
with tab4:
    st.subheader("Delete a Student Record")

    cursor.execute("SELECT id, name FROM students")
    all_students = cursor.fetchall()

    if not all_students:
        st.info("No students to delete.")
    else:
        options = {f"{s[0]} - {s[1]}": s[0] for s in all_students}
        selected = st.selectbox("Select student to delete", list(options.keys()), key="delete_select")
        student_id = options[selected]

        st.warning(f"This will permanently delete: **{selected}**")
        if st.button("🗑️ Confirm Delete"):
            cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
            conn.commit()
            st.success("✅ Student deleted.")
            st.rerun()

# ---------- TAB 5: INSIGHTS + IMPORT/EXPORT ----------
with tab5:
    st.subheader("Course Distribution")

    if all_df.empty:
        st.info("No data yet to visualize.")
    else:
        course_counts = all_df["Course"].value_counts().reset_index()
        course_counts.columns = ["Course", "Students"]
        fig = px.bar(course_counts, x="Course", y="Students", title="Students per Course", text="Students")
        st.plotly_chart(fig, use_container_width=True)

        age_fig = px.histogram(all_df, x="Age", nbins=10, title="Age Distribution")
        st.plotly_chart(age_fig, use_container_width=True)

    st.divider()
    st.subheader("Export Data")

    if not all_df.empty:
        csv = all_df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download All Students as CSV", csv, "students.csv", "text/csv")
    else:
        st.caption("No data to export yet.")

    st.divider()
    st.subheader("Bulk Import from CSV")
    st.caption("CSV must have columns: name, age, course")

    uploaded_csv = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_csv is not None:
        try:
            import_df = pd.read_csv(uploaded_csv)
            required_cols = {"name", "age", "course"}

            if not required_cols.issubset(set(import_df.columns.str.lower())):
                st.error("❌ CSV must contain columns: name, age, course")
            else:
                import_df.columns = import_df.columns.str.lower()
                st.dataframe(import_df.head(), use_container_width=True)

                if st.button("✅ Confirm Import"):
                    count = 0
                    for _, row in import_df.iterrows():
                        if pd.notna(row["name"]) and pd.notna(row["age"]) and pd.notna(row["course"]):
                            cursor.execute(
                                "INSERT INTO students(name, age, course) VALUES (?, ?, ?)",
                                (str(row["name"]).strip(), int(row["age"]), str(row["course"]).strip())
                            )
                            count += 1
                    conn.commit()
                    st.success(f"✅ Imported {count} student(s) successfully.")
                    st.rerun()
        except Exception as e:
            st.error(f"❌ Error reading CSV: {e}")