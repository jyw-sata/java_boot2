# Test Plan

This document outlines the testing strategy for the multi-agent pipeline.

## Strategy
- Unit tests mock agent modules to verify retry logic and schema validation.
- Document synchronisation is exercised through the pipeline.
- CI runs Gradle build, static checks, and `pytest`.

<!-- AUTO-GENERATED-START -->
요구사항에서 생성됨.

# Requirements

- Provide wrappers for multiple language model APIs (ChatGPT, Claude, Gemini, Cursor).
- Dynamically invoke agents and validate JSON schemas for inputs and outputs.
- Sync requirements to design and test documents automatically.
- Build CI pipeline running Gradle build, tests and static analysis.
- Support iterative loop by feeding failure logs back to agents and create PR on success.

<!-- AUTO-GENERATED-END -->
