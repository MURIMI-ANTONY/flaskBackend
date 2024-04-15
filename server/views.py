from flask import Blueprint , render_template ,make_response, request, flash,redirect,url_for,jsonify
from flask_restful import Api, Resource
from flask_login import login_required, current_user
from .models import Note,db
import json

views = Blueprint('views', __name__)
api = Api(views)


class Home(Resource):
    @login_required
    def get(self):
        return make_response(render_template("home.html", user=current_user))
    
    def post(self):
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short', category = 'error')
        else:
            new_note = Note(data=note, user_id= current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added successfully',category='success')
            return redirect(url_for('views.home'))
    
class DeleteNote(Resource):
    @login_required
    def post(self):
        data = json.loads(request.data)
        noteId = data['noteId']
        note = Note.query.get(noteId)
        if  note:
            if note.user_id == current_user.id:
                db.session.delete(note)
                db.session.commit()
                return jsonify({"note deleted "})
        


api.add_resource(Home,'/')
api.add_resource(DeleteNote,'/delete-note')
