from flask import Flask, render_template, request, redirect, url_for
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

FILE_NAME = "students.csv"

# Create CSV file if not exists
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Roll", "Name", "Maths", "Science", "English", "Total", "Percentage", "Grade"])


def calculate_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 75:
        return "A"
    elif percentage >= 60:
        return "B"
    elif percentage >= 50:
        return "C"
    else:
        return "Fail"


@app.route("/")
def index():
    students = []
    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            students.append(row)
    return render_template("index.html", students=students)


@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        roll = request.form["roll"]
        name = request.form["name"]
        maths = int(request.form["maths"])
        science = int(request.form["science"])
        english = int(request.form["english"])

        total = maths + science + english
        percentage = round(total / 3, 2)
        grade = calculate_grade(percentage)

        with open(FILE_NAME, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([roll, name, maths, science, english, total, percentage, grade])

        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/delete/<roll>")
def delete_student(roll):
    rows = []
    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] != roll:
                rows.append(row)

    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    return redirect(url_for("index"))


@app.route("/graph")
def graph():
    df = pd.read_csv(FILE_NAME)

    if not df.empty:
        plt.figure()
        plt.bar(df["Name"], df["Percentage"])
        plt.xticks(rotation=45)
        plt.title("Class Performance")
        plt.xlabel("Students")
        plt.ylabel("Percentage")
        plt.tight_layout()
        plt.savefig("static/graph.png")
        plt.close()

    return render_template("graph.html")


if __name__ == "__main__":
    app.run(debug=True)
