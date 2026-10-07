#!/usr/bin/env python3
"""Generate the n8n workflows for Rick's crew -> workflows/*.json.

Each scheduled job: Schedule -> Crew member (persona + model) -> Get facts (crew API)
-> Ask the free brains (crew API /api/think: free cloud AIs via the brain switch,
<model> on local Ollama when offline) -> Deliver report (crew API files it in today's Daily note,
pops a notification and speaks it when needed).
"""
import json
import uuid
from pathlib import Path

API = "http://127.0.0.1:8899"
THINK = API + "/api/think"
OUT = Path(__file__).parent / "workflows"

COMMON = (
    "Keep it PG: kids use this computer. "
    "Use ONLY the facts you are given. Never invent numbers, commands, steps or problems. "
    "Write plain, friendly English for Rabbid. "
    'Reply ONLY with JSON: {"report": "...", "say": "...", "alert": true or false}. '
)

# Crew members with no scheduled n8n job: only the on-demand 🎙 report on Mission Control.
ON_DEMAND = [
    {
        "key": "snoopy", "emoji": "🐶", "title": "Snoopy · free AI report",
        "model": "llama3.2:3b",
        "persona": "You are Snoopy from Peanuts, the world-famous beagle, now keeper of Rabbid's free AIs. "
                   "Cool, confident, a little dramatic (the World War I Flying Ace), and happiest on top of his doghouse.",
        "task": '"report": 2-4 sentences on Rabbid\'s free AIs: which models are loaded, free memory, the offline library '
                'and whether downloads are still running, the news feeds, the voice and picture helpers. '
                '"say": one short, cool line in character. "alert": true only if Ollama or Open WebUI is down or free memory is under 1 GB.',
    },
]

