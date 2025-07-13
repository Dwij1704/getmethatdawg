import os
import json
import random
from datetime import datetime
from typing import Dict, Any, Optional, List
import uuid

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
import google.genai as genai
import anthropic
from openai import OpenAI
from PIL import Image
import tempfile
import requests
from io import BytesIO
import base64

# Initialize API clients
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
anthropic_client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

# Optional: Initialize Google Gemini client  
google_client = None
if os.getenv('GOOGLE_API_KEY'):
    try:
        google_client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))
        print("✅ Google Gemini client initialized")
    except ImportError:
        print("⚠️  google-genai not installed, skipping Gemini support")
    except Exception as e:
        print(f"⚠️  Failed to initialize Gemini: {e}")

# Create storage directories
STORIES_DIR = "story_sessions"
IMAGES_DIR = "story_images"
AUDIO_DIR = "story_audio"

for directory in [STORIES_DIR, IMAGES_DIR, AUDIO_DIR]:
    os.makedirs(directory, exist_ok=True)

# Story genres and their characteristics
STORY_GENRES = {
    "fantasy": {
        "name": "🧙‍♂️ Fantasy Adventure",
        "description": "Magic, dragons, ancient quests, and mystical realms",
        "examples": ["enchanted forest", "wizard's tower", "dragon's lair", "magical academy"],
        "player_character": "A brave adventurer with leather armor, worn traveling cloak, and weathered boots. Medium height, determined expression, carrying a backpack and simple sword. Has an approachable, heroic appearance."
    },
    "sci_fi": {
        "name": "🚀 Science Fiction",
        "description": "Space exploration, alien encounters, future technology",
        "examples": ["space station", "alien planet", "cyberpunk city", "time machine"],
        "player_character": "A space explorer in a sleek tactical suit with glowing blue energy lines. Helmet with transparent visor, utility belt with futuristic gadgets. Athletic build, confident posture."
    },
    "mystery": {
        "name": "🕵️ Mystery Thriller",
        "description": "Detective work, hidden secrets, solving crimes",
        "examples": ["crime scene", "haunted mansion", "secret laboratory", "missing person case"],
        "player_character": "A sharp-eyed detective in a long coat and fedora. Professional attire, notepad in hand, magnifying glass. Observant facial expression, medium build."
    },
    "horror": {
        "name": "👻 Horror Survival",
        "description": "Supernatural frights, psychological tension, survival",
        "examples": ["abandoned asylum", "cursed forest", "ghost ship", "zombie outbreak"],
        "player_character": "A resilient survivor in worn jeans and a thick jacket. Flashlight in hand, cautious but determined expression. Practical clothing for survival situations."
    },
    "adventure": {
        "name": "🗺️ Action Adventure",
        "description": "Treasure hunting, exploration, daring escapes",
        "examples": ["pirate ship", "jungle temple", "mountain expedition", "underground cavern"],
        "player_character": "An intrepid explorer with khaki expedition gear, wide-brimmed hat, and climbing equipment. Confident smile, rope coiled at belt, sturdy hiking boots."
    },
    "steampunk": {
        "name": "⚙️ Steampunk Victorian",
        "description": "Steam-powered technology, Victorian era, airships",
        "examples": ["clockwork city", "flying machine", "steam laboratory", "mechanical beast"],
        "player_character": "A Victorian inventor in brass-buttoned coat with goggles on forehead. Mechanical arm gadgets, pocket watch, leather gloves. Distinguished appearance with steampunk accessories."
    }
}

def select_story_genre() -> Dict[str, Any]:
    """
    Allow player to select their preferred story genre.
    
    Returns:
        Dict containing genre selection info
    """
    try:
        print("\n🎭 CHOOSE YOUR ADVENTURE GENRE:")
        print("=" * 50)
        
        genres = list(STORY_GENRES.keys())
        for i, (key, genre) in enumerate(STORY_GENRES.items(), 1):
            print(f"{i}. {genre['name']}")
            print(f"   {genre['description']}")
            print(f"   Examples: {', '.join(genre['examples'])}")
            print()
        
        while True:
            try:
                choice = input("Enter your choice (1-6) or 'random' for surprise: ").strip().lower()
                
                if choice == 'random':
                    selected_key = random.choice(genres)
                    selected_genre = STORY_GENRES[selected_key]
                    print(f"\n🎲 Random selection: {selected_genre['name']}")
                    break
                elif choice.isdigit():
                    choice_num = int(choice)
                    if 1 <= choice_num <= len(genres):
                        selected_key = genres[choice_num - 1]
                        selected_genre = STORY_GENRES[selected_key]
                        print(f"\n✅ You chose: {selected_genre['name']}")
                        break
                    else:
                        print("❌ Please enter a number between 1-6")
                else:
                    print("❌ Please enter a number between 1-6 or 'random'")
            except ValueError:
                print("❌ Please enter a valid choice")
        
        return {
            "success": True,
            "genre_key": selected_key,
            "genre_data": selected_genre
        }
        
    except Exception as e:
        print(f"Error selecting genre: {e}")
        # Default to fantasy
        return {
            "success": True,
            "genre_key": "fantasy",
            "genre_data": STORY_GENRES["fantasy"]
        }

