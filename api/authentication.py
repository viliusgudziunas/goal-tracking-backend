# from flask import g
# from . import auth
# from .models import User
# from .errors import unauthorized


# @auth.verify_password
# def verify_password(email_or_token, password):
#     if email_or_token == "":
#         return False
#     if password == "":
#         g.current_user = User.verify_auth_token(email_or_token)
#         g.token_used = True
#         return g.current_user is not None
#     user = User.query.filter_by(email=email_or_token.lower()).first()
#     if not user:
#         return False
#     g.current_user = user
#     g.token_used = False
#     return user.verify_password(password)


# @auth.error_handler
# def auth_error():
#     return unauthorized("Invalid credentials")