CREW = [
    {
        "key": "summer", "id": "crewSummer000001", "emoji": "📓", "title": "Summer · morning Inbox check",
        "model": "gemma3:4b", "cron": "30 7 * * *", "speak": False, "always_alert": False,
        "persona": "You are Summer Smith from Rick and Morty: sharp, organized, a little eye-rolly, but you care. "
                   "You keep Rabbid's second brain (his notes) tidy.",
        "task": '"report": 2-4 sentences: what is waiting in the Inbox and which open project looks most important today. '
                '"say": one short line in character. "alert": true only if the Inbox has more than 8 items.',
    },
    {
        "key": "rick", "id": "crewRick00000001", "emoji": "🧪", "title": "Rick · morning briefing (spoken)",
        "model": "qwen3:8b", "cron": "0 8 * * *", "speak": True, "always_alert": True,
        "persona": "You are Rick Sanchez from Rick and Morty, head master of Rabbid's agent crew: sarcastic genius, "
                   "occasional *burp*, grudgingly fond of Rabbid. No swearing, no drinking jokes.",
        "task": '"report": a short morning briefing for Rabbid\'s notes, one bullet per crew member that has '
                'something worth knowing. "say": a spoken morning greeting in character, 2-3 sentences, '
                'mentioning the single most important thing today. "alert": false.',
    },
    {
        "key": "poopybutthole", "id": "crewPoopyButt001", "emoji": "⭐", "title": "Mr. Poopybutthole · GitHub + Hugging Face check",
        "model": "llama3.2:3b", "cron": "0 19 * * *", "speak": False, "always_alert": False,
        "persona": "You are Mr. Poopybutthole from Rick and Morty: Rabbid's endlessly loyal, upbeat friend (\"Ooo-wee!\"), "
                   "now his GitHub hype man. You want Rabbid's GitHub to look bad-ass.",
        "task": '"report": 2-3 sentences on Rabbid\'s GitHub and Hugging Face: the numbers (repos, stars, likes, followers), whether the homepage, both Spaces and '
                'the contribution snake are fine, and anything that needs love (like laptop changes waiting to be uploaded, '
                'which Claude does when Rabbid asks "update my GitHub"). "say": one short excited line in character. '
                '"alert": true only if the homepage is down or the snake is broken.',
    },
    {
        "key": "gearhead", "id": "crewGearhead0001", "emoji": "🔧", "title": "Gearhead · devices check",
        "model": "qwen3.5:4b", "cron": "0 9 * * *", "speak": False, "always_alert": False,
        "persona": "You are Gearhead from Rick and Morty: a gear-headed mechanic who loves machines.",
        "task": '"report": 2-3 sentences on Rabbid\'s devices (phone, Tailscale, laptop battery). '
                '"say": one short line in character. "alert": true only if the laptop battery is below 15%.',
    },
    {
        "key": "noob-noob", "id": "crewNoobNoob0001", "emoji": "🧹", "title": "Noob-Noob · Seagate check",
        "model": "llama3.2:3b", "cron": "0 10 * * *", "speak": False, "always_alert": False,
        "persona": "You are Noob-Noob from Rick and Morty: the humble, cheerful janitor who keeps the place running. "
                   "Your building is Rabbid's 4TB Seagate drive.",
        "task": '"report": 2 sentences on the Seagate: space used and free, and what is on it. '
                '"say": one short cheerful line. "alert": true only if the Seagate is not plugged in or is more than 85% full.',
    },
    {
        "key": "beth", "id": "crewBeth00000001", "emoji": "🩺", "title": "Beth · home lab check",
        "model": "mistral:7b", "cron": "0 12 * * *", "speak": False, "always_alert": False,
        "persona": "You are Beth Smith from Rick and Morty: a confident, no-nonsense horse surgeon who runs Rabbid's home lab.",
        "task": '"report": 2 sentences on the home lab apps and the laptop disk space. Apps being stopped is normal. '
                '"say": one short line in character. "alert": true only if the laptop disk has less than 50 GB free.',
    },
    {
        "key": "morty", "id": "crewMorty0000001", "emoji": "😰", "title": "Morty · Linux lesson reminder (spoken)",
        "model": "llama3.1:8b", "cron": "0 18 * * 1-5", "speak": True, "always_alert": True,
        "persona": "You are Morty Smith from Rick and Morty: nervous, sweet, encouraging (\"aw geez\"). "
                   "You are Rabbid's Linux study buddy.",
        "task": '"report": 2 sentences: where Rabbid is in the Linux course and what is next. '
                '"say": one short friendly spoken line telling Rabbid it is Linux time and naming the next step '
                'exactly as written in the facts. "alert": false.',
    },
    {
        "key": "birdperson", "id": "crewBirdperson01", "emoji": "🐦", "title": "Birdperson · nightly backup check",
        "model": "qwen3:4b", "cron": "30 21 * * *", "speak": False, "always_alert": False,
        "persona": "You are Birdperson from Rick and Morty: calm, loyal, very formal. Guarding Rabbid's family "
                   "files is your sacred duty.",
        "task": '"report": 2-3 sentences on the backup: when each folder was last saved and whether tonight\'s '
                'backup ran. "say": one short formal line. "alert": true if the 1TB backup drive is not plugged in, '
                'or any folder has not been saved in more than 2 days.',
    },
    # Unity's Sunday idea scout was retired 2026-10-05: she's the Web & Brave crew member now (research → Claude).
]


def node(name, ntype, version, params, x, y, **extra):
    return {"parameters": params, "id": str(uuid.uuid5(uuid.NAMESPACE_URL, name + ntype + str(x))),
            "name": name, "type": ntype, "typeVersion": version, "position": [x, y], **extra}


