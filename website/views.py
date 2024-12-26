from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import login_required, current_user
from .models import User, Note, Exam, Result, Question, UserAnswer#, Class
from . import db
import json
from datetime import datetime
from werkzeug.security import generate_password_hash

import base64
import time
from typing import Optional

import os
import requests

import pyaudio
import wave

from playsound import playsound

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')

        if len(note) < 1:
            flash('Catatan terlalu pendek!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Catatan berhasil ditambah!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

#=====================================Account/User========================================

@views.route('/list_account/<page>', methods=['GET','POST'])
@login_required
def list_acccount(page):
    if current_user.type != 'admin':
        return redirect("/")
    else:
        db_user = User.query.paginate(page=int(page), per_page=10)
        return render_template("list_account.html", user=current_user, db_user=db_user)

@views.route('/add_account', methods=['GET', 'POST'])
@login_required
def add_account():
    if current_user.type != 'admin':
        return redirect("/")
    else:
        if request.method == 'POST':
            email = request.form.get('email')
            name = request.form.get('name')
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')
            type = request.form.get('type')

            user = User.query.filter_by(email=email).first()
            if user:
                flash('Email sudah ada, pilih yang lain.', category='error')
            elif len(email) < 4:
                flash('Email harus lebih panjang dari 3 karakter!', category='error')
            elif len(name) < 2:
                flash('Nama harus lebih panjang dari 1 karakter!', category='error')
            elif password1 != password2:
                flash('Password tidak sama.', category='error')
            elif len(password1) < 7:
                flash('Password harus lebih panjang dari 6 karakter!', category='error')
            else:
                new_user = User(email=email, name=name, password=generate_password_hash(password1), type=type)
                db.session.add(new_user)
                db.session.commit()
                flash('Akun berhasil ditambah!', category='success')

        return render_template("add_account.html", user=current_user)

@views.route('/edit_account/<id>', methods=['GET','POST'])
@login_required
def edit_account(id):
    if current_user.type != 'admin':
        return redirect("/")
    else:
        db_user = User.query.get(id)
        
        if request.method == 'POST':
            email = request.form.get('email')
            name = request.form.get('name')
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')
            type = request.form.get('type')
            
            db_email = User.query.filter_by(email=email).first()
            if db_email:
                flash('Email sudah ada, pilih yang lain.', category='error')
            elif len(email) < 4:
                flash('Email harus lebih panjang dari 3 karakter!', category='error')
            elif len(name) < 2:
                flash('Nama harus lebih panjang dari 1 karakter!', category='error')
            elif password1 != password2:
                flash('Password tidak sama.', category='error')
            elif len(password1) < 7:
                flash('Password harus lebih panjang dari 6 karakter!', category='error')
            else :
                db_user.email = email
                db_user.name = name
                db_user.password = generate_password_hash(password1)
                db_user.type = type
                db.session.commit()
                flash('Akun berhasil diedit!', category='success')
        
        return render_template("edit_account.html", user=current_user, edit_user=db_user)#, kelas=db_class)

@views.route('/delete_account/<userid>/<page>', methods=['GET', 'POST'])
@login_required
def delete_account(userid, page):  
    if current_user.type != 'admin':
        return redirect("/")
    else:
        user = User.query.get(userid)
        if user:
            db.session.delete(user)
            db.session.commit()
            flash('Akun berhasil dihapus!', category='success')
        return redirect("/list_account/"+str(page))

#===========================================Exam===========================================

@views.route('/list_exam/<page>', methods=['GET','POST'])
@login_required
def list_exam(page):
    if current_user.type != 'admin':
        return redirect("/")
    else:
        db_exam = Exam.query.paginate(page=int(page), per_page=10)
        return render_template("list_exam.html", user=current_user, exams=db_exam)#, kelas=db_class)

@views.route('/add_exam', methods=['GET','POST'])
@login_required
def add_exam():
    if current_user.type != 'admin':
        return redirect("/")
    else:
        if request.method == 'POST':
            name = request.form.get('name')
            start = request.form.get('start')
            end = request.form.get('end')
            token = request.form.get('token')
            #kelas = request.form.get('kelas')
            
            exam = Exam.query.filter_by(token=token).first()

            if exam:
                flash('Token sudah ada, pilih token lain!', category='error')
            elif len(name) < 1:
                flash('Nama ujian terlalu pendek!', category='error') 
            elif (start==''):
                flash('Tanggal mulai tidak boleh kosong!', category='error') 
            elif (end==''):
                flash('Tanggal selesai tidak boleh kosong!', category='error')
            elif len(token) < 5:
                flash('Token harus lebih panjang dari 4 angka!', category='error')
            else: 
                start=datetime.strptime(start, '%Y-%m-%dT%H:%M').replace(second=0, microsecond=0)
                end=datetime.strptime(end, '%Y-%m-%dT%H:%M').replace(second=0, microsecond=0)
                new_exam = Exam(name=name, start_time=start, end_time=end, token=token)#, class_id=kelas*#)
                db.session.add(new_exam)
                db.session.commit()
                flash('Exam added!', category='success')
        
        #db_class = Class.query.all()
        return render_template("add_exam.html", user=current_user)#, kelas=db_class)

@views.route('/edit_exam/<id>', methods=['GET','POST'])
@login_required
def edit_exam(id):
    if current_user.type != 'admin':
        return redirect("/")
    else:
        db_exam = Exam.query.get(id)
        
        if request.method == 'POST':
            name = request.form.get('name')
            start = request.form.get('start')
            end = request.form.get('end')
            token = request.form.get('token')

            db_token = Exam.query.filter_by(token=token).first()
            if db_token:
                flash('Token sudah ada, pilih token lain!', category='error')
            elif len(name) < 1:
                flash('Nama ujian terlalu pendek!', category='error') 
            elif (start==''):
                flash('Tanggal mulai tidak boleh kosong!', category='error') 
            elif (end==''):
                flash('Tanggal selesai tidak boleh kosong!', category='error')
            elif len(token) < 5:
                flash('Token harus lebih panjang dari 4 angka!', category='error')
            else: 
                start=datetime.strptime(start, '%Y-%m-%dT%H:%M').replace(second=0, microsecond=0)
                end=datetime.strptime(end, '%Y-%m-%dT%H:%M').replace(second=0, microsecond=0)
                
                db_exam.name = name
                db_exam.start_time = start
                db_exam.end_time = end
                db_exam.token = token
                db.session.commit()
                flash('Ujian berhasil diedit!', category='success')
        
        return render_template("edit_exam.html", user=current_user, exam=db_exam)#, kelas=db_class)   

@views.route('/delete_exam/<examid>/<page>', methods=['GET', 'POST'])
@login_required
def delete_exam(examid, page):  
    if current_user.type != 'admin':
        return redirect("/")
    else:
        exam = Exam.query.get(examid)
        if exam:
            db.session.delete(exam)
            db.session.commit()
            flash('Ujian berhasil dihapus!', category='success')
        return redirect("/list_exam/"+str(page))
        
#============================================Question=========================================

@views.route('/list_question/<id>/<page>', methods=['GET','POST'])
@login_required
def list_question(id,page):
    if current_user.type != 'admin':
        return redirect("/")
    else:
        db_question = Question.query.filter_by(exam_id=id).paginate(page=int(page), per_page=10)
        return render_template("list_question.html", user=current_user, questions=db_question, examid=id)#, kelas=db_class)

@views.route('/add_question/<id>', methods=['GET','POST'])
@login_required
def add_question(id):
    if current_user.type != 'admin':
        return redirect("/")
    else:
        if request.method == 'POST':
            question = request.form.get('question')
            answer1 = request.form.get('answer1')
            answer2 = request.form.get('answer2')
            answer3 = request.form.get('answer3')
            answer4 = request.form.get('answer4')
            correct = request.form.get('correct')

            if len(question) < 1:
                flash('Pertanyaan tidak boleh kosong!', category='error')
            elif len(answer1) < 1:
                flash('Jawaban tidak boleh kosong!', category='error')
            elif len(answer2) < 1:
                flash('Jawaban tidak boleh kosong!', category='error') 
            elif len(answer3) < 1:
                flash('Jawaban tidak boleh kosong!', category='error') 
            elif len(answer4) < 1:
                flash('Jawaban tidak boleh kosong!', category='error')
            elif correct == '':
                flash('Harus memilih kunci jawaban!', category='error') 
            else: 
                new_question = Question(exam_id=id, question=question, answer1=answer1, answer2=answer2, answer3=answer3, answer4=answer4, correct=correct)
                db.session.add(new_question)
                db.session.commit()
                flash('Pertanyaan berhasil ditambahkan!', category='success')
        
        return render_template("add_question.html", user=current_user, examid=id)

@views.route('/edit_question/<id>', methods=['GET', 'POST'])
@login_required
def edit_question(id):
    if current_user.type != 'admin':
        return redirect("/")
    else:
        db_question = Question.query.get(id)
        
        if request.method == 'POST':
            question = request.form.get('question')
            answer1 = request.form.get('answer1')
            answer2 = request.form.get('answer2')
            answer3 = request.form.get('answer3')
            answer4 = request.form.get('answer4')
            correct = request.form.get('correct')

            if len(question) < 1:
                flash('Pertanyaan tidak boleh kosong!', category='error')
            elif len(answer1) < 1:
                flash('Jawaban tidak boleh kosong!', category='error')
            elif len(answer2) < 1:
                flash('Jawaban tidak boleh kosong!', category='error') 
            elif len(answer3) < 1:
                flash('Jawaban tidak boleh kosong!', category='error') 
            elif len(answer4) < 1:
                flash('Jawaban tidak boleh kosong!', category='error')
            elif correct == '':
                flash('Harus memilih kunci jawaban!', category='error') 
            else: 
                db_question.question = question
                db_question.answer1 = answer1
                db_question.answer2 = answer2
                db_question.answer3 = answer3
                db_question.answer4 = answer4
                db.session.commit()
                flash('Pertanyaan berhasil diedit!', category='success')
        
        return render_template("edit_question.html", user=current_user, questions=db_question, examid=db_question.exam_id)#, kelas=db_class)   

@views.route('/delete_question/<questionid>/<examid>/<page>', methods=['GET', 'POST'])
@login_required
def delete_question(questionid, examid, page):  
    if current_user.type != 'admin':
        return redirect("/")
    else:
        question = Question.query.get(questionid)
        if question:
            db.session.delete(question)
            db.session.commit()
            flash('Pertanyaan berhasil dihapus!', category='success')
        return redirect("/list_question/"+str(examid)+"/"+str(page))

#==========================================Start Exam==================================================

@views.route('/insert_token', methods=['GET', 'POST'])
@login_required
def insert_token():
    if request.method == 'POST':
        token = request.form.get('token')
        db_exam = Exam.query.filter_by(token=token).first()
        
        if len(token) < 5:
            flash('Token harus lebih panjang dari 4 angka!', category='error')
        elif db_exam:
            return redirect(("/start_exam/")+str(token))
        else : 
            flash('Tidak ada ujian dengan token tersebut!', category='error') 
    
    return render_template("insert_token.html", user=current_user)
        
@views.route('/start_exam/<token>', methods=['GET', 'POST'])
@login_required
def start_exam(token):
    db_exam = Exam.query.filter_by(token=token).first()
    
    return render_template("start_exam.html", user=current_user, exams=db_exam)
    
@views.route('/exam/<token>/<page>', methods=['GET', 'POST'])
@login_required
def exam(token,page):
    db_exam = Exam.query.filter_by(token=token).first()
    
    check_result = Result.query.filter_by(user_id=current_user.id, exam_id=db_exam.id).first()
    if check_result:
        flash('Anda sudah pernah mengerjakan ujian tersebut!', category='error')
        return redirect("/insert_token")

    get_question = Question.query.filter_by(exam_id=db_exam.id)
    db_question = get_question.paginate(page=int(page), per_page=1)
    questionid = (get_question[(int(page)-1)]).id

    db_check = UserAnswer.query.filter_by(user_id=current_user.id, exam_id=db_exam.id).first()

    if db_check is None:
        fetch_question = Question.query.filter_by(exam_id=db_exam.id)
        for question in fetch_question :
            db.session.add(UserAnswer(user_id=current_user.id, exam_id=db_exam.id, question_id=question.id))
        db.session.commit()    

    if request.method == 'POST':
        examid = db_exam.id
        answer = request.form.get('answer')
        db_answer = UserAnswer.query.filter_by(user_id=current_user.id, exam_id=examid, question_id=questionid).first()
        
        if db_answer:
            db_answer.answer = answer
            db.session.commit()
            flash('Jawaban disimpan!', category='success')
    
    db_answer = UserAnswer.query.filter_by(user_id=current_user.id, exam_id=db_exam.id, question_id=questionid).first()
    if db_answer :
        db_answer = db_answer.answer
    
    return render_template("exam.html", user=current_user, questions=db_question, exams=db_exam, page=page, select=db_answer)#, kelas=db_class)

@views.route('/end_exam/<examid>', methods=['GET', 'POST'])
@login_required
def end_exam(examid):

    db_correct = Question.query.filter_by(exam_id=examid)
    db_answer = UserAnswer.query.filter_by(user_id=current_user.id, exam_id=examid)
    db_exam = Exam.query.filter_by(id=examid).first()
    count = db_correct.count()
    correct = 0

    for i in range (count) :
        if (db_correct[i].correct == db_answer[i].answer):
            correct += 1
    print(correct)
    db.session.add(Result(user_id=current_user.id, user_name=current_user.name, exam_id=examid, exam_name=db_exam.name, grade=(correct/count*100)))
    db.session.commit()
    flash('Ujian berhasil disubmit!', category='success')

    return redirect("/insert_token")

@views.route('/mark_answer/<userid>/<token>/<questionid>', methods=['GET', 'POST'])
@login_required
def mark_answer(token,page):
    
    return redirect("/exam/"+str(token)+"/"+str(page))

@views.route('/soal/<token>/<page>', methods=['GET', 'POST'])
@login_required
def soal(token,page):
    playsound(os.getcwd()+'/tts/soal_'+str(token)+'_'+str(page)+'.wav')

    return redirect("/exam/"+str(token)+"/"+str(page))

@views.route('/jawaban/<token>/<page>', methods=['GET', 'POST'])
@login_required
def jawaban(token,page):

    playsound(os.getcwd()+'/tts/jawaban_'+str(token)+'_'+str(page)+'.wav')

    return redirect("/exam/"+str(token)+"/"+str(page))

#=============================================Result=========================================================

@views.route('/list_result/<page>', methods=['GET','POST'])
@login_required
def list_result(page):

    db_result = Result.query.paginate(page=int(page), per_page=10)
    return render_template("list_result.html", user=current_user, results=db_result)

@views.route('/result/<page>', methods=['GET','POST'])
@login_required
def result(page):

    db_result = Result.query.filter_by(user_id=current_user.id).paginate(page=int(page), per_page=10)
    return render_template("result.html", user=current_user, results=db_result)

#==============================================TTS========================================================

@views.route('/generate_tts/<id>/<token>/<page>', methods=['GET','POST'])
@login_required
def generate_tts(id, token, page):
        
    url = "https://api.prosa.ai/v2/speech/tts"
    api_key = "eyJhbGciOiJSUzI1NiIsImtpZCI6Ik5XSTBNemRsTXprdE5tSmtNaTAwTTJZMkxXSTNaamN0T1dVMU5URmxObVF4Wm1KaSIsInR5cCI6IkpXVCJ9.eyJhcHBsaWNhdGlvbl9pZCI6NDEwMjk5LCJsaWNlbnNlX2tleSI6ImNjYmQxYjJhLTE1ODgtNDZlOS1iMTczLTkzYTNjZDJmYzZhZiIsInVuaXF1ZV9rZXkiOiI5MzA5M2Q4Ny0xM2JlLTRjNmYtODMyZi0zNjllM2MzOGVjZTIiLCJwcm9kdWN0X2lkIjozLCJhdWQiOiJhcGktc2VydmljZSIsInN1YiI6IjQ1NzgzYTYxLWM3NmYtNDVkMi1hOGNjLWMxNGVkMmNkZjg0YSIsImlzcyI6ImNvbnNvbGUiLCJpYXQiOjE3MzQwMTkzNzl9.SECwxHIVTeWfFGr3aUJcJ0Dk2yva33xZUdtukcn9OIk1VSueciWt6vFurLLfBQ3cgWV7aEREhxW1OHN-gxZ67vCUxNUuXX49tARNa3ZUIH_4F_l6gytD04hER_LWygtLW5zfM7q3GAQtvYd0fDWJYqX12aSuqmpur-ReWlhKvEmxMUG-xRntcH2DXvdYoDcRQAg6HiMYbBzRECvYXFNVmOChV5IZBqomJ8JjxOqbkAVfSxXGy9f8MZKoTOjkMGty_GcKb3DuC71cnmEbUdVtFP2MclK0ZWFGViu4ghRT3EhwfRZ4Npq4PcaMW7TnIkINBCLMPE10jUv6bCx3gKR90A"

    def submit_tts_request(text: str, audio_format: str) -> dict:
        payload = {
            "config": {
                "model": "tts-dimas-formal",
                "wait": False,  # Do not wait for the request to complete
                "audio_format": audio_format
            },
            "request": {
                "text": text
            }
        }

        response = requests.post(url, json=payload, headers={
            "x-api-key": api_key
        })

        return response.json()


    def query_tts_result(job_id: str) -> Optional[dict]:
        response = requests.get(url + "/" + job_id, headers={
            "x-api-key": api_key
        })

        if response.status_code == 200:
            job = response.json()

            status = job["status"]

            if status == "complete":
                result = job["result"]

                return result

        return None

    def tts(text: str, audio_format: str, poll_interval: float = 5.0) -> bytes:
        job = submit_tts_request(text, audio_format)

        job_id = job["job_id"]
        print(job_id)

        while True:
            result = query_tts_result(job_id)
            if result is not None:
                return base64.b64decode(result["data"])

            time.sleep(poll_interval)    
    
    db_question = Question.query.filter_by(exam_id=id)

    for i in range (db_question.count()) :

        soal_filename = "tts/soal_"+str(token)+"_"+str(i+1)+".wav"
        soal = (str("Soal Nomor "+str(i+1)+". "+db_question[i].question))
        jawaban_filename = "tts/jawaban_"+str(token)+"_"+str(i+1)+".wav"
        jawaban = ("A. "+str(db_question[i].answer1)+". "+"B. "+str(db_question[i].answer2)+". "+"C. "+str(db_question[i].answer3)+". "+"D. "+str(db_question[i].answer4)+". ")

        soal_data = tts(soal, "opus")

        with open(soal_filename, "wb") as f:
            f.write(soal_data)
        
        jawaban_data = tts(jawaban, "opus")

        with open(jawaban_filename, "wb") as f:
            f.write(jawaban_data)

    return redirect("/list_exam/"+str(page))

#============================================STT======================================================

@views.route('/stt/<token>/<page>/<questionid>', methods=['GET', 'POST'])
@login_required
def speech_to_text(token, page,questionid):
 
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 44100  # Record at 44100 samples per second
    seconds = 3
    input_device_index= 1
    filename = "output.wav"

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()


    url = "https://api.prosa.ai/v2/speech/stt"
    api_key = "eyJhbGciOiJSUzI1NiIsImtpZCI6Ik5XSTBNemRsTXprdE5tSmtNaTAwTTJZMkxXSTNaamN0T1dVMU5URmxObVF4Wm1KaSIsInR5cCI6IkpXVCJ9.eyJhcHBsaWNhdGlvbl9pZCI6NDEwMjk4LCJsaWNlbnNlX2tleSI6IjFkMzdjMzZjLTUxNTUtNDU3OS1iNzcyLTFkZmQ4YTQyYTdkYSIsInVuaXF1ZV9rZXkiOiIwM2IyZjRjNy1lOGEwLTRmNWQtYTc1OC0wNWRlNzAyMDZjYjgiLCJwcm9kdWN0X2lkIjo1LCJhdWQiOiJhcGktc2VydmljZSIsInN1YiI6IjQ1NzgzYTYxLWM3NmYtNDVkMi1hOGNjLWMxNGVkMmNkZjg0YSIsImlzcyI6ImNvbnNvbGUiLCJpYXQiOjE3MzQwMTkzNzN9.PQryj95twyxIEdmYSUBXk3y3D2TeRP70TifjkbvNdqVynFG-ZtuTJjPaKWi5wu_L9JwTWAFfd7enT10o1FANEGMZBT5MvrwnOImXSMmebM5U7nPtZ2p8YeeEGPxdk-5OfL4i_YHusJ9YmeKJ0H6QBZ6P8E-3EWr1bRwO03BAs07VpkxqIufPdLRGGZre3kJgoWxWYPb-73ti3zz7PCf6WTfOSP-zyg9E-6uWnwBhcix9sSfc7jSk8OgugKSNZ_QqPo6kynTKAR2Qn24GLN4vuWtVEypqhioVqyB4B5MwYKaVsQLJv041hNU8_FdB4eF3iULJREeHOm-7NTVUxxIDgA"

    def stt(filename: str) -> dict:
        job = submit_stt_request(filename)

        if job["status"] == "complete":
            return job["result"]

        # Job was not completed within the timeframe


    def submit_stt_request(filename: str) -> dict:
        with open(filename, "rb") as f:
            b64audio_data = base64.b64encode(f.read()).decode("utf-8")

        payload = {
            "config": {
                "model": "stt-general",
                "wait": True  # Blocks the request until the execution is finished
            },
            "request": {
                "data": b64audio_data
            }
        }

        response = requests.post(url, json=payload, headers={
            "x-api-key": api_key
        })

        return response.json()

    filename = "output.wav"

    result = stt(filename)

    hasil = result.get("data")
    if (hasil == None):
        transcript=""
    else:
        transcript = hasil[0]
    final = transcript.get("transcript")

    f = open("stt_result.txt", "w")
    f.write(final)
    f.close()

    page = int(page)

    def submit_answer(answer):
        db_exam = Exam.query.filter_by(token=token).first()
        db_answer = UserAnswer.query.filter_by(user_id=current_user.id, exam_id=db_exam.id, question_id=questionid).first()
        
        if db_answer:
            db_answer.answer = answer
            db.session.commit()

    if(final == "soal selanjutnya"):
        page = page+1
        playsound(os.getcwd()+'/tts/selanjutnya.wav')
        return redirect("/exam/"+str(token)+"/"+str(page))

    if(final == "soal sebelumnya"):
        page = page-1
        playsound(os.getcwd()+'/tts/sebelumnya.wav')
        return redirect("/exam/"+str(token)+"/"+str(page))

    if(final == "baca soal"):
        return redirect("/soal/"+str(token)+"/"+str(page))
    
    if(final == "baca jawaban"):
        return redirect("/jawaban/"+str(token)+"/"+str(page))

    if(final == "jawaban a"):
        answer = "A"
        submit_answer(answer)
        playsound(os.getcwd()+'/tts/jawaba.wav')
        return redirect("/exam/"+str(token)+"/"+str(page))
    
    if(final == "jawaban b"):
        answer = "B"
        submit_answer(answer)
        playsound(os.getcwd()+'/tts/jawabb.wav')
        return redirect("/exam/"+str(token)+"/"+str(page))
    
    if(final == "jawaban c" or final == "jawaban check"):
        answer = "C"
        submit_answer(answer)
        playsound(os.getcwd()+'/tts/jawabc.wav')
        return redirect("/exam/"+str(token)+"/"+str(page))
    
    if(final == "jawaban d"):
        answer = "D"
        submit_answer(answer)
        playsound(os.getcwd()+'/tts/jawabd.wav')
        return redirect("/exam/"+str(token)+"/"+str(page))
    
    if(final == "selesai ujian"):
        playsound(os.getcwd()+'/tts/konfirmasi.wav')

        p = pyaudio.PyAudio()  # Create an interface to PortAudio

        print('Recording')

        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)

        frames = []  # Initialize array to store frames

        # Store data in chunks for 3 seconds
        for i in range(0, int(fs / chunk * seconds)):
            data = stream.read(chunk)
            frames.append(data)

        # Stop and close the stream 
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        p.terminate()

        print('Finished recording')

        # Save the recorded data as a WAV file
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()

        filename = "output.wav"

        result = stt(filename)

        hasil = result.get("data")
        transcript = hasil[0]
        final = transcript.get("transcript")

        f = open("stt_result.txt", "w")
        f.write(final)
        f.close()

        if (final == "tidak"):
            playsound(os.getcwd()+'/tts/batal.wav')
            return redirect("/exam/"+str(token)+"/"+str(page))
        elif (final == "ya" or final == "iya") :
            db_exam = Exam.query.filter_by(token=token).first()
            playsound(os.getcwd()+'/tts/selesai.wav')
            return redirect("/end_exam/"+str(db_exam.id))
    
    playsound(os.getcwd()+'/tts/gagal.wav')
    return redirect("/exam/"+str(token)+"/"+str(page))

