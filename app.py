import json
import secrets
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for


app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

DATA_FILE = Path(__file__).with_name("students.json")

SUBJECTS = [
    "Data Structure",
    "AI",
    "OOPM",
    "Introduction to Probability",
    "Technical Communication",
]

BRANCH_OPTIONS = [
    "Computer Science and Engineering (CSE)",
    "Information Technology (IT)",
    "Artificial Intelligence and Data Science (AI&DS)",
    "Electronics and Communication Engineering (ECE)",
    "Electrical and Electronics Engineering (EEE)",
    "Mechanical Engineering",
    "Civil Engineering",
]

MST1_PASS_MARK = 9
MST2_PASS_MARK = 15


def load_students():
    if not DATA_FILE.exists():
        return {}

    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_students(students):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(students, file, indent=4, ensure_ascii=False)


def read_marks(form, prefix, maximum):
    marks = {}

    for index, subject in enumerate(SUBJECTS):
        raw_value = form.get(f"{prefix}_{index}", "").strip()

        try:
            mark = int(raw_value)
        except ValueError:
            return None, f"Enter a whole number for {subject}."

        if not 0 <= mark <= maximum:
            return None, (
                f"Invalid input for {subject}. "
                f"Enter a mark from 0 to {maximum}."
            )

        marks[subject] = mark

    return marks, None


@app.get("/")
def index():
    students = load_students()

    return render_template(
        "index.html",
        students=students,
        subjects=SUBJECTS,
        branches=BRANCH_OPTIONS,
        mst1_pass_mark=MST1_PASS_MARK,
        mst2_pass_mark=MST2_PASS_MARK,
    )


@app.post("/students")
def add_student():
    enrollment = request.form.get("enrollment", "").strip()
    name = request.form.get("name", "").strip()
    branch = request.form.get("branch", "").strip()

    if branch == "Other":
        branch = request.form.get("branch_other", "").strip()

    semester = request.form.get("semester", "").strip()
    year = request.form.get("year", "").strip()
    degree = request.form.get("degree", "").strip()

    if not all((enrollment, name, branch, semester, year, degree)):
        flash("Please complete all student information fields.", "error")
        return redirect(url_for("index"))

    students = load_students()

    if enrollment in students:
        flash("That enrollment number already exists.", "error")
        return redirect(url_for("index"))

    students[enrollment] = {
        "name": name,
        "branch": branch,
        "semester": semester,
        "year": year,
        "degree": degree,
        "marks": {
            subject: {"mst1": None, "mst2": None}
            for subject in SUBJECTS
        },
    }

    save_students(students)
    flash(f"Student information saved for {name}.", "success")
    return redirect(url_for("index"))


@app.post("/students/<enrollment>/mst1")
def save_mst1(enrollment):
    students = load_students()
    student = students.get(enrollment)

    if student is None:
        flash("Student not found.", "error")
        return redirect(url_for("index"))

    marks, error = read_marks(request.form, "mst1", 20)

    if error:
        flash(error, "error")
        return redirect(url_for("index"))

    for subject, mark in marks.items():
        student["marks"][subject]["mst1"] = mark

    save_students(students)
    flash(f"MST 1 marks saved for {student['name']}.", "success")
    return redirect(url_for("index"))


@app.post("/students/<enrollment>/mst2")
def save_mst2(enrollment):
    students = load_students()
    student = students.get(enrollment)

    if student is None:
        flash("Student not found.", "error")
        return redirect(url_for("index"))

    if any(
        student["marks"][subject]["mst1"] is None
        for subject in SUBJECTS
    ):
        flash(
            "Enter all MST 1 marks before entering MST 2 marks.",
            "error",
        )
        return redirect(url_for("index"))

    marks, error = read_marks(request.form, "mst2", 30)

    if error:
        flash(error, "error")
        return redirect(url_for("index"))

    for subject, mark in marks.items():
        student["marks"][subject]["mst2"] = mark

    save_students(students)
    flash(f"MST 2 marks saved for {student['name']}.", "success")
    return redirect(url_for("index"))


@app.post("/students/<enrollment>/delete")
def delete_student(enrollment):
    students = load_students()

    if enrollment not in students:
        flash("Student not found.", "error")
    else:
        name = students[enrollment]["name"]
        del students[enrollment]
        save_students(students)
        flash(f"Deleted student record for {name}.", "success")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=False)