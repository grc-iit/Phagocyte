"""Google Gemini agent for reference parsing.

Two modes available:
1. google-adk: Uses Google ADK (Agent Development Kit) - simpler setup
2. gemini: Direct google-generativeai API (requires GOOGLE_API_KEY)
"""

import os

from .base import AgentParser, AgentParseResult


class GeminiAgent(AgentParser):
    """Agent that uses Google Gemini for reference parsing.

    Supports two backends:
    - google-adk: Uses ADK framework (recommended)
    - google-generativeai: Direct API access
    """

    @property
    def default_model(self) -> str:
        """Default Gemini model."""
        return "gemini-2.0-flash"

    @property
    def agent_type(self) -> str:
        """Agent type identifier."""
        return "gemini"

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        use_adk: bool = True,  # Default to ADK
    ):
        """Initialize Gemini agent.

        Args:
            api_key: Google API key (uses GOOGLE_API_KEY env var if not provided)
            model: Model to use (default: gemini-2.0-flash)
            use_adk: If True, use google-adk. If False, use google-generativeai directly.
        """
        super().__init__(api_key, model)
        self.use_adk = use_adk
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")

        # API key is needed for both modes currently
        if not self.api_key:
            raise ValueError(
                "Google API key required. Set GOOGLE_API_KEY environment variable "
                "or pass api_key parameter. Get one at: https://aistudio.google.com/apikey"
            )

    async def parse_async(self, text: str) -> AgentParseResult:
        """Parse text using Gemini asynchronously.

        Args:
            text: Document text to parse

        Returns:
            AgentParseResult with extracted references
        """
        if self.use_adk:
            return await self._parse_with_adk(text)
        else:
            return await self._parse_with_genai(text)

    async def _parse_with_adk(self, text: str) -> AgentParseResult:
        """Parse using google-adk (Agent Development Kit)."""
        try:
            from google.adk.agents import Agent
            from google.adk.runners import Runner
            from google.genai import types
        except ImportError as e:
            raise ImportError(
                "google-adk package not installed. Install with: pip install google-adk"
            ) from e

        # Set up environment for ADK
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"
        os.environ["GOOGLE_API_KEY"] = self.api_key

        # Create the agent
        agent = Agent(
            name="reference_parser",
            model=self.model,
            description="Agent to extract and categorize references from research documents.",
            instruction=self.SYSTEM_PROMPT,
        )

        # Create runner and execute
        runner = Runner(agent=agent, app_name="parser_app")
        session = await runner.session_service.create_session(
            app_name="parser_app",
            user_id="parser_user",
        )

        user_message = f"Please extract and categorize all references from the following research document:\n\n---\n\n{text}\n\n---\n\nReturn the references as a JSON array."

        response_text = ""
        async for event in runner.run_async(
            user_id="parser_user",
            session_id=session.id,
            new_message=types.Content(
                role="user",
                parts=[types.Part(text=user_message)]
            ),
        ):
            if hasattr(event, 'content') and event.content:
                for part in event.content.parts:
                    if hasattr(part, 'text'):
                        response_text += part.text

        # Parse references from response
        references = self._parse_response_json(response_text)

        return AgentParseResult(
            references=references,
            raw_response=response_text,
            model=self.model,
            agent_type="google-adk",
            tokens_used={},  # ADK doesn't expose token counts easily
            metadata={
                "session_id": session.id,
                "backend": "google-adk",
            }
        )

    async def _parse_with_genai(self, text: str) -> AgentParseResult:
        """Parse using google-genai directly."""
        try:
            from google import genai
        except ImportError as e:
            raise ImportError(
                "google-genai package not installed. Install with: "
                "pip install google-genai"
            ) from e

        # Create client
        client = genai.Client(api_key=self.api_key)

        user_message = f"{self.SYSTEM_PROMPT}\n\nPlease extract and categorize all references from the following research document:\n\n---\n\n{text}\n\n---\n\nReturn the references as a JSON array."

        # Generate response
        response = await client.aio.models.generate_content(
            model=self.model,
            contents=user_message,
        )

        response_text = response.text if hasattr(response, 'text') else str(response)

        # Parse references from response
        references = self._parse_response_json(response_text)

        # Extract token usage if available
        tokens_used = {}
        if hasattr(response, 'usage_metadata'):
            usage = response.usage_metadata
            if hasattr(usage, 'prompt_token_count'):
                tokens_used["input"] = usage.prompt_token_count
            if hasattr(usage, 'candidates_token_count'):
                tokens_used["output"] = usage.candidates_token_count

        return AgentParseResult(
            references=references,
            raw_response=response_text,
            model=self.model,
            agent_type="gemini",
            tokens_used=tokens_used,
            metadata={"backend": "google-generativeai"},
        )

    def parse(self, text: str) -> AgentParseResult:
        """Parse text using Gemini synchronously.

        Uses google-genai directly for simpler sync usage.

        Args:
            text: Document text to parse

        Returns:
            AgentParseResult with extracted references
        """
        try:
            from google import genai
        except ImportError as e:
            raise ImportError(
                "google-genai package not installed. Install with: "
                "pip install google-genai"
            ) from e

        # Create client
        client = genai.Client(api_key=self.api_key)

        user_message = f"{self.SYSTEM_PROMPT}\n\nPlease extract and categorize all references from the following research document:\n\n---\n\n{text}\n\n---\n\nReturn the references as a JSON array."

        # Generate response
        response = client.models.generate_content(
            model=self.model,
            contents=user_message,
        )

        response_text = response.text if hasattr(response, 'text') else str(response)

        # Parse references from response
        references = self._parse_response_json(response_text)

        # Extract token usage if available
        tokens_used = {}
        if hasattr(response, 'usage_metadata'):
            usage = response.usage_metadata
            if hasattr(usage, 'prompt_token_count'):
                tokens_used["input"] = usage.prompt_token_count
            if hasattr(usage, 'candidates_token_count'):
                tokens_used["output"] = usage.candidates_token_count

        return AgentParseResult(
            references=references,
            raw_response=response_text,
            model=self.model,
            agent_type="gemini",
            tokens_used=tokens_used,
            metadata={"backend": "google-generativeai"},
        )
