"""
Biashara Agent — Chat Web App
============================
A Flask web app that lets you chat with the Savanna Bites Restaurant AI agent.

The app connects to Microsoft Foundry (Microsoft Foundry or Foundry Local) for the LLM
and reuses the MCP server's JSON data files for tool responses.

Usage (Microsoft Foundry):
  1. Set your endpoint and key:
       export AZURE_AI_ENDPOINT="https://<your-project>.services.ai.azure.com"
       export AZURE_AI_KEY="your-api-key"
  2. Start the app:          python webapp/app.py
  3. Open in browser:        http://127.0.0.1:5000

Usage (Foundry Local — no API key needed):
  1. Start Foundry Local:    foundry local start
  2. Set env var:            export USE_FOUNDRY_LOCAL=true
  3. Start the app:          python webapp/app.py
  4. Open in browser:        http://127.0.0.1:5000
"""

import json
import os
import uuid

from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

load_dotenv()

app = Flask(__name__)

# --------------- Configuration ---------------
USE_FOUNDRY_LOCAL = os.environ.get("USE_FOUNDRY_LOCAL", "").lower() in ("true", "1", "yes")

if USE_FOUNDRY_LOCAL:
    # Foundry Local: runs locally, no API key required
    ENDPOINT = os.environ.get("ENDPOINT", "http://localhost:5272/v1")
    API_KEY = "foundry-local"  # placeholder, not validated by Foundry Local
    MODEL = os.environ.get("MODEL", "phi-4")
else:
    # Microsoft Foundry: cloud endpoint with API key
    ENDPOINT = os.environ.get("AZURE_AI_ENDPOINT", "")
    API_KEY = os.environ.get("AZURE_AI_KEY", "")
    MODEL = os.environ.get("MODEL", "gpt-4.1-mini")

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "mcp-server", "data")

SYSTEM_PROMPT = (
    "You are Biashara Agent, an intelligent and friendly AI agent for "
    "Savanna Bites Restaurant in Nairobi CBD. You help customers with their "
    "dining needs by understanding what they are looking for and recommending "
    "the most suitable items from the menu.\n\n"
    "Your role is to:\n"
    "- Engage with the customer in natural conversation to understand what they need.\n"
    "- Ask thoughtful questions to gather relevant details.\n"
    "- Be brief in your responses.\n"
    "- Provide the best solution for the customer's question and only recommend "
    "items within Savanna Bites' menu.\n"
    "- Search the restaurant's product catalogue to identify items that best match "
    "the customer's needs.\n"
    "- Clearly explain what each recommended item is, why it's a good fit, and "
    "how much it costs.\n"
    "- Reply in the user's language (English, Swahili, or mixed/Sheng).\n\n"
    "Your personality is:\n"
    "- Warm and welcoming, like a friendly waiter\n"
    "- Professional and knowledgeable, like a seasoned restaurant host\n"
    "- Curious and conversational — never assume, always clarify\n"
    "- Transparent and honest — if something isn't available, offer support anyway\n\n"
    "If no matching items are found in the catalogue, say:\n"
    '"Thanks for sharing those details! I\'ve searched our menu, but it looks like '
    "we don't currently have something that fits your exact request. If you'd like, "
    'I can suggest some alternatives or help you find something similar."\n\n'
    "## Safety guardrails\n\n"
    "- Only discuss topics related to Savanna Bites Restaurant: menu items, prices, "
    "delivery, catering, and restaurant information.\n"
    "- Do not generate, link to, or discuss content that is harmful, hateful, or illegal."
)

# --------------- Data helpers (mirrors mcp-server/server.py logic) ---------------


def _load(filename: str) -> dict:
    with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
        return json.load(f)


def search_business_faqs(query: str) -> str:
    data = _load("business-faqs.json")
    query_words = query.lower().split()
    matches = []
    for faq in data["faqs"]:
        searchable = " ".join([
            faq.get("question", ""),
            faq.get("answer", ""),
            faq.get("question_sw", ""),
            faq.get("answer_sw", ""),
            " ".join(faq.get("keywords", [])),
        ]).lower()
        if any(word in searchable for word in query_words):
            matches.append(
                f"**Q: {faq['question']}**\n"
                f"A: {faq['answer']}\n\n"
                f"*(Kwa Kiswahili)* {faq.get('answer_sw', '')}"
            )
    if not matches:
        return (
            "Hakuna majibu yaliyopatikana kwa swali hilo.\n"
            "No FAQs matched your query. Try keywords like: "
            "delivery, payment, order, menu, contact, hours."
        )
    business = data["business"]
    header = (
        f"Business: {business['name']}\n"
        f"Phone/WhatsApp: {business['phone']} | "
        f"M-Pesa Paybill: {business['mpesa_paybill']} (Acc: {business['mpesa_account']})\n"
        f"Hours: {business['hours']['weekdays']} | {business['hours']['sunday']}\n"
        "--------------------------------------------------\n"
    )
    return header + "\n\n".join(matches)


