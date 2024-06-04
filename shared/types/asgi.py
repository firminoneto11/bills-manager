from fastapi import FastAPI
from starlette.datastructures import State


class CustomAppState(State):
    _mounted_applications: list[FastAPI]


class ASGIApp(FastAPI):
    state: CustomAppState
