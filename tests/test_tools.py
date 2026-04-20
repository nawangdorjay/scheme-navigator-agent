"""Tests for Scheme Navigator Agent tools."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from agent.tools import execute_tool


def test_search_farm():
    r = execute_tool("search_schemes", {"query": "farmer"})
    assert r["count"] > 0
    print(f"✅ test_search_farm ({r['count']} schemes)")


def test_search_health():
    r = execute_tool("search_schemes", {"query": "hospital"})
    assert r["count"] > 0
    print(f"✅ test_search_health ({r['count']} schemes)")


def test_search_loan():
    r = execute_tool("search_schemes", {"query": "loan"})
    assert r["count"] > 0
    print(f"✅ test_search_loan ({r['count']} schemes)")


def test_search_scholarship():
    r = execute_tool("search_schemes", {"query": "scholarship"})
    assert r["count"] > 0
    print(f"✅ test_search_scholarship ({r['count']} schemes)")


def test_search_pension():
    r = execute_tool("search_schemes", {"query": "pension"})
    assert r["count"] > 0
    print(f"✅ test_search_pension ({r['count']} schemes)")


def test_eligibility_farmer():
    r = execute_tool("check_eligibility", {"age": 35, "gender": "male", "occupation": "farmer", "income": "1_3lakh"})
    assert len(r["eligible"]) > 0
    names = [s["name"] for s in r["eligible"]]
    print(f"✅ test_eligibility_farmer ({len(r['eligible'])} eligible: {', '.join(names[:3])})")


def test_eligibility_student():
    r = execute_tool("check_eligibility", {"age": 20, "gender": "female", "occupation": "student", "income": "below_1lakh", "category": "sc"})
    assert len(r["eligible"]) > 0
    print(f"✅ test_eligibility_student ({len(r['eligible'])} eligible)")


def test_eligibility_woman():
    r = execute_tool("check_eligibility", {"age": 30, "gender": "female", "occupation": "worker", "income": "below_1lakh"})
    assert len(r["eligible"]) > 0
    print(f"✅ test_eligibility_woman ({len(r['eligible'])} eligible)")


def test_scheme_pm_kisan():
    r = execute_tool("get_scheme_details", {"scheme_name": "PM-KISAN"})
    assert r["found"] is True
    assert "documents_needed" in r
    print(f"✅ test_scheme_pm_kisan")


def test_ayushman():
    r = execute_tool("get_scheme_details", {"scheme_name": "Ayushman"})
    assert r["found"] is True
    print("✅ test_ayushman")


def test_scheme_mudra():
    r = execute_tool("get_scheme_details", {"scheme_name": "MUDRA"})
    assert r["found"] is True
    print(f"✅ test_scheme_mudra")


def test_documents():
    r = execute_tool("get_required_documents", {"scheme_name": "PM-KISAN"})
    assert r.get("found") is not False
    assert len(r["documents"]) > 0
    print(f"✅ test_documents ({len(r['documents'])} docs needed)")


if __name__ == "__main__":
    tests = [
        test_search_farm, test_search_health, test_search_loan,
        test_search_scholarship, test_search_pension,
        test_eligibility_farmer, test_eligibility_student, test_eligibility_woman,
        test_scheme_pm_kisan, test_ayushman, test_scheme_mudra,
        test_documents,
    ]
    passed = failed = 0
    for t in tests:
        try:
            t(); passed += 1
        except Exception as e:
            print(f"❌ {t.__name__}: {e}"); failed += 1
    print(f"\n{'='*40}\n{passed} passed, {failed} failed")
    if not failed:
        print("All tests passed! 🎉")
