def greet(name: str = "World"):
    """Greet someone"""
    return {"greeting": f"Hello, {name}!"}

def calculate(x: float, y: float, operation: str = "add"):
    """Perform calculations"""
    if operation == "add":
        return {"result": x + y}
    elif operation == "multiply":
        return {"result": x * y}
    return {"error": "Unknown operation"}
