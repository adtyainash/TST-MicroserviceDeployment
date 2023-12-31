from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional
import json

router = APIRouter()

SECRET_KEY = "b7bf32a1e45548858e1e7ee19a5f0258c3bc05f870c53bca4c03d327cfdaaa09"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
# file_path = "users.json"

with open("users.json", "r") as json_file:
    db = json.load(json_file)

# db = {{
#         "user_id": 1,
#         "username": "nunu",
#         "name": "nunu",
#         "password_hash": "$2b$12$aM0eOR3rqJoVUND7cjenFeU4Pqp90Voo4e2DsVoGf.NfP/HVoOFCO",
#         "disabled": 0
#     }}

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCredentials(BaseModel):
    username: str
    password: str

class TokenData(BaseModel):
    username: str or None = None


class User(BaseModel):
    user_id: int 
    username: str
    password_preprocessed: str
    name: str or None = None
    disabled: bool or None = None

# class UserCreate():
#     user_id: int 
#     username: str
#     password_preprocessed: str
#     name: Optional[str] = None
#     disabled: Optional[bool] = None
#     password_hash: str

class UserCreate:
    def __init__(self, user_id: int, username: str, password_preprocessed: str,
                 password_hash: str, name: Optional[str] = None, disabled: Optional[bool] = None):
        self.user_id = user_id
        self.username = username
        self.password_preprocessed = password_preprocessed
        self.password_hash = password_hash
        self.name = name
        self.disabled = disabled


class UserInDB(User):
    password_hash: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl= 'token')

def read_users_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            users = json.load(file)
    except FileNotFoundError:
        users = {}
    return users

# Function to write user data to the JSON file
def write_users_to_file(file_path, users):
    with open(file_path, "w") as file:
        json.dump(users, file, indent=2)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_all_username(userlist: dict):
    user_arr = []
    for user in userlist:
        user_arr.append(user.lower())
    return user_arr


def get_user(userlist: dict, username: str):
    arr_username = get_all_username(db)
    if username.lower() in arr_username:
        user_data = userlist[username]
        return UserInDB(**user_data)
        
        
def authenticate_user(userlist: dict, username: str, password: str):
    user = get_user(userlist, username)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    
    return user

def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes = 10)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt # the access token


# get current user based on token
async def get_current_user(token: str = Depends(oauth_2_scheme)):
    credential_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, 
                                         detail="coud not validate user credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        # parse out the token and decode it
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        # check if the user exists
        if username is None:
            raise credential_exception
        # get the user data
        token_data = TokenData(username = username)
    except JWTError:
        raise credential_exception
    
    # checks if the user exists in the database
    user = get_user(db, username = token_data.username)
   
    if user is None:
        raise credential_exception
    
    return user

# check if the user is enabled or disabled
async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user

# writing tokens
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    
    access_token_expires = timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta= access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# get current user
@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

#Register a new user
@router.post('/register')
async def register_user(credentials: UserCredentials):
    username = credentials.username
    password = credentials.password

    users = read_users_from_file("users.json")
    last_user_id = max([user['user_id'] for user in users.values()], default=0)
    new_user_id = last_user_id + 1
    user_found = False

    for user in db:
        if username == user:
            user_found = True
    
    if not user_found:
        created_user = UserCreate(
            user_id=new_user_id,
            username=username,
            password_preprocessed="",
            password_hash=get_password_hash(password),
            disabled=False  # Assuming you want to set disabled to False by default
        )

        # Convert the created user to a dictionary
        final_new_user = vars(created_user)

        # Add the new user to the existing users
        users[username] = final_new_user

        # Write the updated user data back to the file
        write_users_to_file("users.json", users)

        return final_new_user

    else:
        return "Username or ID taken"


@router.get("/users/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": current_user.user_id, "owner": current_user}]