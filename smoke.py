from pathlib import Path
import subprocess
import sys
import tempfile
import shutil
ROOT=Path(__file__).resolve().parent
COMMANDS=[]
COMMAND_LINES=['python main.py --board outputs/demo-board.json init', 'python main.py --board outputs/demo-board.json add "Implement parser" --accept "Empty and Unicode inputs pass"', 'python main.py --board outputs/demo-board.json move T001 doing', 'python main.py --board outputs/demo-board.json move T001 done --evidence "Unit tests passed"', 'python main.py --board outputs/demo-board.json export --out outputs/demo']
import shlex
with tempfile.TemporaryDirectory() as temp:
    target=Path(temp)
    shutil.copytree(ROOT/'examples',target/'examples')
    for line in COMMAND_LINES:
        args=shlex.split(line)
        subprocess.run([sys.executable,str(ROOT/'main.py'),*args[2:]],cwd=target,check=True)
    assert list((target/'outputs').rglob('*.html')), 'No HTML report generated'
print('Examples passed')
