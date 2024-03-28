from fastapi import FastAPI

from .classes import *
from .handlers import *


def register_all_exceptions(app: FastAPI):
    app.add_exception_handler(UserIsAlreadyExistsException, user_is_already_exists_handler)
    app.add_exception_handler(UnauthorizedException, unauthorized_handler)
    app.add_exception_handler(MissingRequiredParameterException, missing_required_parameter_handler)
    app.add_exception_handler(TokenInvalidException, token_invalid_handler)
    app.add_exception_handler(TokenExpiredException, token_expired_handler)
    app.add_exception_handler(PaymentNotFoundException, payment_not_found_handler)
    app.add_exception_handler(TicketNotFoundException, ticket_not_found_handler)
    app.add_exception_handler(RequestNotFoundException, request_not_found_handler)
    app.add_exception_handler(UserBalanceIsTooLowException, user_balance_is_too_low_handler)
    ...
