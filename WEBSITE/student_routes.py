import os
import sys
sys.path.insert(0,os.path.join(os.path.dirname(__file__),".."))
from flask import Blueprint
from flask import render_template
from flask import flash
from flask import current_app
from flask import redirect
from flask import url_for

routes = Blueprint('routes', __name__)
admin_routes = Blueprint('admin_routes', __name__)
authentication_routes = Blueprint('authentication_routes',  __name__)

student_routes = Blueprint('student_routes', __name__)

@student_routes.route('/student_profile/<int:student_id>')
def student_profile(student_id):
    """Route pro zobrazeni stedntovo informaci"""
    cursor = current_app.mysql.connection.cursor()
    cursor.execute("""
        SELECT student_id, user_profile_pic, first_name, last_name, bcn, student_email, 
               student_phone_number, student_adress, parent_email, parent_phone_number, parent_adress 
        FROM students 
        WHERE student_id = %s
    """, (student_id,))
    result = cursor.fetchone()

    columns = [col[0] for col in cursor.description]
    cursor.close()

    if result is None:
        flash("Student nebyl nalezen.", "error")
        return redirect(url_for('routes.home_teacher'))

    student = dict(zip(columns, result))

    return render_template('student/student_profile.html', student=student)

@student_routes.route('/student_profile/more_info')
def student_more_info():
    """Rozsirene informace pro studenta"""
    return render_template('student/more_info.html')