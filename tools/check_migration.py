"""Run the current device BOM ownership migration audit; no recalculation or writes."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).resolve().parents[1]/'tests/validate_chassis_migration.py'),run_name='__main__')
