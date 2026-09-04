# engine.py

def run_inference(applicant, trace):
    """Mutates `applicant` dict in place, appends (label, detail, status)
    tuples to `trace` for the UI to render, and returns the applicant."""

    trace.append(("Goal", "Decide an outcome for this application.", "info"))

    if not applicant["documents_complete"]:
        applicant["decision"] = "review"
        applicant["reason"] = "Application file is incomplete and needs manual follow-up."
        trace.append(("Check file", "Documents are incomplete.", "review"))
        return applicant

    trace.append(("Check file", "Documents are complete.", "pass"))

    income = applicant["monthly_income"]
    debts = applicant["existing_debts"]
    dti = (debts / income * 100.0) if income > 0 else 0.0
    applicant["dti_ratio"] = dti
    trace.append(("Compute DTI", f"{debts:,} / {income:,} x 100 = {dti:.1f}%", "info"))

    score = applicant["credit_score"]
    has_default = applicant["default_history"]

    deny_holds = score < 550 or has_default
    trace.append((
        "Rule 2 — Deny",
        f"Score {score} (need < 550) or default on file: {'yes' if has_default else 'no'}.",
        "deny" if deny_holds else "fail",
    ))
    if deny_holds:
        applicant["decision"] = "denied"
        applicant["reason"] = "Credit score and/or a prior default do not meet the minimum bar."
        return applicant

    approve_holds = score >= 700 and dti <= 30.0
    trace.append((
        "Rule 1 — Approve",
        f"Score {score} (need >= 700), DTI {dti:.1f}% (need <= 30%).",
        "approve" if approve_holds else "fail",
    ))
    if approve_holds:
        applicant["decision"] = "approved"
        applicant["reason"] = f"Credit score {score} and DTI {dti:.1f}% clear the approval thresholds."
        return applicant

    applicant["decision"] = "review"
    applicant["reason"] = f"Score {score} / DTI {dti:.1f}% falls between the approve and deny thresholds."
    trace.append(("Rule 3 — Refer to review", "Neither rule fired outright.", "review"))
    return applicant