import os
import json
import csv
import random
import requests
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response, session
from sqlalchemy import select

from backend.database import SessionLocal, engine, Base
from backend.models import User, Group, Module, UserModuleProgress
from backend.security import get_password_hash, verify_password, create_access_token, SECRET_KEY
from config import (MIN_XP_FOR_GIT, INITIAL_QUESTION_STOCK, 
                    RECHARGE_COINS_COST, STOCK_RECHARGE_TIME_H, XP_ROUND_DECIMALS)
import jwt

app = Flask(__name__)
# Configurations
app.config["SECRET_KEY"] = SECRET_KEY

# Dependency injection for DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Decorador JWT basado en cookies
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("access_token")
        if not token:
            return redirect(url_for('login'))
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            with SessionLocal() as db_session:
                user = db_session.execute(select(User).where(User.username == data['sub'])).scalars().first()
                if not user:
                    return redirect(url_for('login'))
                # Load necessary data before session closes or detach
                db_session.expunge(user)
        except jwt.ExpiredSignatureError:
            return redirect(url_for('login'))
        except jwt.InvalidTokenError:
            return redirect(url_for('login'))

        return f(user, *args, **kwargs)
    return decorated

@app.route("/")
def index():
    token = request.cookies.get("access_token")
    if token:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        with SessionLocal() as db:
            user = db.execute(select(User).where(User.username == username)).scalars().first()
            
            if not user or not verify_password(password, user.password_hash):
                return render_template("login.html", error="Credenciales inválidas")
                
            token = create_access_token({"sub": user.username, "role": user.role})
            
        resp = make_response(redirect(url_for('dashboard')))
        resp.set_cookie("access_token", token, httponly=True, max_age=3600*24)
        return resp
        
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        
        with SessionLocal() as db:
            existing = db.execute(select(User).where(User.username == username)).scalars().first()
            if existing:
                return render_template("register.html", error="El usuario ya existe")
                
            new_user = User(
                username=username, 
                email=email,
                password_hash=get_password_hash(password),
                role="aprendiz"
            )
            db.add(new_user)
            db.commit()
            
        return redirect(url_for("login"))
        
    return render_template("register.html")

@app.route("/logout")
def logout():
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie("access_token", "", expires=0)
    return resp

