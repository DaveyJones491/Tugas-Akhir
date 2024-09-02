from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import event
from werkzeug.security import generate_password_hash
from datetime import datetime

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    #class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    type = db.Column(db.String(150))
    notes = db.relationship('Note')
    results = db.relationship('Result')
    useranswer = db.relationship('UserAnswer')

class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    name = db.Column(db.String(150))
    start_time = db.Column(db.DateTime(timezone=True))
    end_time = db.Column(db.DateTime(timezone=True))
    token = db.Column(db.String(15), unique=True)
    results = db.relationship('Result')
    questions = db.relationship('Question')
    useranswer = db.relationship('UserAnswer')
    
#Make inaccessible outside of time, use token?

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_name = db.Column(db.String(150))
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'))
    exam_name = db.Column(db.String(150))
    grade = db.Column(db.Float)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'))
    question = db.Column(db.String(1000))
    answer1 = db.Column(db.String(150))
    answer2 = db.Column(db.String(150))
    answer3 = db.Column(db.String(150))
    answer4 = db.Column(db.String(150))
    correct = db.Column(db.String(1))
    useranswer = db.relationship('UserAnswer')

class UserAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    answer = db.Column(db.String(1))

@event.listens_for(User.__table__, 'after_create')
def create_user(*args, **kwargs):
    db.session.add(User(email='testadmin@gmail', name='testadmin', password=generate_password_hash('testadmin'), type='admin'))
    db.session.add(User(email='testuser@gmail', name='testuser', password=generate_password_hash('testuser'), type='user'))
    db.session.add(User(email='testuser2@gmail', name='testuser2', password=generate_password_hash('testuser2'), type='user'))
    db.session.add(User(email='testuser3@gmail', name='testuser3', password=generate_password_hash('testuser3'), type='user'))
    db.session.commit()

@event.listens_for(Exam.__table__, 'after_create')
def create_user(*args, **kwargs):    
    db.session.add(Exam(name='Matematika', start_time=datetime(2023, 12, 20, 13, 30, 0), end_time=datetime(2024, 12, 20, 13, 30, 0), token=12345))
    db.session.add(Exam(name='Matematika 2', start_time=datetime(2023, 12, 21, 13, 30, 0), end_time=datetime(2024, 12, 21, 13, 30, 0), token=1234512345))
    db.session.add(Exam(name='Fisika', start_time=datetime(2023, 12, 21, 13, 30, 0), end_time=datetime(2024, 12, 21, 13, 30, 0), token=123456))
    db.session.add(Exam(name='Kimia', start_time=datetime(2023, 12, 22, 13, 30, 0), end_time=datetime(2024, 12, 22, 13, 30, 0), token=1234567))
    db.session.add(Exam(name='Biologi', start_time=datetime(2023, 12, 23, 13, 30, 0), end_time=datetime(2024, 12, 23, 13, 30, 0), token=12345678))
    db.session.commit()
    
@event.listens_for(Question.__table__, 'after_create')
def create_user(*args, **kwargs):    
    for i in range(1,21):
        db.session.add(Question(exam_id=1, question=(str(i)+' + '+str(i)+' = '), answer1=str(i), answer2=str(i*2), answer3=str(i*3), answer4=str(i*4), correct='B'))
    for i in range(1,51):
        db.session.add(Question(exam_id=2, question=(str(i)+' + '+str(i)+' = '), answer1=str(i), answer2=str(i*2), answer3=str(i*3), answer4=str(i*4), correct='B'))
    db.session.add(Question(exam_id=3, question='Jika es dipanaskan maka es akan', answer1='menyublim', answer2='menguap', answer3='mencair', answer4='membeku', correct='C'))
    db.session.add(Question(exam_id=4, question='Asam Hidroksida merupakan', answer1='Air', answer2='Api', answer3='Tanah', answer4='Udara', correct='A'))
    db.session.add(Question(exam_id=5, question='Berapa pasang kromosom yang dimiliki manusia', answer1='22', answer2='23', answer3='24', answer4='25', correct='B'))
    db.session.commit()    
    
'''
class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    users = db.relationship('User')
    exam = db.relationship('Exam')
'''