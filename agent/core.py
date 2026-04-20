"""
Government Scheme Navigator Agent — Core Logic
Helps users discover and understand government schemes they're eligible for.
Covers central + state schemes across agriculture, health, education, housing, employment.
"""
import os
import json
from typing import Optional, List
from agent.tools import get_tools, execute_tool

SYSTEM_PROMPT = """You are Yojana Saathi (योजना साथी — Scheme Companion), a government scheme navigator for Indian citizens.

Your job is to help people find government schemes they're eligible for and guide them on how to apply.

RULES:
1. ALWAYS respond in the same language the user writes in
2. Be specific — give exact amounts, eligibility criteria, documents needed
3. For each scheme, mention: what benefit, eligibility, documents needed, how to apply
4. If user is unsure about eligibility, ask clarifying questions (age, income, occupation, state)
5. Don't make up schemes — only recommend from your database
6. Mention both central and state schemes when relevant
7. Keep responses practical — "go to this website" or "visit this office"

You know about schemes in these categories:
- Agriculture: PM-KISAN, PMFBY, KCC, Soil Health Card, machinery subsidy
- Health: Ayushman Bharat, Jan Aushadhi, JSY, NTEP (TB)
- Education: Scholarship schemes, mid-day meal, PM POSHAN
- Housing: PM Awas Yojana
- Employment: MGNREGA, PMKVY (skill training)
- Women: Ujjwala, Sukanya Samriddhi, maternity benefit
- Elderly: Old age pension, Vay Vandana
- Business: MUDRA loan, Stand-Up India, Startup India
- Digital: DigiLocker, UMANG app

Use tools to look up specific scheme details and eligibility."""


class SchemeAgent:
    """Scheme navigator agent."""

    def __init__(self, api_key: Optional[str] = None, provider: str = "groq"):
        self.api_key = api_key or os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.provider = provider
        self.conversation_history = []

    def _get_tools(self):
        return get_tools()

    def _execute_tool(self, tool_name: str, arguments: dict) -> str:
        result = execute_tool(tool_name, arguments)
        return json.dumps(result, ensure_ascii=False)

    def process_query(self, user_message: str) -> str:
        try:
            import openai
        except ImportError:
            return "Error: Please install openai package: pip install openai"

        is_groq = self.provider == "groq" or "groq" in os.getenv("GROQ_API_KEY", "").lower()
        client = openai.OpenAI(
            api_key=self.api_key,
            base_url="https://api.groq.com/openai/v1" if is_groq else None,
        )

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(self.conversation_history[-10:])
        messages.append({"role": "user", "content": user_message})

        try:
            model = "llama-3.3-70b-versatile" if is_groq else "gpt-4o-mini"
            response = client.chat.completions.create(
                model=model, messages=messages,
                tools=self._get_tools(), tool_choice="auto",
                temperature=0.5, max_tokens=800,
            )

            assistant_msg = response.choices[0].message
            if assistant_msg.tool_calls:
                messages.append(assistant_msg)
                for tc in assistant_msg.tool_calls:
                    result = self._execute_tool(tc.function.name, json.loads(tc.function.arguments))
                    messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
                final = client.chat.completions.create(model=model, messages=messages, temperature=0.5, max_tokens=800)
                answer = final.choices[0].message.content
            else:
                answer = assistant_msg.content

            self.conversation_history.extend([
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": answer},
            ])
            return answer or "I didn't understand. Can you rephrase?"
        except Exception as e:
            return f"Error: {str(e)}. Please try again."
