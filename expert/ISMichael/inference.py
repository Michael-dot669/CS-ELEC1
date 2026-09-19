import clips

def run_inference(applicant, trace):
    trace.append(("Goal", "Decide an outcome using CLIPS Expert System.", "info"))

    env = clips.Environment()

    try:
        env.load("loan_rules.clp")
    except Exception as e:
        trace.append(("Error", f"Failed to load loan_rules.clp: {e}", "deny"))
        applicant["decision"] = "review"
        applicant["reason"] = "Could not load CLIPS rules file."
        return applicant

    # Calculate DTI
    income = float(applicant.get("monthly_income", 0))
    debts = float(applicant.get("existing_debts", 0))
    dti = (debts / income * 100.0) if income > 0 else 0.0
    applicant["dti_ratio"] = dti

    trace.append(("Compute DTI", f"{debts:,.0f} / {income:,.0f} x 100 = {dti:.1f}%", "info"))

    # Map Python data to CLIPS
    app_id = applicant.get("applicant_id") or "N/A"
    full_name = applicant.get("full_name") or "N/A"
    
    emp = applicant.get("employment_status", "employed")
    emp_status = "Self-Employed" if emp == "self-employed" else ("Unemployed" if emp == "unemployed" else "Employed")
    
    docs_complete = "yes" if applicant.get("documents_complete") else "no"
    has_default = "yes" if applicant.get("default_history") else "no"
    score = int(applicant.get("credit_score", 650))
    history_yrs = float(applicant.get("credit_history_length", 0))

    fact_str = f"""
    (applicant 
        (applicant-id "{app_id}")
        (full-name "{full_name}")
        (employment-status {emp_status})
        (monthly-income {income})
        (credit-score {score})
        (credit-history-years {history_yrs})
        (existing-debts {debts})
        (debt-to-income {dti:.1f})
        (documents-complete {docs_complete})
        (history-of-default {has_default})
    )
    """

    env.assert_string(fact_str)
    trace.append(("Assert Fact", "Applicant facts loaded into CLIPS memory.", "info"))

    # Run CLIPS rules
    env.run()

    # Get decision from CLIPS
    decision_found = False
    for fact in env.facts():
        if fact.template.name == "decision":
            decision_found = True
            raw_status = str(fact["status"]).lower()
            reason = str(fact["reason"])
            rule_fired = str(fact["rule-fired"])

            if raw_status == "approve":
                status_tag = "approved"
                trace_tag = "approve"
            elif raw_status == "deny":
                status_tag = "denied"
                trace_tag = "deny"
            else:
                status_tag = "review"
                trace_tag = "review"

            applicant["decision"] = status_tag
            applicant["reason"] = f"[{rule_fired}] {reason}"

            trace.append((f"Fired: {rule_fired}", reason, trace_tag))
            break

    if not decision_found:
        applicant["decision"] = "review"
        applicant["reason"] = "No CLIPS rule triggered."
        trace.append(("Fallback", "No CLIPS decision fact created.", "review"))

    return applicant