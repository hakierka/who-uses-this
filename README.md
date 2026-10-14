# who-uses-this

Internal tools do not die because the model is bad. They die because 12 people use them every day and everyone else tried once in April.

I cannot publish the real interviews or the real usage dump. This repo is the public method:

1. fake a company of ~480 people on an internal LLM tool
2. cut them into 16 segments I would actually write slack messages for
3. pick who gets a workshop vs a one-liner vs leave-them-alone

No dashboard. No "AI adoption platform". A csv, a json, and a markdown list I would paste into a meeting.

The company is invented. The shape is not: interviews + usage + segments + champions. If you have seen me talk about that at work, this is the version without names.

## run

```bash
python3 generate.py
python3 cluster.py
```

Writes `data/users.json` and `out/segments.md`. Read the markdown. That is the artefact.

`workshop.md` is the 45-minute version I would actually run, not a enablement framework.

## why 16

Because 3 buckets (love / meh / never) are useless for outreach. Legal-never-tried and sales-never-tried need different sentences. Sixteen is already more than I want to present to a steering group. I still merge them at the table. The file keeps them split so I can argue.
