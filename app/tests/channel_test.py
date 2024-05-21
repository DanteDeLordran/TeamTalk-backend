from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
import pytest
from ..models.channel import Channel, ChannelRequest
from ..main import app
import random

client = TestClient(app)

valid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkxvcmRyYWFhYWFuIiwiZW1haWwiOiJsb3JkcmFuQGxvcmRyYW4uZGV2IiwiZXhwaXJhdGlvbiI6IjIwMjQtMDUtMjdUMjM6MTc6MDkuMDQwNTUzIn0.jhXr-S3jr2vPCyYWKqpMxVKONUaM08o3z4GFNVjF60s"
invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkxvcmRyYWFhYWFuIiwiZW1haWwiOiJsb3JkcmFuQGxvcmRyYW4uZGV2IiwiZXhwaXJhdGlvbiI6IjIwMjQtMDUtMTBUMjM6MTc6MDkuMDQwNTUzIn0.GQF1-Z6ASAEn6ccO296sGd4TDvtVJKdvGR1q1XfZmfg"
group_id = "6630ac50b5ac49018d63ea9a"

def test_create_channel_R1():
    request = ChannelRequest(
        channel_name=f"Canal R1 {random.randint(0,999)}",
        group_id=group_id
    )
    res = client.post(
        '/channels/create',
        headers={
            
        },
        json={
            'channel_name' : request.channel_name,
            'group_id': request.group_id
        }
    )
    assert res.status_code == 400
    
def test_create_channel_R2():
    request = ChannelRequest(
        channel_name=f"Canal R2 {random.randint(0,999)}",
        group_id=group_id
    )
    res = client.post(
        '/channels/create',
        headers={
            'token': invalid_token
        },
        json={
            'channel_name' : request.channel_name,
            'group_id': request.group_id
        }
    )
    assert res.status_code == 400

def test_create_channel_R3():
    request = ChannelRequest(
        channel_name=f"Java master",
        group_id=group_id
    )
    res = client.post(
        '/channels/create',
        headers={
            'token': valid_token
        },
        json={
            'channel_name' : request.channel_name,
            'group_id': request.group_id
        }
    )
    assert res.status_code == 400

def test_create_channel_R4():
    request = ChannelRequest(
        channel_name=f"Canal R4 {random.randint(0,99999)}",
        group_id=group_id
    )
    res = client.post(
        '/channels/create',
        headers={
            'token': valid_token
        },
        json={
            'channel_name' : request.channel_name,
            'group_id': request.group_id
        }
    )
    assert res.status_code == 201
    
def test_get_all_channels_R3():
    res = client.get(
        f'/channels/All/{group_id}',
        headers={
            'token': valid_token
        }
    )
    assert res.status_code == 200