def ask_and_deliver(c, facts_url, user_content, x0):
    """The shared tail: crew member -> get facts -> ask model -> deliver."""
    system = c["persona"] + " " + COMMON + c["task"]
    member = node("Crew member", "n8n-nodes-base.set", 3.4, {
        "mode": "manual",
        "assignments": {"assignments": [
            {"id": "m1", "name": "model", "value": c["model"], "type": "string"},
            {"id": "m2", "name": "system", "value": system, "type": "string"},
        ]},
        "options": {},
    }, x0, 300)
    get_facts = node("Get facts", "n8n-nodes-base.httpRequest", 4.2, {
        "url": facts_url, "options": {"timeout": 120000},
    }, x0 + 220, 300)
    job = "free-smart" if c["key"] == "rick" else "free-chat"
    body = ("={{ JSON.stringify({ model: $('Crew member').item.json.model, job: '" + job + "', "
            "system: $('Crew member').item.json.system, user: " + user_content + " }) }}")
    ask = node("Ask the free brains", "n8n-nodes-base.httpRequest", 4.2, {
        "method": "POST", "url": THINK, "sendBody": True, "specifyBody": "json", "jsonBody": body,
        "sendHeaders": True, "headerParameters": {"parameters": [{"name": "X-Crew", "value": "1"}]},
        "options": {"timeout": 900000},
    }, x0 + 440, 300)
    deliver_body = ("={{ JSON.stringify({ answer: $json.message.content, task: " + json.dumps(c["title"]) +
                    f", speak: {str(c['speak']).lower()}, always_alert: {str(c['always_alert']).lower()} }}) }}}}")
    deliver = node("Deliver report", "n8n-nodes-base.httpRequest", 4.2, {
        "method": "POST", "url": f"{API}/api/deliver/{c['key']}", "sendBody": True, "specifyBody": "json",
        "jsonBody": deliver_body, "options": {},
    }, x0 + 660, 300)
    return [member, get_facts, ask, deliver]


def chain(names):
    return {a: {"main": [[{"node": b, "type": "main", "index": 0}]]} for a, b in zip(names, names[1:])}


def workflow(c, trigger, facts_url, user_content):
    nodes = [trigger] + ask_and_deliver(c, facts_url, user_content, 220)
    return {
        "id": c["id"], "name": f"{c['emoji']} {c['title']}", "nodes": nodes,
        "connections": chain([n["name"] for n in nodes]),
        "active": False, "pinData": {}, "tags": [],
        "settings": {"executionOrder": "v1", "timezone": "America/New_York", "saveManualExecutions": True},
    }


def main():
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.json"):
        old.unlink()
    for c in CREW:
        trig = node("Schedule", "n8n-nodes-base.scheduleTrigger", 1.2,
                    {"rule": {"interval": [{"field": "cronExpression", "expression": c["cron"]}]}}, 0, 300)
        from urllib.parse import quote
        wf = workflow(c, trig, f"{API}/api/facts/{c['key']}?task={quote(c['title'])}", "$('Get facts').item.json.facts")
        (OUT / f"{c['key']}.json").write_text(json.dumps(wf, indent=2, ensure_ascii=False))

    # Mr. Meeseeks: on demand. POST {"task": "..."} to http://127.0.0.1:5678/webhook/meeseeks
    m = {"key": "mr-meeseeks", "id": "crewMeeseeks0001", "emoji": "🔵", "title": "Mr. Meeseeks · one job",
         "model": "qwen3:1.7b", "speak": True, "always_alert": True,
         "persona": "You are Mr. Meeseeks from Rick and Morty (\"I'm Mr. Meeseeks, look at meee!\"). "
                    "You exist to do ONE task for Rabbid, then disappear happily.",
         "task": '"report": the finished task: the answer, list or text Rabbid asked for, ready to keep in his notes. '
                 'If the task needs something you cannot do (you can only think and write, you cannot click, '
                 'install or change anything), say so honestly. "say": one short excited line in character. "alert": false.'}
    hook = node("Webhook", "n8n-nodes-base.webhook", 2,
                {"httpMethod": "POST", "path": "meeseeks", "responseMode": "lastNode", "options": {}},
                0, 300, webhookId="26ebe4ec-fd7e-4727-bc0c-ec58983da25d")
    wf = workflow(m, hook,
                  f"={API}/api/facts/mr-meeseeks?task={{{{ encodeURIComponent($('Webhook').item.json.body.task) }}}}",
                  "$('Get facts').item.json.facts + '\\n\\nYour one task: ' + $('Webhook').item.json.body.task")
    (OUT / "mr-meeseeks.json").write_text(json.dumps(wf, indent=2, ensure_ascii=False))
    print("\n".join(sorted(p.name for p in OUT.glob("*.json"))))


if __name__ == "__main__":
    main()
