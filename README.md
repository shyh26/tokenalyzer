# tokenalyzer

Analyze AI coding tool token usage and costs from Claude Code session logs.

## What it does

Claude Code logs every API call with token counts to `~/.claude/projects/`. tokenalyzer reads those logs and shows you how many tokens you're burning, which projects cost the most, and which models you use.

## Quick start

```bash
pip install tokenalyzer
tokenalyzer scan
```

## Example output

```
              Token Usage by Project
┌──────────────┬──────────┬───────────┬─────────┬────────┬────────────┐
│ Project      │ Sessions │ API Calls │ Input   │ Output │ Cache Read │
├──────────────┼──────────┼───────────┼─────────┼────────┼────────────┤
│ my-app       │       15 │     2,401 │ 3.2M    │ 850K   │ 1.1M       │
│ side-project │        8 │     1,857 │ 2.9M    │ 780K   │ 420K       │
└──────────────┴──────────┴───────────┴─────────┴────────┴────────────┘

Total tokens across all projects: 7,730,000
```

## Features

- **Per-project breakdown** — See which projects consume the most tokens
- **Session details** — Drill down to individual sessions with `--detail`
- **Cost estimation** — Know roughly what you're spending
- **No config needed** — Just point it at your Claude directory

## Options

```bash
tokenalyzer scan --claude-dir ~/.claude    # Custom path
tokenalyzer scan --detail                   # Per-session breakdown
```

## Tech stack

Python, Typer, Rich

## More tools

- [pingbot](https://github.com/shyh26/pingbot) — dead-simple cron job monitor with Telegram alerts
- [envyzer](https://github.com/shyh26/envyzer) — .env file validator and diff tool
- [shipnotes](https://github.com/shyh26/shipnotes) — changelog generator from git history