@app.route("/dashboard")
@token_required
def dashboard(current_user):
    # Role handler
    if current_user.role == "experto":
        return render_template("dashboard_experto.html", user=current_user)
    
    # Load role and skills info from JSON
    json_path = os.path.join(app.root_path, 'static', 'data', 'roles_info.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            roles_data = json.load(f)
    except Exception:
        roles_data = {"roles": {}, "universal_skills": []}

    # Render Aprendiz
    with SessionLocal() as db:
        available_groups = db.execute(select(Group).where(Group.status == "En desarrollo")).scalars().all()
        # expunge iterables to pass to template safely
        for g in available_groups:
            db.expunge(g)
            
        # Cargar datos de entrenamiento
        user_db = db.query(User).get(current_user.id)
        all_modules = db.query(Module).order_by(Module.id).all()
        user_progress = db.query(UserModuleProgress).filter_by(user_id=current_user.id).all()
        
        progress_map = {p.module_id: p.status for p in user_progress}
        
        modules_data = []
        for m in all_modules:
            status = progress_map.get(m.id, "locked")
            
            # Requisito especial para Módulo 2 (Git)
            if m.id == 3 and user_db.xp < MIN_XP_FOR_GIT:
                status = "locked"
            elif status == "locked":
                if not m.prerequisite_id or progress_map.get(m.prerequisite_id) == "completed":
                    status = "available"
            
            modules_data.append({
                "id": m.id,
                "title": m.title,
                "description": m.description,
                "status": status,
                "xp": m.xp_reward,
                "locked_by_xp": m.id == 3 and user_db.xp < MIN_XP_FOR_GIT
            })
            
        return render_template("dashboard_aprendiz.html", 
                               user=user_db, 
                               groups=available_groups, 
                               roles_info=roles_data.get("roles", {}),
                               universal_skills=roles_data.get("universal_skills", []),
                               modules=modules_data,
                               min_xp_git=MIN_XP_FOR_GIT)

import json
import csv
import random
from backend.models import Module, UserModuleProgress, User
from config import (MIN_XP_FOR_GIT, INITIAL_QUESTION_STOCK, 
                    RECHARGE_COINS_COST, STOCK_RECHARGE_TIME_H, XP_ROUND_DECIMALS)

@app.route("/entrenamiento")
@token_required
def training(current_user):
    with SessionLocal() as db:
        user_db = db.query(User).get(current_user.id)
        all_modules = db.query(Module).order_by(Module.id).all()
        user_progress = db.query(UserModuleProgress).filter_by(user_id=current_user.id).all()
        
        progress_map = {p.module_id: p.status for p in user_progress}
        
        modules_data = []
        for m in all_modules:
            status = progress_map.get(m.id, "locked")
            
            # Requisito especial para Módulo 2 (Git)
            if m.id == 3 and user_db.xp < MIN_XP_FOR_GIT:
                status = "locked"
            elif status == "locked":
                if not m.prerequisite_id or progress_map.get(m.prerequisite_id) == "completed":
                    status = "available"
            
            modules_data.append({
                "id": m.id,
                "title": m.title,
                "description": m.description,
                "status": status,
                "xp": m.xp_reward,
                "locked_by_xp": m.id == 3 and user_db.xp < MIN_XP_FOR_GIT
            })
            
        return render_template("entrenamiento.html", user=user_db, modules=modules_data, min_xp_git=MIN_XP_FOR_GIT)

@app.route("/evaluacion/<int:module_id>")
@token_required
def evaluation(current_user, module_id):
    with SessionLocal() as db:
        user_db = db.query(User).get(current_user.id)
        
        # Verificar recarga automática de stock por tiempo
        if user_db.question_stock == 0:
            diff = datetime.now() - user_db.last_stock_recharge
            if diff.total_seconds() >= STOCK_RECHARGE_TIME_H * 3600:
                user_db.question_stock = INITIAL_QUESTION_STOCK
                user_db.last_stock_recharge = datetime.now()
                db.commit()

        # Cargar preguntas desde CSV consolidado
        questions = []
        try:
            with open("preguntas.csv", mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                questions = [q for q in reader if q.get('Modulo') == str(module_id)]
                for q in questions:
                    if 'Pregunta' in q:
                        q['Pregunta'] = q['Pregunta'].replace('\\n', '\n')
        except Exception as e:
            return f"Error cargando preguntas: {e}", 500

        # Obtener o crear progreso
        progress = db.query(UserModuleProgress).filter_by(user_id=current_user.id, module_id=module_id).first()
        if not progress:
            progress = UserModuleProgress(user_id=current_user.id, module_id=module_id, status="available")
            db.add(progress)
            db.flush()

        if progress.status == "completed":
            return redirect(url_for('training'))

        # Inicializar cola si está vacía o nunca se ha evaluado
        if not progress.evaluation_queue:
            q_ids = list(range(len(questions)))
            random.shuffle(q_ids)
            progress.evaluation_queue = json.dumps(q_ids)
            db.commit()

        queue = json.loads(progress.evaluation_queue)
        if not queue:
            progress.status = "completed"
            db.commit()
            return redirect(url_for('training'))

        current_q_idx = queue[0]
        current_question = questions[current_q_idx]
        current_question['id'] = current_q_idx
        return render_template("evaluacion.html", user=user_db, question=current_question, 
                               remaining=len(queue), total=len(questions), stock=user_db.question_stock)

@app.route("/verify-answer/<int:module_id>", methods=["POST"])
@token_required
def verify_answer(current_user, module_id):
    answer = request.form.get("answer", "").strip()
    q_id = request.form.get("q_id") # Opcional, solo para Módulo 1
    
    with SessionLocal() as db:
        user_db = db.query(User).get(current_user.id)
        progress = db.query(UserModuleProgress).filter_by(user_id=current_user.id, module_id=module_id).first()
        module = db.query(Module).get(module_id)

        if user_db.question_stock <= 0:
            return jsonify({
                "success": False, 
                "message": "Stock agotado. Espera una hora o compra más.", 
                "out_of_stock": True,
                "correct": False,
                "xp": 0,
                "coins": 0,
                "completed": False,
                "stock": 0,
                "remaining": 0
            })

        success = False
        message = ""
        xp_gain = 0
        coin_gain = 0
        completed = False

        # --- Lógica para Módulo 1 y Examen de Inflexión (Evaluación Circular) ---
        if module_id in [0, 1]:
            if not q_id:
                return jsonify({"success": False, "message": "ID de pregunta faltante."})
            
            q_id = int(q_id)
            questions = []
            with open("preguntas.csv", mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                questions = [q for q in reader if q.get('Modulo') == str(module_id)]
            
            # Quitado sorted() temporal para que los índices originales mapeen 1 a 1 a la variable questions
            
            question = questions[q_id]
            expected = question['Correcta'].strip().upper()
            provided = answer.strip().upper()
            
            # 1. Corrección del Validador (Debug)
            print(f"\n[--- LOG DE EVALUACIÓN ---]")
            print(f"DEBUG: Intentando validar Pregunta ID: [{q_id}]")
            print(f"DEBUG: Usuario: '{provided}' | Esperado CSV: '{expected}'")
            
            # Si el tiempo se agota, es incorrecto pero con tratamiento especial
            is_timeout = (provided == "TIMEOUT")
            is_correct = (provided == expected) and not is_timeout
            
            xp_value = int(question['XP'])
            # Lógica de Validación (El Algoritmo Circular usando Session)
            queue = session.get('cola_preguntas', [])
            
            user_db.question_stock -= 1
            
            # Procesar acierto
            if is_correct:
                if q_id in queue:
                    queue.remove(q_id) # Elimina definitivamente de la sesión
                
                xp_gain = int(user_db.calculate_gain(xp_value))
                user_db.xp += xp_gain
                progress.current_streak += 1
                coin_gain = 5 + (progress.current_streak // 3) * 2
                user_db.coins += coin_gain
                success = True
                message = "Output Expected === True. Hash validado."
                print(f"-> ¡CORRECTO! +{xp_gain} XP")
                
            # Procesar Timeout
            elif is_timeout:
                if queue and queue[0] == q_id:
                    id_fallido = queue.pop(0)
                    queue.append(id_fallido)
                elif q_id in queue:
                    queue.remove(q_id)
                    queue.append(q_id)
                xp_gain = 0
                message = "Proceso abortado por exceder límite de TTL (Time-To-Live)."
                print("-> TIMEOUT. Movido al final de la cola.")
                
            # Procesar Error
            else:
                if queue and queue[0] == q_id:
                    id_fallido = queue.pop(0)
                    queue.append(id_fallido)
                elif q_id in queue:
                    queue.remove(q_id)
                    queue.append(q_id)
                
                xp_gain = -5
                user_db.xp = max(0, user_db.xp + xp_gain)
                progress.current_streak = 0
                message = f"Traceback (most recent call last):\nAssertionError: Expected {expected}, got {provided}"
                print(f"-> INCORRECTO. Penalización {xp_gain} XP. Movido al final de la cola.")

            # Guardamos la rotación en sesión y base de datos
            session['cola_preguntas'] = queue
            session.modified = True
            progress.evaluation_queue = json.dumps(queue)
            
            # 5. Prueba de Estrés:
            print(f"> Pregunta ID {q_id} resuelta. Quedan {len(queue)} en la cola")
            print(f"[-------------------------]\n")
            
            # Completar evaluación si la cola está vacía
            if not queue:
                completed = True
                progress.status = "completed"
                progress.completed_at = datetime.now().isoformat()
                if module_id == 0:
                    user_db.last_exam_attempt = datetime.now()
                    user_db.skill_backend = min(100, user_db.skill_backend + 5)

            final_stock = user_db.question_stock
            final_coins = user_db.coins
            db.commit()

            return jsonify({
                "success": True, 
                "correct": is_correct, 
                "completed": completed,
                "message": message, 
                "xp": xp_gain, 
                "coins": coin_gain,
                "stock": final_stock,
                "remaining": len(queue)
            })

        # --- Lógica para otros Módulos (2, 3, 4) ---
        if module_id not in [0, 1]:
            user_db.question_stock -= 1 # También consumen stock
            
            if module_id == 2: # Python (Ya cubierto por Módulo 1 en su nueva versión, pero mantenemos por si acaso)
                if "print" in answer.lower():
                    success = True
            elif module_id == 3: # Git/GitHub
                try:
                    res = requests.get(f"https://api.github.com/users/{answer}")
                    if res.status_code == 200:
                        success = True
                    else:
                        message = "Usuario de GitHub no encontrado."
                except:
                    message = "Error de conexión con GitHub."
            elif module_id == 4: # Repositorio
                if "github.com/" in answer and len(answer) > 20:
                    success = True
                else:
                    message = "URL de repositorio inválida."

            if success:
                if progress.status != "completed":
                    progress.status = "completed"
                    progress.completed_at = datetime.now().isoformat()
                    xp_gain = user_db.calculate_gain(module.xp_reward)
                    user_db.xp += xp_gain
                    user_db.coins += 50 # Premio gordo por completar módulo
                db.commit()
                return jsonify({
                    "success": True, 
                    "completed": True, 
                    "xp": xp_gain, 
                    "coins": 50,
                    "message": "¡Misión completada!",
                    "correct": True
                })
            
            db.commit()
            return jsonify({
                "success": False, 
                "message": message or "Validación fallida.",
                "xp": 0,
                "coins": 0,
                "correct": False
            })

@app.route("/onboarding/diagnostico")
@token_required
def diagnostic(current_user):
    with SessionLocal() as db:
        user_db = db.query(User).get(current_user.id)
        # Si ya hizo el diagnóstico inicial (selección), ir al examen
        if user_db.is_polyglot is not None:
             return redirect(url_for('inflection_exam'))
        return render_template("diagnostico.html", user=user_db)

@app.route("/tutorial/<int:module_id>")
@token_required
def view_tutorial(current_user, module_id):
    with SessionLocal() as db:
        user_db = db.query(User).get(current_user.id)
        if module_id == 1:
            return render_template("tutorial_entorno.html", user=user_db)
        return redirect(url_for('view_module', module_id=module_id))

@app.route("/save-diagnostic", methods=["POST"])
@token_required
def save_diagnostic(current_user):
    is_polyglot = request.form.get("is_polyglot") == "1"
    with SessionLocal() as db:
        user_db = db.query(User).get(current_user.id)
        user_db.is_polyglot = 1 if is_polyglot else 0
        db.commit()
    return redirect(url_for('inflection_exam'))

@app.route("/evaluacion-inflexion")
@token_required
def inflection_exam(current_user):
    with SessionLocal() as db:
        user_db = db.query(User).get(current_user.id)
        
        # Verificar recarga automática de stock por tiempo
        if user_db.question_stock == 0:
            diff = datetime.now() - user_db.last_stock_recharge
            if diff.total_seconds() >= STOCK_RECHARGE_TIME_H * 3600:
                user_db.question_stock = INITIAL_QUESTION_STOCK
                user_db.last_stock_recharge = datetime.now()
                db.commit()
        
        # 1. Verificar bloqueo de 24 horas (DESHABILITADO por solicitud para acceso ininterrumpido)
        # if user_db.last_exam_attempt:
        #     diff = datetime.now() - user_db.last_exam_attempt
        #     if diff.total_seconds() < 24 * 3600:
        #         hours_left = 24 - (diff.total_seconds() // 3600)
        #         return render_template("bloqueo_energia.html", user=user_db, hours=int(hours_left))

        # 2. Cargar preguntas consolidadas (Modulo 0)
        questions = []
        try:
            with open("preguntas.csv", mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                filtered_qs = [q for q in reader if q.get('Modulo') == '0']
                for index, q in enumerate(filtered_qs):
                    if 'Pregunta' in q:
                        q['Pregunta'] = q['Pregunta'].replace('\\n', '\n')
                    q['original_id'] = index  # Attach fixed original index
                    questions.append(q)
        except Exception as e:
            return f"Error en archivos de datos: {e}", 500

        # 3. Inicializar sesión de examen (Cola Progresiva)
        # Ordenamos por dificultad: Facil -> Media -> Dificil
        order = {"Facil": 0, "Media": 1, "Dificil": 2}
        sorted_qs = sorted(questions, key=lambda x: (order.get(x['Dificultad'].strip(), 3), x['Pregunta'].strip()))
        
        # Guardar en progreso de módulo especial (ID 0 para el test inicial)
        progress = db.query(UserModuleProgress).filter_by(user_id=current_user.id, module_id=0).first()
        if not progress:
            progress = UserModuleProgress(user_id=current_user.id, module_id=0, status="available")
            db.add(progress)
            db.flush()

        if progress.status == "completed":
            return redirect(url_for('training'))

        queue = session.get('cola_preguntas', [])
        
        # Recuperar de DB si session se limpió espontáneamente o es nueva
        if not queue and progress.evaluation_queue:
            try:
                queue = json.loads(progress.evaluation_queue)
                session['cola_preguntas'] = queue
                session.modified = True
            except:
                queue = []

        # Inicializar si nunca se ha jugado o está en 0 sin haber completado
        if not queue:
            # Guardamos la cola como los original_id en el orden ordenado de dificultad
            q_ids = [q['original_id'] for q in sorted_qs]
            session['cola_preguntas'] = q_ids
            session.modified = True
            progress.evaluation_queue = json.dumps(q_ids)
            db.commit()
            queue = q_ids

        # 2. Lógica de "Get Question"
        current_q_id = queue[0]
        # Devolverla encontrándola por su original_id desde la lista questions
        current_question = next((q for q in questions if q['original_id'] == current_q_id), None)
        if current_question is None:
            # Fallback en caso de corrupción extrema
            current_question = questions[0]
            current_q_id = 0
            
        current_question['id'] = current_q_id # Mantener ID de vista sincronizado

        return render_template("evaluacion.html", user=user_db, question=current_question, 
                               remaining=len(queue), total=len(questions), stock=user_db.question_stock, 
                               is_inflection=True)

@app.route("/buy-questions", methods=["POST"])
@token_required
def buy_questions(current_user):
    with SessionLocal() as db:
        user_db = db.query(User).get(current_user.id)
        if user_db.coins >= RECHARGE_COINS_COST:
            user_db.coins -= RECHARGE_COINS_COST
            user_db.question_stock += 10
            db.commit()
            return jsonify({"success": True, "new_stock": user_db.question_stock, "new_coins": user_db.coins})
        return jsonify({"success": False, "message": "Monedas insuficientes."})

@app.route("/entrenamiento_detalle/<int:module_id>")
@token_required
def view_module(current_user, module_id):
    with SessionLocal() as db:
        user_db = db.query(User).get(current_user.id)
        module = db.query(Module).get(module_id)
        if not module:
            return redirect(url_for('training'))
        
        # Check access (prerequisite)
        if module.prerequisite_id:
            prereq = db.query(UserModuleProgress).filter_by(user_id=current_user.id, module_id=module.prerequisite_id, status="completed").first()
            if not prereq:
                return redirect(url_for('training'))
        
        # Módulo 2 (Git) XP lock
        if module_id == 3 and user_db.xp < MIN_XP_FOR_GIT:
            return redirect(url_for('training'))
                
        progress = db.query(UserModuleProgress).filter_by(user_id=current_user.id, module_id=module_id).first()
        status = progress.status if progress else "available"
        return render_template("modulo_detalle.html", user=user_db, module=module, status=status)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    app.run(debug=True, port=8000)
