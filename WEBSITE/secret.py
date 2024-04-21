from flask import Blueprint
from flask import render_template
from flask import flash
from flask import current_app
from flask import session
from flask import jsonify
from flask import redirect
from flask import url_for
from flask import request
import random

secret = Blueprint('secret', __name__)



def quizs_questions():
    """Otazky do quizu"""
    quizzes =[
                {
                    "questions": [
                        {
                            "text": "Jak se máš?",
                            "answers": ["Dobře", "Špatně", "Nevím"],
                            "correct_answer": "Dobře"
                        },
                        {
                            "text": "Kolik je hodin?",
                            "answers": ["12", "3", "9"],
                            "correct_answer": "12"
                        },
                        {
                            "text": "Jaké je hlavní město Japonska?",
                            "answers": ["Tokyo", "Kyoto", "Osaka"],
                            "correct_answer": "Tokyo"
                        },
                        {
                            "text": "Kdo napsal knihu '1984'?",
                            "answers": ["George Orwell", "Aldous Huxley", "Ray Bradbury"],
                            "correct_answer": "George Orwell"
                        },
                        {
                            "text": "Jaký prvek je značen jako 'O' v periodické tabulce?",
                            "answers": ["Kyslík", "Osmium", "Zlato"],
                            "correct_answer": "Kyslík"
                        },
                        {
                            "text": "Kolik kontinentů je na Zemi?",
                            "answers": ["5", "6", "7"],
                            "correct_answer": "7"
                        },
                        {
                            "text": "Jaké je chemické vzorce vody?",
                            "answers": ["H2O", "CO2", "NaCl"],
                            "correct_answer": "H2O"
                        }
                    ]
                },
                
                {
                    "questions": [
                        {
                            "text": "Jaká je nejvyšší hora na světě?",
                            "answers": ["Mount Everest", "K2", "Kangchenjunga"],
                            "correct_answer": "Mount Everest"
                        },
                        {
                            "text": "Kdo objevil Ameriku?",
                            "answers": ["Kryštof Kolumbus", "Leif Eriksson", "Amerigo Vespucci"],
                            "correct_answer": "Kryštof Kolumbus"
                        },
                        {
                            "text": "Jaký je nejběžnější prvek ve vesmíru?",
                            "answers": ["Vodík", "Helium", "Kyslík"],
                            "correct_answer": "Vodík"
                        },
                        {
                            "text": "Kdo je autorem Harryho Pottera?",
                            "answers": ["J.K. Rowling", "Stephen King", "Philip Pullman"],
                            "correct_answer": "J.K. Rowling"
                        },
                        {
                            "text": "Jaký je symbol pro zlato?",
                            "answers": ["Au", "Ag", "Pb"],
                            "correct_answer": "Au"
                        },
                        {
                            "text": "Jak dlouho trvá den na Marsu?",
                            "answers": ["Přibližně 24 hodin a 37 minut", "24 hodin", "25 hodin"],
                            "correct_answer": "Přibližně 24 hodin a 37 minut"
                        },
                        {
                            "text": "Jaký je vzorec pro fotosyntézu?",
                            "answers": ["6CO2 + 6H2O -> C6H12O6 + 6O2", "C6H12O6 + 6O2 -> 6CO2 + 6H2O", "2H2 + O2 -> 2H2O"],
                            "correct_answer": "6CO2 + 6H2O -> C6H12O6 + 6O2"
                        }
                    ]
                },

                {
                    "questions": [
                        {
                            "text": "Jaký je nejhlubší oceán?",
                            "answers": ["Mariana Trench", "Tongská propast", "Filipínský příkop"],
                            "correct_answer": "Mariana Trench"
                        },
                        {
                            "text": "Kdo napsal 'Hamlet'?",
                            "answers": ["William Shakespeare", "Christopher Marlowe", "Ben Jonson"],
                            "correct_answer": "William Shakespeare"
                        },
                        {
                            "text": "Jaký je atomové číslo helia?",
                            "answers": ["2", "4", "1"],
                            "correct_answer": "2"
                        },
                        {
                            "text": "Jaký je název největšího jezera v Africe?",
                            "answers": ["Victoria", "Tanganyika", "Malawi"],
                            "correct_answer": "Victoria"
                        },
                        {
                            "text": "Co je hlavní město Austrálie?",
                            "answers": ["Canberra", "Sydney", "Melbourne"],
                            "correct_answer": "Canberra"
                        },
                        {
                            "text": "Kdo vyhrál fotbalové mistrovství světa v roce 2018?",
                            "answers": ["Francie", "Chorvatsko", "Belgie"],
                            "correct_answer": "Francie"
                        },
                        {
                            "text": "Jaký je vzorec pro sílu?",
                            "answers": ["F = ma", "F = mv", "F = m/a"],
                            "correct_answer": "F = ma"
                        }
                    ]
                },

                {
                    "questions": [
                        {
                            "text": "Kdo byl první člověk ve vesmíru?",
                            "answers": ["Jurij Gagarin", "Neil Armstrong", "John Glenn"],
                            "correct_answer": "Jurij Gagarin"
                        },
                        {
                            "text": "Jaký je nejdelší řeka na světě?",
                            "answers": ["Nil", "Amazonka", "Jang-c’-ťiang"],
                            "correct_answer": "Nil"
                        },
                        {
                            "text": "Jaké je hlavní město Brazílie?",
                            "answers": ["Brasília", "Rio de Janeiro", "São Paulo"],
                            "correct_answer": "Brasília"
                        },
                        {
                            "text": "Kdo napsal 'Sto roků samoty'?",
                            "answers": ["Gabriel García Márquez", "Mario Vargas Llosa", "Jorge Luis Borges"],
                            "correct_answer": "Gabriel García Márquez"
                        },
                        {
                            "text": "Jaký prvek má atomové číslo 1?",
                            "answers": ["Vodík", "Helium", "Lithium"],
                            "correct_answer": "Vodík"
                        },
                        {
                            "text": "Jaké je hlavní město Španělska?",
                            "answers": ["Madrid", "Barcelona", "Valencie"],
                            "correct_answer": "Madrid"
                        },
                        {
                            "text": "Jaký je chemický vzorec ethanolu?",
                            "answers": ["C2H5OH", "C2H6O", "CH3OH"],
                            "correct_answer": "C2H5OH"
                        }                      
                    ]
                }, 

                {                      
                    "questions": [
                        {
                            "text": "Co je kapitál Švýcarska?",
                            "answers": ["Bern", "Curych", "Ženeva"],
                            "correct_answer": "Bern"
                        },
                        {
                            "text": "Jaký film získal Oscara za nejlepší film v roce 2020?",
                            "answers": ["Parasite", "Joker", "1917"],
                            "correct_answer": "Parasite"
                        },
                        {
                            "text": "Jaký je vzorec pro výpočet rychlosti?",
                            "answers": ["v = s/t", "v = t/s", "v = st"],
                            "correct_answer": "v = s/t"
                        },
                        {
                            "text": "Která země vyrobila první automobil?",
                            "answers": ["Německo", "USA", "Francie"],
                            "correct_answer": "Německo"
                        },
                        {
                            "text": "Jaký je symbol pro železo?",
                            "answers": ["Fe", "Au", "Ag"],
                            "correct_answer": "Fe"
                        },
                        {
                            "text": "Kdo zpíval píseň 'Thriller'?",
                            "answers": ["Michael Jackson", "Prince", "Madonna"],
                            "correct_answer": "Michael Jackson"
                        },
                        {
                            "text": "Jaký je vzdálenost od Země k Měsíci?",
                            "answers": ["384 400 km", "150 000 km", "450 000 km"],
                            "correct_answer": "384 400 km"
                        }
                    ]
                },
                {                      
                    "questions" : [
                        {
                            "text": "Kdy byla založena SPŠE Ječná?",
                            "answers": ["1945", "1949", "1952"],
                            "correct_answer": "1949"
                        },
                        {
                            "text": "Který studijní obor není nabízen na SPŠE Ječná?",
                            "answers": ["Informační technologie", "Biochemie", "Robotika"],
                            "correct_answer": "Biochemie"
                        },
                        {
                            "text": "Jaký jedinečný certifikát mohou studenti na SPŠE Ječná získat?",
                            "answers": ["Cambridge English Certificate", "TOEFL", "IELTS"],
                            "correct_answer": "Cambridge English Certificate"
                        },
                        {
                            "text": "Jak se počítá bodové hodnocení uchazeče pro přijetí na SPŠE Ječná?",
                            "answers": ["Na základě známek a výsledků přijímací zkoušky", "Losování", "Výkon na pohovoru"],
                            "correct_answer": "Na základě známek a výsledků přijímací zkoušky"
                        },
                        {
                            "text": "Jaký je povinný požadavek na přihlášku na SPŠE Ječná kromě běžných dokumentů?",
                            "answers": ["Portfolio projektů", "Lékařský posudek", "Doporučující dopis"],
                            "correct_answer": "Lékařský posudek"
                        },
                        {
                            "text": "Jaké jsou dva hlavní specializační obory na SPŠE Ječná?",
                            "answers": ["Stavební inženýrství a chemie", "Informační technologie a elektrotechnika", "Právo a obchod"],
                            "correct_answer": "Informační technologie a elektrotechnika"
                        },
                        {
                            "text": "Kdy se obvykle konají dny otevřených dveří na SPŠE Ječná?",
                            "answers": ["Během léta", "Na začátku akademického roku", "Nikdy"],
                            "correct_answer": "Na začátku akademického roku"
                        }
                    ]
                }
            ]
    
    return random.choice(quizzes)
    


