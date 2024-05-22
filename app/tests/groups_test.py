from fastapi.testclient import TestClient
from dotenv import load_dotenv
import uuid
import os
from ..main import app
import pytest

client = TestClient(app)
load_dotenv()

VALID_TOKEN = os.getenv("VALID_TOKEN")
INVALID_TOKEN_EXPIRED = os.getenv("INVALID_TOKEN_EXPIRED")

group_name = 'New Channel'

# MARK: Create Group Tests


def test_create_group_r1():
    uuid_str = str(uuid.uuid4())
    group = {
        'name': f'{group_name} {uuid_str}'
    }

    res = client.post('/groups/create',
                      json=group)
    
    message = res.json()['message']

    assert res.status_code == 400 and message == 'NOT_GIVEN_TOKEN'


def test_create_group_r2():
    uuid_str = str(uuid.uuid4())
    group = {
        'name': f'{group_name} {uuid_str}'
    }

    res = client.post('/groups/create',
                      headers={
                          'token': INVALID_TOKEN_EXPIRED
                      },
                      json=group)
    
    message = res.json()['message']

    assert res.status_code == 400 and message == 'NOT_VALID_TOKEN'


def test_create_group_r3():
    group = {
        'name': ''
    }

    res = client.post('/groups/create',
                      headers={
                          'token': VALID_TOKEN
                      },
                      json=group)

    print(res.json()) 
    message = str(res.json()['detail'][0]['type']).upper()

    assert res.status_code == 422 and message == 'STRING_TOO_SHORT'
    

def test_create_group_r4():
    uuid_str = str(uuid.uuid4())
    group = {
        'name': f'{group_name} {uuid_str}'
    }

    res = client.post('/groups/create',
                      headers={
                          'token': VALID_TOKEN
                      },
                      json=group)
    
    assert res.status_code == 200
    

def test_get_user_groups_r1():
    res = client.get('/groups/All')

    message = res.json()["message"]

    assert res.status_code == 400 and message == 'NOT_GIVEN_TOKEN'


def test_get_user_groups_r2():
    res = client.get('/groups/All',
                     headers={
                         'token': INVALID_TOKEN_EXPIRED
                     })
    
    message = res.json()["message"]

    assert res.status_code == 400 and message == 'NOT_VALID_TOKEN'


def test_get_user_groups_r3():
    res = client.get('/groups/All',
                     headers={
                         'token': VALID_TOKEN
                     })

    assert res.status_code == 200
