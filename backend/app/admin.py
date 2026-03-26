from app.db import SessionLocal
from app.models.user import User
from app.utils.auth import hash_password

def create_admin_if_not_exists():
    db = SessionLocal()
    admin_email = "roccoempire2@example.com"
    admin_password = "pattubeta"  

    # Check if admin already exists
    admin = db.query(User).filter(User.email == admin_email).first()
    if not admin:
        new_admin = User(
            email=admin_email,
            password=hash_password(admin_password),
            role="admin"  # This is key
        )
        db.add(new_admin)
        db.commit()
        print(f" Admin created: {admin_email} / {admin_password}")
    else:
        print(f" Admin already exists: {admin_email}")

    db.close()