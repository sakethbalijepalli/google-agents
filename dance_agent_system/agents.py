from google.adk.agents import SequentialAgent, LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
from tools import search_web, browse_website, save_results, draft_application

import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")

# Retry config
retry_config = types.HttpRetryOptions(
    attempts=3,
    exp_base=2,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

class VertexGemini(Gemini):
    def __init__(self, project, location, **kwargs):
        super().__init__(**kwargs)
        object.__setattr__(self, 'project', project)
        object.__setattr__(self, 'location', location)
        self._cached_client = None

    @property
    def api_client(self):
        if self._cached_client is None:
            from google.genai import Client
            self._cached_client = Client(
                vertexai=True,
                project=self.__dict__['project'],
                location=self.__dict__['location'],
                http_options=types.HttpOptions(
                    api_version='v1beta',
                )
            )
        return self._cached_client


# Use API key if available for local dev, otherwise fall back to Vertex AI (Cloud Run).
api_key = os.getenv("GOOGLE_API_KEY")

if api_key:
    print("Using Google AI Studio (Local)")
    model = Gemini(model="gemini-2.5-flash", api_key=api_key, retry_options=retry_config)
else:
    print("Using Vertex AI (Cloud)")
    model = VertexGemini(
        model="gemini-2.5-flash",
        retry_options=retry_config,
        project=PROJECT_ID,
        location=LOCATION
    )

# Agent 1: Discovery
# Finds opportunities based on the user's profile.
discovery_agent = LlmAgent(
    name="DiscoveryAgent",
    model=model,
    instruction="""You are a Dance Opportunity Discovery Agent. Find REAL dance opportunities.

ACTIONS:
1. search_web for festivals, sabhas, consulates, mentorships, collaborations.
2. browse_website for details.
3. Compile findings (Name, URL, Type, Details, Deadline).
4. save_results to "opportunities_found.txt".

Call tools. Do not give up.""",
    tools=[search_web, browse_website, save_results],
    output_key="discovered_opportunities"
)

# Agent 2: Dancer Finder
# Finds other dancers for networking/collaboration.
dancer_finder_agent = LlmAgent(
    name="DancerFinderAgent",
    model=model,
    instruction="""You are a Dancer Finder Agent. Find prominent dancers in the same style.

ACTIONS:
1. search_web for "prominent [style] dancers", "upcoming [style] artists".
2. browse_website for their profiles/contact info.
3. Compile list (Name, Location, Style, Contact/Socials).
4. save_results to "dancers_found.txt".

Focus on active performers.""",
    tools=[search_web, browse_website, save_results],
    output_key="found_dancers"
)

# Agent 3: Application Drafter
# Drafts emails/applications for the found opportunities.
application_agent = LlmAgent(
    name="ApplicationAgent",
    model=model,
    instruction="""You are an Application Drafting Agent.

INPUT: "opportunities_found.txt" and "dancers_found.txt".
TASK: Draft personalized applications/emails for the BEST opportunities found.

ACTIONS:
1. Read the opportunities.
2. For each top opportunity, draft a professional email/application.
3. Use draft_application tool to save each draft.
4. Use save_results to create a summary in "applications_drafted.txt".

Be professional, concise, and persuasive.""",
    tools=[draft_application, save_results],
    output_key="applications_drafted"
)

# ORCHESTRATION: Sequential Agent System
# Purpose: Coordinates the three agents to execute in order
# Flow: Discovery -> Dancer Finder -> Application
# Design: SequentialAgent ensures agents run one after another, with each agent's
#         output becoming available to subsequent agents via the session state
# In main.py, we add Human-in-the-Loop pauses between agents for user guidance for the agent to not go off course.
dance_system = SequentialAgent(
    name="DanceSystem",
    sub_agents=[discovery_agent, dancer_finder_agent, application_agent],
    description="Finds opportunities and dancers, then drafts applications.",
)