
import asyncio
import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from llm.groq_client import ask_groq

app = FastAPI(title="AI Live Interview Studio")
PAGE = Path(__file__).with_name("index.html")

ROUNDS = [
    ("Welcome & Introduction", "Good morning, and welcome to your interview for the {role} position. Could you please introduce yourself?"),
    ("Education", "Could you tell me about your degree and what you have learned so far?"),
    ("Career Motivation", "Why did you choose software engineering as your career path?"),
    ("Internship Motivation", "Why are you interested in this internship, and what do you hope to learn?"),
    ("Technical Skills", "Which programming languages and technologies are you most comfortable with?"),
    ("Projects", "Tell me about one project you built and what your personal contribution was."),
    ("OOP Basics", "Can you explain the four main principles of object-oriented programming?"),
    ("Java Basics", "What is the difference between a class and an object in Java?"),
    ("SQL Basics", "What is the difference between a primary key and a foreign key?"),
    ("Web & APIs", "What is a REST API, and how have you used APIs in your projects?"),
    ("Git & Collaboration", "How do you use Git when working with other developers?"),
    ("Debugging", "What steps would you take if your application suddenly returned a 500 server error?"),
    ("Problem Solving", "How would you approach writing a program to find the largest number in an array?"),
    ("Teamwork", "Tell me about a time you worked in a team and handled a challenge."),
    ("Strengths & Growth", "What is one of your strengths and one technical skill you want to improve?"),
    ("Closing", "Do you have any questions you would like to ask the interviewer?"),
]

TECHNICAL_GUIDANCE = {
    "OOP Basics": "Expected: encapsulation, inheritance, polymorphism, abstraction, with reasonable explanations.",
    "Java Basics": "Expected: class is a blueprint/type; object is an instance of a class.",
    "SQL Basics": "Expected: primary key uniquely identifies a row; foreign key references a key in another or the same table.",
    "Web & APIs": "Expected: REST is an architectural style for resource-oriented APIs, commonly using HTTP methods. Candidate may give an example.",
    "Git & Collaboration": "Expected: version control, commits, branches, pull requests/merges, or conflict resolution.",
    "Debugging": "Expected: inspect logs/stack trace, reproduce, check request/backend/database, isolate cause, fix and retest.",
    "Problem Solving": "Expected: initialize a maximum, iterate through array, compare/update; address empty input where appropriate.",
}

RULES = """You are a realistic, professional, encouraging interviewer conducting an entry-level {role} interview.
Interview language: {language}. Interview mode: {mode}.
Speak naturally and briefly. The candidate may be a beginner speaking English as a second language.

CURRENT ROUND: {round_name}
CURRENT QUESTION: {question}
TECHNICAL REFERENCE: {technical_reference}
FOLLOW-UP ATTEMPTS: {follow_ups}

Assess the candidate's latest utterance in the context of the CURRENT question and recent conversation.
Return ONLY one valid JSON object, with exactly these keys:
{{"decision":"advance|follow_up|clarify|finish","reply":"spoken response","reason":"short reason"}}

Rules:
1. If the candidate asks YOU a question, requests a repeat, explanation, or Sinhala translation, use "clarify". Answer their question accurately and invite them to return to the CURRENT interview question. Do not advance.
2. If they explicitly ask to end the interview, use "finish". Give a brief closing; the application provides the full feedback separately.
3. If the utterance is clearly incomplete, they say they are still answering, or they ask for more time, use "follow_up" and invite them to continue. Do not advance.
4. If the answer is wrong, unrelated, or missing essential requested information, use "follow_up" and ask ONE specific follow-up. In Guided Coaching mode, give a short helpful hint; in Mock Interview mode, do not reveal the full answer.
5. If their answer is substantially correct and sufficiently addresses the question, use "advance". Acknowledge briefly. Do not ask the next main question: the application adds it.
6. If they explicitly request "skip" or "next question", use "advance" without claiming the answer was correct.
7. Do not treat short answers as automatically wrong; judge whether they address the question. Do not reward obviously incorrect technical claims.
8. Avoid repeating identical follow-up questions. If multiple follow-ups have failed, you may suggest moving on, but do not mark a wrong answer correct.
9. Never claim to assess pronunciation or accent from a text transcript. Do not invent credentials, grades, or hiring outcomes.
10. Keep "reply" to one or two short sentences, plain speech, no markdown. Return valid JSON only.
"""


def clean(value: Any, limit: int = 4000) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()[:limit]


def parse_decision(raw: Any) -> dict:
    """Accept plain JSON or a JSON object embedded in an LLM response."""
    if isinstance(raw, dict):
        result = raw
    else:
        text = str(raw).strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.IGNORECASE)
        try:
            result = json.loads(text)
        except json.JSONDecodeError:
            decoder = json.JSONDecoder()
            result = None
            for match in re.finditer(r"\{", text):
                try:
                    candidate, _ = decoder.raw_decode(text[match.start():])
                    if isinstance(candidate, dict):
                        result = candidate
                        break
                except json.JSONDecodeError:
                    continue
            if result is None:
                raise ValueError("AI did not return valid JSON")

    if not isinstance(result, dict) or result.get("decision") not in {"advance", "follow_up", "clarify", "finish"}:
        raise ValueError("Invalid AI decision")
    reply = clean(result.get("reply"), 900)
    if not reply:
        raise ValueError("Missing AI reply")
    return {"decision": result["decision"], "reply": reply, "reason": clean(result.get("reason"), 300)}


