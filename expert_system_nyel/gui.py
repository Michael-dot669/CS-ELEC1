

import tkinter as tk
from tkinter import ttk

from config import COLORS
from engine import run_inference


class InfoManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Information Management Expert System")
        self.geometry("900x640")
        self.configure(bg=COLORS["bg"])
        self.minsize(800, 580)

        self._build_style()
        self._build_layout()

    def _build_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("TFrame", background=COLORS["panel"])
        style.configure("Root.TFrame", background=COLORS["bg"])
        style.configure("TLabel", background=COLORS["panel"], foreground=COLORS["text"], font=("Segoe UI", 10))
        style.configure("Muted.TLabel", background=COLORS["panel"], foreground=COLORS["muted"], font=("Segoe UI", 9))
        style.configure("Heading.TLabel", background=COLORS["panel"], foreground=COLORS["text"], font=("Georgia", 13, "bold"))
        style.configure("Hero.TLabel", background=COLORS["bg"], foreground=COLORS["text"], font=("Georgia", 18, "bold"))
        style.configure("Lede.TLabel", background=COLORS["bg"], foreground=COLORS["muted"], font=("Segoe UI", 10), wraplength=780, justify="left")

        style.configure("TCombobox", fieldbackground=COLORS["panel_alt"], background=COLORS["panel_alt"], foreground=COLORS["text"])
        style.configure("Run.TButton", background=COLORS["accent"], foreground="#FFFFFF", font=("Segoe UI", 10, "bold"), padding=8)
        style.map("Run.TButton", background=[("active", "#5473E8")])

    def _build_layout(self):
        root = ttk.Frame(self, style="Root.TFrame", padding=20)
        root.pack(fill="both", expand=True)

        ttk.Label(root, text="Information Management Expert System", style="Hero.TLabel").pack(anchor="w")
        ttk.Label(
            root,
            text="Simulate forward-chaining reasoning to organize and verify record compliance.",
            style="Lede.TLabel",
        ).pack(anchor="w", pady=(4, 14))

        workspace = ttk.Frame(root, style="Root.TFrame")
        workspace.pack(fill="both", expand=True)
        workspace.columnconfigure(0, weight=1, uniform="col")
        workspace.columnconfigure(1, weight=1, uniform="col")
        workspace.rowconfigure(0, weight=1)

        self._build_intake_panel(workspace)
        self._build_trace_panel(workspace)

    def _panel(self, parent, col):
        frame = tk.Frame(parent, bg=COLORS["panel"], highlightbackground=COLORS["line"], highlightthickness=1, bd=0)
        frame.grid(row=0, column=col, sticky="nsew", padx=(0, 10) if col == 0 else (10, 0))
        inner = ttk.Frame(frame, padding=18)
        inner.pack(fill="both", expand=True)
        return inner

    def _build_intake_panel(self, parent):
        panel = self._panel(parent, 0)
        ttk.Label(panel, text="Record Input", style="Heading.TLabel").pack(anchor="w", pady=(0, 12))

        self.record_id_var = tk.StringVar(value="REC-2026-001")
        self._field_label(panel, "Record ID")
        tk.Entry(panel, textvariable=self.record_id_var, bg=COLORS["panel_alt"], fg=COLORS["text"], relief="flat").pack(fill="x", pady=(0, 8), ipady=3)

        self.record_type_var = tk.StringVar(value="Document")
        self._field_label(panel, "Record Type")
        ttk.Combobox(panel, textvariable=self.record_type_var, state="readonly", values=["Document", "Customer Data", "Report", "File"]).pack(fill="x", pady=(0, 8))

        self.date_created_var = tk.StringVar(value="2024-01-15")
        self._field_label(panel, "Date Created (YYYY-MM-DD)")
        tk.Entry(panel, textvariable=self.date_created_var, bg=COLORS["panel_alt"], fg=COLORS["text"], relief="flat").pack(fill="x", pady=(0, 8), ipady=3)

        self.last_updated_var = tk.StringVar(value="2024-05-20")
        self._field_label(panel, "Last Updated (YYYY-MM-DD)")
        tk.Entry(panel, textvariable=self.last_updated_var, bg=COLORS["panel_alt"], fg=COLORS["text"], relief="flat").pack(fill="x", pady=(0, 8), ipady=3)

        self.category_var = tk.StringVar(value="Confidential")
        self._field_label(panel, "Category")
        ttk.Combobox(panel, textvariable=self.category_var, state="readonly", values=["Personal", "Financial", "Operational", "Confidential"]).pack(fill="x", pady=(0, 8))

        self.access_level_var = tk.StringVar(value="Public")
        self._field_label(panel, "Access Level")
        ttk.Combobox(panel, textvariable=self.access_level_var, state="readonly", values=["Public", "Restricted", "Confidential"]).pack(fill="x", pady=(0, 8))

        self.completeness_var = tk.StringVar(value="Incomplete")
        self._field_label(panel, "Completeness")
        ttk.Combobox(panel, textvariable=self.completeness_var, state="readonly", values=["Complete", "Incomplete"]).pack(fill="x", pady=(0, 14))

        ttk.Button(panel, text="Run Inference", style="Run.TButton", command=self.run_analysis).pack(fill="x")

    def _field_label(self, parent, text):
        label = ttk.Label(parent, text=text, style="Muted.TLabel")
        label.pack(anchor="w", pady=(0, 2))
        return label

    def _build_trace_panel(self, parent):
        panel = self._panel(parent, 1)
        ttk.Label(panel, text="Reasoning Trace", style="Heading.TLabel").pack(anchor="w", pady=(0, 4))
        ttk.Label(
            panel,
            text="Forward-chaining rules triggered based on facts.",
            style="Muted.TLabel", wraplength=340, justify="left",
        ).pack(anchor="w", pady=(0, 10))

        self.trace_text = tk.Text(
            panel, height=14, wrap="word", bg=COLORS["panel_alt"], fg=COLORS["text"],
            relief="flat", padx=10, pady=8, font=("Segoe UI", 9), state="disabled",
        )
        self.trace_text.pack(fill="both", expand=True, pady=(0, 12))
        self.trace_text.tag_configure("pass", foreground=COLORS["approve"])
        self.trace_text.tag_configure("approve", foreground=COLORS["approve"])
        self.trace_text.tag_configure("deny", foreground=COLORS["deny"])
        self.trace_text.tag_configure("review", foreground=COLORS["review"])
        self.trace_text.tag_configure("fail", foreground=COLORS["muted"])
        self.trace_text.tag_configure("info", foreground=COLORS["muted"])
        self.trace_text.tag_configure("bold", font=("Segoe UI", 9, "bold"))

        self.verdict_frame = tk.Frame(panel, bg=COLORS["panel_alt"], highlightthickness=1, highlightbackground=COLORS["line"])
        self.verdict_frame.pack(fill="x")
        self.verdict_record = tk.Label(self.verdict_frame, text="", bg=COLORS["panel_alt"], fg=COLORS["muted"], font=("Segoe UI", 9, "bold"), anchor="w", padx=10)
        self.verdict_record.pack(fill="x", pady=(8, 0))
        self.verdict_label = tk.Label(self.verdict_frame, text="Run analysis to see evaluation status.", bg=COLORS["panel_alt"], fg=COLORS["muted"], font=("Georgia", 11, "bold"), anchor="w", padx=10)
        self.verdict_label.pack(fill="x", pady=(2, 2))
        self.verdict_reason = tk.Label(self.verdict_frame, text="", bg=COLORS["panel_alt"], fg=COLORS["muted"], font=("Segoe UI", 9), anchor="w", justify="left", wraplength=320, padx=10)
        self.verdict_reason.pack(fill="x", pady=(0, 8))

    def run_analysis(self):
        record = {
            "record_id": self.record_id_var.get().strip() or "—",
            "record_type": self.record_type_var.get(),
            "date_created": self.date_created_var.get().strip(),
            "last_updated": self.last_updated_var.get().strip(),
            "category": self.category_var.get(),
            "access_level": self.access_level_var.get(),
            "completeness": self.completeness_var.get(),
            "verified": False,
            "needs_update": False,
            "decision": "PENDING",
            "reason": ""
        }

        trace = []
        run_inference(record, trace)

        self.trace_text.config(state="normal")
        self.trace_text.delete("1.0", "end")
        for label, detail, status in trace:
            self.trace_text.insert("end", label + "\n", ("bold", status))
            self.trace_text.insert("end", detail + "\n\n", status)
        self.trace_text.config(state="disabled")

        self.verdict_record.config(text=f"{record['record_id']} ({record['record_type']})")

        decision = record["decision"]
        if decision == "COMPLIANT & VERIFIED":
            color = COLORS["approve"]
        elif decision == "PENDING VERIFICATION":
            color = COLORS["review"]
        else:
            color = COLORS["deny"]

        self.verdict_label.config(text=decision, fg=color)
        self.verdict_reason.config(text=record["reason"])