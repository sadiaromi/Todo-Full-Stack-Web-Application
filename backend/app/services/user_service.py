from sqlmodel import Session, select
from typing import Optional
import uuid
from passlib.context import CryptContext

from ..models.user import User, UserBase
from ..utils.password import verify_password, get_password_hash


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, email: str, password: str) -> User:
        """Create a new user with hashed password."""
        password_hash = get_password_hash(password)
        user = User(email=email, password_hash=password_hash)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by their email address."""
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()

    def get_user_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """Get a user by their ID."""
        statement = select(User).where(User.id == user_id)
        return self.session.exec(statement).first()

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate a user by email and password."""
        user = self.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user