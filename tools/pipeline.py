"""Isolated financial pipeline; only completed stages publish current outputs."""
import shutil, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def run_pipeline(steps):
    from validate_data import validate_collections
    validate_collections()
    with tempfile.TemporaryDirectory(prefix='logix-model-',dir=ROOT.parent) as tmp:
        stage=Path(tmp)/'project'
        shutil.copytree(ROOT,stage,ignore=shutil.ignore_patterns('.git','__pycache__','node_modules','.venv'))
        for step in steps:
            result=subprocess.run([sys.executable,str(stage/'tools'/step[0]),*step[1:]],cwd=stage,capture_output=True,text=True)
            if result.returncode:
                print(result.stdout);print(result.stderr,file=sys.stderr)
                raise RuntimeError('Stage failed; current outputs unchanged: '+' '.join(step))
            print('Staged',*step)
        subprocess.run([sys.executable,str(stage/'tools/build_site.py')],cwd=stage,check=True)
        subprocess.run([sys.executable,str(stage/'tests/validate_data_structure.py')],cwd=stage,check=True)
        candidates=[]
        for folder in ('generated/models','data'):
            candidates.extend((stage/folder).rglob('*.json'))
        candidates.extend(stage.glob('*.html'))
        changed=0
        for source in candidates:
            destination=ROOT/source.relative_to(stage)
            content=source.read_bytes()
            if not destination.exists() or destination.read_bytes()!=content:
                destination.parent.mkdir(parents=True,exist_ok=True)
                destination.write_bytes(content);changed+=1
        print('Published',changed,'changed files after completed pipeline')
