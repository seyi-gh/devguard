import os

from pydantic import BaseModel
from pydantic import BaseModel

from celery.result import AsyncResult

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.celery_app import celery_app
from app.pdf import generate_pdf

app = FastAPI(title='DevGuard API')

app.add_middleware(
  CORSMiddleware,
  allow_origins=['http://localhost:3000'], #? Debug in cors
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*'],
)

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

@app.get('/api/scans/{job_id}/report')
def download_pdf_report(job_id: str):
  task_result = AsyncResult(job_id, app=celery_app)

  if task_result.state != 'SUCCESS':
    raise HTTPException(status_code=400, detail='Scan is not completed yet.')

  data = task_result.result

  #? Trying create the temp directory
  reports_dir = '/tmp/devguard/reports'
  os.makedirs(reports_dir, exist_ok=True)

  #? Generate the pdf
  pdf_path = generate_pdf(job_id, data.get('findings', []), reports_dir)

  return FileResponse(
    path=pdf_path,
    filename=f'DevGuard_Report_{job_id}.pdf',
    media_type='application/pdf'
  )

#? Health method
@app.get('/health')
def health(): return { 'status': 'active', 'message': 'The backend is working' }