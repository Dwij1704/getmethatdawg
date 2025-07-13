"""
Simple WANDB Test - Verify Observability Integration
A minimal example to test WANDB/weave integration without heavy dependencies.
"""

import os
import json
from datetime import datetime
from typing import Dict, Any

def hello_world() -> Dict[str, Any]:
    """
    Simple hello world endpoint to test basic functionality.
    
    Returns:
        Dict with greeting and timestamp
    """
    return {
        "message": "Hello from getmethatdawg with WANDB observability!",
        "timestamp": datetime.now().isoformat(),
        "wandb_enabled": bool(os.getenv('WANDB_API_KEY')),
        "status": "success"
    }

def get_environment_info() -> Dict[str, Any]:
    """
    Get information about the deployment environment.
    
    Returns:
        Dict with environment details
    """
    env_vars = {
        'WANDB_API_KEY': bool(os.getenv('WANDB_API_KEY')),
        'OPENAI_API_KEY': bool(os.getenv('OPENAI_API_KEY')),
        'PORT': os.getenv('PORT', '5000')
    }
    
    return {
        "environment": "production",
        "api_keys_present": env_vars,
        "wandb_observability": bool(os.getenv('WANDB_API_KEY')),
        "deployment_time": datetime.now().isoformat(),
        "message": "WANDB integration test successful!" if env_vars['WANDB_API_KEY'] else "No WANDB key found"
    }

def test_function_tracking(data: str = "test") -> Dict[str, Any]:
    """
    Test function to verify observability tracking.
    
    Args:
        data: Test data to process
        
    Returns:
        Dict with processing results
    """
    # Simulate some processing
    processed_data = data.upper()
    
    return {
        "input_data": data,
        "processed_data": processed_data,
        "function_name": "test_function_tracking",
        "tracked_with_weave": "This function should be automatically tracked with @weave.op()",
        "timestamp": datetime.now().isoformat()
    }

def calculate_something(x: int, y: int) -> Dict[str, Any]:
    """
    Simple calculation function to test observability.
    
    Args:
        x: First number
        y: Second number
        
    Returns:
        Dict with calculation results
    """
    result = x + y
    product = x * y
    
    return {
        "x": x,
        "y": y,
        "sum": result,
        "product": product,
        "operation": "addition and multiplication",
        "weave_tracking": "enabled" if os.getenv('WANDB_API_KEY') else "disabled"
    } 