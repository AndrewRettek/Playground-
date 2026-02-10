## chat_api.rpy - DeepInfra API integration for chatbot responses

init python:
    import json

    ## ---------------------------------------------------------------
    ## CONFIGURATION - Set your API key and model here
    ## ---------------------------------------------------------------

    ## Your DeepInfra API key. For production, load from environment
    ## or a config file rather than hardcoding.
    DEEPINFRA_API_KEY = "YOUR_DEEPINFRA_API_KEY"

    ## DeepSeek V3.2 model identifier on DeepInfra
    DEEPINFRA_MODEL = "deepseek-ai/DeepSeek-V3-0324"

    ## API endpoint
    DEEPINFRA_URL = "https://api.deepinfra.com/v1/openai/chat/completions"

    ## Default system prompt - replace with your character prompts
    DEFAULT_SYSTEM_PROMPT = """You are Mallory, a friendly and witty character. You are texting with the player through a messaging app. Keep your responses conversational, casual, and in-character. Use texting abbreviations naturally but don't overdo it. Keep responses to 1-3 short paragraphs."""

    ## ---------------------------------------------------------------
    ## API CALL FUNCTION
    ## ---------------------------------------------------------------

    def call_deepinfra(player_message, conversation_history, system_prompt=None):
        """
        Call the DeepInfra API with the player's message and return the AI response.

        Args:
            player_message: The text the player just typed
            conversation_history: List of {"role": "user"/"assistant", "content": "..."} dicts
            system_prompt: Optional system prompt override

        Returns:
            String containing the AI's response text
        """
        if system_prompt is None:
            system_prompt = DEFAULT_SYSTEM_PROMPT

        ## Build the messages array for the API
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(conversation_history)
        messages.append({"role": "user", "content": player_message})

        payload = {
            "model": DEEPINFRA_MODEL,
            "messages": messages,
            "max_tokens": 300,
            "temperature": 0.85,
            "top_p": 0.9,
        }

        try:
            response = renpy.fetch(
                DEEPINFRA_URL,
                json=payload,
                headers={"Authorization": "Bearer " + DEEPINFRA_API_KEY},
                timeout=30,
                result="json"
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            return "(Message failed to send. Check your connection and try again.)"

    ## ---------------------------------------------------------------
    ## CHAT STATE MANAGEMENT
    ## ---------------------------------------------------------------

    class ChatMessage(object):
        """Represents a single message in the chat."""
        def __init__(self, sender, text, timestamp=""):
            self.sender = sender    # "player" or character name
            self.text = text
            self.timestamp = timestamp

    class ChatSession(object):
        """Manages a conversation with a single character."""
        def __init__(self, character_name, system_prompt=None, avatar=None):
            self.character_name = character_name
            self.system_prompt = system_prompt or DEFAULT_SYSTEM_PROMPT
            self.avatar = avatar or "images/characters/placeholder_avatar.png"
            self.messages = []          # List of ChatMessage for display
            self.api_history = []       # List of dicts for API context
            self.is_loading = False

        def send_message(self, player_text):
            """Send a player message and get AI response."""
            if not player_text.strip():
                return

            ## Add player message
            self.messages.append(ChatMessage("player", player_text.strip()))

            ## Get AI response
            self.is_loading = True
            ai_response = call_deepinfra(
                player_text.strip(),
                list(self.api_history),
                self.system_prompt
            )
            self.is_loading = False

            ## Update histories
            self.api_history.append({"role": "user", "content": player_text.strip()})
            self.api_history.append({"role": "assistant", "content": ai_response})
            self.messages.append(ChatMessage(self.character_name, ai_response))

            ## Keep API history reasonable (last 20 exchanges)
            if len(self.api_history) > 40:
                self.api_history = self.api_history[-40:]

        def get_last_message_preview(self):
            """Get a short preview of the last message for the contacts list."""
            if self.messages:
                last = self.messages[-1]
                preview = last.text[:40]
                if len(last.text) > 40:
                    preview += "..."
                return preview
            return "Tap to start chatting"
