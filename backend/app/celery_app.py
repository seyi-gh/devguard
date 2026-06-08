import os
import time
import shutil
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
  time.sleep(5) #? Simulate a real project

  #! Fake data for testing
  return {
    'status': 'completed',
    'repo': repo_url,
    'findings': [
      { 'tool': 'bandit', 'severity': 'HIGH', 'message': 'Simulated secret found' }
    ]
  }