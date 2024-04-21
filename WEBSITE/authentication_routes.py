from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import current_app
from flask import session
from flask import jsonify
from werkzeug.security import check_password_hash

routes = Blueprint('routes', __name__)
admin_routes = Blueprint('admin_routes', __name__)
authentication_routes = Blueprint('authentication_routes',  __name__)

@authentication_routes.route('/', methods=['GET', 'POST'])
def login():
    """Přihlšení podle SID"""
    if request.method == 'POST':
        sid = request.form['sid']
        password = request.form['password']

        cursor = current_app.mysql.connection.cursor()
        cursor.execute("SELECT user_password, user_role FROM employees WHERE user_sid = %s", (sid,))
        user_login_data = cursor.fetchone()
        cursor.close()

        if user_login_data:

            if check_password_hash(user_login_data[0], password):
                session['user_info'] = {
                    'role': user_login_data[1],
                    'sid': sid
                }
                load_user_data()

                if session['user_info']['role'] == "Admin":
                    return redirect(url_for('routes.admin')) 
                elif session['user_info']['role'] == "Ředitel/ka":
                    return redirect(url_for('routes.boss'))
                elif session['user_info']['role'] == "Zástupce ředitele":
                    return redirect(url_for('routes.assistant'))
                elif session['user_info']['role'] == "Učitel/ka":
                    return redirect(url_for('routes.teacher'))
                else:
                    flash("Role nebyla rozpoznána.")
                    return render_template('login/login.html')
            else:
                flash("Nesprávné heslo.")
                return render_template('login/login.html')
        else:
            flash("Nesprávné SID.")
            return render_template('login/login.html')

    return render_template('login/login.html')

@authentication_routes.route('/user/manage_profile', methods=['GET'])
def get_all_user_data_by_sid():
    """Route ktery vypisuje infromace ziskane SID"""
    user_sid = session.get('user_info', {}).get('sid')
    if not user_sid:
        flash("Přihlášení vypršelo, přihlašte se", "warning")
        return redirect(url_for('authentication_routes.login'))

    cursor = current_app.mysql.connection.cursor()
    cursor.execute("""
        SELECT e.user_sid, e.user_profile_pic, e.first_name, e.last_name, 
               e.title_before_name, e.title_after_name, e.bcn, e.user_email, 
               e.user_phone_number, e.user_adress, e.user_role, e.user_school_email, 
               e.user_school_phone_number, s.school_name
        FROM employees e
        JOIN school s ON e.school_id = s.school_id
        WHERE e.user_sid = %s
    """, (user_sid,))
    
    user_details = cursor.fetchone()
    cursor.close()

    if user_details:
        keys = ["sid", "profile_pic", "first_name", "last_name", 
                "title_before_name", "title_after_name", "bcn", "email", 
                "phone_number", "adress", "role", "school_email", "school_phone_number", "school_name"]
        user_info = dict(zip(keys, user_details))

        return render_template('user/manage_profile.html', user=user_info)
    else:
        flash("Data nenalezena.")
        return redirect(url_for('authentication_routes.login'))

@authentication_routes.route('/get_user_data', methods=['GET', 'POST'])
def load_user_data():
    """Nacita informace na stranku"""
    sid = session.get('user_info', {}).get('sid')

    if sid:
        cursor = current_app.mysql.connection.cursor()
        cursor.execute("SELECT first_name, last_name, user_role FROM employees WHERE user_sid = %s", (sid,))
        user_details = cursor.fetchone()
        cursor.close()
# NOTE : Zmenit hodnty none na zadne
        if user_details:

            first_name = str(user_details[0])
            last_name = str(user_details[1])
            role = user_details[2]

            session['user_info']['name'] = first_name + ' ' + last_name
            session['user_info']['role'] = role
            return jsonify({'name': session['user_info']['name'], 'role': role})
        else:
            return jsonify({'error': 'User data nenalezena.'}), 404
    else:
        return jsonify({'error': 'Chybí SID.'}), 400
    
@authentication_routes.route('/logout', methods=['GET', 'POST'])
def logout():
    """Odhlaseni"""
    session.pop('user_info', None)
    return redirect(url_for('authentication_routes.login'))

