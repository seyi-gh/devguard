from fastapi import FastAPI
from pydantic import BaseModel
from celery.result import AsyncResult
from app.celery_app import celery_app

app = FastAPI(title='DevGuard API')

class ScanRequest(BaseModel):
  repo_url: str

@app.post('/api/scans')
def create_scan(request: ScanRequest):
  task = celery_app.send_task('scan_repo_task', args=[request.repo_url])
  return { 'job_id': task.id, 'status': 'queued' }

@app.get('/api/scans/{job_id}')
def get_scan_status(job_id: str):
  task_result = AsyncResult(job_id, app=celery_app) #? Getting the status of redis and celery

  print('Test:', task_result.result)

  if task_result.state == 'PENDING':
    return { 'status': 'running' }
  elif task_result.state == 'SUCCESS':
    return task_result.result
  else:
    return { 'status': task_result.state }


#? Health method
@app.get('/health')
def health(): return { 'status': 'active', 'message': 'The backend is working' }