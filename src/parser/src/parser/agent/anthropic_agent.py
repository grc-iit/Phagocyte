"""Anthropic Claude agent for reference parsing.

Two modes available:
1. claude-agent-sdk: Uses Claude Code CLI (no API key needed, just be logged into Claude Code)
2. anthropic: Direct API access (requires ANTHROPIC_API_KEY)
"""

import os

from .base import AgentParser, AgentParseResult


class AnthropicAgent(AgentParser):
    """Agent that uses Anthropic Claude for reference parsing.

    Supports two backends:
    - claude-agent-sdk: No API key needed (uses Claude Code CLI)
    - anthropic: Requires API key
    """

    @property
    def default_model(self) -> str:
        """Default Claude model."""
        return "claude-sonnet-4-20250514"

    @property
    def agent_type(self) -> str:
        """Agent type identifier."""
        return "anthropic"

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        use_agent_sdk: bool = True,  # Default to agent SDK (no API key needed)
    ):
        """Initialize Anthropic agent.

        Args:
            api_key: Anthropic API key (only needed if use_agent_sdk=False)
            model: Model to use (default: claude-sonnet-4-20250514)
            use_agent_sdk: If True, use claude-agent-sdk (no API key needed).
                          If False, use direct anthropic SDK (requires API key).
        """
        super().__init__(api_key, model)
        self.use_agent_sdk = use_agent_sdk

        # Check for API key only if not using agent SDK
        if not use_agent_sdk:
            self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
            if not self.api_key:
                raise ValueError(
                    "Anthropic API key required when use_agent_sdk=False. "
                    "Set ANTHROPIC_API_KEY environment variable or pass api_key parameter. "
                    "Alternatively, use use_agent_sdk=True (no API key needed)."
                )

    async def parse_async(self, text: str) -> AgentParseResult:
        """Parse text using Claude asynchronously.

        Args:
            text: Document text to parse

        Returns:
            AgentParseResult with extracted references
        """
        if self.use_agent_sdk:
            return await self._parse_with_agent_sdk(text)
        else:
            return await self._parse_with_anthropic_sdk(text)

    async def _parse_with_agent_sdk(self, text: str) -> AgentParseResult:
        """Parse using claude-agent-sdk (no API key needed)."""
        try:
            from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, TextBlock, query
        except ImportError as e:
            raise ImportError(
                "claude-agent-sdk package not installed. Install with: "
                "pip install claude-agent-sdk"
            ) from e

        user_message = f"""{self.SYSTEM_PROMPT}

---
DOCUMENT TO ANALYZE:
---

{text}

---
END OF DOCUMENT
---

Now extract ALL references from the document above and return them as a JSON array. Start your response with [ and end with ]. Do not include any other text before or after the JSON array."""

        options = ClaudeAgentOptions(
            max_turns=1,
        )

        response_text = ""
        async for message in query(prompt=user_message, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        response_text += block.text

        # Parse references from response
        references = self._parse_response_json(response_text)

        return AgentParseResult(
            references=references,
            raw_response=response_text,
            model="claude-code",  # Agent SDK uses Claude Code
            agent_type="claude-agent-sdk",
            tokens_used={},  # SDK doesn't expose token counts
            metadata={"backend": "claude-agent-sdk"}
        )

    async def _parse_with_anthropic_sdk(self, text: str) -> AgentParseResult:
        """Parse using direct anthropic SDK (requires API key)."""
        try:
            from anthropic import AsyncAnthropic
        except ImportError as e:
            raise ImportError(
                "anthropic package not installed. Install with: pip install anthropic"
            ) from e

        client = AsyncAnthropic(api_key=self.api_key)

        message = await client.messages.create(
            model=self.model,
            max_tokens=8192,
            system=self.SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": f"Please extract and categorize all references from the following research document:\n\n---\n\n{text}\n\n---\n\nReturn the references as a JSON array."
                }
            ]
        )

        response_text = ""
        for block in message.content:
            if hasattr(block, "text"):
                response_text += block.text

        references = self._parse_response_json(response_text)

        return AgentParseResult(
            references=references,
            raw_response=response_text,
            model=self.model,
            agent_type=self.agent_type,
            tokens_used={
                "input": message.usage.input_tokens,
                "output": message.usage.output_tokens,
            },
            metadata={
                "stop_reason": message.stop_reason,
                "message_id": message.id,
                "backend": "anthropic-sdk",
            }
        )

    def parse(self, text: str) -> AgentParseResult:
        """Parse text using Claude synchronously.

        Args:
            text: Document text to parse

        Returns:
            AgentParseResult with extracted references
        """
        if self.use_agent_sdk:
            return self._parse_sync_with_agent_sdk(text)
        else:
            return self._parse_sync_with_anthropic_sdk(text)

    def _parse_sync_with_agent_sdk(self, text: str) -> AgentParseResult:
        """Parse using claude-agent-sdk synchronously.

        Falls back to direct Anthropic SDK if agent SDK fails.
        """
        import asyncio
        try:
            return asyncio.run(self._parse_with_agent_sdk(text))
        except Exception as e:
            error_msg = str(e)

            # Check for rate limit error
            if "exit code 1" in error_msg.lower() or "rate limit" in error_msg.lower():
                print("\n⚠️  Claude CLI rate limit may have been hit.")
                print("    Check with: claude auth status")

            # Agent SDK failed, try falling back to direct API
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if api_key:
                print("Claude Agent SDK failed, falling back to direct Anthropic API...")
                self.api_key = api_key
                return self._parse_sync_with_anthropic_sdk(text)
            else:
                # Re-raise original error if no API key available
                raise RuntimeError(
                    f"Claude Agent SDK failed: {e}\n\n"
                    "Possible causes:\n"
                    "  1. Claude CLI rate limit hit (check: claude auth status)\n"
                    "  2. Claude CLI not authenticated (run: claude auth login)\n"
                    "  3. Network issues\n\n"
                    "To use direct API fallback, set ANTHROPIC_API_KEY environment variable."
                ) from e

    def _parse_sync_with_anthropic_sdk(self, text: str) -> AgentParseResult:
        """Parse using direct anthropic SDK synchronously."""
        try:
            from anthropic import Anthropic
        except ImportError as e:
            raise ImportError(
                "anthropic package not installed. Install with: pip install anthropic"
            ) from e

        client = Anthropic(api_key=self.api_key)

        message = client.messages.create(
            model=self.model,
            max_tokens=8192,
            system=self.SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": f"Please extract and categorize all references from the following research document:\n\n---\n\n{text}\n\n---\n\nReturn the references as a JSON array."
                }
            ]
        )

        response_text = ""
        for block in message.content:
            if hasattr(block, "text"):
                response_text += block.text

        references = self._parse_response_json(response_text)

        return AgentParseResult(
            references=references,
            raw_response=response_text,
            model=self.model,
            agent_type=self.agent_type,
            tokens_used={
                "input": message.usage.input_tokens,
                "output": message.usage.output_tokens,
            },
            metadata={
                "stop_reason": message.stop_reason,
                "message_id": message.id,
                "backend": "anthropic-sdk",
            }
        )
