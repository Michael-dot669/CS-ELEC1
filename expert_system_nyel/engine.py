

from datetime import datetime

def run_inference(record, trace):
    """
    Simulates the Forward-Chaining Inference Process matching the CLIPS logic.
    """
    trace.append(("Inference Goal", "Evaluate record conditions using Forward-Chaining.", "info"))
    
    actions_triggered = []

    
    try:
        updated_date = datetime.strptime(record["last_updated"], "%Y-%m-%d")
        today = datetime.now()
        days_old = (today - updated_date).days

        
        if updated_date > today:
            trace.append((
                "Rule 1 — Outdated Check", 
                f"Invalid date: '{record['last_updated']}' is a future date. Set to current/past date.", 
                "deny"
            ))
            actions_triggered.append("INVALID_DATE")
        elif days_old > 365:
            record["needs_update"] = True
            actions_triggered.append("UPDATE_NEEDED")
            trace.append((
                "Rule 1 — Outdated Check", 
                f"Last updated {days_old} days ago (> 365 days). Flagged as 'Needs Update'.", 
                "deny"
            ))
        else:
            trace.append((
                "Rule 1 — Outdated Check", 
                f"Last updated {days_old} days ago. Record date is valid.", 
                "pass"
            ))
    except ValueError:
        trace.append(("Rule 1 — Outdated Check", "Invalid date format (use YYYY-MM-DD).", "fail"))
        actions_triggered.append("INVALID_DATE")

    
    if record["completeness"] == "Incomplete":
        record["status"] = "Pending Verification"
        actions_triggered.append("PENDING_VERIFICATION")
        trace.append((
            "Rule 2 — Completeness Check", 
            "Completeness is 'Incomplete'. Status set to 'Pending Verification'.", 
            "review"
        ))
    else:
        trace.append((
            "Rule 2 — Completeness Check", 
            "Record completeness is 'Complete'.", 
            "pass"
        ))

   
    if record["category"] == "Confidential" and record["access_level"] != "Restricted":
        actions_triggered.append("SECURITY_REVIEW")
        trace.append((
            "Rule 3 — Security Compliance", 
            f"Confidential category with '{record['access_level']}' access level. Flagged for Security Review.", 
            "deny"
        ))
    else:
        trace.append((
            "Rule 3 — Security Compliance", 
            "Category and Access Level compliance passed.", 
            "pass"
        ))

    
    if "INVALID_DATE" in actions_triggered:
        record["decision"] = "INVALID DATE INPUT"
        record["reason"] = "Last updated date cannot be in the future or in an invalid format."
    elif "SECURITY_REVIEW" in actions_triggered or "UPDATE_NEEDED" in actions_triggered:
        record["decision"] = "FLAGGED FOR ACTION"
        record["reason"] = "Record violated security policies and/or requires updating."
    elif "PENDING_VERIFICATION" in actions_triggered:
        record["decision"] = "PENDING VERIFICATION"
        record["reason"] = "Record requires additional documentation before completion."
    else:
        record["decision"] = "COMPLIANT & VERIFIED"
        record["reason"] = "Record passed all verification, classification, and security rules."

    return record