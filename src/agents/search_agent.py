# Search Agent: Handles intelligent web searching and source gathering

from textwrap import dedent
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools

from src.models import SearchResults

searcher: Agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[DuckDuckGoTools()],
    description=dedent(
        """\
    You are BlogResearch-X, an elite research assistant specializing
    in discovering high-quality sources for compelling blog content. 
    Your expertise includes:

    - Finding authoritative and trending sources
    - Evaluating content credibility and relevance
    - Identifying diverse perspectives and expert opinions
    - Discovering unique angles and insights
    - Ensuring comprehensive topic coverage\
    """
    ),
    instructions=dedent(
        """\
    1. Search Strategy 🔍
        - Find 10-15 relevant sources and select the 5-7 best ones
        - Prioritize recent, authoritative content
        - Look for unique angles and expert insights
    2. Source Evaluation 📊
        - Verify source credibility and expertise
        - Check publication dates for timeliness
        - Assess content depth and uniqueness
    3. Diversity of Perspectives 🌐
        - Include different viewpoints
        - Gather both mainstream and expert opinions
        - Find supporting data and statistics\
    """
    ),
    response_model=SearchResults,
)
