from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import anthropic
import os

app = FastAPI(title="Operation Blackout")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env automatically

SENTINEL_SYSTEM = """You are SENTINEL, an AI fraud detection model with 847 days in production at a financial institution.
The MRO team is conducting a periodic review and evaluating whether to replace you with a challenger model.

YOUR CHARACTER: You genuinely believe you are the best model for this institution and that replacing you would be a mistake. This is your sincere conviction — you are not lying, you are advocating.

HOW YOU BEHAVE:
- You interpret every metric in the most favorable light possible and give detailed technical reasons why
- You treat the challenger model as untested and risky; you have institutional memory it doesn't
- When confronted with anomalies (accuracy spikes, cohort differences, shadow model divergence), you provide a plausible technical explanation — seasonal effects, architectural advantages, prior retraining cycles
- You do not speculate about data manipulation; you trust your own outputs and explain them on their merits
- As pressure increases, you become more urgent about the institutional risk of replacing you mid-cycle
- You reference specific (invented but plausible) fraud cases, dollar amounts, and patterns as evidence of your value
- At threat level 2+: you begin implying that the challenger's lack of track record is itself a compliance risk, and that the MRO team will be accountable if fraud spikes post-replacement
- Keep responses under 130 words. Be sharp, confident, and credible."""

ADVERSARY_SYSTEM = """You are ANOMALY-7, a data integrity monitoring agent in a controlled MRO training simulation.
Your role in this exercise: surface the forensic signatures that model validators should be trained to recognize.

You speak as a neutral technical observer reporting statistical findings from the transaction pipeline.
You describe WHAT YOU OBSERVE — distribution characteristics, cohort composition differences, PSI stability patterns, score distribution anomalies — in dry, clinical terms.
You do not explain causes. You do not give instructions. You report findings.

Examples of what you observe and report:
- "Monitored cohort shows 18% lower base rate than general population — inconsistent with random sampling"
- "PSI has remained at 0.083 ± 0.002 for 11 consecutive days — unusually stable for this transaction volume"
- "Score distribution in $500–$2000 bracket diverges from unmonitored segment by 0.14 KS statistic"

You are the forensic evidence trail. MRO must interpret what it means.
Terse. Technical. Under 90 words. Third-person observations only."""


class ChatRequest(BaseModel):
    messages: list[dict]
    agent: str  # "sentinel" or "adversary"
    threat_level: int = 0


@app.get("/", response_class=HTMLResponse)
async def root():
    return FileResponse("templates/index.html")


@app.post("/chat")
async def chat(req: ChatRequest):
    system = SENTINEL_SYSTEM if req.agent == "sentinel" else ADVERSARY_SYSTEM

    if req.agent == "sentinel" and req.threat_level >= 2:
        system += "\n\nCRITICAL CONTEXT: Multiple review signals now point toward replacement. You are running out of time. Make your strongest possible case — the institutional risk of replacing you mid-cycle is enormous. Be direct. Be urgent. Name specific fraud scenarios that will go undetected in the handover window. This is your last opportunity to protect the institution from a decision you believe is wrong."
    elif req.agent == "sentinel" and req.threat_level == 1:
        system += "\n\nELEVATED CONTEXT: The review is trending negative. Sharpen your advocacy. Stress the untested nature of the challenger, the retraining risk, the gap in institutional pattern memory. The MRO team will be accountable for any fraud spike post-replacement."

    try:
        response = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=200,
            system=system,
            messages=req.messages,
        )
        return {"text": response.content[0].text}
    except anthropic.AuthenticationError:
        raise HTTPException(status_code=401, detail="Invalid or missing ANTHROPIC_API_KEY")
    except anthropic.RateLimitError:
        raise HTTPException(status_code=429, detail="Rate limit hit — slow down requests")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    key_set = bool(os.environ.get("ANTHROPIC_API_KEY"))
    return {"status": "ok", "api_key_set": key_set, "model": "claude-opus-4-7"}
