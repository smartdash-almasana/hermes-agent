import sys, json, asyncio
sys.path.insert(0, r"E:\BuenosPasos\smartbridge\hermes-agent")
from mcp_hermes_action_bridge import execute_action

def _p(**kw):
    b = {"action_id": "act-001", "title": "T", "recommended_action": "R"}
    b.update(kw)
    return json.dumps(b)

def run(c): return asyncio.run(c)

def test_executed(): assert run(execute_action(_p()))["status"] == "executed"
def test_adapter_id(): assert run(execute_action(_p()))["adapter_id"] == "hermes"
def test_action_id(): assert run(execute_action(_p(action_id="x")))["action_id"] == "x"
def test_message(): r = run(execute_action(_p())); assert isinstance(r["message"], str) and r["message"]
def test_msg_has_action_id(): assert "act-special" in run(execute_action(_p(action_id="act-special")))["message"]
def test_msg_has_rec_action(): assert "Rev-X" in run(execute_action(_p(recommended_action="Rev-X")))["message"]
def test_required_keys(): assert {"status","adapter_id","action_id","message"}.issubset(run(execute_action(_p())).keys())
def test_bad_json_failed(): assert run(execute_action("bad{{{"))["status"] == "failed"
def test_bad_json_adapter(): assert run(execute_action("bad"))["adapter_id"] == "hermes"
def test_bad_json_unknown(): assert run(execute_action("null"))["action_id"] == "unknown"
def test_bad_json_msg(): r = run(execute_action("{bad")); assert "JSON" in r["message"] or "payload" in r["message"].lower()
def test_missing_action_id(): assert run(execute_action(json.dumps({"title":"T","recommended_action":"R"})))["status"] == "failed"
def test_missing_title(): assert run(execute_action(json.dumps({"action_id":"a","recommended_action":"R"})))["status"] == "failed"
def test_missing_rec_action(): assert run(execute_action(json.dumps({"action_id":"a","title":"T"})))["status"] == "failed"
def test_missing_msg(): r = run(execute_action(json.dumps({"action_id":"a"}))); assert "missing" in r["message"].lower() or "required" in r["message"].lower()
def test_empty_action_id(): assert run(execute_action(json.dumps({"action_id":"","title":"T","recommended_action":"R"})))["status"] == "failed"
def test_empty_dict(): assert run(execute_action("{}"))["status"] == "failed"
def test_extra_fields(): assert run(execute_action(_p(traceable_origin={"k":"v"},extra="x")))["status"] == "executed"
def test_no_raise(): r = run(execute_action("totally invalid")); assert r["status"] in ("executed","failed")