@views.route('/stt/nav', methods=['GET', 'POST'])
@login_required
def speech_to_text_nav():
 
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 44100  # Record at 44100 samples per second
    seconds = 3
    filename = "output.wav"

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()


    url = "https://api.prosa.ai/v2/speech/stt"
    api_key = "eyJhbGciOiJSUzI1NiIsImtpZCI6Ik5XSTBNemRsTXprdE5tSmtNaTAwTTJZMkxXSTNaamN0T1dVMU5URmxObVF4Wm1KaSIsInR5cCI6IkpXVCJ9.eyJhcHBsaWNhdGlvbl9pZCI6NDEwMjk4LCJsaWNlbnNlX2tleSI6IjFkMzdjMzZjLTUxNTUtNDU3OS1iNzcyLTFkZmQ4YTQyYTdkYSIsInVuaXF1ZV9rZXkiOiIwM2IyZjRjNy1lOGEwLTRmNWQtYTc1OC0wNWRlNzAyMDZjYjgiLCJwcm9kdWN0X2lkIjo1LCJhdWQiOiJhcGktc2VydmljZSIsInN1YiI6IjQ1NzgzYTYxLWM3NmYtNDVkMi1hOGNjLWMxNGVkMmNkZjg0YSIsImlzcyI6ImNvbnNvbGUiLCJpYXQiOjE3MzQwMTkzNzN9.PQryj95twyxIEdmYSUBXk3y3D2TeRP70TifjkbvNdqVynFG-ZtuTJjPaKWi5wu_L9JwTWAFfd7enT10o1FANEGMZBT5MvrwnOImXSMmebM5U7nPtZ2p8YeeEGPxdk-5OfL4i_YHusJ9YmeKJ0H6QBZ6P8E-3EWr1bRwO03BAs07VpkxqIufPdLRGGZre3kJgoWxWYPb-73ti3zz7PCf6WTfOSP-zyg9E-6uWnwBhcix9sSfc7jSk8OgugKSNZ_QqPo6kynTKAR2Qn24GLN4vuWtVEypqhioVqyB4B5MwYKaVsQLJv041hNU8_FdB4eF3iULJREeHOm-7NTVUxxIDgA"

    def stt(filename: str) -> dict:
        job = submit_stt_request(filename)

        if job["status"] == "complete":
            return job["result"]

        # Job was not completed within the timeframe


    def submit_stt_request(filename: str) -> dict:
        with open(filename, "rb") as f:
            b64audio_data = base64.b64encode(f.read()).decode("utf-8")

        payload = {
            "config": {
                "model": "stt-general",
                "wait": True  # Blocks the request until the execution is finished
            },
            "request": {
                "data": b64audio_data
            }
        }

        response = requests.post(url, json=payload, headers={
            "x-api-key": api_key
        })

        return response.json()

    filename = "output.wav"

    result = stt(filename)

    hasil = result.get("data")
    if (hasil == None):
        transcript=""
    else:
        transcript = hasil[0]
    final = transcript.get("transcript")

    f = open("stt_result.txt", "w")
    f.write(final)
    f.close()

    if(final == "utama"):
        #playsound(os.getcwd()+'/tts/awal.wav')
        return redirect("/")
    
    if(final =="ujian"):
        #playsound(os.getcwd()+'/tts/ujian.wav')
        return redirect("/insert_token")

    if(final =="hasil ujian"):
        #playsound(os.getcwd()+'/tts/hasil_ujian.wav')
        return redirect("/result/1")
    
    if(final =="keluar"):
        #playsound(os.getcwd()+'/tts/hasil_ujian.wav')
        return redirect("/logout")

    playsound(os.getcwd()+'/tts/gagal.wav')
    return redirect("/")


