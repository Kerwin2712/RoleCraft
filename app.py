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
    
    # Render Aprendiz
    with SessionLocal() as db:
        available_groups = db.execute(select(Group).where(Group.status == "En desarrollo")).scalars().all()
        # expunge iterables to pass to template safely
        for g in available_groups:
            db.expunge(g)
            
    return render_template("dashboard_aprendiz.html", user=current_user, groups=available_groups)

@app.route("/grupos/<int:group_id>/unirse", methods=["POST"])
@token_required
def join_group(current_user, group_id):
    if current_user.role != "aprendiz":
        return "No autorizado", 403
        
    with SessionLocal() as db:
        group = db.execute(select(Group).where(Group.id == group_id)).scalars().first()
        
        if not group:
            return "Grupo no encontrado", 404
            
        roles = group.vacant_roles or ""
        needs_pm = "PM" in roles or "Liderazgo" in roles
        
        has_pm_skill = current_user.skill_pm > 0
        if needs_pm and not has_pm_skill:
            db.expunge(group)
            return render_template("components/group_card.html", grupo=group, user=current_user, error="Requiere habilidad de Liderazgo")
            
        # Asignar
        current_user_db = db.execute(select(User).where(User.id == current_user.id)).scalars().first()
        current_user_db.group_id = group.id
        db.commit()
        
        # Actualizar la variable visual actual temporal
        current_user.group_id = group.id
        db.expunge(group)
        
    return render_template("components/group_card.html", grupo=group, user=current_user, joined=True)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    app.run(debug=True, port=8000)
