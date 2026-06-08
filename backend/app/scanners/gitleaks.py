import os
import json
import subprocess

def run_gitleaks(repo_path: str) -> list:
  report_path = os.path.join(repo_path, 'gitleaks_report.json')

  subprocess.run(
    [
      '/usr/local/bin/gitleaks', 'detect',
      '--source', repo_path,
      '--report-format', 'json',
      '--report-path', report_path,
      '--no-git',
      '--exit-code', '0'
    ],
    capture_output=True,
    text=True
  )

  if not os.path.exists(report_path): return []

  #? Normalize the json
  with open(report_path, 'r') as f:
    try:
      data = json.load(f)
      findings = []

      for item in data:
        findings.append({
          'tool': 'gitleaks',
          'severity': 'CRITICAL',
          'message': f'Secret detected ({item.get('RuleID')}) in the file: {item.get('File')}'
        })
      
      return findings
    except json.JSONDecodeError:
      return []