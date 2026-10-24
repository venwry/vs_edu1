"""Run the current component-identity migration audit; no recalculation or writes."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).resolve().parents[1]/'tests/validate_component_migration.py'),run_name='__main__')
