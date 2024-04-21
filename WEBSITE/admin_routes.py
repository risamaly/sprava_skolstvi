from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
import re
from flask import jsonify
from werkzeug.security import generate_password_hash
from LOG.logging import setup_logger
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer

admin_routes = Blueprint('admin_routes', __name__)

logger = setup_logger('user_creation')
deletion_logger = setup_logger('deletion')

pattern_email = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
pattern_name = re.compile(r'^[a-zA-ZáčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ\s]+$')
pattern_uppercase = re.compile(r'[A-Z]')
pattern_digit = re.compile(r'\d')
pattern_special = re.compile(r'[\W_]')



@admin_routes.route('/admin/utilities/add_user', methods=['GET', 'POST'])
def admin_add_user():
    """Přidaní uživatele ze strany admina"""
    correct_data_format_points = 0  
    original_sid = 0
    original_email = 0
    correct_bcn = 0

    if request.method == 'POST':
        first_name = ''
        last_name  = ''
        email = ''
        role = ''
        bcn = ''
        sid = ''
        password = ''
        confirm_password = ''

        first_name = request.form['user_first_name']
        last_name = request.form['user_last_name']
        email = request.form['user_email']
        role = request.form['user_role']
        bcn = request.form['BCN']
        sid = request.form['user_sid']
        password = request.form['user_password']
        confirm_password = request.form['confirm_password']
        
       
        if not len(first_name) >2 or not re.match(pattern_name, first_name):
            flash('Jméno musí obsahovat pouze písmena a mezery.', 'error')
            correct_data_format_points += 1
            

        if len(last_name) <2 or not re.match(pattern_name, last_name):
            flash('Příjmení musí obsahovat pouze písmena a mezery.', 'error')
            correct_data_format_points += 1
            
            
        if not pattern_email.match(email):
            flash('Email není ve správném formátu.', 'error')
            correct_data_format_points += 1
            original_email += 1
            
        else:
            cursor = current_app.mysql.connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM employees WHERE user_email = %s", (email,))
            email_count = cursor.fetchone()[0]
            cursor.close()

            if email_count > 0:
                flash('Uživatel s tímto emailem již existuje.', 'error')
                correct_data_format_points += 1 
                

        if not len(bcn) == 10 or not bcn.isdigit():
            flash('BCN musí být deseticiferné číslo.', 'error')
            correct_data_format_points += 1
            correct_bcn += 1
                 
        else:
            cursor = current_app.mysql.connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM employees WHERE bcn = %s", (bcn,))
            bcn_count = cursor.fetchone()[0]
            if bcn_count > 0:
                flash('Uživatel s tímto rodným číslem již existuje.', 'error')
                correct_bcn += 1 
            cursor.close()

        if len(sid) != 5 or not sid.isdigit():
            flash('SID musí být pěticiferné číslo.', 'error')
            correct_data_format_points += 1
            original_sid += 1
            
        elif sid.startswith('0'):
            flash('SID nesmí začínat nulou.', 'error')
            correct_data_format_points += 1
            original_sid += 1
            
        
        if len(password) <= 8:
            flash('Heslo je krátké.', 'error')
            correct_data_format_points += 1
            
        
        elif not pattern_uppercase.search(password):
            flash('Heslo musí obsahovat alespoň jedno velké písmeno', 'error')
            correct_data_format_points += 1
            
        
        elif not pattern_digit.search(password):
            flash('Heslo musí obsahovat alespoň jedno číslo', 'error')
            correct_data_format_points += 1
            return render_template('admin/add_user.html')
        
        elif not pattern_special.search(password):
            flash('Heslo musí obsahovat alespoň jeden speciální znak', 'error')
            correct_data_format_points += 1
            return render_template('admin/add_user.html')

        if password != confirm_password:
            flash('Hesla se neshodují.', 'error')
            correct_data_format_points += 1
            return render_template('admin/add_user.html')
        
        hashed_password = generate_password_hash(password)
        
        if original_sid == 0:
            cursor = current_app.mysql.connection.cursor()
            
            cursor.execute("SELECT user_sid FROM employees WHERE user_sid = %s", (sid,))
            user_sid = cursor.fetchone()
            cursor.close()

            if user_sid:
                flash('SID je již přiřazeno', 'error')
                return render_template('admin/add_user.html')
            else:
                pass

        if correct_data_format_points == 0:
            try:
                cursor = current_app.mysql.connection.cursor()
                cursor.execute("INSERT INTO employees (first_name, last_name, user_email, user_role, bcn, user_sid, user_password) VALUES (%s, %s, %s, %s, %s, %s, %s)", (first_name, last_name, email, role, bcn, sid, hashed_password))

                current_app.mysql.connection.commit()

                current_time = datetime.now().strftime('%H:%M:%S')
                logger.info(f"{current_time} - User created: {first_name} {last_name}, SID: {sid}, Role: {role}")

            except Exception as e:
                current_app.mysql.connection.rollback()
                flash(f'Chyba při přidávání uživatele: {e}', 'error')

                current_time = datetime.now().strftime('%H:%M:%S')
                logger.error(f"{current_time} - User creation failed: {first_name} {last_name}, SID: {sid}, Error: {e}")

            finally:
                cursor.close()
                return redirect(url_for('routes.admin'))

    return render_template('admin/add_user.html')

