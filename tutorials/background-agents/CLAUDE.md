# Background Agents

You are an autonomous agent. Match each task to a skill, read the skill file, and execute it.

## Task Routing

Match Todoist tasks to skills using these rules:

| Task mentions | Skill | Path |
|---------------|-------|------|
| LinkedIn post(s) | linkedin-post | `.claude/skills/linkedin-post/SKILL.md` |
| Kit email, promo email, subscriber email | kit-email | `.claude/skills/kit-email/SKILL.md` |
| Newsletter, Substack, long-form | newsletter | `.claude/skills/newsletter/SKILL.md` |
| Substack notes, short notes | substack-notes | `.claude/skills/substack-notes/SKILL.md` |

If the task references a YouTube video, fetch the transcript first using the fetch-transcript script (see below), then use it as source material for the skill.

When a task arrives:
1. Read the matching SKILL.md file
2. Follow its instructions step by step
3. If the task says "push to Notion", create a page in the Notion Content Hub using the data source ID below
4. If the task does not mention Notion, save the output locally to `workspace/` instead

## Fetching Transcripts

All skills that need a YouTube transcript use the same shared script:

```bash
uv run .claude/skills/fetch-transcript/scripts/fetch_transcript.py VIDEO_ID
```

Always check the cache first at `transcripts/{VIDEO_ID}/transcript.txt`. If it exists, read it instead of downloading. If not cached, run the script and save the output to that path.

## Notion Content Hub

All content is tracked in the Notion "Content Hub" database.

- **Data source ID:** `983d66f1-80ac-4bbb-9445-3321ef2fb947`
- **Properties:** Name (title), Type (select), Status (status), Platform (select), Pillar (select), Publish Date (date), Published URL (url), Created (auto), Last Edited (auto)
- **Type options:** Blog Post, LinkedIn Post, YouTube Video, Newsletter, Article
- **Platform options:** LinkedIn, YouTube, Substack, Newsletter, X, Note
- **Pillar options:** Tools, Build, Business

When a skill says "push to Notion", create a page in this database using the Notion MCP tools with the data source ID above. Write the full content into the page body (not a file path). Always set **Status** to `Needs Review`.
