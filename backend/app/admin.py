
from app.db import AsyncSessionLocal 
from app.models.user import User
from app.utils.auth import hash_password
import logging

logger = logging.getLogger(__name__)

from sqlalchemy import select
from app.db import AsyncSessionLocal 
from app.models.user import User
from app.utils.auth import hash_password
import logging

logger = logging.getLogger(__name__)

async def create_admin_if_not_exists():
    admin_email = "rmpire2@example.com" 
    admin_password = "pattubeta"

    async with AsyncSessionLocal() as db:
        # Check if admin exists using ORM select
        result = await db.execute(select(User).where(User.email == admin_email))
        admin = result.scalar_one_or_none()  # returns User object or None

        if not admin:
            new_admin = User(
                email=admin_email,
                password=hash_password(admin_password),
                role="admin"
            )
            db.add(new_admin)
            await db.commit()
            await db.refresh(new_admin)
            logger.info(f"Admin created: {admin_email} / {admin_password}")
        else:
            logger.info(f"Admin already exists: {admin_email}")