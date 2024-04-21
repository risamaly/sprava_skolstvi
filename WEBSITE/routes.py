from flask import Blueprint
from flask import render_template
from flask import flash
from flask import current_app
from flask import session
from flask import jsonify
from flask import redirect
from flask import url_for
from flask import request
from werkzeug.security import generate_password_hash
import re
from LOG.logging import setup_logger
from werkzeug.security import check_password_hash

routes = Blueprint('routes', __name__)
admin_routes = Blueprint('admin_routes', __name__)
authentication_routes = Blueprint('authentication_routes',  __name__)

@routes.route('/admin')
def admin():
    """route pro admina"""
    return render_template("admin/admin_home.html")

@routes.route('/home_boss')
def boss():
    """route pro reditele"""
    user_sid = session.get('user_info', {}).get('sid')
    if not user_sid:
        flash("Přihlášení vypršelo, přihlašte se", "warning")
        return redirect(url_for('authentication_routes.login'))

    cursor = current_app.mysql.connection.cursor()
    

    cursor.execute("SELECT school_id FROM employees WHERE user_sid = %s", (user_sid,))
    school_id_result = cursor.fetchone()
    if school_id_result:
        school_id = school_id_result[0]
        
        cursor.execute("SELECT school_name FROM school WHERE school_id = %s", (school_id,))
        school_name = cursor.fetchone()[0]

        cursor.execute("""
            SELECT user_sid, first_name, last_name, user_email, bcn 
            FROM employees 
            WHERE school_id = %s
        """, (school_id,))
        employees = cursor.fetchall()
    else:
        school_name = "Škola nenalezena"
        employees = []

    cursor.close()

    return render_template("user/boss.html", school_name=school_name, employees=employees)

@routes.route('/home_deputy')
def assistant():
    """route pro zastupce reditele"""
    user_sid = session.get('user_info', {}).get('sid')
    if not user_sid:
        flash("Přihlášení vypršelo, přihlašte se", "warning")
        return redirect(url_for('authentication_routes.login'))

    return render_template("user/deputy.html")


@routes.route('/home_teacher', methods=['GET', 'POST'])
def teacher():
    """route pro ucitele"""
    user_sid = session.get('user_info', {}).get('sid')
    if not user_sid:
        flash("Přihlášení vypršelo, přihlašte se", "warning")
        return redirect(url_for('authentication_routes.login'))

    cursor = current_app.mysql.connection.cursor()

    cursor.execute("""
        SELECT c.class_id, c.class_name
        FROM class c
        JOIN employees e ON c.user_sid = e.user_sid
        WHERE e.user_sid = %s
    """, (user_sid,))
    class_info = cursor.fetchone()

    if not class_info:
        flash("Učitel nemá přiřazenou žádnou třídu.", "warning")
        class_info = (None, "Třída nepřiřazena")
        students = []
    else:
        class_id = class_info[0]
        cursor.execute("""
            SELECT s.student_id, s.first_name, s.last_name, s.student_email
            FROM students s
            WHERE s.class_id = %s
        """, (class_id,))
        students = cursor.fetchall()

    cursor.close()

    return render_template("user/teacher.html", class_info=class_info, students=students)


@routes.route('/get_all_students', methods=['GET'])
def get_all_students():
    """vypis studentu do ucitelskeho routu"""

    user_info = session.get('user_info', {})  
    user_sid = user_info.get('sid')
    if not user_sid:
        return jsonify({'error': 'Uživatel není přihlášen.'}), 401

    cursor = current_app.mysql.connection.cursor()

    cursor.execute("""
        SELECT class_id FROM class 
        WHERE user_sid = %s
    """, (user_sid,))
    class_info = cursor.fetchone()

    if not class_info:
        return jsonify({'error': 'Učitel nemá přiřazenou žádnou třídu.'}), 404

    class_id = class_info[0]

    cursor.execute("""
        SELECT student_id, first_name, last_name, student_email 
        FROM students 
        WHERE class_id = %s
    """, (class_id,))
    students = cursor.fetchall()
    cursor.close()

    student_data = [{
        'student_id': student[0],
        'first_name': student[1],
        'last_name': student[2],
        'student_email': student[3],
    } for student in students]

    return jsonify(student_data)

