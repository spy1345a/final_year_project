from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from passlib.context import CryptContext
from jose import jwt, JWTError
from pydantic import BaseModel
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# ---------------- CONFIG ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "..", ".env")

load_dotenv(dotenv_path=ENV_PATH)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

DB_NAME = os.getenv("DATABASE_NAME", "users.db")
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, DB_NAME)}"

# ---------------- DATABASE ----------------
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")

Base.metadata.create_all(bind=engine)

# ---------------- SECURITY ----------------
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def create_access_token(data: dict, expires_minutes: int):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ---------------- SCHEMAS ----------------
class SignupRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    username: str
    role: str

# ---------------- DEPENDENCIES ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

# ---------------- APP ----------------
app = FastAPI(title="Auth API")

# ---------------- SIGNUP ----------------
@app.post("/signup")
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    validate_password(data.password)

    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(
        username=data.username,
        hashed_password=hash_password(data.password),
        role="user"
    )

    db.add(user)
    db.commit()

    return {"message": "Signup successful"}

# ---------------- LOGIN ----------------
@app.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.username == form_data.username
    ).first()

    if not user or not verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    token = create_access_token(
        data={"sub": user.username},
        expires_minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    return {"access_token": token}

# ---------------- PROFILE ----------------
@app.get("/profile", response_model=UserResponse)
def profile(user: User = Depends(get_current_user)):
    return {
        "username": user.username,
        "role": user.role
    }

#---------------PASSOWRD VALIDATION-------------------
def validate_password(password: str):
    if len(password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters long"
        )

    if len(password) > 256:
        raise HTTPException(
            status_code=400,
            detail="Password too long"
        )

    if not any(c.isalpha() for c in password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one letter"
        )

    if not any(c.isdigit() for c in password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one number"
        )

#--------------- USER LIST----------------
@app.get("/users")
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    users = db.query(User).all()

    return [
        {
            "id": u.id,
            "username": u.username,
            "role": u.role,
        }
        for u in users
    ]

#-------------- Prediction call -------------
class TextInput(BaseModel):
    text: str
from ai_intratation.ai_main import predict_text

@app.post("/predict")
def post_predict(data: TextInput):
    return predict_text(data.text)

