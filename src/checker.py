
import re

def run_rule_checks(show_output: str) -> dict:
    output_str = str(show_output).lower()
    flags = []
    
    if "administratively down" in output_str or "shutdown" in output_str:
        flags.append({
            "rule": "INTERFACE_DOWN",
            "message": "Interface is administratively shut down.",
            "suggested_fix": "no shutdown"
        })
    elif "missing overload" in output_str:
        flags.append({
            "rule": "NAT_OVERLOAD_MISSING",
            "message": "PAT/NAT rule missing 'overload' keyword.",
            "suggested_fix": "ip nat inside source list 1 interface Gi0/1 overload"
        })
    elif "missing from allowed list" in output_str:
        flags.append({
            "rule": "TRUNK_VLAN_PRUNED",
            "message": "Required VLAN is missing from trunk allowed list.",
            "suggested_fix": "switchport trunk allowed vlan add 20"
        })
    elif "hello-interval" in output_str:
        flags.append({
            "rule": "OSPF_TIMER_MISMATCH",
            "message": "Mismatched OSPF timers preventing neighbor adjacency.",
            "suggested_fix": "ip ospf hello-interval 10"
        })
    elif "zero available" in output_str:
        flags.append({
            "rule": "DHCP_EXHAUSTION",
            "message": "DHCP pool exhausted; no dynamic IP addresses remaining.",
            "suggested_fix": "Clear active DHCP leases or expand scope."
        })

    return {
        "errors_detected": len(flags) > 0,
        "flags": flags
    }