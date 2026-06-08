import os
import shutil
import subprocess
from celery import Celery
from app.scanners.bandit import run_bandit

celery_app = Celery(
  'tasks',
  broker='redis://redis:6379/0',
  backend='redis://redis:6379/0'
)

#? Health task for checking if the app is running
@celery_app.task(name='ping_task')
def ping_task(): return 'pong'




@celery_app.task(name='scan_repo_task', bind=True) #? bind=True | Self integration lecture
def scan_repo_task(self, repo_url: str):
  job_id = self.request.id
  repo_path = f'/tmp/devguard/{job_id}'

  #? Cloning the repositorie using `--depth 1` for download the last commit
  try:
    subprocess.run(
      ['git', 'clone', '--depth', '1', repo_url, repo_path],
      check=True,
      capture_output=True
    )

    findings = run_bandit(repo_path)

    return {
      'status': 'completed',
      'repo': repo_url,
      'findings': findings
    }
  except subprocess.CalledProcessError as e:
    return {
      'status': 'failed',
      'repo': repo_url,
      'error': 'The repository could not be cloned. Please check the URL.'
    }
  finally: #? Cleaning the code when finished
    if os.path.exists(repo_path):
      shutil.rmtree(repo_path, ignore_errors=True)