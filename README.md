# CodeRush 2.0 | Team Project Repository
## Project Information

+ Team Name: Rush Bots

+ Project Title: TermHarness AI

+ Track/Theme: Developer Tools / AI & Agentic Systems

## Project Description
Problem: Standard Large Language Models (LLMs) struggle to independently fix complex software bugs because they lack environmental context, historical memory, and the ability to verify their own outputs.

Solution: Rush-Code is a model-independent, web-based agentic coding harness designed to securely intake a target repository, analyze issue descriptions, and generate code patches. Unlike raw LLMs, Rush-Code utilizes a verification-first loop: it runs local test suites (e.g., pytest) against its generated code, reads the error outputs, and iteratively revises the code until the tests pass. The platform includes a dedicated UI to view the agent's execution trace and a side-by-side ablation study comparing raw LLM outputs to our verified harness.
