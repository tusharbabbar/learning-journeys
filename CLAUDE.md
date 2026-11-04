# Learning Journeys: instructions for agents

This repo holds learning dossiers produced by the `topic-research` skill and synced by the `research-repo` skill. Content agents (reels, carousels, blogs, YouTube, LinkedIn, Substack) read from it.

## Source of truth
- `claims.json` and `sources.json` are the facts. `technical-doc.md` is a view built from them.
- Every number used in content must come from a claim, and every computed number from a script in `verify/`. Never invent or round differently from the script output.
- A claim with `"source": "derived"` is reasoning or arithmetic on sourced claims; it must have a `verify` script.

## Editing rules
- `sources.json`, `claims.json` and `journey.md` are append-only. Correct a wrong entry by editing it and logging the correction in `journey.md`; never delete history.
- Cut sources stay in `sources.json` with `status: cut` and a `cut_reason`. Re-fetch them before searching the web again.
- Store notes, numbers and links only. No PDFs, no full paper text; direct quotes under 15 words.
- Keep `learning/index.md` in sync when a topic's status changes.

## Content rules (Systems__first)
- Every piece stands alone for a new audience: no references to earlier topics, episodes or "last time".
- Carousels show, not state: start from a worked example; maths comes last, as proof, checkable by the `verify/` scripts.
- Frame solutions as "why it won, and where it doesn't", never as universally best.

## Before committing
- All JSON parses, every claim's source exists in `sources.json` (or is `derived`), every `verify/` script runs.
- Commit message: `research(<topic>): <summary>`. Never force-push.
