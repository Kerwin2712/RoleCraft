from backend.database import SessionLocal
from backend.models import Module

def seed_modules():
    db = SessionLocal()
    try:
        # Clear existing modules to ensure fresh seed with new URLs
        db.query(Module).delete()
        
        m1 = Module(
            title="Módulo 1: Entorno de Trabajo",
            description="Configuración profesional de VS Code y Antigravity para el desarrollo de misiones en Windows 10.",
            video_url="https://www.youtube.com/embed/VqCgcpAypFQ",
            xp_reward=50
        )
        db.add(m1)
        db.flush()

        m2 = Module(
            title="Módulo 2: Instalación de Python",
            description="Primeras líneas de código y ejecución de print('Hola Mundo') siguiendo los estándares de Microsoft.",
            video_url="https://www.youtube.com/embed/8DvywoWv6fI",
            xp_reward=100,
            prerequisite_id=m1.id
        )
        db.add(m2)
        db.flush()

        m3 = Module(
            title="Módulo 3: Git & GitHub",
            description="Instalación de Git, configuración de identidad y el corazón de la colaboración en la red.",
            video_url="https://www.youtube.com/embed/hiT6yA8GvEc",
            xp_reward=75,
            prerequisite_id=m2.id
        )
        db.add(m3)
        db.flush()

        m4 = Module(
            title="Módulo 4: Mi Primer Repositorio",
            description="Dominio de git init, add, commit y push para desplegar tu primer proyecto oficial.",
            video_url="https://www.youtube.com/embed/3GymExBkK_s",
            xp_reward=150,
            prerequisite_id=m3.id
        )
        db.add(m4)
        
        db.commit()
        print("Módulos oficiales actualizados y poblados con éxito.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding modules: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_modules()
