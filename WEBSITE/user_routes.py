import os
import sys
sys.path.insert(0,os.path.join(os.path.dirname(__file__),".."))
from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import current_app
from flask import session
import re
from itsdangerous import URLSafeTimedSerializer
from LOG.logging import setup_logger
from flask import jsonify

routes = Blueprint('routes', __name__)
admin_routes = Blueprint('admin_routes', __name__)
authentication_routes = Blueprint('authentication_routes',  __name__)
user_routes = Blueprint('user_routes', __name__)

user_logger = setup_logger('user__logger')

@user_routes.route('/user/change_my_informations', methods=['GET', 'POST'])
def change_my_informations():
    """Route načítající informace z databaze"""
    user_sid = session.get('user_info', {}).get('sid')
    if not user_sid:
        flash("Přihlášení vypršelo", "warning")
        return redirect(url_for('authentication_routes.login'))

    cursor = current_app.mysql.connection.cursor()
    cursor.execute("""
        SELECT user_sid, user_profile_pic, first_name, last_name, title_before_name, title_after_name, 
               bcn, user_email, user_phone_number, user_adress, user_role, user_school_email, user_school_phone_number, school_id
        FROM employees WHERE user_sid = %s
    """, [user_sid])
    user_details = cursor.fetchone()
    cursor.close()

    if user_details:
        user_data = {k: (v if v is not None else '') for k, v in zip([
            'sid', 'profile_pic', 'first_name', 'last_name',
            'title_before_name', 'title_after_name', 'bcn', 'user_email',  
            'user_phone_number', 'user_adress', 'role', 'user_school_email', 'user_school_phone_number', 'school_id'
        ], user_details)}

        return render_template('user/change_my_informations.html', user=user_data)
    else:
        flash("Nepodařilo se načíst data.", "error")
        return redirect(url_for('authentication_routes.login'))
        

@user_routes.route('/user/update_information', methods=['POST'])
def update_information():
    """route odesílající inforamce do databaze"""
    user_sid = session.get('user_info', {}).get('sid')
    if not user_sid:
        flash("Přihlášení vypršelo, přihlašte se", "warning")
        return redirect(url_for('authentication_routes.login'))
    
    
    title_before_name = request.form.get('title_before_name', '')
    first_name = request.form.get('first_name', '')
    last_name = request.form.get('last_name', '')
    title_after_name = request.form.get('title_after_name', '')
    user_email = request.form.get('user_email', '')
    user_phone_number = request.form.get('user_phone_number', '')
    user_adress = request.form.get('user_adress', '')
    user_school_email = request.form.get('user_school_email', '')
    user_school_phone_number = request.form.get('user_school_phone_number', '')
    school_id = request.form.get('school_id', '')

    correct_data_format = True

    pattern_email = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    pattern_phone = re.compile(r'^\+?\d{0,3} ?\d{3} ?\d{3} ?\d{3,4}$')
    pattern_address = re.compile(r'^[0-9a-zA-ZáčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ .,/-]+$')


    if not (pattern_email.match(user_email or '') and pattern_email.match(user_school_email or '')):
        flash('Jeden nebo oba emaily nejsou ve správném formátu.', 'error')
        correct_data_format = False

    if not (pattern_phone.match(user_phone_number or '') and pattern_phone.match(user_school_phone_number or '')):
        flash('Jedno nebo obě telefonní čísla nejsou ve správném formátu.', 'error')
        correct_data_format = False

    if not pattern_address.match(user_adress or ''):
        flash('Adresa není ve správném formátu.', 'error')
        correct_data_format = False
    
    if not correct_data_format:
        return redirect(url_for('user_routes.change_my_informations'))
    
    try:

        cursor = current_app.mysql.connection.cursor()
        cursor.execute("""
        UPDATE employees
        SET title_before_name=%s, first_name=%s, last_name=%s, 
            title_after_name=%s, user_email=%s, user_phone_number=%s, 
            user_adress=%s, user_school_email=%s, user_school_phone_number=%s, school_id=%s
        WHERE user_sid=%s
    """, (title_before_name, first_name, last_name, title_after_name, 
        user_email, user_phone_number, user_adress, user_school_email, user_school_phone_number, school_id, user_sid))

        current_app.mysql.connection.commit()
        flash('Vaše informace byly úspěšně aktualizovány.', 'success')
        
    except Exception as e:
        current_app.mysql.connection.rollback()
        flash(f'Nepodařilo se aktualizovat informace: {e}', 'error')
    finally:
        cursor.close()

    return redirect(url_for('user_routes.change_my_informations'))

