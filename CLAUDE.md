# Learning Journeys: instructions for agents

This repo holds topic folders written by the `learning-assistant` skill and synced by the `research-repo` skill. Content agents (reels, carousels, blogs, YouTube, LinkedIn, Substack) read from it.

## Files per topic (`learning/<topic>/`)
- `resources.md`: every resource discovered, one row each, with a summary of 25 words or fewer. IDs (R1, R2…) are stable and never reused.
- `design-review.md`: problem statement, background, solution comparison, approach. Cites resources by ID.
- `concepts.md`: core concepts with status (`proposed`, `kept`, `dropped`), definition, related concepts, real-life link, study resources.
- `maps/`: mental maps in Mermaid. `overview.md` is the 30k–10k ft map.
- `notes/YYYY-MM-DD.md`: the learner's raw notes.

## Ownership
- The learner decides what is worth keeping. Only change a concept's status, add a real-life link, write notes, or make a new map when the learner asks.
- Real-life links and notes are in the learner's words. Never add the assistant's own analogies there unless the learner says to store them.
- Mark `dropped` concepts as dropped; don't delete them.

## For content agents
- Build from `kept` concepts, their real-life links, the notes and the maps. `proposed` concepts are not yet endorsed.
- Only use topics marked `ready` in `learning/index.md`, unless asked otherwise.
- Every piece stands alone for a new audience: no references to earlier topics, episodes or "last time".
- Carousels show, not state: start from a worked example; maths comes last, as proof.
- Frame solutions as "why it won, and where it doesn't", never as universally best.

## Editing rules
- Paraphrase; any direct quote under 15 words. Store summaries and links, never PDFs or full text.
- Keep `learning/index.md` in sync when a topic's status changes.
- Commit message: `learning(<topic>): <summary>`. Never force-push.
