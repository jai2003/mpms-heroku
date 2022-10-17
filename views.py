from flask import Blueprint

from flask import Flask, redirect ,url_for,render_template,request,session,flash

from .models import Note
from .__init__ import db
import json
from flask_login import login_user,login_required,logout_user,current_user

views=Blueprint('views',__name__)


@views.route('/',methods=['GET', 'POST'])
@login_required
def home():
   
            
    return render_template("home.html",user=current_user)

@views.route('/notes',methods=['GET', 'POST'])
@login_required
def notes():
    if request.method== "POST" :
        note =request.form.get('note')
        
        if len(note)<1:
            flash('Note is too short!',category='error')
            
        else:
            new_note=Note(data=note,user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added',category="success")
    return render_template("notes.html",user=current_user)

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