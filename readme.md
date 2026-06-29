# 🎓 Student Management System

A CRUD-based student record management app, originally built as a Python CLI tool with SQLite, later rebuilt as an interactive Streamlit web app with added analytics and bulk data tools.

🔗 **Live Demo:** [add your Streamlit Cloud link here]
💻 **Source:** https://github.com/adityagahlan-lab/student-management-system

---

## 📌 Overview

This started as my first programming project — a command-line student database using Python and SQLite. I rebuilt it as a web app to practice translating CLI logic into a UI, and extended it with search/filtering, data visualization, and CSV import/export.

---

## ⚙️ Features

- **Add Student** — form-based entry with validation (empty name check, numeric age check, duplicate detection)
- **View / Search** — searchable, filterable, sortable table of all students (by name, course, or column)
- **Update** — select a student from a dropdown and edit their details
- **Delete** — select and remove a student record with a confirmation step
- **Insights Dashboard** — bar chart of students per course, histogram of age distribution, live KPI cards (total students, total courses, average age)
- **CSV Export** — download all student records as a CSV file
- **CSV Bulk Import** — upload a CSV to add multiple students at once, with column validation and a preview before confirming

---

## 🧠 Evolution of the Project

| Version | What it was |
|---|---|
| v1 | Python CLI app — `input()`/`print()` menu, SQLite backend, basic CRUD |
| v2 | Rebuilt as a Streamlit web app — same SQLite logic, replaced CLI prompts with forms, dropdowns, and tables |
| v3 | Added KPI cards, course/age visualizations (Plotly), CSV export, and CSV bulk import with validation |

This progression itself is a good example of revisiting and improving an existing project rather than abandoning it after the first version — same database logic throughout, just better interfaces and more functionality layered on top.

---

## 🛠️ Tech Stack

- **Python** — core logic
- **SQLite** — persistent local database
- **Streamlit** — web UI
- **Pandas** — data handling for tables/CSV import-export
- **Plotly** — charts (course distribution, age histogram)

---

## 📁 Project Structure
student-management-system/

├── main.py            # Streamlit app — all tabs and logic

├── students.db        # SQLite database (auto-created on first run)

├── requirements.txt

└── README.md

---

## 🚀 Running Locally

```bash
git clone <your-repo-url>
cd student-management-system
pip install -r requirements.txt
streamlit run main.py
```

---

## 🔮 Future Improvements

- Add authentication so only admins can edit/delete records
- Add attendance or grades as a related table (relational DB practice)
- Add data validation rules (e.g. prevent exact duplicate name+course entries instead of just warning)
- Pagination for large student lists

---

## 👤 Author

Aditya Gahlan
