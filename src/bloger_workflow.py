# Blog Post Generator Workflow
"""
A sophisticated blog post generator that combines
web research capabilities with professional writing expertise.

The workflow uses a multi-stage approach:
1. Intelligent web research and source gathering
2. Content extraction and processing
3. Professional blog post writing with proper citations

Key capabilities:
- Advanced web research and source evaluation
- Content scraping and processing
- Professional writing with SEO optimization
- Automatic content caching for efficiency
- Source attribution and fact verification
"""

import json
from typing import Dict, Iterator, Optional
from textwrap import dedent

from agno.agent import Agent
from agno.run.workflow import WorkflowCompletedEvent
from agno.utils.log import logger
from agno.workflow import Workflow, RunResponse

from src.agents.search_agent import searcher
from src.agents.article_scraper_agent import article_scraper
from src.agents.blog_writer_agent import writer
from src.models import ScrapedArticle, SearchResults

import os
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


class BlogPostGenerator(Workflow):
    """
    Advanced workflow for generating professional blog posts with proper
    research and citations.
    """

    description: str = dedent(
        """\
    An intelligent blog post generator that creates engaging,
    well-researched content.
    This workflow orchestrates multiple AI agents to research, analyze,
    and craft compelling blog posts that combine journalistic rigor with
    engaging storytelling.
    The system excels at creating content that is both informative and
    optimized for digital consumption.
    """
    )

    # Search Agent: Handles intelligent web searching and source gathering
    searcher: Agent = searcher
    # Content Scraper: Extracts and processes article content
    article_scraper: Agent = article_scraper
    # Content Writer Agent: Crafts engaging blog posts from research
    writer: Agent = writer

    def run(
        self,
        topic: str,
        use_search_cache: bool = True,
        use_scrape_cache: bool = True,
        use_cached_report: bool = True,
    ) -> Iterator[RunResponse]:
        logger.info(f"Generating a blog post on: {topic}")

        # Use the cached blog post if use_cache is True
        if use_cached_report:
            cached_blog_post = self.get_cached_blog_post(topic)
            if cached_blog_post:
                yield WorkflowCompletedEvent(
                    run_id=self.run_id,
                    content=cached_blog_post,
                )
                return

        # Search the web for articles on the topic
        search_results: Optional[SearchResults] = self.get_search_results(
            topic, use_search_cache
        )
        # If no search_results are found for the topic, end the workflow
        if search_results is None or len(search_results.articles) == 0:
            yield WorkflowCompletedEvent(
                run_id=self.run_id,
                content=(
                    f"Sorry, could not find any articles on the topic: {topic}"
                ),  # no-qa
            )
            return

        # Scrape the search results
        scraped_articles: Dict[str, ScrapedArticle] = self.scrape_articles(
            topic, search_results, use_scrape_cache
        )

        # Prepare the input for the writer
        writer_input = {
            "topic": topic,
            "articles": [v.model_dump() for v in scraped_articles.values()],
        }

        # Run the writer and yield the response
        yield from self.writer.run(
            json.dumps(writer_input, indent=4),
            stream=True,
        )

        # Save the blog post in the cache
        self.add_blog_post_to_cache(topic, self.writer.run_response.content)

    def get_cached_blog_post(self, topic: str) -> Optional[str]:
        logger.info("Checking if cached blog post exists")

        return self.session_state.get("blog_posts", {}).get(topic)

    def add_blog_post_to_cache(self, topic: str, blog_post: str):
        logger.info(f"Saving blog post for topic: {topic}")
        self.session_state.setdefault("blog_posts", {})
        self.session_state["blog_posts"][topic] = blog_post

    def get_cached_search_results(self, topic: str) -> Optional[SearchResults]:
        logger.info("Checking if cached search results exist")
        search_results = self.session_state.get("search_results", {}).get(
            topic
        )  # no-qa
        return (
            SearchResults.model_validate(search_results)
            if search_results and isinstance(search_results, dict)
            else search_results
        )

    def add_search_results_to_cache(
        self, topic: str, search_results: SearchResults
    ):  # no-qa
        logger.info(f"Saving search results for topic: {topic}")
        self.session_state.setdefault("search_results", {})
        self.session_state["search_results"][topic] = search_results

    def get_cached_scraped_articles(
        self, topic: str
    ) -> Optional[Dict[str, ScrapedArticle]]:
        logger.info("Checking if cached scraped articles exist")
        scraped_articles = self.session_state.get("scraped_articles", {}).get(
            topic,
        )
        return (
            ScrapedArticle.model_validate(scraped_articles)
            if scraped_articles and isinstance(scraped_articles, dict)
            else scraped_articles
        )

    def add_scraped_articles_to_cache(
        self,
        topic: str,
        scraped_articles: Dict[str, ScrapedArticle],
    ):
        logger.info(f"Saving scraped articles for topic: {topic}")
        self.session_state.setdefault("scraped_articles", {})
        self.session_state["scraped_articles"][topic] = scraped_articles

    def get_search_results(
        self, topic: str, use_search_cache: bool, num_attempts: int = 3
    ) -> Optional[SearchResults]:
        # Get cached search_results from the session state
        # if use_search_cache is True
        if use_search_cache:
            try:
                search_results_from_cache = self.get_cached_search_results(
                    topic,
                )
                if search_results_from_cache is not None:
                    search_results = SearchResults.model_validate(
                        search_results_from_cache
                    )
                    logger.info(
                        f"Found {len(search_results.articles)} "
                        "articles in cache."  # no-qa
                    )
                    return search_results
            except Exception as e:
                logger.warning(
                    f"Could not read search results from cache: {e}",
                )  # no-qa

        # If there are no cached search_results, use the searcher to
        # find the latest articles
        for attempt in range(num_attempts):
            try:
                searcher_response: RunResponse = self.searcher.run(topic)
                if (
                    searcher_response is not None
                    and searcher_response.content is not None
                    and isinstance(searcher_response.content, SearchResults)
                ):
                    article_count = len(searcher_response.content.articles)
                    logger.info(
                        f"Found {article_count} articles "
                        "on attempt {attempt + 1}"  # no-qa
                    )
                    # Cache the search results
                    self.add_search_results_to_cache(
                        topic,
                        searcher_response.content,
                    )
                    return searcher_response.content
                else:
                    logger.warning(
                        f"Attempt {attempt + 1}/{num_attempts} failed: "
                        "Invalid response type"
                    )
            except Exception as e:
                logger.warning(
                    f"Attempt {attempt + 1}/{num_attempts} failed: {str(e)}"
                )  # no-qa

        logger.error(
            f"Failed to get search results after {num_attempts} attempts"
        )  # no-qa
        return None

    def scrape_articles(
        self, topic: str, search_results: SearchResults, use_scrape_cache: bool
    ) -> Dict[str, ScrapedArticle]:
        scraped_articles: Dict[str, ScrapedArticle] = {}

        # Get cached scraped_articles from the session state
        # if use_scrape_cache is True
        if use_scrape_cache:
            try:
                scraped_articles_from_cache = self.get_cached_scraped_articles(
                    topic,
                )
                if scraped_articles_from_cache is not None:
                    scraped_articles = scraped_articles_from_cache
                    logger.info(
                        f"Found {len(scraped_articles)} scraped "
                        "articles in cache."  # no-qa
                    )
                    return scraped_articles
            except Exception as e:
                logger.warning(
                    f"Could not read scraped articles from cache: {e}",
                )

        # Scrape the articles that are not in the cache
        for article in search_results.articles:
            if article.url in scraped_articles:
                logger.info(f"Found scraped article in cache: {article.url}")
                continue

            article_scraper_response: RunResponse = self.article_scraper.run(
                article.url
            )
            if (
                article_scraper_response is not None
                and article_scraper_response.content is not None
                and isinstance(
                    article_scraper_response.content,
                    ScrapedArticle,
                )
            ):
                scraped_articles[article_scraper_response.content.url] = (
                    article_scraper_response.content
                )
                logger.info(
                    f"Scraped article: {article_scraper_response.content.url}",
                )

        # Save the scraped articles in the session state
        self.add_scraped_articles_to_cache(topic, scraped_articles)
        return scraped_articles
