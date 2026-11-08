from pathlib import Path
import hashlib
import zipfile
ROOT = Path(__file__).resolve().parent
NAME = ROOT.name
# A release is built from explicit source/documentation paths, never local outputs.
paths = [ROOT / x for x in ('main.py', 'common.py', 'smoke.py', 'build_release.py', 'README.md', 'LICENSE', 'CHANGELOG.md', 'CONTRIBUTING.md', 'RELEASE_NOTES.md', '.gitignore')]
for folder in ('tests', 'examples', 'docs', '.github'):
    paths += [p for p in (ROOT / folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts]
output = ROOT / 'dist'
output.mkdir(exist_ok=True)
archive = output / (NAME + '-v1.0.0-source.zip')
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as bundle:
    for path in sorted(paths):
        info = zipfile.ZipInfo(NAME + '/' + path.relative_to(ROOT).as_posix(), date_time=(2026, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        bundle.writestr(info, path.read_bytes())
(output / 'SHA256SUMS.txt').write_text(hashlib.sha256(archive.read_bytes()).hexdigest() + '  ' + archive.name + '\n', encoding='ascii')
print(archive.name)
