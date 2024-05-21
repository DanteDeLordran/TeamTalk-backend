from fastapi.testclient import TestClient
import pytest
from ..main import app
from ..models.message import Message, MessageRequest

client = TestClient(app)

valid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkxvcmRyYWFhYWFuIiwiZW1haWwiOiJsb3JkcmFuQGxvcmRyYW4uZGV2IiwiZXhwaXJhdGlvbiI6IjIwMjQtMDUtMjdUMjM6MTc6MDkuMDQwNTUzIn0.jhXr-S3jr2vPCyYWKqpMxVKONUaM08o3z4GFNVjF60s"
invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkxvcmRyYWFhYWFuIiwiZW1haWwiOiJsb3JkcmFuQGxvcmRyYW4uZGV2IiwiZXhwaXJhdGlvbiI6IjIwMjQtMDUtMTBUMjM6MTc6MDkuMDQwNTUzIn0.GQF1-Z6ASAEn6ccO296sGd4TDvtVJKdvGR1q1XfZmfg"
channel_id = "6630a9ea85fe4d6a14612389"
user_id = "6630a2a085fe4d6a14612387"


def test_send_message_R1():
    
    request = MessageRequest(
        channel_id=channel_id,
        user_id=user_id,
        message="Odio los lunes"
    )
    
    res = client.post(
        '/messages/send',
        headers={
            
        },
        json={
            'user_id': request.user_id,
            'message': request.message,
            'channel_id' : request.channel_id
        }
    )

    assert res.status_code == 400

def test_send_message_R2():
    
    request = MessageRequest(
        channel_id=channel_id,
        user_id=user_id,
        message="Odio los lunes"
    )
    
    res = client.post(
        '/messages/send',
        headers={
            'token': invalid_token
        },
        json={
            'user_id': request.user_id,
            'message': request.message,
            'channel_id' : request.channel_id
        }
    )
    
    assert res.status_code == 400

def test_send_message_R3():
    
    request = MessageRequest(
        channel_id=channel_id,
        user_id=user_id,
        message="Odio los lunes"
    )
    
    res = client.post(
        '/messages/send',
        headers={
            'token': valid_token
        },
        json={
            'user_id': request.user_id,
            'message': request.message,
            'channel_id' : request.channel_id
        }
    )
    
    assert res.status_code == 200

def test_get_messages_R1():
    
    res = client.get(
        f'/messages/get/{channel_id}',
        headers={
            
        }
    )
    
    assert res.status_code == 400
    
def test_get_messages_R2():
    
    res = client.get(
        f'/messages/get/{channel_id}',
        headers={
            'token' : invalid_token
        }
    )
    
    assert res.status_code == 400

def test_get_messages_R3():
    
    res = client.get(
        f'/messages/get/{channel_id}',
        headers={
            'token' : valid_token
        }
    )
    
    assert res.status_code == 200

