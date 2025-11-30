# Dance Agent System

### Problem
Classical dancers, particularly those specializing in traditional Indian dance forms like Kuchipudi, face significant challenges in discovering performance opportunities globally. The process of finding relevant festivals, sabhas, consulates, and cultural events is fragmented across multiple websites, social media platforms, and regional networks. Additionally, identifying collaboration opportunities with other dancers and crafting personalized applications for each opportunity is time-consuming and often inefficient.

### Solution
The Dance Agent System is an intelligent multi-agent application that automates the entire workflow of discovering dance opportunities, researching potential collaborators, and drafting professional applications. Built using Google's Agent Development Kit (ADK), the system employs three specialized agents working in sequence:

1. **Discovery Agent**: Searches the web for relevant performance opportunities, festivals, and cultural events
2. **Dancer Finder Agent**: Identifies prominent dancers in the same genre for networking and collaboration
3. **Application Agent**: Generates personalized application drafts based on discovered opportunities

### Value Proposition
- **Time Savings**: Reduces hours of manual research to minutes of automated discovery
- **Comprehensive Coverage**: Searches globally across multiple platforms and sources
- **Personalization**: Maintains user context (profile, preferences) via Memory Bank for tailored results
- **Intelligent Workflow**: Agents collaborate through A2A (Agent-to-Agent) Protocol for seamless information flow
- **Human-in-the-Loop**: Allows user guidance at each stage for quality control and direction
- **Resilience**: Crash recovery ensures long-running operations can resume from last checkpoint

## Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Dance Agent System                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────┐  │
│  │  Discovery   │─────▶│ Dancer Finder│─────▶│Application│ │
│  │    Agent     │      │    Agent     │      │   Agent   │  │
│  └──────────────┘      └──────────────┘      └──────────┘  │
│         │                     │                     │        │
│         ▼                     ▼                     ▼        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Session & State Management              │  │
│  │         (File-based persistence in data/)            │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                   Memory Bank                         │  │
│  │        (Long-term user context: memory.md)            │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                  Custom Tools                         │  │
│  │  • search_web    • browse_website                     │  │
│  │  • save_results  • draft_application                  │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            A2A Protocol (JSON messaging)              │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Observability (Logging to /tmp/agent.log)     │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Key Components

#### 1. Multi-Agent System
- **Discovery Agent** (LlmAgent): Uses `search_web` and `browse_website` tools to find opportunities
- **Dancer Finder Agent** (LlmAgent): Searches for dancers and collaboration opportunities
- **Application Agent** (LlmAgent): Drafts personalized applications using `draft_application` tool
- **Sequential Orchestration**: Agents execute in order, each building on previous results

#### 2. Custom Tools (`tools.py`)
- `search_web(query)`: DuckDuckGo search integration
- `browse_website(url)`: Web scraping with BeautifulSoup
- `save_results(filename, content)`: Persistent storage
- `draft_application(...)`: Template-based application generation

#### 3. A2A Protocol (`protocol.py`)
- `format_message(sender, receiver, content, metadata)`: Structured JSON messaging
- `compact_context(text, max_length)`: Context engineering for token efficiency

#### 4. Sessions & State Management (`session.py`)
- `save_state(key, content)`: File-based persistence
- `load_state(key)`: State retrieval
- Enables crash recovery and resume functionality

#### 5. Long-Term Memory (`data/memory.md`)
- Stores user profile, preferences, and application style
- Injected into agent context for personalization

#### 6. Human-in-the-Loop (`main.py`)
- **Dynamic Name Input**: Prompts for user's name at startup for personalization
- Interactive pauses after each agent
- User feedback injection into subsequent prompts
- Enables guided execution

#### 7. Observability (`logger.py`)
- Structured logging to `/tmp/agent.log`
- Console and file output
- Tracks agent execution flow

#### 8. Agent Evaluation (`evaluation.py`)
- LLM-as-a-Judge pattern
- Evaluates agent output quality
- Provides scoring and feedback

## Key Concepts Demonstrated

### ✅ 1. Multi-Agent System
Three specialized agents (`discovery_agent`, `dancer_finder_agent`, `application_agent`) orchestrated via `SequentialAgent` pattern.

### ✅ 2. Custom Tools
Four custom tools integrated with agents:
- `search_web`: Web search capability
- `browse_website`: Content extraction
- `save_results`: Data persistence
- `draft_application`: Application generation

### ✅ 3. Sessions & State Management
File-based session management with:
- `save_state()` and `load_state()` functions
- Persistent storage in `data/` directory
- Crash recovery via checkpoint detection

### ✅ 4. Long-Term Memory (Memory Bank)
- `data/memory.md` stores user context
- Loaded at runtime and injected into prompts
- Enables personalized agent behavior

### ✅ 5. Context Engineering
- `compact_context()` function truncates large contexts
- Prevents token limit errors
- Maintains focus on relevant information

### ✅ 6. A2A Protocol
- Structured JSON messaging between agents
- `format_message()` creates standardized messages
- Metadata support for message routing

### ✅ 7. Observability (Logging)
- Custom logger with file and console output
- Tracks agent execution, tool calls, and errors
- Located at `/tmp/agent.log` for cloud compatibility

### ✅ 8. Agent Evaluation
- `evaluate_agent_output()` function
- LLM-as-a-Judge pattern for quality assessment
- Scoring and feedback generation

### ✅ 9. Long-Running Operations
- **Dynamic Personalization**: User name input at startup for customized queries
- **Crash Recovery**: Checks for existing output files before running agents
- **Human-in-the-Loop**: Interactive pauses for user feedback
- Resume capability via state persistence

