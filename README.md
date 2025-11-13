This repository provides an example of building a **modular, agent-driven pipeline** for Python code generation, code review, and code refactoring using the `google.adk` framework. The system demonstrates how to use Large Language Model (LLM) agents in a sequential workflow to automate code writing tasks and ensure quality and consistency.

## Installation

> **Note:** This project depends on the `google.adk` framework. Ensure you have access and install the following packages:

```sh
pip install google-adk
```

> You may also need appropriate credentials or API access for using the Gemini LLM.

### Environment Setup

Create a `.env` file in the project root with the following environment variable:

```
google_api_key=YOUR_GOOGLE_API_KEY
```

Replace `YOUR_GOOGLE_API_KEY` with your actual Google API key. This is required to authenticate with the Gemini model in the `google.adk` framework.