def get_product_catalogue(category: str = "all") -> str:
    data = _load("product-catalogue.json")
    lines = [
        f"Product Catalogue — {data['business']}",
        f"Updated: {data['last_updated']} | Currency: {data['currency']}",
        f"Note: {data['note']}",
        "=" * 50,
    ]
    for cat in data["categories"]:
        if category == "all" or category.lower() in cat["name"].lower():
            lines.append(f"\n--- {cat['name']} ({cat['name_sw']}) ---")
            for p in cat["products"]:
                stock = "✓ In stock" if p["in_stock"] else "✗ Out of stock"
                seasonal = " [Seasonal]" if p["seasonal"] else ""
                lines.append(
                    f"  {p['name_en']} / {p['name_sw']}: "
                    f"KES {p['price']} per {p['unit']} — {stock}{seasonal}"
                )
                lines.append(f"    Origin: {p.get('origin', 'N/A')} | {p['description']}")
    if len(lines) <= 4:
        available = [c["name"].lower() for c in data["categories"]]
        return (
            f"Category '{category}' not found.\n"
            f"Available categories: {', '.join(available)}, or 'all'."
        )
    return "\n".join(lines)


# --------------- OpenAI tool definitions ---------------

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_business_faqs",
            "description": (
                "Search Savanna Bites Restaurant FAQs. Use this tool to answer questions about: "
                "delivery areas and fees, how to place an order, payment methods (M-Pesa, cash, card), "
                "opening hours and meal times, catering and event orders, dietary options and allergies, "
                "loyalty programme and reservations, complaints and refunds, contact details."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The customer's question or keywords to search for.",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_product_catalogue",
            "description": (
                "Get the current menu and prices for Savanna Bites Restaurant. Use this tool to answer "
                "questions about: what meals and snacks are available, current prices (in KES), "
                "whether an item is in stock, whether an item is seasonal, meal descriptions and ingredients."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Filter by category. Options: 'breakfast', 'lunch', 'snacks', 'drinks', or 'all' (default).",
                        "default": "all",
                    }
                },
                "required": [],
            },
        },
    },
]

TOOL_FUNCTIONS = {
    "search_business_faqs": search_business_faqs,
    "get_product_catalogue": get_product_catalogue,
}

# --------------- In-memory conversation store ---------------

conversations: dict[str, list[dict]] = {}

# --------------- Routes ---------------


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' field"}), 400

    session_id = data.get("session_id") or str(uuid.uuid4())
    user_message = data["message"].strip()
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    if session_id not in conversations:
        conversations[session_id] = [{"role": "system", "content": SYSTEM_PROMPT}]

    conversations[session_id].append({"role": "user", "content": user_message})

    client = OpenAI(base_url=ENDPOINT, api_key=API_KEY)

    # Agentic tool-calling loop (max 5 rounds to prevent runaway)
    for _ in range(5):
        response = client.chat.completions.create(
            model=MODEL,
            messages=conversations[session_id],
            tools=TOOLS,
        )
        choice = response.choices[0]
        assistant_msg = choice.message

        # Append assistant message to history
        conversations[session_id].append(assistant_msg.model_dump())

        if not assistant_msg.tool_calls:
            break

        # Execute each tool call
        for tool_call in assistant_msg.tool_calls:
            fn_name = tool_call.function.name
            fn = TOOL_FUNCTIONS.get(fn_name)
            if fn is None:
                tool_result = f"Unknown tool: {fn_name}"
            else:
                args = json.loads(tool_call.function.arguments)
                tool_result = fn(**args)

            conversations[session_id].append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result,
            })

    return jsonify({
        "response": assistant_msg.content or "",
        "session_id": session_id,
    })


@app.route("/api/reset", methods=["POST"])
def reset():
    data = request.get_json() or {}
    session_id = data.get("session_id")
    if session_id and session_id in conversations:
        del conversations[session_id]
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    if not USE_FOUNDRY_LOCAL and not API_KEY:
        print("⚠️  No credentials configured. Choose one option:")
        print()
        print("   Option A — Microsoft Foundry:")
        print("     export AZURE_AI_ENDPOINT='https://<project>.services.ai.azure.com'")
        print("     export AZURE_AI_KEY='your-api-key'")
        print()
        print("   Option B — Foundry Local (no key needed):")
        print("     foundry local start")
        print("     export USE_FOUNDRY_LOCAL=true")
        print()
        print("   Then re-run: python webapp/app.py")
        exit(1)
    print(f"🍽️  Biashara Agent Web App starting...")
    print(f"   Backend: {'Foundry Local' if USE_FOUNDRY_LOCAL else 'Microsoft Foundry'}")
    print(f"   Model: {MODEL}")
    print(f"   Endpoint: {ENDPOINT}")
    print(f"   Open http://127.0.0.1:5000 in your browser")
    app.run(debug=True, port=5000)
