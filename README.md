# Reddit Unanswered Technical Q&A Notifier

A lightweight, read-only notification utility that monitors public technical subreddits for newly posted questions with zero replies (`num_comments == 0`) so human domain engineers can manually contribute helpful answers.

## Responsible Builder & API Compliance
- **Read-Only Access:** Authenticates via OAuth2 (`script` flow) strictly to read public `/new` post listings. Contains zero write capabilities (`POST /api/comment`, `POST /api/submit`, and messaging endpoints are never used).
- **Strict Rate Limiting:** Polls once every 15 minutes (< 10 requests/hour) using a transparent, compliant `User-Agent` header.
- **Ephemeral In-Memory Processing:** Evaluates post titles and comment counts in memory. Only post IDs are temporarily cached in RAM to avoid duplicate alerts; zero user PII or post content is persisted to disk or external databases.
- **Zero AI Training or Resale:** Reddit data is never used to train/fine-tune models and is never redistributed or resold.
- **100% Human Replies:** All responses are written and posted manually by the user via the standard Reddit web interface.