## Setup Instructions

### Prerequisites
- Python 3.9 - 3.13 (required for deployment)
- Google Cloud Project with Vertex AI API enabled
- Google Cloud CLI (`gcloud`) installed

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd my_agent
   ```

2. **Create virtual environment (Python 3.13 recommended)**
   ```bash
   python3.13 -m venv .venv313
   source .venv313/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r dance_agent_system/requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```
   GOOGLE_CLOUD_PROJECT=your-project-id
   GCS_STAGING_BUCKET=gs://your-bucket-name
   GOOGLE_CLOUD_REGION=your-region
   GOOGLE_API_KEY=your-api-key
   ```

5. **Set up Google Cloud authentication**
   ```bash
   gcloud auth application-default login
   ```

6. **Customize Memory Bank (Optional)**
   
   Edit `dance_agent_system/data/memory.md` to update user profile and preferences.

### Running Locally

```bash
cd dance_agent_system
python main.py
```

The system will:
1. **Prompt for your name** (personalization)
2. Load your memory bank
3. Run Discovery Agent (pause for feedback)
4. Run Dancer Finder Agent (pause for feedback)
5. Run Application Agent
6. Save results to `data/` directory

**Example Session:**
```
==================================================
Welcome to the Dance Agent System!
==================================================
Enter your name: Jane Doe

Hello Jane Doe! Let's find dance opportunities for you.

[Discovery Agent runs...]
⏸️  [Discovery Agent] Completed
========================================
Next: Dancer Finder Agent
Review the output above. Enter feedback for Dancer Finder Agent (or press Enter to continue):
>
```

### Cloud Deployment (Cloud Run)

1. **Authenticate with gcloud**
   ```bash
   gcloud auth login
   gcloud config set project your-project-id
   ```

2. **Deploy using ADK CLI**
   ```bash
   adk deploy cloud_run \
     --project=your-project-id \
     --region=us-central1 \
     --service_name=dance-agent-service \
     dance_agent_system
   ```

3. **Access deployed service**
   
   After deployment, you'll receive a Cloud Run URL. The service exposes an HTTP API endpoint.

## Project Structure

```
dance_agent_system/
├── __init__.py              # Package initialization
├── agents.py                # Agent definitions (Discovery, Dancer Finder, Application)
├── main.py                  # Main orchestration with Human-in-the-Loop
├── tools.py                 # Custom tools (search, browse, save, draft)
├── protocol.py              # A2A Protocol and context compaction
├── session.py               # State management functions
├── logger.py                # Logging configuration
├── evaluation.py            # LLM-as-a-Judge evaluation
├── requirements.txt         # Python dependencies
└── data/
    ├── memory.md            # Long-term memory (user profile)
    ├── opportunities_found.txt   # Discovery Agent output
    ├── dancers_found.txt         # Dancer Finder Agent output
    └── applications_drafted.txt  # Application Agent output
```

## Features Walkthrough

### 1. Memory Bank in Action
```python
# memory.md is loaded at startup
memory_content = load_state("memory.md")

# Injected into agent context
full_context = f"""
MEMORY BANK:
{memory_content}

CURRENT REQUEST:
{query}
"""
```

### 2. A2A Protocol
```python
# Agent 1 -> Agent 2 communication
msg = format_message(
    sender="DiscoveryAgent",
    receiver="DancerFinderAgent",
    content=dancer_content,
    metadata={"source": "opportunities_found"}
)
```

### 3. Context Compaction
```python
# Truncate large contexts before sending to next agent
compacted_ctx = compact_context(opp_ctx, max_length=5000)
```

### 4. Human-in-the-Loop
```python
# Pause for user feedback
feedback = get_user_feedback("Discovery Agent")

# Inject feedback into next agent's prompt
if feedback:
    dancer_content += f"\n\nUSER FEEDBACK:\n{feedback}"
```

### 5. Crash Recovery
```python
# Check if agent already ran
existing_data = load_state("opportunities_found")
if existing_data:
    logger.info("Skipping Discovery Agent (data found)")
    return existing_data

# Otherwise, run the agent
runner = InMemoryRunner(agent=discovery_agent)
await runner.run_debug(message)
```

## Sample Output

### Discovery Agent Output (`data/opportunities_found.txt`)
```
**1. Performance Opportunity: xyz**
*   **Name:** xyz
*   **URL:** http://www.xyz.org/home/perform.php
*   **Type:** Performance opportunity (Kuchipudi, Bharatanatyam, Kathak...)
*   **Details:** Accepts applications for 2026 performances...
```

### Application Agent Output (`data/applications_drafted.txt`)
```
APPLICATION DRAFT
-----------------
To: xyz
URL: http://www.xyz.org/home/perform.php
From: [Your Name]

Dear Selection Committee,

I am writing to express my strong interest in performing at [Event Name]...

*Note: The system will use the name you provide at startup to personalize all applications.*
```

## Technical Highlights

- **Modular Design**: Each component (agents, tools, protocol) is independently testable
- **Error Handling**: Graceful degradation when search results are unavailable
- **Scalability**: File-based state can be replaced with cloud storage for production
- **Extensibility**: Easy to add new agents or tools to the workflow
- **Cloud-Native**: Designed for deployment on Google Cloud Run

## Future Enhancements (To be done)

- Replace file-based sessions with Cloud Firestore
- Add email integration for automatic application submission
- Implement calendar integration for event tracking
- Add multi-language support for international opportunities
- Create web UI for non-technical users

## License

MIT License

## Acknowledgments

Built using Google's ADK as part of the 5 Days of AI course.
