"""
Simplified Storytelling Agent - Auto-Detection Demo
This version removes external dependencies to demonstrate getmethatdawg's auto-detection feature.
"""

import json
import random
from typing import Dict, Any, Optional, List

# Story genres and their characteristics
STORY_GENRES = {
    "fantasy": {
        "name": "🧙‍♂️ Fantasy Adventure",
        "description": "Magic, dragons, ancient quests, and mystical realms",
        "examples": ["enchanted forest", "wizard's tower", "dragon's lair", "magical academy"],
    },
    "sci_fi": {
        "name": "🚀 Science Fiction", 
        "description": "Space exploration, alien encounters, future technology",
        "examples": ["space station", "alien planet", "cyberpunk city", "time machine"],
    },
    "mystery": {
        "name": "🕵️ Mystery Thriller",
        "description": "Detective work, hidden secrets, solving crimes",
        "examples": ["crime scene", "haunted mansion", "secret laboratory", "missing person case"],
    }
}

def select_story_genre() -> Dict[str, Any]:
    """
    Allow player to select their preferred story genre.
    
    Returns:
        Dict containing genre selection info
    """
    try:
        genres = list(STORY_GENRES.keys())
        selected_key = random.choice(genres)
        selected_genre = STORY_GENRES[selected_key]
        
        return {
            "success": True,
            "genre_key": selected_key,
            "genre_data": selected_genre,
            "message": f"Selected {selected_genre['name']} adventure!"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "genre_key": "fantasy",
            "genre_data": STORY_GENRES["fantasy"]
        }

def is_simple_game_command(user_input: str) -> Dict[str, Any]:
    """
    Check if user input is a simple game command.
    
    Args:
        user_input: Player's input
        
    Returns:
        Dict with is_simple_command (bool) and response_type (str)
    """
    input_lower = user_input.lower().strip()
    
    # Simple game commands that only need text responses
    simple_commands = {
        "check inventory": "inventory",
        "inventory": "inventory", 
        "help": "help",
        "commands": "help",
        "save": "save_game",
        "quit": "quit_game",
        "where am i": "location_info",
        "look around": "location_info",
    }
    
    # Check for exact matches first
    if input_lower in simple_commands:
        return {
            "is_simple_command": True,
            "command_type": simple_commands[input_lower],
            "original_input": user_input
        }
    
    # Check for partial matches (contains keywords)
    for command, command_type in simple_commands.items():
        if command in input_lower:
            return {
                "is_simple_command": True,
                "command_type": command_type,
                "original_input": user_input
            }
    
    # Not a simple command
    return {
        "is_simple_command": False,
        "command_type": "story_action",
        "original_input": user_input
    }

def handle_simple_game_command(command_type: str, user_input: str, current_state: str, genre: str) -> Dict[str, Any]:
    """
    Handle simple game commands without multimedia generation.
    
    Args:
        command_type: Type of simple command
        user_input: Original user input
        current_state: Current story state
        genre: Current genre
        
    Returns:
        Dict with response text and metadata
    """
    try:
        if command_type == "inventory":
            response_text = "🎒 **Your Inventory is Empty**\n\nYou're not carrying anything right now. Look around for useful items!"
                
        elif command_type == "help":
            response_text = f"""🎮 **Game Master Help**

**Story Commands:**
• Choose numbered options (1, 2, 3) or describe your action
• Be creative! Try things like "examine the door" or "talk to the guard"

**Game Commands:**
• "check inventory" - see what you're carrying
• "look around" - get scene description
• "save game" - save your progress
• "quit" - end the adventure

Ready to continue your adventure?"""

        elif command_type == "location_info":
            response_text = f"""📍 **Current Location**

You are currently in: **Fantasy Adventure**

Genre: {STORY_GENRES.get(genre, {}).get('name', genre.title())}

🌟 Your adventure continues...

What would you like to do next?"""

        elif command_type == "save_game":
            response_text = "💾 **Game Saved Successfully!**\n\nYour adventure progress has been saved. What would you like to do next?"
            
        elif command_type == "quit_game":
            response_text = "👋 **Thanks for Playing!**\n\nUntil next time, adventurer!"
        
        else:
            response_text = "🤔 I'm not sure what you mean. Try 'help' for available commands."
        
        return {
            "success": True,
            "scene_text": response_text,
            "story_options": [
                "Continue the adventure",
                "Check inventory", 
                "Look around"
            ],
            "simple_command": True
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "scene_text": "Sorry, there was an error processing that command.",
            "simple_command": True
        }