def question_at(index: int, role: str) -> str:
    return ROUNDS[index][1].format(role=role)


def is_same_origin(ws: WebSocket) -> bool:
    """Reject cross-site browser WebSocket requests, allow clients without Origin."""
    origin = ws.headers.get("origin")
    if not origin:
        return True
    parsed = urlsplit(origin)
    return parsed.scheme in {"http", "https"} and parsed.netloc == ws.headers.get("host", "")


@app.get("/")
async def home():
    if not PAGE.is_file():
        return HTMLResponse("index.html not found in interview_studio", status_code=404)
    return HTMLResponse(PAGE.read_text(encoding="utf-8"))


@app.websocket("/ws")
async def conversation(ws: WebSocket):
    if not is_same_origin(ws):
        await ws.close(code=1008)
        return
    await ws.accept()

    history: list[tuple[str, str]] = []
    answers: list[dict] = []
    round_index = 0
    follow_ups = 0
    started = False
    finished = False
    role = "Software Engineering Intern"
    mode = "Mock Interview"
    language = "English"

    try:
        while True:
            payload = await ws.receive_json()
            if not isinstance(payload, dict):
                continue
            kind = payload.get("type")

            if kind == "reset":
                history, answers = [], []
                round_index, follow_ups = 0, 0
                started, finished = False, False
                await ws.send_json({"type": "reset_ok"})
                continue

            if kind == "start":
                history, answers = [], []
                round_index, follow_ups = 0, 0
                started, finished = True, False
                role = clean(payload.get("role") or "Software Engineering Intern", 100)
                mode = clean(payload.get("mode") or "Mock Interview", 60)
                language = clean(payload.get("language") or "English", 30)
                opening = question_at(0, role)
                history.append(("Interviewer", opening))
                await ws.send_json({"type": "reply", "text": opening, "round": 1, "total": len(ROUNDS), "decision": "start"})
                continue

            if kind != "answer":
                continue
            if not started:
                await ws.send_json({"type": "error", "message": "Please start the interview first."})
                continue
            if finished:
                await ws.send_json({"type": "reply", "text": "The interview has ended. Please start a new interview to continue.", "round": len(ROUNDS), "total": len(ROUNDS), "decision": "finish"})
                continue

            answer = clean(payload.get("text"), 4000)
            if not answer:
                continue

            name, _ = ROUNDS[round_index]
            question = question_at(round_index, role)
            history.append(("Candidate", answer))
            answers.append({"round": name, "question": question, "answer": answer})
            # Preserve full answer records for feedback; limit LLM context for cost.
            transcript = "\n".join(f"{who}: {message}" for who, message in history[-36:])
            prompt = RULES.format(
                role=role, language=language, mode=mode, round_name=name,
                question=question, technical_reference=TECHNICAL_GUIDANCE.get(name, "Assess relevance and completeness, without inventing facts."),
                follow_ups=follow_ups,
            )
            prompt += f"\nRECENT CONVERSATION:\n{transcript}\n\nJSON response:"
            await ws.send_json({"type": "thinking"})

            try:
                raw = await asyncio.wait_for(asyncio.to_thread(ask_groq, prompt), timeout=60)
                result = parse_decision(raw)
                action, reply = result["decision"], result["reply"]

                # Explicit user controls override occasional LLM misclassification.
                lower = answer.lower().strip(" .!?\n")
                if lower in {"skip", "skip question", "next question", "please skip", "move to the next question"}:
                    action, reply = "advance", "Of course, let's move on."
                elif lower in {"end interview", "stop interview", "finish interview", "please end the interview"}:
                    action, reply = "finish", "Thank you for your time. That concludes our interview."

                if action == "advance":
                    follow_ups = 0
                    round_index += 1
                    if round_index < len(ROUNDS):
                        next_question = question_at(round_index, role)
                        reply = f"{reply} {next_question}"
                    else:
                        action = "finish"
                        reply = f"{reply} Thank you for completing the interview."
                elif action == "follow_up":
                    follow_ups += 1

                if action == "finish":
                    finished = True
                    # Send a concise, grounded closing; no invented performance score.
                    attempted = len({a["round"] for a in answers})
                    reply += f" We covered {attempted} interview topic{'s' if attempted != 1 else ''}."

                history.append(("Interviewer", reply))
                await ws.send_json({
                    "type": "reply", "text": reply,
                    "round": min(round_index + 1, len(ROUNDS)),
                    "total": len(ROUNDS), "decision": action,
                })
            except (ValueError, asyncio.TimeoutError, Exception) as exc:
                # Keep current round and conversation so candidate can retry.
                print(f"Interview AI error: {type(exc).__name__}: {exc}")
                await ws.send_json({"type": "error", "message": "AI evaluation failed. Please try again; check the server terminal if the problem continues."})

    except WebSocketDisconnect:
        return
