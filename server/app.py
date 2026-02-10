"""
FutaDomWorld Chat - Proxy Server
Sits between the game client and DeepInfra API.
- Keeps the real API key server-side (never shipped to players)
- Validates player subscription tokens
- Rate-limits requests per player
- Forwards chat completions to DeepInfra
"""

import os
import time
import hashlib
import json
from functools import wraps
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ---------------------------------------------------------------------------
# CONFIGURATION - Set via environment variables
# ---------------------------------------------------------------------------
DEEPINFRA_API_KEY = os.environ.get("DEEPINFRA_API_KEY", "")
DEEPINFRA_URL = "https://api.deepinfra.com/v1/openai/chat/completions"
DEEPINFRA_MODEL = os.environ.get("DEEPINFRA_MODEL", "deepseek-ai/DeepSeek-V3-0324")

# Secret used to sign/validate player tokens. Generate a random one for production.
TOKEN_SECRET = os.environ.get("TOKEN_SECRET", "CHANGE_ME_IN_PRODUCTION")

# Rate limiting: max requests per player per minute
RATE_LIMIT_PER_MINUTE = int(os.environ.get("RATE_LIMIT_PER_MINUTE", "20"))

# Max tokens per response
MAX_TOKENS = int(os.environ.get("MAX_TOKENS", "300"))

# ---------------------------------------------------------------------------
# IN-MEMORY STORES (replace with Redis/DB in production)
# ---------------------------------------------------------------------------

# Valid subscription tokens: token -> {"player_id": str, "expires": float}
# In production, check against your payment provider / database
valid_tokens = {}

# Rate limit tracking: player_id -> [timestamp, timestamp, ...]
rate_limit_store = {}


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def validate_token(token):
    """
    Validate a player's subscription token.

    In production, replace this with a database lookup or payment
    provider check (Stripe, etc.)
    """
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

    # Clean old entries
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
            return jsonify({"error": "Rate limit exceeded. Please wait a moment."}), 429

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


@app.route("/v1/chat", methods=["POST"])
@require_auth
def chat():
    """
    Main chat endpoint. Accepts messages from the game client,
    forwards to DeepInfra, returns the response.

    Expected JSON body:
    {
        "messages": [{"role": "system"|"user"|"assistant", "content": "..."}],
        "temperature": 0.85,    // optional
        "max_tokens": 300       // optional, capped at server MAX_TOKENS
    }
    """
    data = request.get_json()
    if not data or "messages" not in data:
        return jsonify({"error": "Missing 'messages' in request body"}), 400

    messages = data["messages"]
    temperature = min(max(data.get("temperature", 0.85), 0.0), 2.0)
    max_tokens = min(data.get("max_tokens", MAX_TOKENS), MAX_TOKENS)

    # Forward to DeepInfra
    payload = {
        "model": DEEPINFRA_MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": 0.9,
    }

    try:
        resp = requests.post(
            DEEPINFRA_URL,
            json=payload,
            headers={
                "Authorization": f"Bearer {DEEPINFRA_API_KEY}",
                "Content-Type": "application/json",
            },
            timeout=30,
        )
        resp.raise_for_status()
        result = resp.json()

        # Return just the assistant message content
        content = result["choices"][0]["message"]["content"]
        return jsonify({"content": content})

    except requests.exceptions.Timeout:
        return jsonify({"error": "AI service timed out. Please try again."}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "AI service unavailable. Please try again later."}), 502


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

    # Generate token
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
    if not DEEPINFRA_API_KEY:
        print("WARNING: DEEPINFRA_API_KEY not set!")
    if TOKEN_SECRET == "CHANGE_ME_IN_PRODUCTION":
        print("WARNING: TOKEN_SECRET is default - change for production!")

    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("DEBUG", "false").lower() == "true")