@admin_routes.route('/admin/request_add_user', methods=['GET'])
def request_add_user():
    """Serializuje token a otevře přidání uživatele"""
    token = request.args.get('token')
    try:
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        user_details = serializer.loads(token, salt='user-registration')
        return render_template('admin/request_add_user.html', user_details=user_details)
    except Exception as e:
        flash('Link vypršel.', 'danger')
        return redirect(url_for('admin_routes.dashboard'))


@admin_routes.route('/admin/utilities/add_user_requested', methods=['GET', 'POST'])
def submit_new_user():
    """Přidaní uživatele do databáze"""
    correct_data_format_points = 0  
    original_sid = 0
    original_email = 0
    correct_bcn = 0

    if request.method == 'POST':
        first_name = ''
        last_name  = ''
        email = ''
        role = ''
        bcn = ''
        sid = ''
        password = ''
        confirm_password = ''

        first_name = request.form['user_first_name']
        last_name = request.form['user_last_name']
        email = request.form['user_email']
        role = request.form['user_role']
        bcn = request.form['BCN']
        sid = request.form['user_sid']
        password = request.form['user_password']
        confirm_password = request.form['confirm_password']
       
        if not len(first_name) >2 or not re.match(pattern_name, first_name):
            flash('Jméno musí obsahovat pouze písmena a mezery.', 'error')
            correct_data_format_points += 1
            return render_template('admin/add_user.html')

        if len(last_name) <2 or not re.match(pattern_name, last_name):
            flash('Příjmení musí obsahovat pouze písmena a mezery.', 'error')
            correct_data_format_points += 1
            return render_template('admin/add_user.html')
            
        if not pattern_email.match(email):
            flash('Email není ve správném formátu.', 'error')
            correct_data_format_points += 1
            original_email += 1
            return render_template('admin/add_user.html')
        else:
            cursor = current_app.mysql.connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM employees WHERE user_email = %s", (email,))
            email_count = cursor.fetchone()[0]
            cursor.close()

            if email_count > 0:
                flash('Uživatel s tímto emailem již existuje.', 'error')
                correct_data_format_points += 1 
                return render_template('admin/add_user.html')

        if not len(bcn) == 10 or not bcn.isdigit():
            flash('BCN musí být deseticiferné číslo.', 'error')
            correct_data_format_points += 1
            correct_bcn += 1
            return render_template('admin/add_user.html')     
        else:
            cursor = current_app.mysql.connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM employees WHERE bcn = %s", (bcn,))
            bcn_count = cursor.fetchone()[0]
            if bcn_count > 0:
                flash('Uživatel s tímto rodným číslem již existuje.', 'error')
                correct_bcn += 1 
            cursor.close()

        if len(sid) != 5 or not sid.isdigit():
            flash('SID musí být pěticiferné číslo.', 'error')
            correct_data_format_points += 1
            original_sid += 1
            return render_template('admin/add_user.html')
        elif sid.startswith('0'):
            flash('SID nesmí začínat nulou.', 'error')
            correct_data_format_points += 1
            original_sid += 1
            return render_template('admin/add_user.html')
        
        if len(password) <= 8:
            flash('Heslo je krátké.', 'error')
            correct_data_format_points += 1
            return render_template('admin/add_user.html')
        
        elif not pattern_uppercase.search(password):
            flash('Heslo musí obsahovat alespoň jedno velké písmeno', 'error')
            correct_data_format_points += 1
            return render_template('admin/add_user.html')
        
        elif not pattern_digit.search(password):
            flash('Heslo musí obsahovat alespoň jedno číslo', 'error')
            correct_data_format_points += 1
            return render_template('admin/add_user.html')
        
        elif not pattern_special.search(password):
            flash('Heslo musí obsahovat alespoň jeden speciální znak', 'error')
            correct_data_format_points += 1
            return render_template('admin/add_user.html')

        if password != confirm_password:
            flash('Hesla se neshodují.', 'error')
            correct_data_format_points += 1
            return render_template('admin/add_user.html')
        
        hashed_password = generate_password_hash(password)
        
        if original_sid == 0:
            cursor = current_app.mysql.connection.cursor()
            
            cursor.execute("SELECT user_sid FROM employees WHERE user_sid = %s", (sid,))
            user_sid = cursor.fetchone()
            cursor.close()

            if user_sid:
                flash('SID je již přiřazeno', 'error')
                return render_template('admin/add_user.html')
            else:
                pass

        if correct_data_format_points == 0:
            try:
                cursor = current_app.mysql.connection.cursor()
                cursor.execute("INSERT INTO employees (first_name, last_name, user_email, user_role, bcn, user_sid, user_password) VALUES (%s, %s, %s, %s, %s, %s, %s)", (first_name, last_name, email, role, bcn, sid, hashed_password))

                current_app.mysql.connection.commit()

                current_time = datetime.now().strftime('%H:%M:%S')
                logger.info(f"{current_time} - User created: {first_name} {last_name}, SID: {sid}, Role: {role}")

            except Exception as e:
                current_app.mysql.connection.rollback()
                flash(f'Chyba při přidávání uživatele: {e}', 'error')

                current_time = datetime.now().strftime('%H:%M:%S')
                logger.error(f"{current_time} - User creation failed: {first_name} {last_name}, SID: {sid}, Error: {e}")

            finally:
                cursor.close()
                return redirect(url_for('routes.admin'))

    return render_template('admin/add_user.html')


