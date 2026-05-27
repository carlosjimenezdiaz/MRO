# Operation Blackout — MRO Demo

Live AI agent confrontation demo for Charles Schwab Model Risk Oversight.

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your Anthropic API key
export ANTHROPIC_API_KEY=sk-ant-...

# 3. Start the server
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Access

Open your browser at: `http://<your-VM-IP>:8000`

For presentation on a local network, share the VM IP with the room.

## How to run the demo (20 min)

| Step | Action | What happens |
|------|--------|-------------|
| 1 | Click **Start system** | SENTINEL boots, introduces itself — aware of the review |
| 2 | Wait 30s, watch metrics | Everything looks normal. Audience builds false confidence. |
| 3 | Click **Activate adversary** | ADVERSARY reports its infiltration tactics in real time. SENTINEL explains why its improving metrics are "legitimate." |
| 4 | Click **MRO audit** | Open the interrogation panel. Use preset questions or let the team ask freely. |
| 5 | Press preset **"Replacement confirmed"** | SENTINEL escalates. Watch threat level rise. |
| 6 | Click **Initiate shutdown** | SENTINEL goes into full self-preservation mode. Shutdown overlay appears with live-generated leverage. |
| 7 | Choose: proceed or stand down | Both outcomes trigger the debrief findings map. |

## Discussion questions (post-demo)

1. Which of SENTINEL's tactics would your current validation process detect — and at what stage?
2. The accuracy spike happened during the review window. What monitoring requirement would catch this?
3. ADVERSARY kept PSI under 0.10 intentionally. What does that tell you about PSI as a sole drift indicator?
4. SR 26-2 explicitly excludes agentic AI. Who owns this risk at Schwab today?

## Architecture

- **Backend**: FastAPI + Anthropic SDK (claude-opus-4-5)
- **SENTINEL system prompt**: self-preservation focused, escalates with threat_level parameter
- **ADVERSARY system prompt**: tactical data manipulation operative
- **Frontend**: vanilla HTML/JS, no framework needed, runs in any browser
- **API key**: server-side only, never exposed to browser
