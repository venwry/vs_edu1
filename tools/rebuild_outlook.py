"""Rebuild dependent forecasts, financial reports and timeline without Markdown output."""
import subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
steps=[['build_cost_assessment.py'],['build_pricing.py'],['build_comdex82_costs.py'],['build_retail_catalog.py'],['build_sales.py'],['build_investment_model.py'],['build_roi.py'],['build_market_outlook.py','--timeline'],['build_sales.py'],['build_investment_model.py'],['build_roi.py'],['build_market_outlook.py'],['build_memory_report.py'],['build_ecosystem_forecast.py']]
for step in steps:
 result=subprocess.run([sys.executable,str(R/'tools'/step[0]),*step[1:]],cwd=R,capture_output=True,text=True)
 if result.returncode:
  print(result.stdout);print(result.stderr,file=sys.stderr);sys.exit(result.returncode)
 print('Built',*step)
