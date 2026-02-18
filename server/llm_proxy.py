"""
LLM abstraction layer -- adapted from Yeah Buddy's proxy pattern.

Classes:
    LLMServerProxy       - Abstract base (mirrors Yeah Buddy's LLMServerProxy)
    OpenAICompatibleProxy - Generic OpenAI-compatible endpoint
    DeepSeekProxy         - DeepSeek with retry + <think> tag parsing

Factory:
    get_proxy(config)     - Returns proxy instance by config["llm_type"]
    register_proxy(name, cls) - Register a new provider
"""

import os
import time
import logging
import requests

logger = logging.getLogger(__name__)


class LLMServerProxy:
    """
    Abstract base class for LLM providers.
    Mirrors Yeah Buddy's LLMServerProxy from llm_server_proxy.py.
    """

    def __init__(self, config):
        self.api_endpoint = config.get("llm_model_endpoint")
        self.model_api_key = config.get("llm_model_api_key")
        self.model_version = config.get("llm_model_version")
        self.initial_prompt_role = config.get("initial_prompt_role", "system")
        self.max_tokens = config.get("max_tokens", 300)
        self.temperature = config.get("temperature", 0.85)
        self.timeout = config.get("timeout", 45)

    def query_model(self, system_prompt, messages, user_message):
        """
        Send a chat completion request to the LLM.

        Args:
            system_prompt: The full system prompt (world lore + character prompt)
            messages: Windowed chat history [{"role": ..., "content": ...}]
            user_message: The current user message text

        Returns:
            dict with keys:
                "content"   - str, the assistant's response (think tags stripped)
                "reasoning" - str or None, extracted <think> content
                "metrics"   - dict with timing/debug info
            On error, includes "error" key instead.
        """
        raise NotImplementedError("Subclasses must implement query_model()")


class OpenAICompatibleProxy(LLMServerProxy):
    """
    Generic OpenAI-compatible endpoint.
    Covers DeepInfra, Together, local vLLM, OpenRouter, etc.
    Adapted from Yeah Buddy's HermesLLMServerProxy.
    """

    def query_model(self, system_prompt, messages, user_message):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.model_api_key}",
        }
        payload = {
            "model": self.model_version,
            "messages": [
                {"role": self.initial_prompt_role, "content": system_prompt}
            ] + messages + [
                {"role": "user", "content": user_message}
            ],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": 0.9,
        }

        start_time = time.time()
        resp = requests.post(
            f"{self.api_endpoint}/chat/completions",
            json=payload,
            headers=headers,
            timeout=self.timeout,
        )
        ttfb = time.time() - start_time
        resp.raise_for_status()

        result = resp.json()
        raw_content = result["choices"][0]["message"]["content"]
        request_id = result.get("id", "")

        content, reasoning = self._parse_think_tags(raw_content)

        return {
            "content": content,
            "reasoning": reasoning,
            "metrics": {
                "ttfb": round(ttfb, 3),
                "request_id": request_id,
                "model": self.model_version,
            },
        }

    @staticmethod
    def _parse_think_tags(raw_content):
        """
        Extract <think>...</think> reasoning from response.
        Adapted from Yeah Buddy's DeepSeekLLMServerProxy.handle_llm_resp().
        """
        if "<think>" in raw_content and "</think>" in raw_content:
            think_start = raw_content.find("<think>") + len("<think>")
            think_end = raw_content.find("</think>")
            reasoning = raw_content[think_start:think_end].strip()
            content = raw_content.split("</think>")[-1].strip()
            return content, reasoning
        return raw_content.strip(), None


class DeepSeekProxy(OpenAICompatibleProxy):
    """
    DeepSeek-specific proxy with retry and exponential backoff.
    Adapted from Yeah Buddy's DeepSeekLLMServerProxy.
    """

    def __init__(self, config):
        super().__init__(config)
        self.max_retries = config.get("max_retries", 5)

    def query_model(self, system_prompt, messages, user_message):
        retry_count = 0
        backoff = 1
        total_timeout_delay = 0

        while retry_count < self.max_retries:
            try:
                result = super().query_model(system_prompt, messages, user_message)
                result["metrics"]["total_timeouts"] = retry_count
                result["metrics"]["total_timeout_delay"] = total_timeout_delay
                return result
            except requests.exceptions.Timeout:
                retry_count += 1
                backoff *= 2
                total_timeout_delay += backoff
                logger.warning(
                    "LLM timeout, retry %d/%d, backoff %ds",
                    retry_count, self.max_retries, backoff,
                )
                time.sleep(backoff)
            except requests.exceptions.RequestException as e:
                logger.error("LLM request error: %s", e)
                return {
                    "content": None,
                    "reasoning": None,
                    "error": f"AI service error: {e}",
                    "metrics": {"total_timeouts": retry_count},
                }

        logger.error("LLM timed out after %d retries", retry_count)
        return {
            "content": None,
            "reasoning": None,
            "error": f"AI service unavailable after {retry_count} retries",
            "metrics": {
                "total_timeouts": retry_count,
                "total_timeout_delay": total_timeout_delay,
            },
        }


# ---------------------------------------------------------------------------
# Factory -- adapted from Yeah Buddy's LLMServerProxyFactory
# ---------------------------------------------------------------------------

_PROXY_REGISTRY = {
    "openai_compatible": OpenAICompatibleProxy,
    "deepseek": DeepSeekProxy,
}


def register_proxy(name, cls):
    """Register a new LLM proxy class by name."""
    _PROXY_REGISTRY[name] = cls


def get_proxy(config):
    """
    Factory function. Returns an instantiated LLMServerProxy subclass
    based on config["llm_type"].
    """
    llm_type = config.get("llm_type", "openai_compatible")
    proxy_cls = _PROXY_REGISTRY.get(llm_type)
    if proxy_cls is None:
        raise ValueError(
            f"Unknown LLM type: {llm_type}. "
            f"Available: {list(_PROXY_REGISTRY.keys())}"
        )
    return proxy_cls(config)