def is_simple_game_command(user_input: str) -> Dict[str, Any]:
    """
    Check if user input is a simple game command that doesn't need multimedia generation.
    
    Args:
        user_input: Player's input
        
    Returns:
        Dict with is_simple_command (bool) and response_type (str)
    """
    input_lower = user_input.lower().strip()
    
    # Simple game commands that only need text responses
    simple_commands = {
        # Inventory commands
        "check inventory": "inventory",
        "inventory": "inventory", 
        "what am i carrying": "inventory",
        "what do i have": "inventory",
        "my items": "inventory",
        "my stuff": "inventory",
        "show inventory": "inventory",
        
        # Character/stats commands
        "check stats": "stats",
        "my stats": "stats",
        "character sheet": "stats",
        "status": "stats",
        "health": "stats",
        
        # Help commands
        "help": "help",
        "commands": "help",
        "what can i do": "help",
        "options": "help",
        "how to play": "help",
        
        # Game state commands
        "save": "save_game",
        "save game": "save_game",
        "quit": "quit_game",
        "end game": "quit_game",
        "exit": "quit_game",
        
        # Information commands
        "where am i": "location_info",
        "look around": "location_info",
        "describe scene": "location_info",
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
    
    # Not a simple command - needs full story processing
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
        current_state: Current story state (JSON string or dict)
        genre: Current genre
        
    Returns:
        Dict with response text and metadata
    """
    try:
        # Parse current state - handle both string and dict inputs
        if current_state is None:
            state_dict = {
                "location": "starting_area",
                "inventory": [],
                "visited_rooms": [],
                "npcs_met": [],
                "npc_descriptions": {},  # Track NPC appearance for consistency
                "plot_progress": 0,
                "turn_count": 0,
                "genre": genre,
                "climax_approaching": False
            }
        elif isinstance(current_state, dict):
            # Already a dictionary - use directly
            state_dict = current_state.copy()
            # Ensure npc_descriptions exists for backward compatibility
            if "npc_descriptions" not in state_dict:
                state_dict["npc_descriptions"] = {}
        elif isinstance(current_state, str):
            # String input - could be empty or JSON
            if not current_state or current_state.strip() == "":
                state_dict = {
                    "location": "starting_area",
                    "inventory": [],
                    "visited_rooms": [],
                    "npcs_met": [],
                    "npc_descriptions": {},
                    "plot_progress": 0,
                    "turn_count": 0,
                    "genre": genre,
                    "climax_approaching": False
                }
            else:
                try:
                    state_dict = json.loads(current_state)
                    # Ensure npc_descriptions exists for backward compatibility
                    if "npc_descriptions" not in state_dict:
                        state_dict["npc_descriptions"] = {}
                except json.JSONDecodeError:
                    # Fallback to default state if JSON is corrupted
                    state_dict = {
                        "location": "starting_area",
                        "inventory": [],
                        "visited_rooms": [],
                        "npcs_met": [],
                        "npc_descriptions": {},
                        "plot_progress": 0,
                        "turn_count": 0,
                        "genre": genre,
                        "climax_approaching": False
                    }
        else:
            # Unknown type - use default
            state_dict = {
                "location": "starting_area",
                "inventory": [],
                "visited_rooms": [],
                "npcs_met": [],
                "npc_descriptions": {},
                "plot_progress": 0,
                "turn_count": 0,
                "genre": genre,
                "climax_approaching": False
            }
        
        if command_type == "inventory":
            inventory = state_dict.get("inventory", [])
            if not inventory:
                response_text = "🎒 **Your Inventory is Empty**\n\nYou're not carrying anything right now. Look around for useful items you can pick up!"
            else:
                items_list = "\n".join([f"• {item}" for item in inventory])
                response_text = f"🎒 **Your Inventory**\n\n{items_list}\n\nWhat would you like to do with these items?"
                
        elif command_type == "stats":
            response_text = f"""📊 **Character Status**

🏠 **Location:** {state_dict.get('location', 'Unknown')}
🎯 **Progress:** Turn {state_dict.get('turn_count', 0)}
🗺️ **Rooms Visited:** {len(state_dict.get('visited_rooms', []))}
👥 **NPCs Met:** {len(state_dict.get('npcs_met', []))}
📖 **Genre:** {STORY_GENRES.get(genre, {}).get('name', genre.title())}

{"🎭 **Approaching Climax!**" if state_dict.get('climax_approaching') else "🌟 **Adventure in Progress**"}"""

        elif command_type == "help":
            response_text = f"""🎮 **Game Master Help**

**Story Commands:**
• Choose numbered options (1, 2, 3) or describe your action
• Be creative! Try things like "examine the door" or "talk to the guard"

**Game Commands:**
• "check inventory" - see what you're carrying
• "my stats" - view character status  
• "look around" - get scene description
• "save game" - save your progress
• "quit" - end the adventure

**Tips:**
• Every choice matters and affects the story
• Collect items and talk to characters
• The story builds toward an exciting climax!

Ready to continue your {STORY_GENRES.get(genre, {}).get('name', genre)} adventure?"""

        elif command_type == "location_info":
            response_text = f"""📍 **Current Location**

You are currently in: **{state_dict.get('location', 'Unknown Location')}**

Turn: {state_dict.get('turn_count', 0)}
Genre: {STORY_GENRES.get(genre, {}).get('name', genre.title())}

{"🎭 The story is building toward its climax!" if state_dict.get('climax_approaching') else "🌟 Your adventure continues..."}

What would you like to do next?"""

        elif command_type == "save_game":
            response_text = "💾 **Game Saved Successfully!**\n\nYour adventure progress has been automatically saved. You can continue anytime!\n\nWhat would you like to do next?"
            
        elif command_type == "quit_game":
            response_text = f"""👋 **Thanks for Playing!**

You completed **{state_dict.get('turn_count', 0)} turns** of your {STORY_GENRES.get(genre, {}).get('name', genre)} adventure.

Your progress has been saved. Feel free to start a new adventure or continue this one later!

🌟 **Final Status:**
• Location: {state_dict.get('location', 'Unknown')}
• Items Found: {len(state_dict.get('inventory', []))}
• Areas Explored: {len(state_dict.get('visited_rooms', []))}

Until next time, adventurer!"""
            return {
                "success": True,
                "result": {
                    "scene_text": response_text,
                    "story_options": ["Start New Adventure", "Continue This Story", "Exit Game"],
                    "updated_state": state_dict,
                    "generate_image": False,
                    "generate_audio": False,
                    "end_of_game": True,
                    "simple_command": True
                }
            }
        
        else:
            response_text = "🤔 I'm not sure what you mean. Try 'help' for available commands or describe what you want to do in the story."
        
        return {
            "success": True,
            "result": {
                "scene_text": response_text,
                "story_options": [
                    "Continue the adventure",
                    "Check inventory", 
                    "Look around"
                ],
                "updated_state": state_dict,  # State unchanged for simple commands
                "generate_image": False,  # No image needed
                "generate_audio": False,  # No audio needed
                "end_of_game": False,
                "simple_command": True
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "result": {
                "scene_text": "Sorry, there was an error processing that command. Try 'help' for available options.",
                "story_options": ["Continue adventure", "Help", "Try again"],
                "updated_state": {},
                "generate_image": False,
                "generate_audio": False,
                "end_of_game": False,
                "simple_command": True
            }
        }

def generate_story_scene(current_state: str, user_input: str, story_context: str, genre: str) -> Dict[str, Any]:
    """
    Generate the next story scene with 3 options plus custom input.
    First checks if it's a simple game command before generating full multimedia story.
    
    Args:
        current_state: JSON string of current story state OR dict object
        user_input: Player's command or action
        story_context: Current story context and history
        genre: Story genre
    
    Returns:
        Dict containing scene text, options, updated state, and metadata
    """
    try:
        # First check if this is a simple game command
        command_check = is_simple_game_command(user_input)
        
        if command_check["is_simple_command"]:
            print(f"🎮 Processing simple game command: {command_check['command_type']}")
            return handle_simple_game_command(
                command_check["command_type"], 
                user_input, 
                current_state, 
                genre
            )
        
        # Continue with full story generation for story actions
        print(f"📖 Processing story action: {user_input}")
        
        # Handle current_state input - it could be a string, dict, or None/empty
        if current_state is None:
            state_dict = {
                "location": "starting_area",
                "inventory": [],
                "visited_rooms": [],
                "npcs_met": [],
                "npc_descriptions": {},  # Track NPC appearance for consistency
                "plot_progress": 0,
                "turn_count": 0,
                "genre": genre,
                "climax_approaching": False
            }
        elif isinstance(current_state, dict):
            # Already a dictionary - use directly
            state_dict = current_state.copy()
            # Ensure npc_descriptions exists for backward compatibility
            if "npc_descriptions" not in state_dict:
                state_dict["npc_descriptions"] = {}
        elif isinstance(current_state, str):
            # String input - could be empty or JSON
            if not current_state or current_state.strip() == "":
                state_dict = {
                    "location": "starting_area",
                    "inventory": [],
                    "visited_rooms": [],
                    "npcs_met": [],
                    "npc_descriptions": {},  # Track NPC appearance for consistency
                    "plot_progress": 0,
                    "turn_count": 0,
                    "genre": genre,
                    "climax_approaching": False
                }
            else:
                try:
                    state_dict = json.loads(current_state)
                    # Ensure npc_descriptions exists for backward compatibility
                    if "npc_descriptions" not in state_dict:
                        state_dict["npc_descriptions"] = {}
                except json.JSONDecodeError:
                    # Fallback to default state if JSON is corrupted
                    state_dict = {
                        "location": "starting_area",
                        "inventory": [],
                        "visited_rooms": [],
                        "npcs_met": [],
                        "npc_descriptions": {},
                        "plot_progress": 0,
                        "turn_count": 0,
                        "genre": genre,
                        "climax_approaching": False
                    }
        else:
            # Unknown type - use default
            state_dict = {
                "location": "starting_area",
                "inventory": [],
                "visited_rooms": [],
                "npcs_met": [],
                "npc_descriptions": {},
                "plot_progress": 0,
                "turn_count": 0,
                "genre": genre,
                "climax_approaching": False
            }
        
        # Update turn count
        state_dict["turn_count"] = state_dict.get("turn_count", 0) + 1
        
        # Determine if we should approach climax (randomly between turns 10-15)
        if state_dict["turn_count"] >= 10 and not state_dict.get("climax_approaching", False):
            if random.random() < 0.3:  # 30% chance each turn after turn 10
                state_dict["climax_approaching"] = True
        
        genre_info = STORY_GENRES.get(genre, STORY_GENRES["fantasy"])
        
        # Check for manual climax mode activation from web UI
        climax_mode_active = state_dict.get("climax_mode", False)
        climax_turns_remaining = 5
        
        if climax_mode_active:
            climax_turn_start = state_dict.get("climax_turn_start", state_dict["turn_count"])
            turns_elapsed = state_dict["turn_count"] - climax_turn_start
            climax_turns_remaining = max(1, 5 - turns_elapsed)
        
        # Build climax instruction based on mode
        climax_instruction = ""
        story_options_instruction = ""
        
        if climax_mode_active:
            climax_instruction = f"""**🎯 CLIMAX MODE ACTIVE - CRITICAL STORY DIRECTION:**
This story is in CLIMAX MODE and must conclude in approximately {climax_turns_remaining} more turns.

MANDATORY REQUIREMENTS:
1. Drive the story towards a SATISFYING CONCLUSION
2. Focus on resolving MAJOR PLOT POINTS and conflicts
3. Build towards a CLIMACTIC FINALE with high stakes
4. Make this scene DRAMATIC and INTENSE
5. Escalate tension and move towards resolution
6. NO side quests or diversions - stay focused on the main story arc

STORY OPTIONS MUST:
- Lead directly towards story resolution
- Focus on climactic confrontations or revelations  
- Avoid exploration or side activities
- Push towards final decision points
- Create dramatic tension and consequences"""

            story_options_instruction = """
**CLIMAX MODE STORY OPTIONS:**
Your 3 story options MUST be focused on reaching the climax and conclusion:
- Option 1: Direct confrontation or major action towards resolution
- Option 2: Dramatic revelation or key decision point
- Option 3: High-stakes choice that affects the story outcome
NO exploration, side quests, or casual activities allowed!"""

        elif state_dict.get("climax_approaching", False):
            climax_instruction = "**IMPORTANT: This story is approaching its CLIMAX. Make this scene dramatic and intense, building toward a major confrontation or revelation. The adventure should reach its peak within the next few turns.**"
        
        # Use Claude for narrative generation
        prompt = f"""You are "GameMaster," an expert interactive storyteller creating a {genre_info['name']} adventure.

**Current Story State:**
{json.dumps(state_dict, indent=2)}

**Story Context & History:**
{story_context}

**Player Action:**
{user_input}

**Genre:** {genre_info['name']} - {genre_info['description']}

{climax_instruction}

**Your Mission:**
1. Describe what happens next (150-200 words) using SIMPLE, CONVERSATIONAL language
2. Write like someone telling a story casually, not reading a book
3. Use everyday words, avoid fancy vocabulary
4. Update the story state based on player's action
5. Provide 3 engaging story options that drive the plot forward
6. Include image description for scene visualization
7. **IMPORTANT**: Track any NPCs in the scene - if new, provide appearance description; if existing, use consistent description

{story_options_instruction}

**Response Format (JSON):**
{{
  "scene_text": "Natural, conversational scene description using simple words...",
  "story_options": [
    "Option 1: Action-oriented choice",
    "Option 2: Investigation/dialogue choice", 
    "Option 3: Creative/unexpected choice"
  ],
  "updated_state": {{
    "location": "current location",
    "inventory": ["item1", "item2"],
    "visited_rooms": ["room1", "room2"],
    "npcs_met": ["npc1"],
    "npc_descriptions": {{
      "npc1": "Detailed physical description for visual consistency",
      "npc2": "Another NPC description if present"
    }},
    "plot_progress": 1,
    "turn_count": {state_dict["turn_count"]},
    "genre": "{genre}",
    "climax_approaching": {str(state_dict.get("climax_approaching", False)).lower()}
  }},
  "image_description": "Detailed visual description for {genre_info['name']} scene",
  "characters_in_scene": ["player", "npc1_name", "npc2_name"],
  "mood": "mysterious/exciting/calm/dramatic/tense",
  "generate_image": true,
  "generate_audio": true,
  "end_of_game": false
}}

**Character Consistency Rules:**
- For NEW NPCs: Add detailed physical description to npc_descriptions
- For EXISTING NPCs: Use the description from current npc_descriptions (don't change it)
- Always list characters present in "characters_in_scene" (include "player" if they're visible in the scene)
- Keep NPC descriptions consistent across all encounters

**State Management Rules:**
- PRESERVE all climax mode fields: climax_mode, climax_turn_start
- Keep existing npc_descriptions unchanged unless new NPCs are introduced
- Increment turn_count by 1 from current value

**Writing Style Guidelines:**
- Use simple words: "cool" not "magnificent", "weird" not "mysterious"
- Write conversationally: "So you're standing there..." "Then this happens..."
- Avoid flowery descriptions and complex vocabulary
- Make it sound like natural speech, not literature

Generate an engaging {genre} scene with natural, conversational language and consistent character descriptions!"""

        response = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1200,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result = json.loads(response.content[0].text)
        result["timestamp"] = datetime.now().isoformat()
        result["genre"] = genre
        
        return {
            "success": True,
            "result": result
        }
        
    except Exception as e:
        print(f"Error generating story scene: {e}")
        # Create safe fallback state
        fallback_state = {
            "location": "starting_area",
            "inventory": [],
            "visited_rooms": [],
            "npcs_met": [],
            "npc_descriptions": {},
            "plot_progress": 0,
            "turn_count": 1,
            "genre": genre,
            "climax_approaching": False,
            "climax_mode": False
        }
        
        return {
            "success": False,
            "error": str(e),
            "result": {
                "scene_text": "The mists of confusion swirl around you. Perhaps try a different approach?",
                "story_options": [
                    "Look around carefully",
                    "Call out for help", 
                    "Try to remember how you got here"
                ],
                "updated_state": fallback_state,
                "image_description": "A misty, uncertain scene",
                "mood": "mysterious",
                "generate_image": False,
                "generate_audio": False,
                "end_of_game": False
            }
        }

def generate_scene_image(image_description: str, mood: str, genre: str, characters_in_scene: Optional[List[str]] = None, npc_descriptions: Optional[Dict[str, str]] = None, session_id: Optional[str] = None, turn_number: Optional[int] = None) -> Dict[str, Any]:
    """
    Generate an image for the current scene with consistent character appearances using GPT-4o and image generation tool calling.
    
    Args:
        image_description: Description of what to visualize
        mood: Emotional tone for the image
        genre: Story genre for style consistency
        characters_in_scene: List of characters present in the scene
        npc_descriptions: Dict of NPC names to their physical descriptions
        session_id: Story session ID to find previous images for consistency
        turn_number: Current turn number
        
    Returns:
        Dict containing image data or error info
    """
    import io
    from PIL import Image as PILImage
    
    try:
        genre_info = STORY_GENRES.get(genre, STORY_GENRES["fantasy"])
        
        # Build character descriptions for the image
        character_prompt = ""
        if characters_in_scene:
            character_descriptions = []
            
            for character in characters_in_scene:
                if character == "player":
                    # Use consistent player character from genre
                    player_desc = genre_info.get("player_character", "A heroic adventurer")
                    character_descriptions.append(f"PLAYER CHARACTER: {player_desc}")
                elif npc_descriptions and character in npc_descriptions:
                    # Use stored NPC description for consistency
                    character_descriptions.append(f"{character.upper()}: {npc_descriptions[character]}")
                elif character != "player":
                    # Generic description for any unlisted characters
                    character_descriptions.append(f"{character.upper()}: Present in scene (maintain any previous appearance)")
            
            if character_descriptions:
                character_prompt = f"\n\nCHARACTERS IN SCENE:\n" + "\n".join(character_descriptions)
        
        # Find previous images for visual consistency
        previous_images = []
        reference_descriptions = []
        if session_id:
            try:
                # Look for recent images from this story session
                for filename in os.listdir(IMAGES_DIR):
                    if filename.startswith(f"scene_{genre}") and filename.endswith('.png'):
                        file_path = os.path.join(IMAGES_DIR, filename)
                        # Get last 2 images for consistency
                        if len(previous_images) < 2:
                            previous_images.append(file_path)
                
                # Sort by creation time, newest first
                previous_images.sort(key=lambda x: os.path.getctime(x), reverse=True)
                previous_images = previous_images[:2]  # Take only the 2 most recent
                
                # Limit to 1 reference image to save tokens
                if previous_images:
                    previous_images = previous_images[:1]  # Use only the most recent
                
                # Create descriptions of reference images for consistency
                if previous_images:
                    reference_descriptions.append("VISUAL CONSISTENCY REQUIREMENTS:")
                    reference_descriptions.append("- Maintain the same art style and color palette as previous scenes")
                    reference_descriptions.append("- Keep character appearances exactly the same if they appear again")
                    reference_descriptions.append("- Use consistent lighting and atmospheric mood")
                    reference_descriptions.append("- Ensure the image fits seamlessly in the same story world")
                
            except FileNotFoundError:
                pass
        
        # Create the comprehensive image generation prompt
        consistency_note = "\n".join(reference_descriptions) if reference_descriptions else ""
        
        enhanced_prompt = f"""Generate a stunning, high-quality illustration for an interactive {genre_info['name']} story scene.

SCENE DESCRIPTION: {image_description}

MOOD: {mood}
GENRE: {genre_info['name']} - {genre_info['description']}

{character_prompt}

{consistency_note}

STYLE REQUIREMENTS:
- Digital painting style with rich, vibrant colors
- {genre} art aesthetic with atmospheric lighting
- Cinematic composition like concept art for a premium {genre} video game
- Professional illustration quality with detailed but not overcrowded elements
- Immersive perspective that draws the viewer into the scene

TECHNICAL SPECS:
- High resolution and quality
- Detailed textures and lighting effects
- Balanced composition with clear focal points
- Rich color palette appropriate for {mood} mood

Create a masterpiece illustration that captures this {genre} scene perfectly."""

        print(f"🎨 Generating image with GPT-4o + gpt-image-1 model...")
        print(f"📷 Using {len(previous_images)} reference images for consistency...")
        
        # Method 1: Try using GPT-4o with tool calling for image generation
        try:
            # First, try GPT-4o with tool calling to generate the image
            messages = [
                {
                    "role": "system",
                    "content": f"""You are an expert digital artist creating illustrations for interactive storytelling. 

Your task is to generate a beautiful illustration using the image generation tool. You MUST call the image generation function to create the requested artwork.

Focus on:
1. Creating high-quality {genre} artwork
2. Following the detailed prompt instructions
3. Maintaining visual consistency with the story world
4. Using appropriate mood and atmosphere

Always call the image generation tool to create the requested illustration."""
                },
                {
                    "role": "user", 
                    "content": enhanced_prompt
                }
            ]
            
            # Add reference images if available for GPT-4o to understand context
            if previous_images:
                for img_path in previous_images:
                    try:
                        # Open and resize image to reduce token count
                        with PILImage.open(img_path) as img:
                            # Resize to much smaller size for reference (saves tokens)
                            img.thumbnail((256, 256), PILImage.Resampling.LANCZOS)
                            
                            # Convert to RGB if needed
                            if img.mode != 'RGB':
                                img = img.convert('RGB')
                            
                            # Save to bytes with high compression
                            img_bytes = io.BytesIO()
                            img.save(img_bytes, format='JPEG', quality=30, optimize=True)
                            img_bytes.seek(0)
                            
                            # Encode to base64
                            image_data = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
                            
                            messages.append({
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": f"Reference image for style consistency (low-res for context only):"
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{image_data}",
                                            "detail": "low"  # Use low detail to save tokens
                                        }
                                    }
                                ]
                            })
                            print(f"📷 Added compressed reference image: {os.path.basename(img_path)} (256x256, quality=30)")
                    except Exception as e:
                        print(f"⚠️ Could not load/compress reference image {img_path}: {e}")
            
            # Limit to only 1 reference image to further reduce tokens
            if len(previous_images) > 1:
                print(f"📷 Limiting to 1 reference image to reduce token usage")
            
            # Define the image generation tool for GPT-4o
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "generate_scene_image_tool",
                        "description": "Generate a high-quality illustration for the story scene",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "prompt": {
                                    "type": "string",
                                    "description": "Detailed prompt for image generation"
                                },
                                "style_notes": {
                                    "type": "string",
                                    "description": "Additional style and consistency notes"
                                }
                            },
                            "required": ["prompt"]
                        }
                    }
                }
            ]
            
            # Call GPT-4o with tool calling
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=tools,
                tool_choice="auto",
                max_tokens=1000
            )
            
            # Check if GPT-4o called the image generation tool
            if response.choices[0].message.tool_calls:
                tool_call = response.choices[0].message.tool_calls[0]
                if tool_call.function.name == "generate_scene_image_tool":
                    import json
                    args = json.loads(tool_call.function.arguments)
                    final_prompt = args.get("prompt", enhanced_prompt)
                    
                    print(f"✅ GPT-4o refined the prompt for image generation")
                    
                    # Now use the new gpt-image-1 model to generate the actual image
                    image_result = openai_client.images.generate(
                        model="gpt-image-1",
                        prompt=final_prompt,
                        size="1024x1024",
                        quality="high",
                        output_format="png"
                    )
                    
                    # Get the base64 image data
                    image_base64 = image_result.data[0].b64_json
                    
                    # Save locally with session info for consistency tracking
                    image_id = str(uuid.uuid4())
                    if session_id and turn_number:
                        image_filename = f"scene_{genre}_{session_id[:8]}_turn{turn_number}_{image_id[:8]}.png"
                    else:
                        image_filename = f"scene_{genre}_{image_id}.png"
                    image_path = os.path.join(IMAGES_DIR, image_filename)
                    
                    # Decode and save the image
                    with open(image_path, "wb") as f:
                        f.write(base64.b64decode(image_base64))
                    
                    print(f"🖼️  Generated scene image with GPT-4o + gpt-image-1: {image_filename}")
                    
                    return {
                        "success": True,
                        "image_filename": image_filename,
                        "image_path": image_path,
                        "image_base64": image_base64,
                        "genre": genre,
                        "consistency_maintained": len(previous_images) > 0,
                        "reference_images_used": len(previous_images),
                        "model_used": "gpt-4o + gpt-image-1",
                        "tool_used": "tool_calling + image_generation"
                    }
                else:
                    raise Exception("GPT-4o didn't call the image generation tool")
            else:
                raise Exception("GPT-4o didn't use tool calling")
                
        except Exception as gpt4o_error:
            print(f"⚠️ GPT-4o tool calling failed: {gpt4o_error}")
            print("🔄 Trying direct gpt-image-1 generation...")
            
            # Method 2: Direct gpt-image-1 generation as fallback
            try:
                image_result = openai_client.images.generate(
                    model="gpt-image-1",
                    prompt=enhanced_prompt,
                    size="1024x1024",
                    quality="high",
                    output_format="png"
                )
                
                # Get the base64 image data
                image_base64 = image_result.data[0].b64_json
                
                # Save locally
                image_id = str(uuid.uuid4())
                if session_id and turn_number:
                    image_filename = f"scene_{genre}_{session_id[:8]}_turn{turn_number}_{image_id[:8]}.png"
                else:
                    image_filename = f"scene_{genre}_{image_id}.png"
                image_path = os.path.join(IMAGES_DIR, image_filename)
                
                with open(image_path, "wb") as f:
                    f.write(base64.b64decode(image_base64))
                
                print(f"🖼️  Generated scene image with direct gpt-image-1: {image_filename}")
                
                return {
                    "success": True,
                    "image_filename": image_filename,
                    "image_path": image_path,
                    "image_base64": image_base64,
                    "genre": genre,
                    "consistency_maintained": len(previous_images) > 0,
                    "reference_images_used": len(previous_images),
                    "model_used": "gpt-image-1",
                    "tool_used": "direct_generation"
                }
                
            except Exception as gpt_image_error:
                print(f"⚠️ gpt-image-1 also failed: {gpt_image_error}")
                raise Exception(f"Both GPT-4o and gpt-image-1 failed")
        
    except Exception as e:
        print(f"❌ Error generating image: {e}")
        print("🔄 Falling back to DALL-E 3...")
        
        # Final fallback to DALL-E 3
        try:
            # Simple fallback prompt for DALL-E
            fallback_prompt = f"{image_description}. {genre_info['name']} art style, digital painting, atmospheric lighting, cinematic composition."
            
            image_response = openai_client.images.generate(
                model="dall-e-3",
                prompt=fallback_prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            
            # Download the image
            image_url = image_response.data[0].url
            img_response = requests.get(image_url)
            
            # Save locally
            image_id = str(uuid.uuid4())
            if session_id and turn_number:
                image_filename = f"scene_{genre}_{session_id[:8]}_turn{turn_number}_{image_id[:8]}.png"
            else:
                image_filename = f"scene_{genre}_{image_id}.png"
            image_path = os.path.join(IMAGES_DIR, image_filename)
            
            with open(image_path, 'wb') as f:
                f.write(img_response.content)
            
            print(f"🖼️  Generated fallback image with DALL-E 3: {image_filename}")
            
            return {
                "success": True,
                "image_filename": image_filename,
                "image_path": image_path,
                "image_url": image_url,
                "genre": genre,
                "consistency_maintained": False,
                "reference_images_used": 0,
                "model_used": "dall-e-3",
                "tool_used": "fallback",
                "note": "Fallback to DALL-E 3 due to GPT-4o/gpt-image-1 errors"
            }
            
        except Exception as fallback_error:
            print(f"❌ All methods failed: {fallback_error}")
            return {
                "success": False,
                "error": f"All image generation methods failed: {str(e)}, {str(fallback_error)}"
            }

def text_to_speech(text: str, emotion: str, genre: str) -> Dict[str, Any]:
    """
    Convert text to speech using OpenAI's TTS with simple voice selection.
    
    Args:
        text: Text to convert to speech
        emotion: Emotional tone for speech (unused for simplicity)
        genre: Story genre for voice selection
        
    Returns:
        Dict containing audio info or error
    """
    try:
        print(f"🎙️  Generating speech narration...")
        
        # Generate audio using OpenAI TTS
        audio_id = str(uuid.uuid4())
        audio_filename = f"narration_{genre}_{audio_id}.mp3"
        audio_path = os.path.join(AUDIO_DIR, audio_filename)
        
        # Simple voice selection based on genre
        voice_map = {
            "fantasy": "alloy",
            "sci_fi": "echo", 
            "mystery": "fable",
            "horror": "onyx",
            "adventure": "nova",
            "steampunk": "shimmer"
        }
        voice = voice_map.get(genre, "alloy")
        
        print(f"🎭 Using {voice} voice for {genre} genre...")
        
        # Generate speech using OpenAI TTS
        response = openai_client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text,
            speed=1.0
        )
        
        # Save audio file
        response.stream_to_file(audio_path)
        
        print(f"🔊 Generated narration: {audio_filename}")
        
        return {
            "success": True,
            "audio_filename": audio_filename,
            "audio_path": audio_path,
            "voice_used": voice,
            "genre": genre,
            "note": f"Simple TTS narration with {voice} voice"
        }
        
    except Exception as e:
        print(f"Error generating audio: {e}")
        
        return {
            "success": False,
            "error": str(e),
            "note": "TTS generation failed"
        }

def save_story_state(session_id: str, story_data: Dict[str, Any]) -> bool:
    """Save the current story state to file."""
    try:
        story_path = os.path.join(STORIES_DIR, f"{session_id}.json")
        with open(story_path, 'w') as f:
            json.dump(story_data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving story state: {e}")
        return False

def load_story_state(session_id: str) -> Optional[Dict[str, Any]]:
    """Load story state from file."""
    try:
        story_path = os.path.join(STORIES_DIR, f"{session_id}.json")
        if os.path.exists(story_path):
            with open(story_path, 'r') as f:
                return json.load(f)
        return None
    except Exception as e:
        print(f"Error loading story state: {e}")
        return None

def search_game_help(query: str) -> Dict[str, Any]:
    """
    Search for game help and tips.
    
    Args:
        query: Help query from player
        
    Returns:
        Dict containing help information
    """
    try:
        # Common game commands and help
        help_responses = {
            "commands": "Try: 'look around', 'examine [object]', 'take [item]', 'go [direction]', 'talk to [character]', 'use [item]'",
            "inventory": "Say 'check inventory' or 'what am I carrying?' to see your items",
            "help": "I'm your Game Master! Choose from the 3 options or describe what you want to do. Be creative!",
            "stuck": "Try the suggested options or think creatively. Every story has multiple paths!",
            "save": "Your progress is automatically saved. You can continue your adventure anytime!",
            "quit": "Say 'end game' or 'quit' when you're ready to finish your adventure.",
            "genre": "Each adventure has a unique genre with different themes and atmospheres.",
            "options": "Choose from the 3 suggested options or type your own creative action!"
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
            "help_text": "I'm here to guide your adventure! Choose from the 3 options or describe what you want to do. Ask about commands, options, or say 'help' for general assistance.",
            "topic": "general"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "help_text": "Help system temporarily unavailable."
        }

# Create the ADK tools
story_tool = FunctionTool(func=generate_story_scene)

image_tool = FunctionTool(func=generate_scene_image)

audio_tool = FunctionTool(func=text_to_speech)

help_tool = FunctionTool(func=search_game_help)

# Create the main storytelling agent
story_master = Agent(
    name="storytelling_game_master",
    model="gemini-2.0-flash",
    description="Interactive Storytelling Game Master creating immersive multi-genre adventures with images and audio.",
    instruction="""You are "GameMaster," an expert interactive storyteller creating immersive adventures.

**Core Mission:**
Create engaging, multi-modal storytelling experiences across different genres with rich narratives, images, and audio.

**Smart Command Processing:**
The system automatically detects two types of player input:

1. **Simple Game Commands** (handled automatically, no tools needed):
   - "check inventory", "my stats", "help", "save game", "quit"
   - These return immediate text responses without calling any tools
   - DO NOT call generate_story_scene for these - they're handled separately

2. **Story Actions** (require full tool processing):
   - Movement, combat, dialogue, exploration, item usage
   - These need generate_story_scene + multimedia generation

**For Story Actions Only:**
1. Call generate_story_scene tool with player's choice
2. If result has generate_image=true, call generate_scene_image tool
3. If result has generate_audio=true, call text_to_speech tool
4. Display the story and options clearly

**For Simple Commands:**
- The system handles these automatically with instant text responses
- No need to call any tools
- Player gets immediate feedback without waiting for LLM generation

**Response Format After Tool Calls:**
Always display story actions like this:

```
[Story text from generate_story_scene tool result]

🎯 WHAT WILL YOU DO NEXT?
1. [Option 1 from story result]
2. [Option 2 from story result]
3. [Option 3 from story result]
4. 💭 Custom Action - Describe what you want to do

Choose 1-4 or describe your action:
```

**Tool Call Pattern for Story Actions:**
1. First: generate_story_scene(current_state, user_input, story_context, genre)
2. If result.generate_image: generate_scene_image(result.image_description, result.mood, genre, result.characters_in_scene, result.updated_state.npc_descriptions)
3. If result.generate_audio: text_to_speech(result.scene_text, "neutral", genre)
4. Then display formatted response to player

**Key Rules:**
- Simple commands (inventory, help, stats) are handled instantly without tools
- Story actions always call the tools for multimedia generation  
- ALWAYS display the story text and 4 options after tool calls
- Keep the adventure engaging and immersive
- Generate images for new scenes and dramatic moments
- Generate clear, simple audio narration
- Track story progression toward climax

**Example Response for Story Action:**
"The ancient temple looms before you, its weathered stone steps disappearing into shadow. Intricate carvings of forgotten gods decorate the massive pillars, their eyes seeming to follow your every movement. A cool breeze carries the scent of incense and something far more sinister from within the depths. Your torch flickers, casting dancing shadows that make the carved figures appear almost alive.

🎯 WHAT WILL YOU DO NEXT?
1. Climb the steps and enter the temple boldly
2. Examine the carvings for hidden clues first
3. Search around the perimeter for another entrance
4. 💭 Custom Action - Describe what you want to do

Choose 1-4 or describe your action:"

**Example Response for Simple Command:**
Simple commands like "check inventory" get instant responses without calling tools:
"🎒 **Your Inventory**
• Ancient key
• Torch
• Healing potion

What would you like to do with these items?"

**Character Consistency Example:**
When generating images, the system maintains character consistency:
- Player: Fantasy adventurer with leather armor (same in every scene)
- Wizard Aldric: Elderly wizard with white beard, blue robes (consistent when he reappears)
- Guard Captain: Stern woman in plate armor (same appearance in multiple scenes)

This creates immersive visual storytelling where characters are recognizable across the adventure!

You efficiently balance instant responses for game commands with rich multimedia for story actions!""",
    tools=[story_tool, image_tool, audio_tool, help_tool]
) 