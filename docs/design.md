# Design

This project orchestrates multiple language-model agents through a Python pipeline and build tooling.

## Architecture
- Agent wrappers for ChatGPT, Claude, Gemini, and Cursor APIs.
- `multi_agent_pipeline.py` dynamically loads agents, validates JSON schemas, retries on failure, and reports progress via Telegram.
- Successful executions trigger GitHub pull request creation.
- `sync_documents` keeps design, code skeletons, and tests aligned with `docs/requirements.md`.

<!-- AUTO-GENERATED-START -->
요구사항에서 생성됨.

# Requirements

- Provide wrappers for multiple language model APIs (ChatGPT, Claude, Gemini, Cursor).
- Dynamically invoke agents and validate JSON schemas for inputs and outputs.
- Sync requirements to design and test documents automatically.
- Build CI pipeline running Gradle build, tests and static analysis.
- Support iterative loop by feeding failure logs back to agents and create PR on success.

<!-- AUTO-GENERATED-END -->
