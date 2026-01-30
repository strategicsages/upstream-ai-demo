import streamlit as st
import pandas as pd
import time
import json
def supplier_enablement_agent_mock(supplier):
    confidence = supplier["Avg. AI Confidence"]
    invoices = supplier["Invoices Processed"]
    category = supplier["Category"]

    if confidence < 70:
        return {
            "supplier_maturity": "Low",
            "recommended_path": "Hybrid: AI + Human",
            "diagnosis": "Supplier submits inconsistent, low-quality data. Likely low tooling maturity.",
            "ai_actions": [
                "Auto-generated invoice template",
                "Mobile photo → structured data pipeline",
                "Confidence feedback loop per invoice"
            ],
            "human_actions": [
                "Supplier onboarding call",
                "Training on data submission best practices"
            ],
            "expected_uplift": "+15–20% confidence"
        }

    elif confidence < 85:
        return {
            "supplier_maturity": "Medium",
            "recommended_path": "AI-led enablement",
            "diagnosis": "Supplier is partially structured but inconsistent across invoices.",
            "ai_actions": [
                "Automated validation checks",
                "AI-generated submission guidance"
            ],
            "human_actions": [],
            "expected_uplift": "+8–12% confidence"
        }

    else:
        return {
            "supplier_maturity": "High",
            "recommended_path": "Monitor only",
            "diagnosis": "Supplier data is reliable and consistent.",
            "ai_actions": ["No action required"],
            "human_actions": [],
            "expected_uplift": "+2–3% confidence"
        }
