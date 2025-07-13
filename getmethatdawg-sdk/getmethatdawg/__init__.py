"""
GetMeThatDawg SDK - Zero-config deploy for Python agents
"""

import functools
import inspect
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field

__version__ = "1.1.0"

@dataclass
class Endpoint:
    """Represents an exposed endpoint"""
    func: Callable
    method: str
    path: str
    auth: Optional[str] = None
    func_name: str = field(init=False)
    
    def __post_init__(self):
        self.func_name = self.func.__name__

class EndpointRegistry:
    """Global registry for exposed endpoints"""
    
    def __init__(self):
        self._endpoints: List[Endpoint] = []
    
    def register(self, endpoint: Endpoint):
        """Register an endpoint"""
        self._endpoints.append(endpoint)
    
    def get_endpoints(self) -> List[Endpoint]:
        """Get all registered endpoints"""
        return self._endpoints.copy()
    
    def clear(self):
        """Clear all registered endpoints"""
        self._endpoints.clear()

# Global registry instance
_registry = EndpointRegistry()

def expose(method: str = "GET", path: str = None, auth: Optional[str] = None):
    """
    Decorator to expose a function as a web endpoint.
    
    Args:
        method: HTTP method (GET, POST, PUT, DELETE, etc.)
        path: URL path (defaults to /function_name)
        auth: Authentication method (None, "basic", "bearer", etc.)
    
    Usage:
        @getmethatdawg.expose(method="GET", path="/hello")
        def greet(name: str = "world"):
            return {"msg": f"Hello {name}"}
    """
    def decorator(func: Callable):
        # Determine path if not provided
        endpoint_path = path if path is not None else f"/{func.__name__}"
        
        # Create endpoint and register it
        endpoint = Endpoint(
            func=func,
            method=method.upper(),
            path=endpoint_path,
            auth=auth
        )
        _registry.register(endpoint)
        
        # Return the original function unchanged
        return func
    
    return decorator

def get_registry() -> EndpointRegistry:
    """Get the global endpoint registry"""
    return _registry

def get_endpoints() -> List[Endpoint]:
    """Get all registered endpoints"""
    return _registry.get_endpoints()

# Export key functions and classes
__all__ = [
    "expose",
    "get_registry", 
    "get_endpoints",
    "Endpoint",
    "EndpointRegistry"
] 