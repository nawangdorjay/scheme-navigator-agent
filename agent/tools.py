"""
Government Scheme Navigator — Tool Functions
Comprehensive scheme database with eligibility matching.
"""
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


def _load_json(filename: str) -> dict:
    filepath = DATA_DIR / filename
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def get_tools():
    return [
        {
            "type": "function",
            "function": {
                "name": "search_schemes",
                "description": "Search for government schemes matching a query.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "What user is looking for (e.g., loan, scholarship, subsidy, pension)"},
                        "category": {"type": "string", "description": "Category filter: agriculture, health, education, housing, women, employment, business, elderly"}
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "check_eligibility",
                "description": "Check which schemes a person is eligible for based on their profile.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "age": {"type": "integer", "description": "Age of the person"},
                        "gender": {"type": "string", "description": "male, female, other"},
                        "occupation": {"type": "string", "description": "farmer, student, worker, business, unemployed, retired"},
                        "income": {"type": "string", "description": "annual income range: below_1lakh, 1_3lakh, 3_5lakh, above_5lakh"},
                        "state": {"type": "string", "description": "Indian state name"},
                        "category": {"type": "string", "description": "sc, st, obc, general"}
                    },
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_scheme_details",
                "description": "Get detailed information about a specific scheme.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "scheme_name": {"type": "string", "description": "Name of the scheme"}
                    },
                    "required": ["scheme_name"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_required_documents",
                "description": "Get list of documents needed for a scheme.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "scheme_name": {"type": "string", "description": "Name of the scheme"}
                    },
                    "required": ["scheme_name"]
                }
            }
        },
    ]


def execute_tool(tool_name: str, arguments: dict) -> dict:
    handlers = {
        "search_schemes": _search_schemes,
        "check_eligibility": _check_eligibility,
        "get_scheme_details": _get_scheme_details,
        "get_required_documents": _get_required_documents,
    }
    handler = handlers.get(tool_name)
    if handler:
        return handler(**arguments)
    return {"error": f"Unknown tool: {tool_name}"}


def _search_schemes(query: str, category: str = "") -> dict:
    """Search schemes by keyword."""
    schemes = _load_json("schemes_comprehensive.json")
    query_lower = query.lower()
    matched = []

    for scheme in schemes:
        # Category filter
        if category and scheme.get("category", "").lower() != category.lower():
            continue

        # Keyword match
        searchable = " ".join([
            scheme.get("name", ""),
            scheme.get("description", ""),
            " ".join(scheme.get("keywords", [])),
            scheme.get("category", ""),
        ]).lower()

        if query_lower in searchable or any(qw in searchable for qw in query_lower.split()):
            matched.append(scheme)

    if not matched:
        matched = schemes[:5]

    return {"query": query, "count": len(matched), "schemes": matched[:8]}


def _check_eligibility(age: int = 0, gender: str = "", occupation: str = "",
                        income: str = "", state: str = "", category: str = "") -> dict:
    """Check eligibility for multiple schemes."""
    schemes = _load_json("schemes_comprehensive.json")
    eligible = []
    possibly_eligible = []

    for scheme in schemes:
        elig = scheme.get("eligibility_criteria", {})
        score = 0
        checks = 0

        # Age check
        if elig.get("min_age") and age:
            checks += 1
            if age >= elig["min_age"]:
                score += 1
        if elig.get("max_age") and age:
            checks += 1
            if age <= elig["max_age"]:
                score += 1

        # Gender check
        if elig.get("gender") and gender:
            checks += 1
            if elig["gender"] == "all" or elig["gender"] == gender.lower():
                score += 1

        # Occupation check
        if elig.get("occupation") and occupation:
            checks += 1
            occ_list = elig["occupation"] if isinstance(elig["occupation"], list) else [elig["occupation"]]
            if occupation.lower() in [o.lower() for o in occ_list] or "all" in occ_list:
                score += 1

        # Income check
        if elig.get("income") and income:
            checks += 1
            if income in elig["income"] or "any" in elig["income"]:
                score += 1

        # Category (SC/ST/OBC) check
        if elig.get("reservation_category") and category:
            checks += 1
            cat_list = elig["reservation_category"] if isinstance(elig["reservation_category"], list) else [elig["reservation_category"]]
            if category.lower() in [c.lower() for c in cat_list] or "all" in cat_list:
                score += 1

        if checks == 0:
            possibly_eligible.append({"scheme": scheme, "confidence": "unknown"})
        elif score == checks:
            eligible.append({"scheme": scheme, "confidence": "high"})
        elif score > 0:
            possibly_eligible.append({"scheme": scheme, "confidence": "medium"})

    return {
        "profile": {"age": age, "gender": gender, "occupation": occupation, "income": income, "state": state, "category": category},
        "eligible": [e["scheme"] for e in eligible[:10]],
        "possibly_eligible": [p["scheme"] for p in possibly_eligible[:5]],
    }


def _get_scheme_details(scheme_name: str) -> dict:
    """Get full details of a scheme."""
    schemes = _load_json("schemes_comprehensive.json")
    name_lower = scheme_name.lower()

    for scheme in schemes:
        if name_lower in scheme.get("name", "").lower() or name_lower in scheme.get("short_name", "").lower():
            return {"found": True, **scheme}

    # Fuzzy
    for scheme in schemes:
        keywords = scheme.get("keywords", [])
        if any(name_lower in kw for kw in keywords):
            return {"found": True, **scheme}

    return {"found": False, "message": f"No scheme found matching '{scheme_name}'. Try: PM-KISAN, Ayushman, KCC, MGNREGA, PM Awas."}


def _get_required_documents(scheme_name: str) -> dict:
    """Get documents needed for a scheme."""
    details = _get_scheme_details(scheme_name)
    if details.get("found"):
        return {
            "scheme": details.get("name"),
            "documents": details.get("documents_needed", ["Aadhaar Card", "Bank Account", "Address Proof"]),
            "how_to_apply": details.get("how_to_apply", "Visit nearest CSC or government office"),
        }
    return {"found": False, "message": f"Scheme '{scheme_name}' not found."}