def generate_story_scene(current_state: str, user_input: str, story_context: str, genre: str) -> Dict[str, Any]:
    """
    Generate the next story scene with 3 options.
    
    Args:
        current_state: Current story state
        user_input: Player's command or action
        story_context: Current story context and history
        genre: Story genre
    
    Returns:
        Dict containing scene text, options, updated state
    """
    try:
        # First check if this is a simple game command
        command_check = is_simple_game_command(user_input)
        
        if command_check["is_simple_command"]:
            return handle_simple_game_command(
                command_check["command_type"], 
                user_input, 
                current_state, 
                genre
            )
        
        # Generate story scene
        story_scenes = [
            "You find yourself at the entrance of a mysterious cave. Ancient runes glow faintly on the stone walls.",
            "A bustling marketplace spreads before you. Merchants call out their wares while travelers hurry past.",
            "You stand before a grand castle with towering spires reaching toward the cloudy sky.",
            "A peaceful forest clearing opens up, with a crystal-clear stream bubbling through moss-covered rocks.",
            "You discover an abandoned laboratory filled with strange glowing vials and mysterious equipment."
        ]
        
        scene_text = random.choice(story_scenes)
        
        options = [
            "Explore the area cautiously",
            "Approach boldly and investigate", 
            "Look for hidden secrets"
        ]
        
        return {
            "success": True,
            "scene_text": scene_text,
            "story_options": options,
            "updated_state": {"location": "adventure_scene", "turn_count": 1},
            "generate_image": False,
            "generate_audio": False,
            "end_of_game": False
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "scene_text": "An error occurred while generating the story.",
            "story_options": ["Try again", "Help", "Quit"],
            "updated_state": {}
        }

def save_story_state(session_id: str, story_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Save the current story state.
    
    Args:
        session_id: Unique session identifier
        story_data: Story data to save
        
    Returns:
        Dict with success status
    """
    try:
        # In a real implementation, this would save to a database or file
        return {
            "success": True,
            "session_id": session_id,
            "message": "Story state saved successfully",
            "saved_at": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to save story state"
        }

def load_story_state(session_id: str) -> Dict[str, Any]:
    """
    Load story state from session.
    
    Args:
        session_id: Session identifier
        
    Returns:
        Dict with story state or error
    """
    try:
        # In a real implementation, this would load from a database or file
        return {
            "success": True,
            "session_id": session_id,
            "story_data": {
                "location": "starting_area",
                "inventory": [],
                "turn_count": 0,
                "genre": "fantasy"
            },
            "message": "Story state loaded successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to load story state"
        }

def search_game_help(query: str) -> Dict[str, Any]:
    """
    Search for game help and tips.
    
    Args:
        query: Help query from player
        
    Returns:
        Dict containing help information
    """
    try:
        help_responses = {
            "commands": "Try: 'look around', 'examine [object]', 'take [item]', 'go [direction]'",
            "inventory": "Say 'check inventory' to see your items",
            "help": "I'm your Game Master! Choose from options or describe what you want to do.",
            "save": "Your progress is automatically saved. Continue anytime!",
            "quit": "Say 'quit' when you're ready to finish your adventure.",
        }
        
        query_lower = query.lower()
        for key, response in help_responses.items():
            if key in query_lower:
                return {
                    "success": True,
                    "help_text": response,
                    "topic": key
                }
        
        # Default help
        return {
            "success": True,
            "help_text": "I'm here to guide your adventure! Choose from options or describe what you want to do.",
            "topic": "general"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "help_text": "Help system temporarily unavailable."
        }

def get_story_genres() -> Dict[str, Any]:
    """
    Get available story genres.
    
    Returns:
        Dict with available genres
    """
    return {
        "success": True,
        "genres": STORY_GENRES,
        "total_genres": len(STORY_GENRES)
    } 