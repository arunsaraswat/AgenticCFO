"""LLM configuration for OpenRouter integration."""
from typing import Optional
from langchain_openai import ChatOpenAI
from app.core.config import settings


class LLMConfig:
    """Configuration for LLM models via OpenRouter."""

    # Model mappings - using OpenRouter model IDs
    MODELS = {
        # High-complexity reasoning tasks
        "gpt4": "openai/gpt-4-turbo",
        "claude-3.5": "anthropic/claude-3.5-sonnet",

        # Medium-complexity data analysis
        "gpt-3.5": "openai/gpt-3.5-turbo",

        # Cost-optimized for bulk processing
        "llama-3.1-70b": "meta-llama/llama-3.1-70b-instruct",
    }

    # Agent-to-model mapping (per CLAUDE.md architecture)
    AGENT_MODEL_MAP = {
        "cash_commander": "gpt4",
        "portfolio_allocator": "gpt4",
        "close_copilot": "claude-3.5",
        "margin_mechanic": "claude-3.5",
        "critic": "claude-3.5",
        "forecast_factory": "gpt4",
        "payables_protector": "gpt-3.5",
        "receivables_radar": "gpt-3.5",
        "guardrail": "gpt-3.5",
        "workbook_auditor": "gpt-3.5",
        "compliance_scribe": "llama-3.1-70b",
    }

    @classmethod
    def get_llm(
        cls,
        agent_name: Optional[str] = None,
        model_key: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> ChatOpenAI:
        """
        Get an LLM instance configured for OpenRouter.

        Args:
            agent_name: Name of the agent (e.g., "cash_commander")
            model_key: Direct model key (e.g., "gpt4") - overrides agent_name
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional ChatOpenAI parameters

        Returns:
            Configured ChatOpenAI instance

        Example:
            >>> llm = LLMConfig.get_llm(agent_name="cash_commander")
            >>> llm = LLMConfig.get_llm(model_key="gpt4", temperature=0.2)
        """
        # Determine which model to use
        if model_key:
            model_id = cls.MODELS.get(model_key, model_key)
        elif agent_name:
            model_key = cls.AGENT_MODEL_MAP.get(agent_name, "gpt-3.5")
            model_id = cls.MODELS.get(model_key)
        else:
            # Default to GPT-3.5
            model_id = cls.MODELS["gpt-3.5"]

        # Configure for OpenRouter
        return ChatOpenAI(
            model=model_id,
            openai_api_key=settings.openrouter_api_key,
            openai_api_base="https://openrouter.ai/api/v1",
            temperature=temperature,
            max_tokens=max_tokens,
            model_kwargs={
                "headers": {
                    "HTTP-Referer": "https://agenticcfo.com",  # Optional, for rankings
                    "X-Title": "Agentic CFO Platform",  # Optional, for rankings
                },
                **kwargs
            }
        )

    @classmethod
    def get_model_for_agent(cls, agent_name: str) -> str:
        """Get the model key assigned to an agent."""
        return cls.AGENT_MODEL_MAP.get(agent_name, "gpt-3.5")
