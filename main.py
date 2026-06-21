import sqlite3

# Connect to database
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    course TEXT
)
""")

conn.commit()


def add_student():

    name = input("Enter student name: ").strip()

    if name == "":
        print("❌ Name cannot be empty.\n")
        return

    try:
        age = int(input("Enter age: "))

    except ValueError:
        print("❌ Age must be a number.\n")
        return

    course = input("Enter course: ").strip()

    cursor.execute(
        """
        INSERT INTO students(name, age, course)
        VALUES (?, ?, ?)
        """,
        (name, age, course)
    )

    conn.commit()

    print("✅ Student added successfully.\n")


def view_students():

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    if not students:

        print("No records found.\n")

        return

    print("\n----- Student Records -----")

    for student in students:

        print(
            f"ID: {student[0]} | "
            f"Name: {student[1]} | "
            f"Age: {student[2]} | "
            f"Course: {student[3]}"
        )

    print()


def search_by_id():

    try:

        student_id = int(input("Enter student ID: "))

    except ValueError:

        print("❌ Invalid ID.\n")

        return

    cursor.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    )

    student = cursor.fetchone()

    if student:

        print("\nStudent Found")

        print(
            f"ID: {student[0]}\n"
            f"Name: {student[1]}\n"
            f"Age: {student[2]}\n"
            f"Course: {student[3]}\n"
        )

    else:

        print("Student not found.\n")


def search_by_name():

    name = input("Enter student name: ").strip()

    cursor.execute(
        """
        SELECT * FROM students
        WHERE name LIKE ?
        """,
        (f"%{name}%",)
    )

    students = cursor.fetchall()

    if not students:

        print("Student not found.\n")

        return

    print("\nResults:\n")

    for student in students:

        print(
            f"ID: {student[0]} | "
            f"Name: {student[1]} | "
            f"Age: {student[2]} | "
            f"Course: {student[3]}"
        )

    print()


def update_student():

    try:

        student_id = int(input("Enter student ID: "))

    except ValueError:

        print("❌ Invalid ID.\n")

        return

    name = input("Enter new name: ").strip()

    try:

        age = int(input("Enter new age: "))

    except ValueError:

        print("❌ Invalid age.\n")

        return

    course = input("Enter new course: ").strip()

    cursor.execute(
        """
        UPDATE students
        SET name = ?, age = ?, course = ?
        WHERE id = ?
        """,
        (name, age, course, student_id)
    )

    conn.commit()

    if cursor.rowcount:

        print("✅ Student updated.\n")

    else:

        print("Student not found.\n")


def delete_student():

    try:

        student_id = int(input("Enter student ID: "))

    except ValueError:

        print("❌ Invalid ID.\n")

        return

    cursor.execute(
        """
        DELETE FROM students
        WHERE id = ?
        """,
        (student_id,)
    )

    conn.commit()

    if cursor.rowcount:

        print("✅ Student deleted.\n")

    else:

        print("Student not found.\n")


while True:

    print("===== STUDENT MANAGEMENT SYSTEM =====")

    print("1. Add Student")

    print("2. View Students")

    print("3. Search by ID")

    print("4. Search by Name")

    print("5. Update Student")

    print("6. Delete Student")

    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":

        add_student()

    elif choice == "2":

        view_students()

    elif choice == "3":

        search_by_id()

    elif choice == "4":

        search_by_name()

    elif choice == "5":

        update_student()

    elif choice == "6":

        delete_student()

    elif choice == "7":

        print("Goodbye!")

        break

    else:

        print("❌ Invalid choice.\n")


conn.close()