@user_routes.route('/home_boss/add_user', methods=['GET', 'POST'])
def add_user():
    """route který odesílá email spravcovi pro přidaní nového uživatele"""
    user_sid = session.get('user_info', {}).get('sid')
    if not user_sid:
        flash("Přihlášení vypršelo, přihlašte se", "warning")
        return redirect(url_for('authentication_routes.login'))

    user_details = {}

    if user_sid:
        try:
            cursor = current_app.mysql.connection.cursor()
            cursor.execute("SELECT user_email FROM employees WHERE user_sid = %s", (user_sid,))
            user_data = cursor.fetchone()
            cursor.close()
            
            if user_data:
                user_details['email'] = user_data[0]
                
        except Exception as e:
            user_logger.error(f"Database error when fetching user SID: {e}")
    

    if request.method == 'POST':
        user_details.update({
            'user_first_name': request.form['user_first_name'],
            'user_last_name': request.form['user_last_name'],
            'user_email': request.form['user_email'],
            'user_role': request.form['user_role'],
            'BCN': request.form['BCN'],
            'SID': request.form.get('user_sid')
        })

        user_logger.info(f"User SID {user_sid} requested to add/update user with details: "
                         f"First Name: {user_details['user_first_name']}, "
                         f"Last Name: {user_details['user_last_name']}, "
                         f"Email: {user_details['user_email']}, "
                         f"BCN: {user_details['BCN']}")
        
        pattern_name = re.compile(r'^[a-zA-ZáčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ\s]+$')
        pattern_email = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        pattern_bcn = re.compile(r'^\d{10}$')
        
        if len(user_details['user_first_name']) < 2 or not pattern_name.match(user_details['user_first_name']):
            flash('Jméno je příliš krátké nebo obsahuje neplatné znaky.', 'error')
            return render_template('user/boss_add_user.html', user_details=user_details)

        if len(user_details['user_last_name']) < 2 or not pattern_name.match(user_details['user_last_name']):
            flash('Příjmení je příliš krátké nebo obsahuje neplatné znaky.', 'error')
            return render_template('user/boss_add_user.html', user_details=user_details)

        if not pattern_email.match(user_details['user_email']):
            flash('Email není ve správném formátu.', 'error')
            return render_template('user/boss_add_user.html', user_details=user_details)

        cursor = current_app.mysql.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM employees WHERE user_email = %s", (user_details['user_email'],))
        if cursor.fetchone()[0] > 0:
            flash('Uživatel s tímto emailem již existuje.', 'error')
            cursor.close()
            return render_template('user/boss_add_user.html', user_details=user_details)
        cursor.close()

        if not pattern_bcn.match(user_details['BCN']):
            flash('BCN musí být deseticiferné číslo.', 'error')
            return render_template('user/boss_add_user.html', user_details=user_details)

        cursor = current_app.mysql.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM employees WHERE bcn = %s", (user_details['BCN'],))
        if cursor.fetchone()[0] > 0:
            flash('Uživatel s tímto rodným číslem již existuje.', 'error')
            cursor.close()
            return render_template('user/boss_add_user.html', user_details=user_details)
        cursor.close()

        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        token = serializer.dumps(user_details, salt='user-registration')

        subject = "Žádost o nového užiavtele"
        admin_email = 'ricianek@gmail.com'
        current_app.mail_sender.request_new_user(admin_email, user_details, subject)

        try:
            valid_data = True
            if len(user_details['user_first_name']) < 2:
                flash('Jméno je příliš krátké.', 'error')
                valid_data = False
            if not re.match(r'^[a-zA-ZáčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ\s]+$', user_details['user_first_name']):
                flash('Jméno obsahuje neplatné znaky.', 'error')
                valid_data = False
            if not valid_data:
                raise ValueError("Invalid user name or last name.")
                
        except Exception as e:
            user_logger.error(f"Error when adding user: {e}")
            flash('Chyba při přidávání uživatele.', 'error')
            return render_template('user/boss_add_user.html', user_details=user_details)

        flash('Žádost byla úspěšně odeslána', 'success')
        return redirect(url_for('user_routes.add_user'))
    
    return render_template('user/boss_add_user.html', user_details=user_details)


