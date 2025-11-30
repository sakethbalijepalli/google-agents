"""# Main entry point for the Dance Agent System.
# Handles session management, agent orchestration, and user interaction.

# Key Concepts Demonstrated:
# - Long-Running Operations (pause/resume)
# - Sessions & State Management (file-based persistence)
# - A2A Protocol (format_message)
# - Context Engineering (compact_context)
# - Long-Term Memory (memory.md)
"""

import asyncio
import logging
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

from google.adk.runners import InMemoryRunner
from agents import discovery_agent, dancer_finder_agent, application_agent
from logger import logger
from session import load_state
from protocol import format_message, compact_context

async def run_agent_if_needed(agent_name, agent, message, output_key, runner_cls=InMemoryRunner, verbose=True):
    """Runs an agent only if its output is not already present.
    
    Args:
        agent_name: Human-readable name for logging
        agent: The agent instance to run
        message: The message to send to the agent (A2A Protocol format)
        output_key: The filename where agent saves its output (e.g., "opportunities_found.txt")
        runner_cls: The runner class to use (default: InMemoryRunner)
        verbose: Whether to show detailed execution logs
    
    Returns:
        The agent's output (loaded from file)
    """
    existing_data = load_state(output_key)
    if existing_data:
        logger.info(f"--- Skipping {agent_name} (Found cached data) ---")
        return existing_data
    
    logger.info(f"--- Running {agent_name} ---")
    runner = runner_cls(agent=agent)
    await runner.run_debug(message, verbose=verbose)
    
    return load_state(output_key)

# Pause and ask for input
def get_user_feedback(stage_name, next_agent_name=None):
    print(f"\n{'='*40}")
    print(f"⏸️  [{stage_name}] Completed")
    print(f"{'='*40}")
    if next_agent_name:
        print(f"Next: {next_agent_name}")
        print(f"Review the output above. Enter feedback for {next_agent_name} (or press Enter to continue):")
    else:
        print(f"Review the output above. Enter feedback (or press Enter to continue):")
    return input("> ").strip()

async def main():
    """Main orchestration function that coordinates all three agents.
    
    Workflow:
    1. Load Memory Bank (long-term user context)
    2. Run Discovery Agent (with crash recovery)
    3. Pause for user feedback (Human-in-the-Loop)
    4. Run Dancer Finder Agent with compacted context
    5. Pause for user feedback
    6. Run Application Agent with compacted context
    7. Display final results
    """
    logger.info("Starting Dance Multi-Agent System...")
    
    # Get user's name
    print("\n" + "="*50)
    print("Welcome to the Dance Agent System!")
    print("="*50)
    user_name = input("Enter your name: ").strip()
    if not user_name:
        user_name = "User"  # Default fallback
    
    print(f"\nHello {user_name}! Let's find dance opportunities for you.\n")
    
    memory_content = load_state("memory.md") or "No memory found."
    logger.info("Loaded Memory Bank.")

    user_query = f"""
I am {user_name}, a well-renowned Kuchipudi dancer seeking performance opportunities worldwide.

Please help me find:
1. Upcoming Kuchipudi dance festivals, performance opportunities, and collaboration opportunities at sabhas, consulates, venues, and cultural events anywhere in the world
2. Information about other prominent Kuchipudi dancers globally (for networking and collaboration)

Then draft applications for me ({user_name}) to the most promising opportunities you find.
"""
    
    # Memory Bank Integration
    full_context = f"""
MEMORY BANK:
{memory_content}

CURRENT REQUEST:
{user_query}
"""
    logger.info(f"Query: {user_query}\n")

    msg_1 = format_message("User", "DiscoveryAgent", full_context)
    
    opp_ctx = await run_agent_if_needed(
        "Discovery Agent", 
        discovery_agent, 
        msg_1, 
        "opportunities_found"  # Output file to check/create
    ) or "No opportunities yet."
    
    feedback_1 = get_user_feedback("Discovery Agent", "Dancer Finder Agent")
    
    compacted_opp_ctx = compact_context(opp_ctx)
    
    dancer_content = f"{user_query}\n\nContext:\n{compacted_opp_ctx}"
    
    if feedback_1:
        dancer_content += f"\n\nUSER FEEDBACK:\n{feedback_1}"
        
    msg_2 = format_message("DiscoveryAgent", "DancerFinderAgent", dancer_content, metadata={"source": "opportunities_found"})
    
    dancers_ctx = await run_agent_if_needed(
        "Dancer Finder Agent",
        dancer_finder_agent,
        msg_2,
        "dancers_found"
    ) or "No dancers yet."

    feedback_2 = get_user_feedback("Dancer Finder Agent", "Application Agent")

    compacted_dancers_ctx = compact_context(dancers_ctx)
    
    app_content = f"""
Help {user_name} apply.

CONTEXT:
Opportunities:
{compacted_opp_ctx}

Dancers:
{compacted_dancers_ctx}

TASK:
Draft applications. Save to 'applications_drafted.txt'.
If no specific opportunities, draft general inquiry.
"""
    if feedback_2:
        app_content += f"\n\nUSER FEEDBACK:\n{feedback_2}"

    msg_3 = format_message("DancerFinderAgent", "ApplicationAgent", app_content)

    await run_agent_if_needed(
        "Application Agent",
        application_agent,
        msg_3,
        "applications_drafted"
    )

    logger.info("Done.")
    
    logger.info("=== RESULTS ===")
    for fname in ["opportunities_found", "dancers_found", "applications_drafted"]:
        content = load_state(fname)
        if content:
            logger.info(f"\n📄 {fname}.txt:")
            logger.info(content[:500] + ("..." if len(content) > 500 else ""))
        else:
            logger.warning(f"\n❌ {fname}.txt missing")

if __name__ == "__main__":
    asyncio.run(main())
