from fastapi import FastAPI


def _route():
    ...


def register__routes(app: FastAPI):
    app.add_route("GET", "...", ...)