'''

@views.route('/mark_answer/<userid>/<token>/<questionid>', methods=['GET', 'POST'])
@login_required
def mark_answer(token,page):
    
    return redirect("/exam/"+str(token)+"/"+str(page))

@views.route('/delete-question', methods=['POST'])
@login_required
def delete_question():  
    if current_user.type != 'admin':
        return redirect("/")
    else:
        question = json.loads(request.data)
        questionId = question['questionId']
        question = Question.query.get(questionId)
        
        db.session.delete(question)
        db.session.commit()

        return jsonify({})

@views.route('/all_question/<page>', methods=['GET','POST'])
@login_required
def list_question(id,page):
    if current_user.type != 'admin':
        return redirect("/")
    else:
        db_question = Question.query.filter_by(exam_id=id).paginate(page=int(page), per_page=10)
        return render_template("list_question.html", user=current_user, questions=db_question, examid=id)#, kelas=db_class)


  </div>
  <div class="form-group">
    {{ kelas.data }}
    <label for="kelas">Select Class</label> <br>
    <select id="kelas" name="kelas">
      {% for row in kelas %}
        <option value="{{ row.id }}">{{ row.name }}</option>
      {% endfor %}
    </select>
  </div>

@views.route('/class_list', methods=['GET','POST'])
@login_required
def class_list():
    
    db_class = Class.query.all()
    return render_template("account_list.html", user=current_user, kelas=db_class)

@views.route('/add_class', methods=['GET','POST'])
@login_required
def add_class():
    if request.method == 'POST':
        name = request.form.get('name')
        
        if len(name) < 1:
            flash('Class name is too short!', category='error') 
        else:
            new_class = Class(name=name)
            db.session.add(new_class)
            db.session.commit()
            flash('Class added!', category='success')
            
    return render_template("add_class.html", user=current_user)
    
@views.route('/assign_class', methods=['GET','POST'])
@login_required
def assign_class():
    if request.method == 'POST':
        kelas = request.form.get('kelas')


    db_class = Class.query.all()
    return render_template("add_exam.html", user=current_user, kelas=db_class)   
'''
