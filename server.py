from flask import Flask
from flask import render_template, redirect, request, flash, session, url_for
import os, pathlib
from utils import constants 

# Models
from models.shared import db

# Routes
from user_management import LoginUser, RegisterUser, LogoutUser, AuthorizeUser, GetUser, TeacherDashboard, StudentDashboard
from check_assigment import CheckAPI
from classroom_management import ClassroomCreate, ClassroomMain, ClassroomAddStudent, ClassroomDelete, ClassroomRemoveStudent
from classroom_management import AssignmentCreate, AssignmentMain, AssignmentEdit, AssignmentDelete
from classroom_management import SubmissionDownload, SubmissionDownloadAll, SubmissionDownloadResults

app = Flask(__name__)
app.secret_key = "zHxIwnkAAN"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db" #pathlib.Path(os.path.abspath("data.db")).as_uri()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

SUBMISSION_FOLDER = constants.SUBMISSION_FOLDER
# print(os.path.exists(f"{SUBMISSION_FOLDER}"), os.listdir("res"))
if not os.path.exists(f"{SUBMISSION_FOLDER}"):
    os.mkdir(SUBMISSION_FOLDER)

db.init_app(app)
# with app.app_context():
#     # from models.submission import Submission
#     # Submission.__table__.drop(db.engine)
#     db.drop_all()
#     db.create_all() 


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    return LoginUser()

@app.route("/register", methods=["GET", "POST"])
def register():
    return RegisterUser()

@app.route("/logout", methods=["GET", "POST"])
def logout():
    return LogoutUser()

# @app.route("/clean", methods=["GET"])
# def clean():
#     for key in list(session.keys()):
#         del session[key]
#     return render_template("home.html")

@app.route("/api/check", methods=["POST"])
def check_api():
    return CheckAPI()

# Student
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    isAuthorized = AuthorizeUser("student")
    if isAuthorized:
        if request.method == "GET":
            return StudentDashboard()
        elif request.method == "POST":
            return ClassroomAddStudent()
    
    isAuthorized = AuthorizeUser("teacher")
    if isAuthorized:
        return TeacherDashboard()
    
    flash("Unauthorized! Please login first!", "warning")
    return redirect(url_for("home"))
    

@app.route("/classroom/create", methods=["GET", "POST"])
def classroom_create():
    isAuthorized = AuthorizeUser("teacher")
    if not isAuthorized:
        return redirect(url_for("home"))
    return ClassroomCreate()

@app.route("/classroom/<class_code>", methods=["GET", "POST"])
def classroom_main(class_code):
    isAuthorized = AuthorizeUser()
    if not isAuthorized:
        return redirect(url_for("home"))
    return ClassroomMain(class_code)

@app.route("/classroom/<class_code>/remove/<student_id>", methods=["GET"])
def classroom_remove_student(class_code, student_id):
    isAuthorized = AuthorizeUser()
    if not isAuthorized:
        return redirect(url_for("home"))
    ClassroomRemoveStudent(class_code, student_id)
    return redirect(url_for("classroom_main", class_code=class_code))

@app.route("/classroom/<class_code>/delete", methods=["GET"])
def classroom_delete(class_code):
    isAuthorized = AuthorizeUser()
    if not isAuthorized:
        return redirect(url_for("home"))
    return ClassroomDelete(class_code)

@app.route("/classroom/<class_code>/assignment/create", methods=["GET", "POST"])
def assignment_create(class_code):
    isAuthorized = AuthorizeUser("teacher")
    if not isAuthorized:
        return redirect(url_for("home"))
    return AssignmentCreate(class_code)

@app.route("/assignment/<assignment_code>", methods=["GET", "POST"])
def assignment_main(assignment_code):
    isAuthorized = AuthorizeUser()
    if not isAuthorized:
        return redirect(url_for("home"))
    return AssignmentMain(assignment_code)

@app.route("/assignment/<assignment_code>/edit", methods=["GET", "POST"])
def assignment_edit(assignment_code):
    isAuthorized = AuthorizeUser("teacher")
    if not isAuthorized:
        return redirect(url_for("home"))
    return AssignmentEdit(assignment_code)

@app.route("/assignment/<assignment_code>/delete", methods=["GET", "POST"])
def assignment_delete(assignment_code):
    isAuthorized = AuthorizeUser("teacher")
    if not isAuthorized:
        return redirect(url_for("home"))
    return AssignmentDelete(assignment_code)

@app.route("/submission/download/<assignment_code>/<file_name>", methods=["GET"])
def submission_download(assignment_code, file_name):
    isAuthorized = AuthorizeUser("teacher")
    if not isAuthorized:
        return redirect(url_for("home"))
    return SubmissionDownload(assignment_code, file_name)

@app.route("/submission/download/<assignment_code>/all", methods=["GET"])
def submission_download_all(assignment_code):
    isAuthorized = AuthorizeUser("teacher")
    if not isAuthorized:
        return redirect(url_for("home"))
    return SubmissionDownloadAll(assignment_code)

@app.route("/submission/download/<assignment_code>/results", methods=["GET"])
def submission_download_results(assignment_code):
    isAuthorized = AuthorizeUser("teacher")
    if not isAuthorized:
        return redirect(url_for("home"))
    return SubmissionDownloadResults(assignment_code, request.host_url)

if __name__ == "__main__":
    client_app = app
    app.run(debug=True)