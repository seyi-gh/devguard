import os
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader

def generate_pdf(job_id: str, findings: list, output_dir: str) -> str:
  #? Configurate the template directory and get the actual file
  current_dir = os.path.dirname(os.path.abspath(__file__))
  templates_dir = os.path.join(current_dir, 'templates')

  env = Environment(loader=FileSystemLoader(templates_dir))
  template = env.get_template('report.html')

  #? Calculate the results in the resume
  totals = {
    'critical': sum(1 for f in findings if f.get('severity') == 'CRITICAL'),
    'high': sum(1 for f in findings if f.get('severity') == 'HIGH')
  }

  #? Rendering the HTML with real data
  html_out = template.render(
    job_id=job_id,
    findings=findings,
    totals=totals
  )

  #? Save the pdf
  pdf_path = os.path.join(output_dir, 'report.pdf')
  HTML(string=html_out).write_pdf(pdf_path)

  return pdf_path