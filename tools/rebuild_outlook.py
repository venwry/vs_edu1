"""Recalculate financial models in isolation, then publish the final reassessment."""
from pipeline import run_pipeline
steps=[['build_cost_assessment.py'],['build_pricing.py'],['build_comdex82_costs.py'],['build_retail_catalog.py'],['build_sales.py'],['build_investment_model.py'],['build_roi.py'],['build_market_outlook.py','--timeline'],['build_sales.py'],['build_investment_model.py'],['build_roi.py'],['build_market_outlook.py'],['build_memory_report.py'],['build_ncc82_review.py'],['build_sales_reassessment.py'],['build_ecosystem_forecast.py']]
if __name__=='__main__':run_pipeline(steps)
