from backend.database import SessionLocal
from backend.models import Module

def seed_modules():
    db = SessionLocal()
    try:
        # Check if already seeded
        if db.query(Module).first():
            print("Modules already exist. Skipping seed.")
            return

        m1 = Module(
            title="Módulo 1: Entorno",
            description="Configuración de VSCode y Antigravity para el desarrollo de misiones.",
            video_url="https://www.youtube.com/embed/example1",
            xp_reward=50
        )
        db.add(m1)
        db.flush() # To get ID

        m2 = Module(
            title="Módulo 2: Python Core",
            description="Fundamentos de Python para automatización y backend.",
            video_url="https://www.youtube.com/embed/example2",
            xp_reward=100,
            prerequisite_id=m1.id
        )
        db.add(m2)
        db.flush()

        m3 = Module(
            title="Módulo 3: Git & GitHub",
            description="Control de versiones y colaboración en la red.",
            video_url="https://www.youtube.com/embed/example3",
            xp_reward=75,
            prerequisite_id=m2.id
        )
        db.add(m3)
        db.flush()

        m4 = Module(
            title="Módulo 4: Primer Repo",
            description="Despligue de tu primer repositorio público de RoleCraft.",
            video_url="https://www.youtube.com/embed/example4",
            xp_reward=150,
            prerequisite_id=m3.id
        )
        db.add(m4)
        
        db.commit()
        print("Initial modules seeded successfully.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding modules: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_modules()
