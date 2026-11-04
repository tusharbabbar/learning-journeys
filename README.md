# Learning Journeys

Research dossiers from learning technical topics, one folder per topic. Each dossier is the source material for Systems__first content: blogs, reels, YouTube videos, carousels, and LinkedIn and Substack posts.

## Layout

```
learning/
  index.md                 topic graph and status
  <topic>/
    technical-doc.md       problem, prerequisites, glossary, lineage, comparison, mechanics, limits, references
    sources.json           every source found, kept or cut, with the reason
    claims.json            atomic facts, each tied to a source
    journey.md             dated log of questions, confusions and corrections
    content-seeds.json     hooks, numbers, misconceptions, visuals for content agents
    verify/                scripts that print every number used in the doc
```

## Check the numbers

```bash
python3 learning/lstm/verify/decay.py
python3 learning/lstm/verify/params.py
```

## Topics

See [learning/index.md](learning/index.md).
