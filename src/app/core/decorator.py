from typing import Callable

from app.core.enum import EndpointType


def public(endpointFunction: Callable):
    setattr(endpointFunction, "endpointType", EndpointType.PUBLIC)
    return endpointFunction


def private(endpointFunction: Callable):
    setattr(endpointFunction, "endpointType", EndpointType.PRIVATE)
    return endpointFunction


def protected(endpointFunction: Callable):
    setattr(endpointFunction, "endpointType", EndpointType.PROTECTED)
    return endpointFunction
