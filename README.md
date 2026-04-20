# 🏛️ Yojana Saathi — Government Scheme Navigator Agent

An AI agent that helps Indian citizens discover government schemes they're eligible for, understand benefits, and apply with confidence.

Built by [Nawang Dorjay](https://github.com/nawangdorjay) — from Ladakh, for **GSSoC 2026** (Agents for India Track).

---

## 🎯 The Problem

India has **1000+ government schemes** across agriculture, health, education, housing, employment, and more. But:
- Most citizens don't know which schemes exist
- Eligibility rules are confusing
- Documents required are unclear
- Application process varies by scheme

**Result:** Crores of rupees go unclaimed every year.

---

## 🚀 Features

| Feature | Description |
|---------|-------------|
| 🔍 **Scheme Search** | Search by keyword: "loan", "scholarship", "insurance", "pension" |
| ✅ **Eligibility Matching** | Enter your profile → get list of eligible schemes |
| 📋 **Documents Checklist** | Exact documents needed for each scheme |
| 📝 **Application Guide** | Step-by-step: where to go, what to bring |
| 💰 **Benefit Details** | Exact amounts: ₹6,000/year, ₹5 lakh insurance, etc. |
| 🌐 **Multilingual** | Ask in Hindi, English, or any Indian language |

---

## 📊 Schemes Covered (18+)

| Category | Schemes |
|----------|---------|
| 🌾 **Agriculture** | PM-KISAN, PMFBY, KCC, PM Kusum |
| 🏥 **Health** | Ayushman Bharat, Jan Aushadhi, Maternity Benefit |
| 🏠 **Housing** | PM Awas Yojana |
| 💼 **Employment** | MGNREGA, PMKVY |
| 👩 **Women** | Ujjwala, Sukanya Samriddhi, Maternity Benefit |
| 📚 **Education** | Post Matric Scholarship, PM Scholarship |
| 💰 **Business** | MUDRA Loan, Stand-Up India |
| 👴 **Elderly** | Old Age Pension, Atal Pension |

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Streamlit** — Chat UI with eligibility quick-check sidebar
- **OpenAI / Groq API** — LLM for natural language understanding
- **JSON** — Comprehensive scheme database with eligibility criteria

---

## 📦 Installation

```bash
git clone https://github.com/nawangdorjay/scheme-navigator-agent.git
cd scheme-navigator-agent
pip install -r requirements.txt
cp .env.example .env
# Add GROQ_API_KEY=gsk_xxxxx (free at console.groq.com)
streamlit run app.py
```

---

## 📁 Project Structure

```
scheme-navigator-agent/
├── app.py                          # Streamlit UI with eligibility sidebar
├── agent/
│   ├── __init__.py
│   ├── core.py                     # Agent logic
│   └── tools.py                    # Search, eligibility, scheme details
├── data/
│   └── schemes_comprehensive.json  # 18 schemes with full eligibility data
├── tests/
│   └── test_tools.py               # 12 validation tests
├── .github/workflows/
│   └── ci.yml                      # GitHub Actions CI
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🧪 Testing

```bash
python tests/test_tools.py
```

12 tests covering: scheme search, eligibility matching, scheme details, and document requirements.

---

## 💡 Example Interactions

| User | Agent |
|------|-------|
| "Kisan Credit Card kaise banwayen?" | "KCC ke liye apne bank mein jayein. Saath le jayein: Aadhaar, zameen ke kaagaz, photo. Byaaz sirf 4% saalana." |
| "I need free hospital treatment" | "Ayushman Bharat aapke liye hai. ₹5 lakh tak free ilaaj. Check karein mera.pmjay.gov.in ya call karein 14555." |
| "Mujhe business loan chahiye" | "MUDRA Loan lein — ₹10 lakh tak bina guarantee. Apply karein kisi bhi bank mein." |
| "Meri beti ke liye scholarship" | "Sukanya Samriddhi Yojana mein account kholein. 8.2% byaaz, tax-free. Ya Post Matric Scholarship: scholarships.gov.in" |

---

## 🔮 Future Improvements

- [ ] State-specific schemes database (each state has 50+ schemes)
- [ ] Eligibility quiz (interactive questionnaire)
- [ ] Application status tracking
- [ ] WhatsApp bot integration
- [ ] Voice interface (link with voice-assistant-agent)
- [ ] Scheme deadline reminders

---

## 📄 License

MIT

---

## 👨‍💻 Author

**Nawang Dorjay** — B.Tech CSE (Data Science), MAIT Delhi
From Nubra Valley, Leh, Ladakh 🏔️

- [GitHub](https://github.com/nawangdorjay)
- [Email](mailto:nawangdorjay09@gmail.com)

Built for **GSSoC 2026** — Agents for India Track.
