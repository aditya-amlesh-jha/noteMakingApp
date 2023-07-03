from flask import Blueprint, render_template, request, Response
from flask_login import login_required, current_user
from .models import Note
from . import db

# Blueprint is a way to organize a group of related views and other code.

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'GET':
        return render_template("home.html", title="Home", user=current_user)

@views.route('/add-notes', methods=['GET', 'POST'])
@login_required
def add_notes():
    if request.method == 'GET':
        return render_template("add-note.html", title="Notes", user=current_user)
    
    try:
        data = request.json
        title = data['title']
        content = data['content']

        note = Note(title=title, content=content, user_id=current_user.id)
        db.session.add(note)
        db.session.commit()
        
    except Exception as e:
        return Response("Error in saving note!", status=400)
    
    return Response(status=200)

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    try:
        data = request.json
        note_id = data['note_id']

        note = Note.query.get(note_id)
        if note and note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
        
    except Exception as e:
        return Response("Error in deleting note!", status=400)
    
    return Response(status=200)



