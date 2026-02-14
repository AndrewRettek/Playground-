## chat_api.rpy - Proxy server integration for chatbot responses

init -1 python:
    import json
    import time

    ## ---------------------------------------------------------------
    ## CONFIGURATION
    ## ---------------------------------------------------------------

    ## URL of your proxy server
    PROXY_SERVER_URL = "https://attractive-learning-production-e561.up.railway.app"

    ## Fallback system prompt (character-specific prompts are in characters.rpy)
    DEFAULT_SYSTEM_PROMPT = """You are a character in a chat app. Keep your responses conversational and casual. Keep responses to 1-3 short paragraphs."""

    ## ---------------------------------------------------------------
    ## PLAYER AUTH
    ## ---------------------------------------------------------------

    ## Stored subscription token (persists across sessions via persistent)
    if persistent.player_token is None:
        persistent.player_token = ""

    def set_player_token(token):
        """Save the player's subscription token."""
        persistent.player_token = token.strip()

    def get_player_token():
        """Get the stored subscription token."""
        return persistent.player_token or ""

    def is_logged_in():
        """Check if player has entered a subscription token."""
        return bool(persistent.player_token)

    def prompt_subscription_key():
        """Prompt the player to enter their subscription key."""
        key = renpy.input("Enter your subscription key:", length=128, exclude="{}")
        key = key.strip()
        if key:
            set_player_token(key)
            renpy.notify("Subscription key saved!")

    def clear_subscription_key():
        """Clear the stored subscription key."""
        persistent.player_token = ""
        renpy.notify("Subscription key cleared.")

    ## ---------------------------------------------------------------
    ## API CALL FUNCTION
    ## ---------------------------------------------------------------

    def call_chat_api(player_message, conversation_history, system_prompt=None):
        """
        Call the proxy server with the player's message.

        Args:
            player_message: The text the player just typed
            conversation_history: List of {"role": "user"/"assistant", "content": "..."} dicts
            system_prompt: Optional system prompt override

        Returns:
            String containing the AI's response text
        """
        if system_prompt is None:
            system_prompt = DEFAULT_SYSTEM_PROMPT

        ## Build the messages array
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(conversation_history)
        messages.append({"role": "user", "content": player_message})

        payload = {
            "messages": messages,
            "temperature": 0.85,
            "max_tokens": 300,
        }

        try:
            response = renpy.fetch(
                PROXY_SERVER_URL + "/v1/chat",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30,
                result="json"
            )

            if "error" in response:
                error_msg = response["error"]
                if "subscription" in error_msg.lower() or "expired" in error_msg.lower():
                    return "(Your subscription has expired. Please renew to continue chatting.)"
                elif "rate limit" in error_msg.lower():
                    return "(Slow down! Please wait a moment before sending another message.)"
                else:
                    return "(" + error_msg + ")"

            return response.get("content", "(Empty response from server)")

        except Exception as e:
            return "(Could not reach the server. Check your internet connection.)"

    ## ---------------------------------------------------------------
    ## CHAT STATE MANAGEMENT
    ## ---------------------------------------------------------------

    ## Character accent colors (matching avatar border colors)
    CHARACTER_COLORS = {
        "Mallory": "#d4af37",   # gold
        "Rye": "#e74c3c",       # red
        "Demitria": "#9b59b6",  # purple
        "Gabby": "#1abc9c",     # teal
    }

    def get_timestamp():
        """Return current time as a short string."""
        return time.strftime("%I:%M %p").lstrip("0")

    class ChatMessage(object):
        """Represents a single message in the chat."""
        def __init__(self, sender, text, timestamp=""):
            self.sender = sender    # "player" or character name
            self.text = text
            self.timestamp = timestamp or get_timestamp()
            self.read = False

    class ChatSession(object):
        """Manages a conversation with a single character."""
        def __init__(self, character_name, system_prompt=None, avatar=None):
            self.character_name = character_name
            ## Combine world setting with character-specific prompt
            if system_prompt:
                self.system_prompt = WORLD_SETTING_PROMPT + "\n\n" + system_prompt + "\n\nFORMAT: Write only your character's message text. Never include *typing*, *sends message*, or other action/status markers."
            else:
                self.system_prompt = DEFAULT_SYSTEM_PROMPT
            self.avatar = avatar or "images/characters/placeholder_avatar.png"
            self.accent_color = CHARACTER_COLORS.get(character_name, "#4a6cf7")
            self.messages = []          # List of ChatMessage for display
            self.api_history = []       # List of dicts for API context
            self.is_loading = False
            self.unread_count = 0
            self._sound_pending = False
            self.is_active = False

        def send_message(self, player_text):
            """Send a player message and start async AI response."""
            if not player_text.strip():
                return

            ## Add player message immediately with timestamp
            self.messages.append(ChatMessage("player", player_text.strip(), get_timestamp()))
            self.is_loading = True

            ## Start API call in background thread so the screen stays visible
            renpy.invoke_in_thread(self._fetch_response, player_text.strip(), list(self.api_history))

        def _fetch_response(self, player_text, history):
            """Background thread: call API and update chat when done."""
            try:
                ai_response = call_chat_api(player_text, history, self.system_prompt)
            except Exception:
                ai_response = "(Could not reach the server. Check your internet connection.)"

            ## Update histories
            self.api_history.append({"role": "user", "content": player_text})
            self.api_history.append({"role": "assistant", "content": ai_response})
            self.messages.append(ChatMessage(self.character_name, ai_response, get_timestamp()))
            self.is_loading = False
            if not self.is_active:
                self.unread_count += 1
            self._sound_pending = True

            ## Keep API history reasonable (last 20 exchanges)
            if len(self.api_history) > 40:
                self.api_history = self.api_history[-40:]

            ## Tell Ren'Py to refresh the screen
            renpy.restart_interaction()

        def mark_read(self):
            """Mark all messages as read and reset unread count."""
            self.unread_count = 0
            for msg in self.messages:
                msg.read = True

        def reset(self):
            """Clear all messages and start fresh."""
            self.messages = []
            self.api_history = []
            self.is_loading = False
            self.unread_count = 0
            self._sound_pending = False

        def get_circle_avatar(self):
            """Return the path to this character's circular avatar."""
            return "gui/phone/avatar_" + self.character_name.lower() + "_circle.png"

        def get_last_message_preview(self):
            """Get a short preview of the last message for the contacts list."""
            if self.messages:
                last = self.messages[-1]
                preview = last.text[:40]
                if len(last.text) > 40:
                    preview += "..."
                return preview
            return "Tap to start chatting"