@user_routes.route('/home_boss/search_students', methods=['GET'])
def search_students():
    """route pro vyhledavani studentu ze vsech skol"""
    user_sid = session.get('user_info', {}).get('sid')
    if not user_sid:
        flash("Přihlášení vypršelo, přihlašte se", "warning")
        user_logger.warning("Session expired or SID is not found.")
        return redirect(url_for('authentication_routes.login'))

    try:
        cursor = current_app.mysql.connection.cursor()
        cursor.execute("SELECT student_id, first_name, last_name, bcn FROM students")
        students_data = cursor.fetchall()
        cursor.close()

        students = [{'student_id': student_id, 'first_name': first_name, 'last_name': last_name, 'bcn': bcn}
                    for student_id, first_name, last_name, bcn in students_data]

        user_logger.info(f"User SID {user_sid} searched for all students.")
        return render_template('user/search_student.html', students=students)
    except Exception as e:
        user_logger.error(f"Failed to fetch students: {e}")
        flash(f"Chyba při načítání studentů: {e}", "error")
        return redirect(url_for('home_boss'))

@user_routes.route('/user/get_all_students', methods=['GET'])
def get_all_students():
    """route zpracovavajici vypsani vsechn studentu z databaze"""
    try:
        cursor = current_app.mysql.connection.cursor()
        cursor.execute("SELECT student_id, first_name, last_name, bcn FROM students")
        students_data = cursor.fetchall()
        cursor.close()

        students = [{'student_id': student[0], 'first_name': student[1], 'last_name': student[2], 'bcn': student[3]}
                    for student in students_data]
        return jsonify(students)
    except Exception as e:
        user_logger.error(f"Failed to fetch students for JS: {e}")
        return jsonify([]), 500

@user_routes.route('boss/student_profile/<int:student_id>', methods=['GET'])
def student_profile(student_id):
    """zobrazeni inforamci studenta podle jeho id v databazi"""
    try:
        cursor = current_app.mysql.connection.cursor()
        cursor.execute("SELECT student_id, first_name, last_name, bcn, user_profile_pic, student_email, parent_email FROM students WHERE student_id = %s", (student_id,))
        student = cursor.fetchone()
        cursor.close()
        if student:
            student_data = {
                'student_id': student[0],
                'first_name': student[1],
                'last_name': student[2],
                'bcn': student[3],
                'user_profile_pic': student[4],
                'student_email': student[5],
                'parent_email': student[6]
            }
            return render_template('user/student_profile.html', student=student_data, school_name='Název školy')
        else:
            flash("Student nebyl nalezen.", "error")
            return redirect(url_for('user_routes.search_students'))
    except Exception as e:
        flash(f"Chyba při načítání profilu studenta: {e}", "error")
        return redirect(url_for('user_routes.search_students'))



@user_routes.route('/home_boss/search_school', methods=['GET'])
def search_schools():
    """vyhledavani skol"""
    user_sid = session.get('user_info', {}).get('sid')
    if not user_sid:
        flash("Přihlášení vypršelo, přihlašte se", "warning")
        return redirect(url_for('authentication_routes.login'))

    try:
        cursor = current_app.mysql.connection.cursor()
        cursor.execute("SELECT school_id, school_name, school_type, school_adress FROM school")
        schools_data = cursor.fetchall()
        cursor.close()

        schools = [{'school_id': school[0], 'school_name': school[1], 'school_type': school[2], 'school_adress': school[3]}
                    for school in schools_data]

        return render_template('user/search_school.html', schools=schools)
    except Exception as e:
        flash(f"Chyba při načítání škol: {e}", "error")
        return redirect(url_for('home_boss'))

@user_routes.route('/user/get_all_schools', methods=['GET'])
def get_all_schools():
    """ziskava inforamce o skolach"""
    try:
        cursor = current_app.mysql.connection.cursor()
        cursor.execute("SELECT school_id, school_name, school_type, school_adress FROM school")
        schools_data = cursor.fetchall()
        cursor.close()

        schools = [{'school_id': school[0], 'school_name': school[1], 'school_type': school[2], 'school_adress': school[3]}
                    for school in schools_data]
        return jsonify(schools)
    except Exception as e:
        return jsonify([]), 500
