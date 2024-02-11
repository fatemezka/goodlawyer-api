import os
from fastapi import Request, Depends, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.token_operator import token_parser
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.error_handler import ErrorHandler
from app.api.v1.user.user_controller import UserController
from app.api.v1.lawyer.lawyer_controller import LawyerController


class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print("CustomMiddleware applied.")
        # db = get_db()

        if request.url.path.startswith("/specific-api") and request.method == "POST":
            # if route needs lawyer's auth
            if ():
                await self.lawyer_authenticate(request)
            # if route only needs user's auth
            else:
                await self.user_authenticate(request)

        # Continue processing the request
        response = await call_next(request)
        return response

    async def user_authenticate(self, request: Request):
        try:
            AUTH_HEADER_NAME = os.getenv("AUTH_HEADER_NAME")
            if AUTH_HEADER_NAME not in request.headers:
                ErrorHandler.user_unauthorized()  # TODO

            decode = token_parser(request)
            token_user_id = decode["user_id"]
            token_lawyer_id = decode["lawyer_id"]
            token_is_lawyer = decode["is_lawyer"]

            # db = get_db()
            # user_controller = UserController(db)
            # find_user = user_controller.get_by_id(token_user_id)

            # if not find_user:
            #     ErrorHandler.not_found("User") # TODO
            #     return

            # assign token's data to the request
            request.user_id = token_user_id
            request.lawyer_id = token_lawyer_id
            request.is_lawyer = token_is_lawyer

            print("User Authentication middleware applied")
        except:
            ErrorHandler.user_unauthorized()  # TODO
            return

    async def lawyer_authenticate(self, request: Request):
        try:
            AUTH_HEADER_NAME = os.getenv("AUTH_HEADER_NAME")
            if AUTH_HEADER_NAME not in request.headers:
                ErrorHandler.user_unauthorized()  # TODO

            decode = token_parser(request)
            token_user_id = decode["user_id"]
            token_lawyer_id = decode["lawyer_id"]
            token_is_lawyer = decode["is_lawyer"]

            if not token_is_lawyer:
                ErrorHandler.lawyer_unauthorized()  # TODO

            # db = get_db()
            # lawyer_controller = LawyerController(db)
            # find_lawyer = lawyer_controller.get_by_id_and_user_id(
            #     token_lawyer_id, token_user_id)

            # if not find_lawyer:
            #     ErrorHandler.not_found("Lawyer")
            #     return

            # assign token's data to the request
            request.user_id = token_user_id
            request.lawyer_id = token_lawyer_id
            request.is_lawyer = token_is_lawyer

            print("Lawyer Authentication middleware applied")
        except:
            ErrorHandler.unauthorized()  # TODO
            return
