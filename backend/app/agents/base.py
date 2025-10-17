"""Base agent class for all finance agents."""
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional
from datetime import datetime
import logging
from uuid import UUID

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import Tool

from app.agents.llm_config import LLMConfig

logger = logging.getLogger(__name__)


class AgentOutput:
    """Structured output from an agent execution."""

    def __init__(
        self,
        agent_name: str,
        output: Dict[str, Any],
        confidence_score: float,
        artifacts: List[Dict[str, Any]],
        reasoning_trace: List[str],
        execution_time: float,
        cost_usd: float = 0.0,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize agent output.

        Args:
            agent_name: Name of the agent that produced this output
            output: Main output data (structured dict)
            confidence_score: 0.0-1.0 confidence in the result
            artifacts: List of artifacts generated (Excel, PDF, etc.)
            reasoning_trace: List of reasoning steps (for explainability)
            execution_time: Time taken to execute (seconds)
            cost_usd: Estimated API cost in USD
            metadata: Additional metadata
        """
        self.agent_name = agent_name
        self.output = output
        self.confidence_score = confidence_score
        self.artifacts = artifacts or []
        self.reasoning_trace = reasoning_trace or []
        self.execution_time = execution_time
        self.cost_usd = cost_usd
        self.metadata = metadata or {}
        self.timestamp = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "agent_name": self.agent_name,
            "output": self.output,
            "confidence_score": self.confidence_score,
            "artifacts": self.artifacts,
            "reasoning_trace": self.reasoning_trace,
            "execution_time": self.execution_time,
            "cost_usd": self.cost_usd,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat()
        }


class BaseFinanceAgent(ABC):
    """
    Abstract base class for all finance agents.

    Each agent follows this pattern:
    1. Initialize with LLM and tools
    2. Execute with inputs and policy constraints
    3. Return structured AgentOutput with artifacts

    Subclasses must implement:
    - get_system_prompt(): Return agent-specific prompt
    - get_default_tools(): Return list of tools for this agent
    - _prepare_input(): Format inputs for the agent
    - _parse_output(): Extract structured data from LLM response
    - _generate_artifacts(): Generate Excel/PDF/Word artifacts
    """

    def __init__(
        self,
        agent_name: str,
        model_key: Optional[str] = None,
        temperature: float = 0.1,
        additional_tools: Optional[List[Tool]] = None
    ):
        """
        Initialize base agent.

        Args:
            agent_name: Unique identifier for this agent (e.g., "cash_commander")
            model_key: LLM model key (if None, uses default for agent_name)
            temperature: Sampling temperature for LLM
            additional_tools: Extra tools beyond get_default_tools()
        """
        self.agent_name = agent_name
        self.logger = logging.getLogger(f"agent.{agent_name}")

        # Get LLM instance via OpenRouter
        self.llm = LLMConfig.get_llm(
            agent_name=agent_name,
            model_key=model_key,
            temperature=temperature
        )

        # Collect tools
        self.tools = self.get_default_tools()
        if additional_tools:
            self.tools.extend(additional_tools)

        # Create agent
        self.agent_executor = self._create_agent()

    def _create_agent(self) -> AgentExecutor:
        """Create the LangChain agent executor."""
        # Build prompt
        system_prompt = self.get_system_prompt()
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        # Create agent
        agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )

        # Create executor
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            return_intermediate_steps=True,
            max_iterations=10
        )

    async def execute(
        self,
        inputs: Dict[str, Any],
        policy_constraints: Optional[Dict[str, Any]] = None,
        progress_callback: Optional[Callable[[str, float], None]] = None
    ) -> AgentOutput:
        """
        Execute the agent.

        Args:
            inputs: Input data (datasets, parameters, etc.)
            policy_constraints: Policy rules to enforce
            progress_callback: Optional callback for progress updates

        Returns:
            AgentOutput with results, artifacts, reasoning trace
        """
        start_time = datetime.utcnow()

        try:
            self.logger.info(f"Starting {self.agent_name} execution")

            if progress_callback:
                progress_callback(f"{self.agent_name}: Preparing inputs", 0.1)

            # Prepare inputs
            formatted_input = self._prepare_input(inputs, policy_constraints)

            if progress_callback:
                progress_callback(f"{self.agent_name}: Executing agent", 0.3)

            # Execute agent
            result = await self.agent_executor.ainvoke({
                "input": formatted_input
            })

            if progress_callback:
                progress_callback(f"{self.agent_name}: Parsing output", 0.7)

            # Parse output
            parsed_output = self._parse_output(result)

            if progress_callback:
                progress_callback(f"{self.agent_name}: Generating artifacts", 0.9)

            # Generate artifacts
            artifacts = await self._generate_artifacts(parsed_output)

            # Extract reasoning trace
            reasoning_trace = self._extract_reasoning_trace(result)

            # Calculate confidence score
            confidence = self._calculate_confidence(result, parsed_output)

            # Calculate execution time
            execution_time = (datetime.utcnow() - start_time).total_seconds()

            if progress_callback:
                progress_callback(f"{self.agent_name}: Complete", 1.0)

            return AgentOutput(
                agent_name=self.agent_name,
                output=parsed_output,
                confidence_score=confidence,
                artifacts=artifacts,
                reasoning_trace=reasoning_trace,
                execution_time=execution_time,
                metadata={"model": LLMConfig.get_model_for_agent(self.agent_name)}
            )

        except Exception as e:
            self.logger.error(f"Agent execution failed: {e}", exc_info=True)
            raise

    def _extract_reasoning_trace(self, result: Dict[str, Any]) -> List[str]:
        """Extract reasoning steps from intermediate steps."""
        trace = []
        intermediate_steps = result.get("intermediate_steps", [])

        for step in intermediate_steps:
            if isinstance(step, tuple) and len(step) >= 2:
                action, observation = step[0], step[1]
                trace.append(f"Action: {action.tool} - {action.tool_input}")
                trace.append(f"Observation: {observation[:200]}...")  # Truncate

        return trace

    def _calculate_confidence(self, result: Dict[str, Any], parsed_output: Dict[str, Any]) -> float:
        """
        Calculate confidence score based on execution quality.

        Default implementation returns 0.8. Subclasses should override
        with domain-specific logic.
        """
        # Simple heuristic: if we got intermediate steps, we're more confident
        steps = len(result.get("intermediate_steps", []))
        if steps >= 3:
            return 0.9
        elif steps >= 1:
            return 0.8
        else:
            return 0.6

    # Abstract methods to be implemented by subclasses

    @abstractmethod
    def get_system_prompt(self) -> str:
        """
        Return the system prompt for this agent.

        Should describe:
        - Agent's role and responsibilities
        - Input format expectations
        - Output format requirements
        - Policy constraints to follow
        """
        pass

    @abstractmethod
    def get_default_tools(self) -> List[Tool]:
        """
        Return list of tools available to this agent.

        Example:
            return [
                Tool(
                    name="analyze_bank_statement",
                    func=self._analyze_bank_statement,
                    description="Analyze bank statement to extract cash positions"
                )
            ]
        """
        pass

    @abstractmethod
    def _prepare_input(self, inputs: Dict[str, Any], policy_constraints: Optional[Dict[str, Any]]) -> str:
        """
        Format inputs into a prompt string for the agent.

        Args:
            inputs: Raw input data (datasets, parameters)
            policy_constraints: Policy rules to include

        Returns:
            Formatted string prompt
        """
        pass

    @abstractmethod
    def _parse_output(self, raw_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse agent output into structured format.

        Args:
            raw_output: Raw output from agent executor

        Returns:
            Structured dictionary with parsed data
        """
        pass

    @abstractmethod
    async def _generate_artifacts(self, parsed_output: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate artifacts (Excel, PDF, Word) from parsed output.

        Args:
            parsed_output: Structured output from _parse_output()

        Returns:
            List of artifact metadata dictionaries:
            [
                {
                    "artifact_type": "excel",
                    "filename": "Cash_Ladder.xlsx",
                    "file_path": "/path/to/file.xlsx",
                    "description": "13-week cash forecast"
                }
            ]
        """
        pass
