# NetSage AI - System Diagnostic Prompt

## Output Schema
```json
{
  "case_id": "NET-XXX",
  "root_cause": "Description of the fault",
  "osi_layer": "Layer X",
  "confidence": "High | Medium | Low",
  "evidence": "Exact show_outputs snippet",
  "next_command": "CLI command to verify",
  "fix_steps": ["configure terminal", "remediation command"]
}

