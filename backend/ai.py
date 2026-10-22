import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict, Optional

# Load environment variables
load_dotenv()

# Get AI provider configuration
AI_PROVIDER = os.getenv("AI_PROVIDER", "openrouter")  # 'openrouter' or 'ollama'
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:3b")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Initialize AI client (lazy initialization)
client = None
if AI_PROVIDER == "ollama":
    # Ollama doesn't require an API key, but OpenAI client needs one
    client = OpenAI(
        base_url=OLLAMA_BASE_URL,
        api_key="ollama",  # Dummy key for Ollama
    )
elif AI_PROVIDER == "openrouter" and OPENROUTER_API_KEY:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )


def call_ai(prompt: str, model: str = None) -> str:
    """
    Call the AI with a prompt and return the response.

    Args:
        prompt: The prompt to send to the AI
        model: The model to use (default depends on provider)

    Returns:
        The AI's response as a string

    Raises:
        ValueError: If AI client is not configured
        Exception: If the API call fails
    """
    if not client:
        raise ValueError("AI client is not configured. Set AI_PROVIDER environment variable.")

    # Use provider-specific default model if not specified
    if model is None:
        model = OLLAMA_MODEL if AI_PROVIDER == "ollama" else "openai/gpt-4o-mini"

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"AI call failed: {str(e)}")


def call_ai_with_board(
    message: str,
    board_data: Dict,
    conversation_history: Optional[List[Dict[str, str]]] = None,
    model: str = None
) -> Dict[str, any]:
    """
    Call the AI with board context and return structured output.

    Args:
        message: The user's message
        board_data: The current board data (columns and cards)
        conversation_history: Optional list of previous messages
        model: The model to use (default depends on provider)

    Returns:
        Dict with 'response' (string) and optional 'board_update' (dict)

    Raises:
        ValueError: If API key is not set
        Exception: If the API call fails
    """
    if not client:
        raise ValueError("AI client is not configured. Set AI_PROVIDER environment variable.")

    # Use provider-specific default model if not specified
    if model is None:
        model = OLLAMA_MODEL if AI_PROVIDER == "ollama" else "openai/gpt-4o-mini"

    # Build system prompt with board context
    system_prompt = """You are a helpful AI assistant for a Kanban board.
You MUST respond in valid JSON format with exactly these fields:
- "response": string (your text response to the user)
- "board_update": object or null (only include if user asks to modify the board)

If board_update is not null, it should have:
- "columns": array of column objects (each with id, title, cardIds)
- "cards": object with card IDs as keys (each card has id, title, details)

Example response:
{"response": "I can help with that.", "board_update": null}

Example with board update:
{"response": "I added a new card.", "board_update": {"columns": [...], "cards": {...}}}

Only include board_update if the user explicitly asks you to modify the board."""

    # Build messages
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "system", "content": f"Current board: {json.dumps(board_data)}"},
    ]

    # Add conversation history if provided
    if conversation_history:
        messages.extend(conversation_history)

    # Add current message
    messages.append({"role": "user", "content": message})

    try:
        # Ollama may not support response_format, so handle it conditionally
        if AI_PROVIDER == "ollama":
            response = client.chat.completions.create(
                model=model,
                messages=messages,
            )
        else:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                response_format={"type": "json_object"},
            )

        content = response.choices[0].message.content

        # Try to parse as JSON
        try:
            result = json.loads(content)
        except json.JSONDecodeError:
            # If not pure JSON, try to extract JSON from the response
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group(0))
            else:
                # Fallback: wrap the response in a valid JSON structure
                result = {"response": content, "board_update": None}

        # Ensure response field exists
        if "response" not in result:
            result["response"] = content

        return result
    except Exception as e:
        raise Exception(f"AI call failed: {str(e)}")
