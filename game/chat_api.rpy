## chat_api.rpy - Proxy server integration for chatbot responses
##
## Adapted from Yeah Buddy's CacheQueryUtil (persistent history),
## ModelContext (token windowing delegated to server), and
## CompanionBot (call flow) patterns.

init python:
    import json
    import time

    ## ---------------------------------------------------------------
    ## CONFIGURATION
    ## ---------------------------------------------------------------

    ## URL of the proxy server
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
    ## PERSISTENT CHAT HISTORY
    ## Adapted from Yeah Buddy's CacheQueryUtil + UserBotRelationship.
    ## Uses Ren'Py persistent storage instead of SQLAlchemy/SQLite.
    ## ---------------------------------------------------------------

    if persistent.chat_histories is None:
        persistent.chat_histories = {}

    def get_persistent_history(character_name):
        """Get the API history for a character from persistent storage."""
        if character_name not in persistent.chat_histories:
            persistent.chat_histories[character_name] = []
        return persistent.chat_histories[character_name]

    def append_to_persistent_history(character_name, role, content):
        """
        Append a message to persistent history.
        Client-side backstop caps at 200 messages; the server does
        real token-based windowing.
        """
        history = get_persistent_history(character_name)
        history.append({"role": role, "content": content})
        if len(history) > 200:
            persistent.chat_histories[character_name] = history[-200:]

    def clear_persistent_history(character_name):
        """Clear all persistent history for a character."""
        persistent.chat_histories[character_name] = []

    ## ---------------------------------------------------------------
    ## API CALL FUNCTION
    ## ---------------------------------------------------------------

    def call_chat_api(user_message, conversation_history, system_prompt=None):
        """
        Call the proxy server with the player's message.

        Uses the new structured payload format:
        - system_prompt: sent separately (server prepends to LLM call)
        - messages: raw chat history (server applies token windowing)
        - user_message: the current message

        The server handles model selection, token windowing, and
        <think> tag stripping. Adapted from Yeah Buddy's
        CompanionBot.call_llm() flow.
        """
        if system_prompt is None:
            system_prompt = DEFAULT_SYSTEM_PROMPT

        payload = {
            "system_prompt": system_prompt,
            "messages": conversation_history,
            "user_message": user_message,
        }

        try:
            response = renpy.fetch(
                PROXY_SERVER_URL + "/v1/chat",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=45,
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
        """
        Manages a conversation with a single character.
        Accepts a CharacterConfig object (from characters.rpy).
        Adapted from Yeah Buddy's CompanionBot + ModelContext pattern.
        """
        def __init__(self, character_config):
            self.config = character_config
            self.character_name = character_config.name
            self.system_prompt = character_config.build_system_prompt(WORLD_LORE)
            self.avatar = character_config.avatar
            self.accent_color = character_config.accent_color
            self.messages = []          # List of ChatMessage for display
            self.is_loading = False
            self.unread_count = 0
            self._sound_pending = False

            # Restore display messages from persistent history
            self._restore_from_persistent()

        def _restore_from_persistent(self):
            """
            Rebuild display messages from persistent API history.
            Called on init so conversations survive game restarts.
            """
            history = get_persistent_history(self.character_name)
            for entry in history:
                role = entry.get("role", "")
                content = entry.get("content", "")
                if role == "user":
                    self.messages.append(ChatMessage("player", content))
                elif role == "assistant":
                    self.messages.append(ChatMessage(self.character_name, content))

        @property
        def api_history(self):
            """API history is always read from persistent storage."""
            return get_persistent_history(self.character_name)

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

            ## Persist both messages
            append_to_persistent_history(self.character_name, "user", player_text)
            append_to_persistent_history(self.character_name, "assistant", ai_response)

            ## Update display
            self.messages.append(ChatMessage(self.character_name, ai_response, get_timestamp()))
            self.is_loading = False
            self.unread_count += 1
            self._sound_pending = True

            ## Tell Ren'Py to refresh the screen
            renpy.restart_interaction()

        def mark_read(self):
            """Mark all messages as read and reset unread count."""
            self.unread_count = 0
            for msg in self.messages:
                msg.read = True

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
