"""Recalculate cost/pricing reviews in isolation; publish only after all stages pass."""
from pipeline import run_pipeline
steps=[[name] for name in ['build_cost_assessment.py','build_pricing.py','build_team_review.py','build_comdex82_costs.py','build_retail_catalog.py','build_ncc82_review.py']]
if __name__=='__main__':run_pipeline(steps)
