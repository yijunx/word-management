import jwt
from app.schemas.user import User
from flask import Request, abort
from flask import Request


def decode_token(token: str):
    try:
        data = jwt.decode(jwt=token, options={"verify_signature": False})
    except:
        abort(401, "Decode token error!")
    return data


def get_token_from_cookie(request: Request) -> str:
    token: str = request.cookies.get("token", None)
    return token


def get_token_from_authorization_header(request: Request) -> str:
    bearer_auth: str = request.headers.get("Authorization", None)
    if bearer_auth is None:
        return None
    token = bearer_auth.split(" ")[1]
    return token


def get_user_info_from_request(request: Request) -> User:
    """
    As the user-management will only issue httpOnly token,
    react frontend cannot get it. and chrome will only add the token
    in the cookie accompanying the request sent to the server.
    """
    token = get_token_from_cookie(request)
    if token is None:
        abort(401, "no token!!!")
    else:
        user = User(**decode_token(token=token))
        return user
