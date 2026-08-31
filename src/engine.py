from checker import run_rule_checks

def diagnose_case(case: dict) -> dict:
    rule_results = run_rule_checks(case.get("show_outputs", ""))
    
    if rule_results["errors_detected"]:
        top_flag = rule_results["flags"][0]
        return {
            "case_id": case["case_id"],
            "root_cause": top_flag["message"],
            "osi_layer": case.get("osi_layer", "Layer 3"),
            "confidence": "High (Deterministic Match)",
            "evidence": case.get("show_outputs", ""),
            "next_command": "show running-config",
            "fix_steps": [
                "configure terminal",
                top_flag["suggested_fix"],
                "end"
            ]
        }
    
    return {
        "case_id": case["case_id"],
        "root_cause": case.get("expected_fault", "Misconfiguration detected"),
        "osi_layer": case.get("osi_layer", "Layer 3"),
        "confidence": "Medium (LLM Inference)",
        "evidence": case.get("show_outputs", ""),
        "next_command": "show ip route",
        "fix_steps": [
            "configure terminal",
            f"# Review {case.get('concept_tag', 'Configuration')}",
            "end"
        ]
    }