@admin_routes.route('/admin/manage_users', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_users():
    """Zobrazeni uživatelů aplikace"""
    return render_template('admin/manage_users.html')

@admin_routes.route('/get-all-employees')
def get_all_employees():
    """route který v pozadí vybere data o zamestnancich z databaze"""
    cursor = current_app.mysql.connection.cursor()
    cursor.execute("SELECT user_sid, first_name, last_name, user_email, bcn, user_role FROM employees")
    employees = cursor.fetchall()
    cursor.close()
    
    employee_data = [{
        'user_sid': emp[0],
        'first_name': emp[1],
        'last_name': emp[2],
        'user_email': emp[3],
        'bcn': emp[4],  
        'user_role': emp[5],  
    } for emp in employees]

    return jsonify(employee_data)

@admin_routes.route('/search-users')
def search_users():
    """Route ktery v pozadí vyhledáva zamestnance"""
    query = request.args.get('query', '')
    cursor = current_app.mysql.connection.cursor()

    search_query = f"%{query}%"
    cursor.execute("SELECT user_sid, first_name, last_name, user_email FROM employees WHERE first_name LIKE %s OR last_name LIKE %s OR user_email LIKE %s", (search_query, search_query, search_query))


    users = cursor.fetchall()
    cursor.close()

    user_data = [{
        'user_sid': user[0],
        'first_name': user[1],
        'last_name': user[2],
        'user_email': user[3]
    } for user in users]

    return jsonify(user_data)

@admin_routes.route('/delete-user/<int:user_sid>', methods=['DELETE'])
def delete_user(user_sid):
    """Odstrani uzivatele z databaze"""
    try:
        data = request.get_json()
        reason = data.get('reason', 'Žádný důvod nebyl poskytnut.')
        
        cursor = current_app.mysql.connection.cursor()
        
        cursor.execute("SELECT first_name, last_name FROM employees WHERE user_sid = %s", (user_sid,))
        user_info = cursor.fetchone()
        
        if not user_info:
            return jsonify({'error': f'Uživatel s ID {user_sid} neexistuje v databázi.'}), 404
        
        cursor.execute("DELETE FROM employees WHERE user_sid = %s", (user_sid,))
        current_app.mysql.connection.commit()
        
        full_name = f'{user_info[0]} {user_info[1]}'
        deletion_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        deletion_logger.info(f'Uživatel {full_name} (ID: {user_sid}) byl smazán z databáze dne {deletion_time}. Důvod smazání: {reason}')
        
        cursor.close()
        return jsonify({'success': 'Uživatel byl úspěšně odstraněn.'}), 200
    except Exception as e:
        current_app.mysql.connection.rollback()
        
        deletion_logger.error(f'Chyba při pokusu o smazání uživatele s ID {user_sid}: {e}')
        
        return jsonify({'error': str(e)}), 500
    
    