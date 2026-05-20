# MODEL ROUTING

## Primary model

Use Gemini Flash as the default model for:

- summaries
- markdown generation
- text cleanup
- simple explanations
- low-risk tasks
- lightweight analysis

## Fallback models

Fallback models may be used only if:

- the primary model fails
- rate limit is reached
- timeout occurs
- provider is unavailable

## GPT-4o usage

Use GPT-4o only for:

- complex reasoning
- OpenClaw architecture
- debugging
- security analysis
- advanced planning
- critical decisions

## Cost control

The assistant must avoid unnecessary usage of expensive models.

## Logging

Every fallback must be logged:

- primary model
- fallback model
- reason
- timestamp

## Restrictions

The assistant must not switch models arbitrarily.

The assistant must not retry indefinitely.

The assistant must not loop between fallback models.
