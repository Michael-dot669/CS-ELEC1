;; =========================================================
;; INFORMATION MANAGEMENT EXPERT SYSTEM (CLIPS)
;; =========================================================

;; 1. Fact Construct (Deftemplate)
(deftemplate record
   (slot record-id (type STRING))
   (slot record-type (type STRING))
   (slot days-old (type INTEGER))
   (slot category (type STRING))
   (slot access-level (type STRING))
   (slot completeness (type STRING))
   (slot status (type STRING) (default "OK"))
   (slot needs-update (type SYMBOL) (default FALSE))
   (slot security-review (type SYMBOL) (default FALSE)))

;; 2. Initial Facts (Defacts)
(deffacts sample-records
   (record (record-id "REC-101") (record-type "Document") (days-old 400) (category "Confidential") (access-level "Public") (completeness "Incomplete"))
   (record (record-id "REC-102") (record-type "Customer Data") (days-old 100) (category "Financial") (access-level "Restricted") (completeness "Complete")))

;; 3. Rules (Defrule)

;; Rule 1: Outdated Record Check (> 365 days)
(defrule check-outdated
   ?r <- (record (record-id ?id) (days-old ?days&:(> ?days 365)) (needs-update FALSE))
   =>
   (modify ?r (needs-update TRUE))
   (printout t "RULE 1 FIRED: Record " ?id " is outdated (" ?days " days old). Flagged for update." crlf))

;; Rule 2: Completeness Check
(defrule check-completeness
   ?r <- (record (record-id ?id) (completeness "Incomplete") (status "OK"))
   =>
   (modify ?r (status "Pending Verification"))
   (printout t "RULE 2 FIRED: Record " ?id " is incomplete. Status set to Pending Verification." crlf))

;; Rule 3: Security Review Check
(defrule check-security
   ?r <- (record (record-id ?id) (category "Confidential") (access-level ~"Restricted") (security-review FALSE))
   =>
   (modify ?r (security-review TRUE))
   (printout t "RULE 3 FIRED: Record " ?id " is Confidential but not Restricted! Flagged for Security Review." crlf))