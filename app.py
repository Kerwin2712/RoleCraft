import os
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response
from sqlalchemy import select

from backend.database import SessionLocal, engine, Base
from backend.models import User, Group
from backend.security import get_password_hash, verify_password, create_access_token, SECRET_KEY
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
    import json
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
            
    return render_template("dashboard_aprendiz.html", 
                           user=current_user, 
                           groups=available_groups, 
                           roles_info=roles_data.get("roles", {}),
                           universal_skills=roles_data.get("universal_skills", []))

@app.route("/entrenamiento")
@token_required
def training(current_user):
    from backend.models import Module, UserModuleProgress
    with SessionLocal() as db:
        all_modules = db.query(Module).order_by(Module.id).all()
        user_progress = db.query(UserModuleProgress).filter_by(user_id=current_user.id).all()
        
        # Build progress map
        progress_map = {p.module_id: p.status for p in user_progress}
        
        modules_data = []
        for m in all_modules:
            status = progress_map.get(m.id, "locked")
            
            # Check if available (no prereq or prereq completed)
            if status == "locked":
                if not m.prerequisite_id or progress_map.get(m.prerequisite_id) == "completed":
                    status = "available"
            
            modules_data.append({
                "id": m.id,
                "title": m.title,
                "description": m.description,
                "status": status,
                "xp": m.xp_reward
            })
            
    return render_template("entrenamiento.html", user=current_user, modules=modules_data)

@app.route("/entrenamiento/<int:module_id>")
@token_required
def view_module(current_user, module_id):
    from backend.models import Module, UserModuleProgress
    with SessionLocal() as db:
        module = db.query(Module).get(module_id)
        if not module:
            return redirect(url_for('training'))
        
        # Check access
        if module.prerequisite_id:
            prereq = db.query(UserModuleProgress).filter_by(user_id=current_user.id, module_id=module.prerequisite_id, status="completed").first()
            if not prereq:
                return redirect(url_for('training'))
                
        progress = db.query(UserModuleProgress).filter_by(user_id=current_user.id, module_id=module_id).first()
        status = progress.status if progress else "available"
        
    return render_template("modulo_detalle.html", user=current_user, module=module, status=status)

@app.route("/entrenamiento/verificar/<int:module_id>", methods=["POST"])
@token_required
def verify_module(current_user, module_id):
    import requests
    from backend.models import Module, UserModuleProgress
    
    answer = request.form.get("answer", "").strip()
    
    with SessionLocal() as db:
        module = db.query(Module).get(module_id)
        if not module:
            return jsonify({"success": False, "message": "Módulo no encontrado"})
            
        success = False
        message = ""
        
        # Validation Logic per Module
        if module_id == 1: # Entorno
            if "version" in answer.lower() and "--version" in answer:
                success = True
            else:
                message = "Respuesta incorrecta. Pista: El comando incluye '--version'."
                
        elif module_id == 2: # Python
            # Basic syntax check for a simple print or calculation
            if "print" in answer or ("+" in answer or "*" in answer):
                success = True
            else:
                message = "Error de Sintaxis o script inválido."
                
        elif module_id == 3: # Git/GitHub
            # Verify GitHub user exists
            try:
                # In a real app, use environment variables for keys if needed, 
                # but public profile check doesn't necessarily need one for low rate limit
                res = requests.get(f"https://api.github.com/users/{answer}")
                if res.status_code == 200:
                    success = True
                else:
                    message = "Acceso Denegado: Usuario de GitHub no encontrado."
            except:
                message = "Fallo en la conexión con el servidor Git."
                
        elif module_id == 4: # Primer Repo
            if "github.com/" in answer and len(answer) > 20:
                success = True
            else:
                message = "URL de repositorio inválida o inaccesible."
        
        if success:
            progress = db.query(UserModuleProgress).filter_by(user_id=current_user.id, module_id=module_id).first()
            if not progress:
                progress = UserModuleProgress(user_id=current_user.id, module_id=module_id)
                db.add(progress)
            
            if progress.status != "completed":
                progress.status = "completed"
                progress.completed_at = datetime.now().isoformat()
                # Award XP
                user_db = db.query(User).get(current_user.id)
                user_db.xp += module.xp_reward
                db.commit()
                return jsonify({"success": True, "xp_gain": module.xp_reward})
            else:
                return jsonify({"success": True, "message": "Módulo ya completado previamente."})
                
        return jsonify({"success": False, "message": message})

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    app.run(debug=True, port=8000)
