#!/usr/bin/env python3
"""
Example getmethatdawg agent - demonstrates basic usage
"""

import getmethatdawg

@getmethatdawg.expose(method="GET", path="/hello")
def greet(name: str = "world"):
    """Simple greeting endpoint"""
    return {"msg": f"Hello {name}"}

@getmethatdawg.expose(method="POST", path="/echo")
def echo(message: str):
    """Echo back a message"""
    return {"echo": message}

@getmethatdawg.expose(method="GET", path="/add")
def add(x: int, y: int):
    """Add two numbers"""
    return {"result": x + y}

@getmethatdawg.expose(method="POST", path="/calculate")
def calculate(x: float, y: float, operation: str = "add"):
    """Perform calculations"""
    if operation == "add":
        return {"result": x + y}
    elif operation == "subtract":
        return {"result": x - y}
    elif operation == "multiply":
        return {"result": x * y}
    elif operation == "divide":
        if y == 0:
            return {"error": "Division by zero"}
        return {"result": x / y}
    else:
        return {"error": f"Unknown operation: {operation}"}

@getmethatdawg.expose(method="GET", path="/info")
def info():
    """Get service information"""
    return {
        "service": "getmethatdawg-example-agent",
        "version": "1.0.0",
        "endpoints": [
            {"method": "GET", "path": "/hello", "description": "Simple greeting"},
            {"method": "POST", "path": "/echo", "description": "Echo message"},
            {"method": "GET", "path": "/add", "description": "Add two numbers"},
            {"method": "POST", "path": "/calculate", "description": "Calculator"},
            {"method": "GET", "path": "/info", "description": "Service info"}
        ]
    } 