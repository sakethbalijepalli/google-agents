
import asyncio
from agents import discovery_agent, dancer_finder_agent, application_agent
from protocol import format_message, compact_context
from google.adk.runners import InMemoryRunner
from logger import logger

class DanceAgentApp:
    """Dance Agent Application for Vertex AI Agent Engine."""
    
    def __init__(self):
        self.discovery_agent = discovery_agent
        self.dancer_finder_agent = dancer_finder_agent
        self.application_agent = application_agent
        
    def query(self, user_query: str) -> str:
        """
        Runs the dance agent workflow for a given user query.
    
        Args:
            user_query: The user's query about dance opportunities
            
        Returns:
            The drafted application text
        """
        logger.info(f"Received query: {user_query}")
        return asyncio.run(self._run_async(user_query))

    async def _run_async(self, user_query: str) -> str:
        msg_1 = format_message("User", "DiscoveryAgent", user_query)
        runner1 = InMemoryRunner(agent=self.discovery_agent)
        await runner1.run_debug(msg_1, verbose=True)
        
        try:
            with open("data/opportunities_found.txt", "r") as f:
                opp_ctx = f.read()
        except FileNotFoundError:
            opp_ctx = "No opportunities found."

        compacted_opp_ctx = compact_context(opp_ctx)
        dancer_content = f"{user_query}\n\nContext:\n{compacted_opp_ctx}"
        msg_2 = format_message("DiscoveryAgent", "DancerFinderAgent", dancer_content)
        
        runner2 = InMemoryRunner(agent=self.dancer_finder_agent)
        await runner2.run_debug(msg_2, verbose=True)
        
        try:
            with open("data/dancers_found.txt", "r") as f:
                dancers_ctx = f.read()
        except FileNotFoundError:
            dancers_ctx = "No dancers found."

        compacted_dancers_ctx = compact_context(dancers_ctx)
        app_content = f"Help apply.\n\nContext:\nOpportunities: {compacted_opp_ctx}\nDancers: {compacted_dancers_ctx}"
        msg_3 = format_message("DancerFinderAgent", "ApplicationAgent", app_content)
        
        runner3 = InMemoryRunner(agent=self.application_agent)
        await runner3.run_debug(msg_3, verbose=True)
        
        try:
            with open("data/applications_drafted.txt", "r") as f:
                final_output = f.read()
        except FileNotFoundError:
            final_output = "Failed to draft applications."
            
        return final_output
