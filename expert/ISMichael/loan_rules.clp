(deftemplate applicant
   (slot applicant-id (type STRING) (default "N/A"))
   (slot full-name (type STRING) (default "N/A"))
   (slot employment-status (type SYMBOL) (allowed-symbols Employed Self-Employed Unemployed) (default Employed))
   (slot monthly-income (type FLOAT) (default 0.0))
   (slot credit-score (type INTEGER) (range 300 850) (default 650))
   (slot credit-history-years (type FLOAT) (default 0.0))
   (slot existing-debts (type FLOAT) (default 0.0))
   (slot debt-to-income (type FLOAT) (default 0.0))
   (slot documents-complete (type SYMBOL) (allowed-symbols yes no) (default yes))
   (slot has-collateral (type SYMBOL) (allowed-symbols yes no) (default no))
   (slot history-of-default (type SYMBOL) (allowed-symbols yes no) (default no)))

(deftemplate decision
   (slot status (type SYMBOL) (allowed-symbols APPROVE DENY REVIEW))
   (slot reason (type STRING))
   (slot rule-fired (type STRING)))

(defrule rule-incomplete-documents
   (declare (salience 100))
   (applicant (documents-complete no))
   =>
   (assert (decision (status REVIEW)
                     (reason "Application file is incomplete and needs manual follow-up.")
                     (rule-fired "R0: Incomplete Documents"))))

(defrule rule-history-of-default
   (declare (salience 90))
   (applicant (history-of-default yes))
   =>
   (assert (decision (status DENY)
                     (reason "Applicant has a history of default on prior loans.")
                     (rule-fired "R1: History of Default"))))

(defrule rule-deny-low-score
   (declare (salience 80))
   (applicant (credit-score ?score) (documents-complete yes))
   (test (< ?score 550))
   =>
   (assert (decision (status DENY)
                     (reason (str-cat "Credit score " ?score " is below the minimum threshold of 550."))
                     (rule-fired "R2: Credit Score < 550"))))

(defrule rule-approve
   (declare (salience 70))
   (applicant (credit-score ?score) (debt-to-income ?dti) (documents-complete yes) (history-of-default no))
   (test (>= ?score 700))
   (test (<= ?dti 30.0))
   =>
   (assert (decision (status APPROVE)
                     (reason (str-cat "Credit score " ?score " meets or exceeds 700, and debt-to-income ratio " ?dti "% is at or below 30%."))
                     (rule-fired "R3: Score >= 700 AND DTI <= 30%"))))

(defrule rule-review-high-dti
   (declare (salience 60))
   (applicant (credit-score ?score) (debt-to-income ?dti) (documents-complete yes) (history-of-default no))
   (test (>= ?score 550))
   (test (> ?dti 30.0))
   (not (decision (status APPROVE)))
   (not (decision (status DENY)))
   =>
   (assert (decision (status REVIEW)
                     (reason (str-cat "Debt-to-income ratio " ?dti "% is above the 30% comfort threshold; needs manual review."))
                     (rule-fired "R4: DTI > 30% (borderline)"))))

(defrule rule-review-borderline
   (declare (salience 50))
   (applicant (credit-score ?score) (documents-complete yes) (history-of-default no))
   (test (>= ?score 550))
   (test (< ?score 700))
   (not (decision (status APPROVE)))
   (not (decision (status DENY)))
   (not (decision (status REVIEW)))
   =>
   (assert (decision (status REVIEW)
                     (reason (str-cat "Credit score " ?score " is borderline (550-699); referred to a loan officer for manual review."))
                     (rule-fired "R5: Borderline Credit Score"))))

(defrule rule-fallback-review
   (declare (salience 1))
   (applicant)
   (not (decision))
   =>
   (assert (decision (status REVIEW)
                     (reason "Application does not clearly match an approve or deny rule; referred for manual review.")
                     (rule-fired "R6: Fallback / No Clear Match"))))