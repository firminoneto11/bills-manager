from typing import Protocol

from fastapi import FastAPI
from starlette.datastructures import State


class ApplicationMountProtocol(Protocol):
    path: str
    app: FastAPI
    name: str


class CustomAppState(State):
    _mounted_applications: list[ApplicationMountProtocol]


class ASGIApp(FastAPI):
    state: CustomAppState
