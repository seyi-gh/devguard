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
    raw_results = data.get('results', [])

    findings = []
    for item in raw_results:
      findings.append({
        'tool': 'bandit',
        'severity': item.get('issue_severity', 'LOW').upper(),
        'message': f'[{item.get('test_name', 'Vuln')}] {item.get('issue_text', 'No description')} (File: {item.get('filename', 'Unknown')})'
      })

    return findings
  except Exception as e:
    return []