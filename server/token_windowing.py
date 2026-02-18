"""
Token-based chat history windowing.

Adapted from Yeah Buddy's ModelContext.get_windowed_chat_history().
Uses tiktoken instead of HuggingFace AutoTokenizer.

The algorithm iterates messages newest-first, accumulates token count,
stops when the budget is exceeded, then reverses to chronological order.
"""

import tiktoken


def get_encoder(encoding_name="cl100k_base"):
    """
    Get a tiktoken encoder.
    cl100k_base covers GPT-4, GPT-3.5, and works well as an approximation
    for other modern models (DeepSeek, Llama, etc.).
    """
    return tiktoken.get_encoding(encoding_name)


def count_tokens(text, encoder):
    """Count tokens in a string using the given encoder."""
    return len(encoder.encode(text))


def window_chat_history(messages, max_tokens, encoder=None):
    """
    Trim chat history to fit within a token budget.

    Iterates messages newest-first (reverse chronological), accumulates
    token counts, stops when the budget is exceeded, then reverses back
    to chronological order. This matches the algorithm in Yeah Buddy's
    ModelContext.process_chat_history_row / IterationState pattern.

    Args:
        messages: list of {"role": ..., "content": ...} in chronological order
        max_tokens: maximum total tokens to include in the window
        encoder: tiktoken encoder instance (created if not provided)

    Returns:
        list of messages that fit within the token window, in chronological order
    """
    if encoder is None:
        encoder = get_encoder()

    if not messages:
        return []

    token_count = 0
    collected = []

    for msg in reversed(messages):
        msg_tokens = count_tokens(msg.get("content", ""), encoder)
        if token_count + msg_tokens > max_tokens and collected:
            # Would exceed budget and we already have some messages -- stop
            break
        token_count += msg_tokens
        collected.append(msg)

    collected.reverse()
    return collected
