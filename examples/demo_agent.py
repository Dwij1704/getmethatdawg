#!/usr/bin/env python3
"""
Demo AI Agent for GetMeThatDawg
Demonstrates auto-detection and interactive setup features
"""

import json
import random
from datetime import datetime
import requests  # External dependency for HTTP requests
import pandas as pd  # External dependency for data analysis


def hello_world(name: str = "World"):
    """Simple greeting endpoint"""
    return {
        "message": f"Hello, {name}!",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }


def generate_quote():
    """Generate a random inspirational quote"""
    quotes = [
        "The best time to plant a tree was 20 years ago. The second best time is now.",
        "Your limitation—it's only your imagination.",
        "Push yourself, because no one else is going to do it for you.",
        "Great things never come from comfort zones.",
        "Dream it. Wish it. Do it."
    ]
    
    return {
        "quote": random.choice(quotes),
        "author": "Anonymous",
        "timestamp": datetime.now().isoformat()
    }


def analyze_text(text: str, sentiment: str = "auto"):
    """Analyze text sentiment (mock analysis)"""
    
    # Mock sentiment analysis
    positive_words = ["good", "great", "amazing", "wonderful", "excellent", "love", "happy"]
    negative_words = ["bad", "terrible", "awful", "hate", "sad", "angry", "disappointed"]
    
    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if sentiment == "auto":
        if positive_count > negative_count:
            detected_sentiment = "positive"
        elif negative_count > positive_count:
            detected_sentiment = "negative"
        else:
            detected_sentiment = "neutral"
    else:
        detected_sentiment = sentiment
    
    return {
        "text": text,
        "sentiment": detected_sentiment,
        "confidence": 0.85,
        "positive_words": positive_count,
        "negative_words": negative_count,
        "analysis_timestamp": datetime.now().isoformat()
    }


def create_task(title: str, description: str, priority: str = "medium", due_date: str = None):
    """Create a new task"""
    
    task_id = f"task_{random.randint(1000, 9999)}"
    
    task = {
        "id": task_id,
        "title": title,
        "description": description,
        "priority": priority,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "due_date": due_date
    }
    
    return {
        "success": True,
        "task": task,
        "message": f"Task '{title}' created successfully with ID {task_id}"
    }


def get_weather(city: str = "San Francisco"):
    """Get mock weather information"""
    
    # Mock weather data
    conditions = ["sunny", "cloudy", "rainy", "foggy"]
    temperature = random.randint(60, 85)
    
    return {
        "city": city,
        "temperature": f"{temperature}°F",
        "condition": random.choice(conditions),
        "humidity": f"{random.randint(30, 80)}%",
        "forecast": "Partly cloudy with a chance of brilliance",
        "last_updated": datetime.now().isoformat()
    } 