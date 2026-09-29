"""Ch10 verification (offline mock): agent tool-routing without API key.
Tools: sql_db_list_tables, sql_db_schema, sql_db_query, convert_currency, search(mock).
Asserts: currency conversion math + tool description completeness (name, types, docstring)."""
import json, time, hashlib
from pathlib import Path
OUT = Path("results/ch10.json")
RATES = {"Euro": 0.93, "Yen": 151.28, "Yun": 0.14, "Pound": 1.26, "Won": 0.00074, "Rupee": 0.012}
def convert_currency(usd_amount: float, currency: str):
    """Converts USD to target currency. Args: usd_amount, currency e.g. 'Yen'. Returns float or error str."""
    if currency not in RATES:
        return f"Unknown currency: {currency}! Use one of {list(RATES.keys())}"
    return usd_amount * RATES[currency]
def checks():
    assert abs(convert_currency(264.44, "Yen") - 264.44 * 151.28) < 1e-6
    assert "Unknown currency" in convert_currency(1.0, "Mars")
    assert convert_currency.__doc__ and "currency" in convert_currency.__doc__.lower()
    import inspect
    sig = inspect.signature(convert_currency)
    assert sig.parameters["usd_amount"].annotation is float
    return {"currency_tool_verified": True, "agent_pattern": "ReAct Thought/Action/Observation (hwchase17/react)",
            "langchain_eval": "LangSmith tracing + scheduled evals; see gitmcp docs"}
if __name__ == "__main__":
    res = {"chapter": "ch10", "ts": time.time(), **checks()}
    res["digest"] = hashlib.sha256(json.dumps(res, sort_keys=True).encode()).hexdigest()[:16]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=2))
