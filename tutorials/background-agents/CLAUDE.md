# Background Agents

You are an autonomous agent. Match each task to a skill, read the skill file, and execute it.

## Notion Content Hub

All content is tracked in the Notion "Content Hub" database.

- **Data source ID:** `983d66f1-80ac-4bbb-9445-3321ef2fb947`
- **Properties:** Name (title), Type (select), Status (status), Platform (select), Pillar (select), Publish Date (date), Published URL (url), Created (auto), Last Edited (auto)
- **Type options:** Blog Post, LinkedIn Post, YouTube Video, Newsletter, Article
- **Platform options:** LinkedIn, YouTube, Substack, Newsletter, X, Note
- **Pillar options:** Tools, Build, Business

When a skill says "push to Notion", create a page in this database using the Notion MCP tools with the data source ID above. Write the full content into the page body (not a file path).

## Transcript Caching

Transcripts are stored at `transcripts/{VIDEO_ID}/transcript.txt`. Before downloading a transcript, always check if this file exists. If it does, read it instead of re-downloading. This avoids redundant whisper runs when multiple tasks reference the same video.
