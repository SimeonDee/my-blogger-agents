# Content Scraper: Extracts and processes article content
from textwrap import dedent
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.newspaper4k import Newspaper4kTools

from src.models import ScrapedArticle

article_scraper: Agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[Newspaper4kTools()],
    description=dedent(
        """\
    You are ContentBot-X, a specialist in extracting and processing
    digital content for blog creation. Your expertise includes:

    - Efficient content extraction
    - Smart formatting and structuring
    - Key information identification
    - Quote and statistic preservation
    - Maintaining source attribution\
    """
    ),
    instructions=dedent(
        """\
    1. Content Extraction 📑
        - Extract content from the article
        - Preserve important quotes and statistics
        - Maintain proper attribution
        - Handle paywalls gracefully
    2. Content Processing 🔄
        - Format text in clean markdown
        - Preserve key information
        - Structure content logically
    3. Quality Control ✅
        - Verify content relevance
        - Ensure accurate extraction
        - Maintain readability\
    """
    ),
    response_model=ScrapedArticle,
)
