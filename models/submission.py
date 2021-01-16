import os
from random import choices
from string import ascii_letters

from models.shared import db

SUBMISSION_CODE_LENGTH = 6

class Submission(db.Model):
    __tablename__ = "submission"
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(80), nullable=False, unique=True)
    result = db.Column(db.String(20), nullable=True)
    language = db.Column(db.String(20), nullable=False)

    assignment_id = db.Column(db.Integer, db.ForeignKey("assignment.id"))
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"))

    def __init__(self, file_name, assignment, language, result, student):
        self.file_name = file_name
        self.assignment = assignment
        self.student = student
        self.language = language
        self.result = result
    
    # def generate_assignment_code(self):
    #     code = "".join(choices(ascii_letters, k=SUBMISSION_CODE_LENGTH))
    #     while True:
    #         if Assignment.query.filter_by(code=code).first() == None:
    #             break
    #         code = "".join(choices(ascii_letters, k=SUBMISSION_CODE_LENGTH))
    #     return code
    
    def update(self, **kwargs):
        for key in kwargs.keys():
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
    
    def delete(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)