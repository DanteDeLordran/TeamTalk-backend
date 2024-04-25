from fastapi import Response
from starlette.status import *
import json

def not_given_token():
    return Response(
        status_code=HTTP_400_BAD_REQUEST,
        media_type='application/json',
        content=json.dumps({"message": "NOT_GIVEN_TOKEN"})
    )

def not_valid_token():
    return Response(
        status_code=HTTP_400_BAD_REQUEST,
        media_type='application/json',
        content=json.dumps({"message": "NOT_VALID_TOKEN"})
    )
