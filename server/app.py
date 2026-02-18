"""
FutaDomWorld Chat - Proxy Server

Sits between the game client and the LLM provider.
- Keeps the real API key server-side (never shipped to players)
- Validates player subscription tokens
- Rate-limits requests per player
- Selects LLM backend via factory pattern (adapted from Yeah Buddy)
- Token-based chat history windowing (adapted from Yeah Buddy)
- Strips <think> tags from responses before returning to client
"""

import os
import time
import hashlib
import logging
from functools import wraps
from flask import Flask, request, jsonify

from llm_proxy import get_proxy
from token_windowing import get_encoder, window_chat_history

app = Flask(__name__)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# LLM CONFIGURATION -- adapted from Yeah Buddy's BotConfiguration model
# All values sourced from environment variables.
# ---------------------------------------------------------------------------

LLM_CONFIG = {
    "llm_type": os.environ.get("LLM_TYPE", "deepseek"),
    "llm_model_endpoint": os.environ.get(
        "LLM_ENDPOINT", "https://api.deepinfra.com/v1/openai"),
    "llm_model_api_key": os.environ.get("DEEPINFRA_API_KEY", ""),
    "llm_model_version": os.environ.get(
        "LLM_MODEL", "deepseek-ai/DeepSeek-V3-0324"),
    "initial_prompt_role": os.environ.get("INITIAL_PROMPT_ROLE", "system"),
    "max_tokens": int(os.environ.get("MAX_TOKENS", "300")),
    "temperature": float(os.environ.get("TEMPERATURE", "0.85")),
    "timeout": int(os.environ.get("LLM_TIMEOUT", "45")),
    "max_retries": int(os.environ.get("MAX_RETRIES", "5")),
}

CHAT_HISTORY_TOKEN_WINDOW = int(
    os.environ.get("CHAT_HISTORY_TOKEN_WINDOW", "4000"))

MAX_USER_MESSAGE_LENGTH = int(
    os.environ.get("MAX_USER_MESSAGE_LENGTH", "500"))

# Instantiate LLM proxy and tokenizer encoder on startup
llm = get_proxy(LLM_CONFIG)
encoder = get_encoder()

# ---------------------------------------------------------------------------
# AUTH / RATE LIMITING (unchanged from original)
# ---------------------------------------------------------------------------

TOKEN_SECRET = os.environ.get("TOKEN_SECRET", "CHANGE_ME_IN_PRODUCTION")
RATE_LIMIT_PER_MINUTE = int(os.environ.get("RATE_LIMIT_PER_MINUTE", "20"))

# In-memory stores (replace with Redis/DB in production)
valid_tokens = {}       # token -> {"player_id": str, "expires": float}
rate_limit_store = {}   # player_id -> [timestamp, ...]


def validate_token(token):
    """Validate a player's subscription token."""
    if token in valid_tokens:
        info = valid_tokens[token]
        if info["expires"] > time.time():
            return info["player_id"]
    return None


def check_rate_limit(player_id):
    """Check if player has exceeded rate limit."""
    now = time.time()
    window_start = now - 60

    if player_id not in rate_limit_store:
        rate_limit_store[player_id] = []

    rate_limit_store[player_id] = [
        t for t in rate_limit_store[player_id] if t > window_start
    ]

    if len(rate_limit_store[player_id]) >= RATE_LIMIT_PER_MINUTE:
        return False

    rate_limit_store[player_id].append(now)
    return True


