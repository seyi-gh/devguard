import json
import subprocess

#? Cloning repositories method (git)
def run_bandit(repo_path: str) -> list:
  result = subprocess.run(
    ['bandit', '-r', '.', '-f', 'json', '-q'],
    capture_output=True,
    text=True,
    cwd=repo_path
  )

  try:
    data = json.loads(result.stdout or '{}')
    return data.get('results', [])
  except json.JSONDecodeError:
    return []