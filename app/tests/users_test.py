import pytest
import uuid
from fastapi.testclient import TestClient
from ..models.dto.user_register import UserRegister
from ..main import app
from random import randint
import json

client = TestClient(app)

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
    assert res.status_code == 400

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
    assert res.status_code == 400
    
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
    assert res.status_code == 400

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

    assert res2.status_code == 400

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

