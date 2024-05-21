import pytest
import uuid
from fastapi.testclient import TestClient
from ..models.dto.user_register import UserRegister
from ..models.dto.user_login import UserLogin
from ..models.user import UserRequest
from ..main import app
from dotenv import load_dotenv
import os

load_dotenv()

VALID_TOKEN = os.getenv("VALID_TOKEN")
INVALID_TOKEN_EXPIRED = os.getenv("INVALID_TOKEN_EXPIRED")

client = TestClient(app=app)

# MARK:Register tests


def test_register_r1():
    uuid_str = str(uuid.uuid4()).replace('-', '.')
    register = UserRegister(
        name=f"",
        lastname="",
        username=f"AngelManzo{uuid_str}",
        email=f"angel.manzors{uuid_str}@uanl.edu.mx",
        password=""
    ).model_dump()

    res = client.post('/users/register', json=register)
    message = res.json()['message']

    assert res.status_code == 400 and message == 'SOME_EMPTY_FIELDS'


def test_register_r2():
    uuid_str = str(uuid.uuid4()).replace('-', '.')
    register = UserRegister(
        name="Angel",
        lastname="Manzo",
        username=f"AngelManzo{uuid_str}",
        email=f"angel.manzors{uuid_str}uanl.edu.mx",
        password="Str0ng3stP455!"
    ).model_dump()

    res = client.post('/users/register', json=register)
    message = res.json()['message']

    assert res.status_code == 400 and message == 'NOT_VALID_EMAIL'


def test_register_r3():
    uuid_str = str(uuid.uuid4()).replace('-', '.')
    register = UserRegister(
        name="Angel",
        lastname="Manzo",
        username=f"AngelManzo{uuid_str}",
        email=f"angel.manzors{uuid_str}@uanl.edu.mx",
        password="StrongestPass"
    ).model_dump()

    res = client.post('/users/register', json=register)
    message = res.json()['message']

    assert res.status_code == 400 and message == 'NOT_VALID_PASSWORD'


def test_register_r4():
    uuid_str = str(uuid.uuid4()).replace('-', '.')
    register = UserRegister(
        name=f"Angel",
        lastname="Manzo",
        username=f"AngelManzo{uuid_str}",
        email=f"angel.manzors{uuid_str}@uanl.edu.mx",
        password="Str0ng3rP455!"
    ).model_dump()

    print(register)

    res1 = client.post("/users/register", json=register)
    res2 = client.post("/users/register", json=register)

    message = res2.json()['message']

    assert res2.status_code == 400 and message == 'USER_EXISTS'


def test_register_r5():
    uuid_str = str(uuid.uuid4()).replace('-', '.')
    register = UserRegister(
        name=f"Angel",
        lastname="Manzo",
        username=f"AngelManzo{uuid_str}",
        email=f"angel.manzors{uuid_str}@uanl.edu.mx",
        password="Str0ng3rP455!"
    ).model_dump()

    print(register)

    res = client.post("/users/register", json=register)

    assert res.status_code == 201

# MARK: Login Tests


def test_login_r1():
    login = UserLogin(
        email="angel.manzorsuanl.edu.mx",
        password="Str0ng3stP455!"
    ).model_dump()

    res = client.post('/users/login', json=login)
    message = res.json()['message']

    assert res.status_code == 400 and message == 'NOT_VALID_EMAIL'


def test_login_r2():
    login = UserLogin(
        email="angel.manzors@uanl.edu.mx",
        password="WeakPassword"
    ).model_dump()

    res = client.post('/users/login', json=login)
    message = res.json()['message']

    assert res.status_code == 400 and message == 'NOT_VALID_PASSWORD'


def test_login_r3():
    login = UserLogin(
        email="thisuserdoesnotexist@gmail.com",
        password="Str0ng3stP455!"
    ).model_dump()

    res = client.post('/users/login', json=login)

    assert res.status_code == 404


def test_login_r4():
    uuid_str = str(uuid.uuid4()).replace('-', '.')
    register = UserRegister(
        name=f"Angel",
        lastname="Manzo",
        username=f"AngelManzo{uuid_str}",
        email=f"angel.manzors{uuid_str}@uanl.edu.mx",
        password="Str0ng3rP455!"
    ).model_dump()

    print(register)

    res_register = client.post("/users/register", json=register)

    login = UserLogin(
        email=register["email"],
        password=register["password"]
    ).model_dump()

    res_login = client.post("/users/login", json=login)
    assert res_login.status_code == 200

# MARK: Authenticate tests


def test_authenticate_r1():
    res = client.get("/users/authenticate")
    message = res.json()["message"]
    assert res.status_code == 400 and message == 'NOT_GIVEN_TOKEN'


def test_authenticate_r2():
    res = client.get("/users/authenticate",
                     headers={
                         "token": INVALID_TOKEN_EXPIRED
                     })

    message = res.json()["message"]

    assert res.status_code == 400 and message == 'NOT_VALID_TOKEN'


def test_authenticate_r3():
    res = client.get("/users/authenticate",
                     headers={
                         "token": VALID_TOKEN
                     }
                     )

    assert res.status_code == 200
    
# MARK: Edit User

user_request = UserRequest(
    name='Example',
    lastname='User',
    username='ExampleUser',
    email='example@gmail.com'
)

def test_edit_r1():
    user = user_request.model_dump()
    
    res = client.put('/users/edit', json=user)
    message = res.json()["message"]

    assert res.status_code == 400 and message == 'NOT_GIVEN_TOKEN'


def test_edit_r2():
    user = user_request.model_dump()

    res = client.put('/users/edit', 
                     headers={
                         'token': INVALID_TOKEN_EXPIRED
                     },
                     json=user)
    
    message = res.json()['message']
    assert res.status_code == 400 and message == 'NOT_VALID_TOKEN'


def test_edit_r3():
    user = user_request.model_dump()
    user["username"] = "ExistingUser"

    res = client.put('/users/edit',
                     headers={
                         'token': VALID_TOKEN
                     },
                     json = user)
    
    message = res.json()["message"]
    assert res.status_code == 400 and message == 'TAKEN_USERNAME'

def test_edit_r4():
    user = user_request.model_dump()
    user["email"] = "existinguser@gmail.com"

    res = client.put('/users/edit',
                     headers={
                         'token': VALID_TOKEN
                     },
                     json = user)
    
    message = res.json()["message"]
    assert res.status_code == 400 and message == 'TAKEN_EMAIL'


def test_edit_r5():
    user = user_request.model_dump()
    user["email"] = "existingusergmail.com"

    res = client.put('/users/edit',
                     headers={
                         'token': VALID_TOKEN
                     },
                     json = user)
    
    message = res.json()["message"]
    assert res.status_code == 400 and message == 'NOT_VALID_EMAIL'


def test_edit_r6():
    user = user_request.model_dump()

    res = client.put('/users/edit',
                     headers={
                         'token': VALID_TOKEN
                     },
                     json = user)
    
    assert res.status_code == 200
