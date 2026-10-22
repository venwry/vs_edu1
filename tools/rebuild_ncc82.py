"""Rebuild NCC unit costs/prices and reports without changing demand or financial forecasts."""
import subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
for name in ['build_cost_assessment.py','build_pricing.py','build_team_review.py','build_ncc82_review.py']:
 subprocess.run([sys.executable,str(R/'tools'/name)],cwd=R,check=True)
