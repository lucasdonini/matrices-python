import subprocess
import os

file = 'main.py'
mypy_path = os.path.join(os.path.dirname(__file__), '.venv', 'Scripts', 'mypy.exe')

result = subprocess.run([mypy_path, file])

if result.returncode == 0:
    print(f'\n✅ Type Validation passed. Running {file}...\n')
    subprocess.run(['python', file], encoding='utf-8')
else:
    print('\n❌ Type Validation failed.\n')