@routes.route('/lost_password', methods=['GET','POST'])
def send_email():
    """Odesilani emailu pro reset hesla"""
    if request.method == 'POST':
        email = request.form.get('email')
        cursor = current_app.mysql.connection.cursor()

        cursor.execute("SELECT user_sid FROM employees WHERE user_email = %s", (email,))
        user_sid = cursor.fetchone()

        cursor.close()

        if user_sid:
            current_app.mail_sender.send_email(email, user_sid)
            flash('Email pro obnovu hesla byl odeslán.', 'success')
        else:
            flash('Email není registrován v databázi.', 'danger')

        return redirect(url_for('routes.send_email'))
    else:
        return render_template('login/lost_password.html')

password_reset_logger = setup_logger('password_reset_logger')

@routes.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """route vytvoreni noveho hesla"""
    data = current_app.mail_sender.confirm_token(token)
    if not data:
        flash('Odkaz pro obnovu hesla je neplatný nebo vypršel.', 'danger')
        password_reset_logger.warning('Invalid or expired token for password reset attempt.')
        return redirect(url_for('authentication_routes.login'))

    sid = data['sid']
    email = data['email']

    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('password2')

        pattern_uppercase = re.compile(r'[A-Z]')
        pattern_digit = re.compile(r'\d')
        pattern_special = re.compile(r'[\W_]')

        if password != confirm_password:
            flash('Hesla se neshodují.', 'danger')
        elif len(password) < 8:
            flash('Heslo je příliš krátké.', 'danger')
        elif not pattern_uppercase.search(password):
            flash('Heslo musí obsahovat alespoň jedno velké písmeno.', 'danger')
        elif not pattern_digit.search(password):
            flash('Heslo musí obsahovat alespoň jedno číslo.', 'danger')
        elif not pattern_special.search(password):
            flash('Heslo musí obsahovat alespoň jeden speciální znak.', 'danger')
        else:
            hashed_password = generate_password_hash(password)
            try:
                cursor = current_app.mysql.connection.cursor()
                cursor.execute("""
                    UPDATE employees 
                    SET user_password = %s 
                    WHERE user_sid = %s AND user_email = %s
                """, (hashed_password, sid, email))
                current_app.mysql.connection.commit()
                flash('Vaše heslo bylo úspěšně změněno.', 'success')
                password_reset_logger.info(f'User with SID {sid} and email {email} has successfully reset their password.')
                return redirect(url_for('authentication_routes.login'))
            except Exception as e:
                flash('Chyba při změně hesla: ' + str(e), 'danger')
                current_app.mysql.connection.rollback()
                password_reset_logger.error(f'Failed password reset attempt for SID {sid}: {e}')
            finally:
                cursor.close()

    return render_template('login/reset_password.html', token=token)


@routes.route('/support', methods=['GET', 'POST'])
def support():
    """route pro odelsani stiznosti na podporu"""
    user_sid = session.get('user_info', {}).get('sid')
    if not user_sid:
        flash("Přihlášení vypršelo, přihlašte se", "warning")
        return redirect(url_for('authentication_routes.login'))

    cursor = current_app.mysql.connection.cursor()
    cursor.execute("SELECT user_email, user_password FROM employees WHERE user_sid = %s", (user_sid,))
    user_data = cursor.fetchone()
    cursor.close()

    if user_data is None:
        flash("Nelze najít e-mailovou adresu pro vaše uživatelské SID.", "error")
        return render_template('login/support.html')

    user_email, user_password_hash = user_data

    if request.method == 'POST':
        password = request.form.get('password')
        if not check_password_hash(user_password_hash, password):
            flash("Nesprávné heslo, zkuste to znovu.", "error")
            return render_template('login/support.html')

        subject = request.form['request_subject']
        description = request.form['request_description']
        support_email = "ricianek@gmail.com"
        
        try:
            current_app.mail_sender.send_support_mail(user_email, support_email, subject, description)
            flash('Vaše žádost byla úspěšně odeslána.', 'success')
        except Exception as e:
            flash('Nepodařilo se odeslat email. ' + str(e), 'error')

        return redirect(url_for('routes.support'))

    return render_template('login/support.html')