def require_auth(f):
    """Decorator that checks for valid Authorization header."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing authorization token"}), 401

        token = auth_header[7:]
        player_id = validate_token(token)
        if not player_id:
            return jsonify({"error": "Invalid or expired subscription"}), 403

        if not check_rate_limit(player_id):
            return jsonify({
                "error": "Rate limit exceeded. Please wait a moment."
            }), 429

        request.player_id = player_id
        return f(*args, **kwargs)
    return decorated


# ---------------------------------------------------------------------------
# ROUTES
# ---------------------------------------------------------------------------

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok"})


@app.route("/v1/config", methods=["GET"])
def get_config():
    """
    Return client-relevant configuration.
    The client can fetch this on startup for informational purposes,
    but the server enforces the limits regardless.
    """
    return jsonify({
        "chat_history_token_window": CHAT_HISTORY_TOKEN_WINDOW,
        "max_user_message_length": MAX_USER_MESSAGE_LENGTH,
        "max_tokens": LLM_CONFIG["max_tokens"],
    })


@app.route("/v1/chat", methods=["POST"])
def chat():
    """
    Main chat endpoint. Accepts messages from the game client,
    applies token windowing, forwards to the LLM via the abstraction
    layer, strips <think> tags, and returns the clean response.

    Supports two payload formats for backward compatibility:

    NEW FORMAT (detected by presence of "user_message" key):
    {
        "system_prompt": "...",
        "messages": [{"role": "user"|"assistant", "content": "..."}],
        "user_message": "..."
    }

    OLD FORMAT (legacy -- messages array with system prompt baked in):
    {
        "messages": [{"role": "system"|"user"|"assistant", "content": "..."}],
        "temperature": 0.85,
        "max_tokens": 300
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing request body"}), 400

    # Detect payload format
    if "user_message" in data:
        return _handle_new_format(data)
    elif "messages" in data:
        return _handle_legacy_format(data)
    else:
        return jsonify({"error": "Missing 'messages' or 'user_message'"}), 400


def _handle_new_format(data):
    """
    New structured payload: system_prompt + messages (history) + user_message.
    Server handles token windowing, model selection, and think-tag parsing.
    """
    system_prompt = data.get("system_prompt", "")
    messages = data.get("messages", [])
    user_message = data.get("user_message", "")

    if not user_message:
        return jsonify({"error": "Missing user_message"}), 400

    # Token windowing -- adapted from Yeah Buddy's ModelContext
    windowed = window_chat_history(messages, CHAT_HISTORY_TOKEN_WINDOW, encoder)

    try:
        result = llm.query_model(system_prompt, windowed, user_message)
    except Exception as e:
        logger.error("LLM error: %s", e)
        return jsonify({
            "error": "AI service unavailable. Please try again later."
        }), 502

    if result.get("error"):
        logger.error("LLM returned error: %s", result["error"])
        return jsonify({
            "error": "AI service unavailable. Please try again later."
        }), 502

    if result.get("metrics"):
        logger.info("LLM metrics: %s", result["metrics"])

    return jsonify({"content": result["content"]})


def _handle_legacy_format(data):
    """
    Legacy payload format: messages array with system prompt as first message.
    Kept for backward compatibility with older game clients.
    Routes through the same LLM abstraction layer.
    """
    messages = data["messages"]
    if not messages:
        return jsonify({"error": "Empty messages array"}), 400

    # Extract system prompt from messages if present
    system_prompt = ""
    history = []
    user_message = ""

    for msg in messages:
        role = msg.get("role", "")
        content = msg.get("content", "")
        if role == "system":
            system_prompt = content
        elif role == "user":
            # Last user message is the current one
            if user_message:
                history.append({"role": "user", "content": user_message})
            user_message = content
        elif role == "assistant":
            history.append({"role": "assistant", "content": content})

    if not user_message:
        return jsonify({"error": "No user message found"}), 400

    # Apply token windowing to history
    windowed = window_chat_history(
        history, CHAT_HISTORY_TOKEN_WINDOW, encoder)

    try:
        result = llm.query_model(system_prompt, windowed, user_message)
    except Exception as e:
        logger.error("LLM error (legacy): %s", e)
        return jsonify({
            "error": "AI service unavailable. Please try again later."
        }), 502

    if result.get("error"):
        return jsonify({
            "error": "AI service unavailable. Please try again later."
        }), 502

    return jsonify({"content": result["content"]})


# ---------------------------------------------------------------------------
# TOKEN MANAGEMENT (admin endpoints - protect in production)
# ---------------------------------------------------------------------------

@app.route("/admin/create_token", methods=["POST"])
def create_token():
    """
    Create a subscription token for a player.
    In production, call this from your payment webhook.

    Expected JSON:
    {
        "admin_key": "...",
        "player_id": "...",
        "duration_days": 30
    }
    """
    data = request.get_json()
    admin_key = data.get("admin_key", "")

    if admin_key != os.environ.get("ADMIN_KEY", "CHANGE_ME"):
        return jsonify({"error": "Unauthorized"}), 403

    player_id = data.get("player_id", "")
    duration_days = data.get("duration_days", 30)

    if not player_id:
        return jsonify({"error": "Missing player_id"}), 400

    raw = f"{player_id}:{time.time()}:{TOKEN_SECRET}"
    token = hashlib.sha256(raw.encode()).hexdigest()

    valid_tokens[token] = {
        "player_id": player_id,
        "expires": time.time() + (duration_days * 86400),
    }

    return jsonify({
        "token": token,
        "player_id": player_id,
        "expires_in_days": duration_days,
    })


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    if not LLM_CONFIG["llm_model_api_key"]:
        print("WARNING: DEEPINFRA_API_KEY not set!")
    if TOKEN_SECRET == "CHANGE_ME_IN_PRODUCTION":
        print("WARNING: TOKEN_SECRET is default - change for production!")

    print(f"LLM type: {LLM_CONFIG['llm_type']}")
    print(f"LLM model: {LLM_CONFIG['llm_model_version']}")
    print(f"Token window: {CHAT_HISTORY_TOKEN_WINDOW}")

    port = int(os.environ.get("PORT", "8080"))
    debug = os.environ.get("DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
