import json
from pathlib import Path
from typing import List, Dict

DATA_PATH = Path(__file__).parent / "data" / "sample_contracts.json"

def load_contracts() -> List[Dict]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def search_contracts(query: str) -> List[Dict]:
    q = query.lower()
    results = []
    for c in load_contracts():
        hay = f"{c['vendor']} {c['contract_id']} {c['summary']}".lower()
        if any(term in hay for term in q.split()):
            results.append(c)
    return results