@secret.route('/jecnajevecna', methods=['GET', 'POST'])
def secret_route():
    """route pro zpracovani otazek z quizu"""
    if 'chosen_quiz' not in session:
        session['chosen_quiz'] = quizs_questions()
        session['correct_answers'] = 0
        session['question_index'] = 0
    else:
        chosen_quiz = session['chosen_quiz']

    if request.method == 'POST':
        current_question = chosen_quiz['questions'][session['question_index']]
        selected_answer = request.form.get('answer')
        correct_answer = current_question['correct_answer']
        
        if selected_answer == correct_answer:
            session['correct_answers'] += 1
        
        session['question_index'] += 1
        total_questions = len(chosen_quiz['questions'])
        
        if session['question_index'] >= total_questions:
            if session['correct_answers'] == total_questions:
                return redirect(url_for('secret.secret_reward'))
            else:
                flash('Zkus to znova! Neuhodl jsi všechny odpovědi správně.', 'warning')
                session.clear()  
                return redirect(url_for('secret.secret_route'))

    if session['question_index'] < len(session['chosen_quiz']['questions']):
        current_question = session['chosen_quiz']['questions'][session['question_index']]
        return render_template('admin/secret.html', question=current_question)

    flash('Došlo k chybě, začni znovu.', 'error')
    session.clear()
    return redirect(url_for('secret.secret_route'))

@secret.route('/jecnajevecna/reward', methods=['GET'])
def secret_reward():
    """odmena za uspesne splneni quizu"""
    score = session.get('correct_answers', 0)
    session.clear()
    return render_template("admin/results.html", score=score)