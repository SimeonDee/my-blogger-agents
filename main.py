from typing import Iterator

from agno.storage.sqlite import SqliteStorage
from agno.workflow import RunResponse
from fastapi import FastAPI
import uvicorn

from src.bloger_workflow import BlogPostGenerator
from src.models import Query

app = FastAPI()

blog_post_generator = BlogPostGenerator(
    storage=SqliteStorage(
        table_name="generate_blog_post_workflows",
        mode="workflow",
        auto_upgrade_schema=True,
        db_file="tmp/blogger_workflows.db",
    ),
    debug_mode=True,
)


@app.get("/health")
def health_check():
    return {"health": "Ok"}


@app.post("/workflow/run")
def run_agent(query: Query):
    """Execute the workflow with caching enabled, to generate Blog Post
    on given topic.

    Args:
        query (Query): A Request Body containing the blog topic. A json object
            with a "topic" property. e.g.
            {"topic": "Latest AI Technologies their and Use-cases"}.

    Returns:
        str: The generated blog post content.
    """

    # Convert the topic to a URL-safe string for use in session_id
    url_safe_topic = query.topic.lower().replace(" ", "-")

    blog_post_generator.session_id = f"generate-blog-post-on-{url_safe_topic}"
    blog_post: Iterator[RunResponse] = blog_post_generator.run(
        topic=query.topic,
        use_search_cache=True,
        use_scrape_cache=True,
        use_cached_report=True,
    )
    return blog_post


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
