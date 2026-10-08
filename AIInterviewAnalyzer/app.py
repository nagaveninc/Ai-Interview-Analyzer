from flask import Flask, render_template, request, redirect, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from config import db, cursor
from models.resume_analyzer import ResumeAnalyzer
from models.report_generator import ReportGenerator
import os

app = Flask(__name__)
app.secret_key = "AIInterviewAnalyzer2026"
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")

# ---------------- SIGNUP ----------------

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]

        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            flash("Email already exists!")
            return redirect("/signup")

        hashed_password = generate_password_hash(password)

        cursor.execute(
            """
            INSERT INTO users(fullname, email, phone, password)
            VALUES(%s, %s, %s, %s)
            """,
            (fullname, email, phone, hashed_password)
        )

        db.commit()

        flash("Account created successfully!")

        return redirect("/login")

    return render_template("signup.html")

# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        user = cursor.fetchone()

        if user and check_password_hash(user["password"], password):

            session["user_id"] = user["id"]
            session["user_name"] = user["fullname"]

            return redirect("/dashboard")

        flash("Invalid Email or Password")

    return render_template("login.html")


# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        username=session["user_name"]
    )


# ---------------- INTERVIEW ----------------

@app.route("/interview")
def interview():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "interview.html",
        username=session["user_name"]
    )

# ---------------- SAVE ANSWER ----------------

@app.route("/save_answer", methods=["POST"])
def save_answer():

    if "user_id" not in session:
        return jsonify({"status": "error"})

    question = request.form["question"]
    answer = request.form["answer"]

    cursor.execute(
        """
        INSERT INTO interview_answers(user_id, question, answer)
        VALUES(%s,%s,%s)
        """,
        (
            session["user_id"],
            question,
            answer
        )
    )

    db.commit()

    return jsonify({"status": "success"})
# ---------------- REPORT ----------------

@app.route("/report")
def report():

    if "user_id" not in session:
        return redirect("/login")

    cursor.execute("""
        SELECT question, answer
        FROM interview_answers
        WHERE user_id=%s
        ORDER BY id ASC
    """, (session["user_id"],))

    answers = cursor.fetchall()

    generator = ReportGenerator()

    report_data = generator.generate_report(answers)

    return render_template(
        "report.html",
        username=session["user_name"],
        results=report_data["results"],
        overall_score=report_data["overall_score"],
        overall_grade=report_data["overall_grade"]
    )
# ---------------- RESUME ----------------

@app.route("/upload_resume", methods=["POST"])
def upload_resume():

    if "user_id" not in session:
        return redirect("/login")

    if "resume" not in request.files:
        flash("Please select a resume.")
        return redirect("/resume")

    file = request.files["resume"]

    if file.filename == "":
        flash("Please choose a file.")
        return redirect("/resume")

    filename = secure_filename(file.filename)

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    file.save(filepath)

    cursor.execute(
        "UPDATE users SET resume=%s WHERE id=%s",
        (filename, session["user_id"])
    )

    db.commit()

    analyzer = ResumeAnalyzer()

    result = analyzer.analyze(filepath)

    return render_template(
        "resume_result.html",
        ats_score=result["ats_score"],
        skills=result["skills"],
        suggestions=result["suggestions"]
    )
# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")
# ---------------- RESUME ----------------

@app.route("/resume")
def resume():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("resume.html")

# ---------------- RUN APP ----------------

if __name__ == "__main__":
    app.run(debug=True)