# my-blogger-agents

A sophisticated Multi-agent Blog Post Generator that combines web research capabilities with professional writing expertise. Provided as a RESTful API Service (implemented using FastAPI).

The workflow uses a multi-stage approach:

1. Intelligent web research and source gathering
2. Content extraction and processing
3. Professional blog post writing with proper citations.

**Key capabilities:**

- Advanced web research and source evaluation
- Content scraping and processing
- Professional writing with SEO optimization
- Automatic content caching for efficiency
- Source attribution and fact verification

**Example blog topics to try:**

- "The Rise of Artificial Intelligence: Latest Technologies and Use-cases"
- "How Quantum Computing is Revolutionizing Artificial Intelligence"
- "How to build a Multi-agent AI Systems"
- "Sustainable Living in 2024: Practical Tips for Reducing Carbon Footprint"
- "The Future of Work: AI and Human Collaboration"
- "Mindfulness and Mental Health in the Digital Age"
- "The Evolution of Electric Vehicles: Current State and Future Trends"

## Technologies and Tools Used:

- `Agno`: A Multi-agentic framework
- `OpenAI`: LLM
- `sqlite`: Agents' storage and memory
- `duckduckgo`: Web search tool used for most relevant topic search and retrieval.
- `newspaper4k`: Web search tool, for latest news search.
- `Pydantic`: Used for structured/formatted agent response.

## Endpoints

- **BASE URL**: `http://0.0.0.0/5000`

- GET `/health`: Health check

- POST `/workflow/run`: Trigers the workflow run to generate a blog post

  **_Request Body:_**

  ```json
  {
    "topic": "the topic to generate a blog for"
  }
  ```

  **_Sample Response:_**

  ```json
  {
    "response": "The generated blog post"
  }
  ```

## Setup

- Clone repo
- Open repo dir on terminal (MacOS and Linux) or command prompt/Powershell (Windows)

### Install uv

```bash
$ pip install uv
```

### Create and activate a virtual environment

- Create a virtual environment

  ```bash
  $ uv venv
  ```

- Activate the virtual environment

  - MacOs and Linux users (Terminal):

    ```bash
    $ source .venv/bin/activate
    ```

  - Windows users (CMD):

    ```bash
    $ .venv\Scripts\activate.bat
    ```

  - Windows users (Powershell):

    ```bash
    $ .venv/Scripts/activate.ps1
    ```

### Install Dependencies

```bash
$ make install
```

### Start the server (FastAPI)

```bash
$ make run-server
```

### Stop the server (FastAPI)

- Go to the terminal or command prompt or powershell
- Press `Cntrl` + `C` (windows) or `cmd` + `C` (MacOS)

### Contacts

`Adedoyin Simeon Adeyemi` | [LinkedIn](https://www.linkedin.com/in/adedoyin-adeyemi-a7827b160/)
