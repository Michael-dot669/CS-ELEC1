import tkinter as tk
from tkinter import ttk

from styles import COLORS
from inference import run_inference


class LoanExpertSystemApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Loan Analysis Expert System")
        self.geometry("880x620")
        self.configure(bg=COLORS["bg"])
        self.minsize(760, 560)

        self._build_style()
        self._build_layout()

    def _build_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("TFrame", background=COLORS["panel"])
        style.configure("Root.TFrame", background=COLORS["bg"])
        style.configure("TLabel", background=COLORS["panel"], foreground=COLORS["text"],
                        font=("Segoe UI", 10))
        style.configure("Muted.TLabel", background=COLORS["panel"], foreground=COLORS["muted"],
                        font=("Segoe UI", 9))
        style.configure("Heading.TLabel", background=COLORS["panel"], foreground=COLORS["text"],
                        font=("Georgia", 13, "bold"))
        style.configure("Hero.TLabel", background=COLORS["bg"], foreground=COLORS["text"],
                        font=("Georgia", 20, "bold"))
        style.configure("Lede.TLabel", background=COLORS["bg"], foreground=COLORS["muted"],
                        font=("Segoe UI", 10), wraplength=760, justify="left")

        style.configure("TCombobox", fieldbackground=COLORS["panel_alt"], background=COLORS["panel_alt"],
                        foreground=COLORS["text"])
        style.configure("Horizontal.TScale", background=COLORS["panel"])
        style.configure("TCheckbutton", background=COLORS["panel"], foreground=COLORS["text"])
        style.configure("Run.TButton", background=COLORS["accent"], foreground="#FFFFFF",
                        font=("Segoe UI", 10, "bold"), padding=8)
        style.map("Run.TButton", background=[("active", "#5473E8")])

    def _build_layout(self):
        root = ttk.Frame(self, style="Root.TFrame", padding=20)
        root.pack(fill="both", expand=True)

        ttk.Label(root, text="Loan Analysis Expert System", style="Hero.TLabel").pack(anchor="w")
        ttk.Label(
            root,
            text="Enter an applicant's numbers and run the analysis to see the system "
                 "reason from the goal approve or deny back to the facts that support it.",
            style="Lede.TLabel",
        ).pack(anchor="w", pady=(6, 16))

        workspace = ttk.Frame(root, style="Root.TFrame")
        workspace.pack(fill="both", expand=True)
        workspace.columnconfigure(0, weight=1, uniform="col")
        workspace.columnconfigure(1, weight=1, uniform="col")
        workspace.rowconfigure(0, weight=1)

        self._build_intake_panel(workspace)
        self._build_trace_panel(workspace)

    def _panel(self, parent, col):
        frame = tk.Frame(parent, bg=COLORS["panel"], highlightbackground=COLORS["line"],
                         highlightthickness=1, bd=0)
        frame.grid(row=0, column=col, sticky="nsew", padx=(0, 10) if col == 0 else (10, 0))
        inner = ttk.Frame(frame, padding=18)
        inner.pack(fill="both", expand=True)
        return inner

    def _build_intake_panel(self, parent):
        panel = self._panel(parent, 0)
        ttk.Label(panel, text="Applicant intake", style="Heading.TLabel").pack(anchor="w", pady=(0, 14))

        self.applicant_id_var = tk.StringVar(value="")
        self._field_label(panel, "Applicant ID")
        tk.Entry(panel, textvariable=self.applicant_id_var, bg=COLORS["panel_alt"], fg=COLORS["text"],
                 insertbackground=COLORS["text"], relief="flat").pack(fill="x", pady=(0, 12), ipady=4)

        self.full_name_var = tk.StringVar(value="")
        self._field_label(panel, "Full name")
        tk.Entry(panel, textvariable=self.full_name_var, bg=COLORS["panel_alt"], fg=COLORS["text"],
                 insertbackground=COLORS["text"], relief="flat").pack(fill="x", pady=(0, 12), ipady=4)

        self.employment_var = tk.StringVar(value="employed")
        self._field_label(panel, "Employment status")
        ttk.Combobox(panel, textvariable=self.employment_var, state="readonly",
                     values=["employed", "self-employed", "unemployed"]).pack(fill="x", pady=(0, 12))

        self.income_var = tk.IntVar(value=45000)
        self._field_label(panel, "Monthly income (PHP)")
        tk.Entry(panel, textvariable=self.income_var, bg=COLORS["panel_alt"], fg=COLORS["text"],
                 insertbackground=COLORS["text"], relief="flat").pack(fill="x", pady=(0, 12), ipady=4)

        self.score_var = tk.IntVar(value=680)
        self._field_label(panel, "Credit score (300–850)")
        tk.Entry(panel, textvariable=self.score_var, bg=COLORS["panel_alt"], fg=COLORS["text"],
                 insertbackground=COLORS["text"], relief="flat").pack(fill="x", pady=(0, 12), ipady=4)

        self.history_var = tk.IntVar(value=4)
        self._field_label(panel, "Credit history length (yrs)")
        tk.Entry(panel, textvariable=self.history_var, bg=COLORS["panel_alt"], fg=COLORS["text"],
                 insertbackground=COLORS["text"], relief="flat").pack(fill="x", pady=(0, 12), ipady=4)

        self.debts_var = tk.IntVar(value=9000)
        self._field_label(panel, "Existing monthly debt payments (PHP)")
        tk.Entry(panel, textvariable=self.debts_var, bg=COLORS["panel_alt"], fg=COLORS["text"],
                 insertbackground=COLORS["text"], relief="flat").pack(fill="x", pady=(0, 12), ipady=4)

        self.docs_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(panel, text="Documents complete", variable=self.docs_var).pack(anchor="w", pady=(0, 8))

        self.default_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(panel, text="History of default on a prior loan",
                         variable=self.default_var).pack(anchor="w", pady=(0, 16))

        ttk.Button(panel, text="Run analysis", style="Run.TButton",
                   command=self.run_analysis).pack(fill="x")

        ttk.Label(
            panel,
            text="Employment status and history length are captured on every "
                 "application but aren't part of the approval rules yet.",
            style="Muted.TLabel", wraplength=340, justify="left",
        ).pack(anchor="w", pady=(14, 0))

    def _field_label(self, parent, text):
        label = ttk.Label(parent, text=text, style="Muted.TLabel")
        label.pack(anchor="w", pady=(0, 4))
        return label

    def _build_trace_panel(self, parent):
        panel = self._panel(parent, 1)
        ttk.Label(panel, text="Reasoning trace", style="Heading.TLabel").pack(anchor="w", pady=(0, 6))
        ttk.Label(
            panel,
            text="Backward-chaining: the system starts from the goal and checks "
                 "which rule's conditions actually hold.",
            style="Muted.TLabel", wraplength=340, justify="left",
        ).pack(anchor="w", pady=(0, 14))

        self.trace_text = tk.Text(
            panel, height=16, wrap="word", bg=COLORS["panel_alt"], fg=COLORS["text"],
            relief="flat", padx=12, pady=10, font=("Segoe UI", 9), state="disabled",
        )
        self.trace_text.pack(fill="both", expand=True, pady=(0, 14))
        self.trace_text.tag_configure("pass", foreground=COLORS["approve"])
        self.trace_text.tag_configure("approve", foreground=COLORS["approve"])
        self.trace_text.tag_configure("deny", foreground=COLORS["deny"])
        self.trace_text.tag_configure("review", foreground=COLORS["review"])
        self.trace_text.tag_configure("fail", foreground=COLORS["muted"])
        self.trace_text.tag_configure("info", foreground=COLORS["muted"])
        self.trace_text.tag_configure("bold", font=("Segoe UI", 9, "bold"))

        self.verdict_frame = tk.Frame(panel, bg=COLORS["panel_alt"], highlightthickness=1,
                                       highlightbackground=COLORS["line"])
        self.verdict_frame.pack(fill="x")
        self.verdict_applicant = tk.Label(self.verdict_frame, text="", bg=COLORS["panel_alt"],
                                           fg=COLORS["muted"], font=("Segoe UI", 9, "bold"),
                                           anchor="w", padx=12)
        self.verdict_applicant.pack(fill="x", pady=(10, 0))
        self.verdict_label = tk.Label(self.verdict_frame, text="Run the analysis to see a verdict.",
                                       bg=COLORS["panel_alt"], fg=COLORS["muted"],
                                       font=("Georgia", 13, "bold"), anchor="w", padx=12)
        self.verdict_label.pack(fill="x", pady=(2, 4))
        self.verdict_reason = tk.Label(self.verdict_frame, text="", bg=COLORS["panel_alt"],
                                        fg=COLORS["muted"], font=("Segoe UI", 9), anchor="w",
                                        justify="left", wraplength=340, padx=12)
        self.verdict_reason.pack(fill="x", pady=(0, 10))

    def run_analysis(self):
        applicant = {
            "applicant_id": self.applicant_id_var.get().strip() or "—",
            "full_name": self.full_name_var.get().strip() or "—",
            "employment_status": self.employment_var.get(),
            "monthly_income": self.income_var.get(),
            "credit_score": self.score_var.get(),
            "credit_history_length": self.history_var.get(),
            "existing_debts": self.debts_var.get(),
            "documents_complete": self.docs_var.get(),
            "default_history": self.default_var.get(),
            "decision": "pending",
            "reason": "",
        }

        trace = []
        run_inference(applicant, trace)

        self.trace_text.config(state="normal")
        self.trace_text.delete("1.0", "end")
        for label, detail, status in trace:
            self.trace_text.insert("end", label + "\n", ("bold", status))
            self.trace_text.insert("end", detail + "\n\n", status)
        self.trace_text.config(state="disabled")

        self.verdict_applicant.config(
            text=f"{applicant['applicant_id']} — {applicant['full_name']}"
        )

        decision = applicant["decision"]
        color_key = {"approved": "approve", "denied": "deny", "review": "review"}[decision]
        label_text = {"approved": "APPROVE", "denied": "DENY", "review": "REFER TO REVIEW"}[decision]

        self.verdict_label.config(text=label_text, fg=COLORS[color_key])
        self.verdict_reason.config(text=applicant["reason"])


if __name__ == "__main__":
    app = LoanExpertSystemApp()
    app.mainloop()