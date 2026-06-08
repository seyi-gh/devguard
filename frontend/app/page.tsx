"use client";

import { useState } from "react";
import useSWR from "swr";
import { ShieldCheck, Loader2, Download, AlertTriangle } from "lucide-react";

const fetcher = (url: string) => fetch(url).then((res) => res.json());

export default function Dashboard() {
  const [repoUrl, setRepoUrl] = useState("");
  const [jobId, setJobId] = useState<string | null>(null);

  // SWR hace la magia del polling automáticamente
  const { data: scan } = useSWR(
    jobId ? `http://localhost:8000/api/scans/${jobId}` : null,
    fetcher,
    {
      refreshInterval: (data) =>
        data?.status === "completed" || data?.status === "failed" ? 0 : 2000,
    }
  );

  const handleScan = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!repoUrl) return;
    setJobId(null);

    const res = await fetch("http://localhost:8000/api/scans", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ repo_url: repoUrl }),
    });
    const data = await res.json();
    setJobId(data.job_id);
  };

  const isRunning = scan?.status === "queued" || scan?.status === "running";
  const isDone = scan?.status === "completed";

  return (
    <main className="max-w-5xl mx-auto p-8">
      {/* Cabecera */}
      <div className="flex items-center gap-3 mb-10">
        <ShieldCheck className="w-10 h-10 text-blue-600" />
        <h1 className="text-3xl font-bold text-slate-800">DevGuard Audit</h1>
      </div>

      {/* Formulario de Escaneo */}
      <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 mb-8">
        <form onSubmit={handleScan} className="flex gap-4">
          <input
            type="url"
            required
            placeholder="https://github.com/usuario/repo"
            className="flex-1 px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 outline-none"
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
            disabled={isRunning}
          />
          <button
            type="submit"
            disabled={isRunning}
            className="bg-slate-900 text-white px-8 py-3 rounded-lg font-medium hover:bg-slate-800 disabled:opacity-50 flex items-center gap-2 transition-colors"
          >
            {isRunning ? <Loader2 className="w-5 h-5 animate-spin" /> : "Run Security Scan"}
          </button>
        </form>
      </div>

      {/* Resultados e Interfaz Condicional */}
      {isDone && (
        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
          <div className="flex justify-between items-center bg-white p-6 rounded-xl shadow-sm border border-slate-200">
            <div>
              <h2 className="text-xl font-bold text-slate-800">Security Report</h2>
              <p className="text-slate-500 mt-1">
                Detected <span className="font-bold text-slate-900">{scan.findings_count}</span> vulnerabilities.
              </p>
            </div>
            
            {/* Botón para generar el PDF a demanda */}
            <a
              href={`http://localhost:8000/api/scans/${jobId}/report`}
              target="_blank"
              rel="noreferrer"
              className="flex items-center gap-2 bg-blue-50 text-blue-700 px-5 py-2.5 rounded-lg font-medium hover:bg-blue-100 transition-colors"
            >
              <Download className="w-5 h-5" />
              Download PDF
            </a>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
            <table className="w-full text-left text-sm">
              <thead className="bg-slate-50 border-b border-slate-200 text-slate-600">
                <tr>
                  <th className="p-4 font-medium">Scanner</th>
                  <th className="p-4 font-medium">Severity</th>
                  <th className="p-4 font-medium">Finding Description</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {scan.findings?.map((finding: any, i: number) => (
                  <tr key={i} className="hover:bg-slate-50 transition-colors">
                    <td className="p-4 font-medium text-slate-700 uppercase">
                      {finding.tool}
                    </td>
                    <td className="p-4">
                      <span className={`px-2.5 py-1 rounded-full text-xs font-bold ${
                        finding.severity === 'CRITICAL' ? 'bg-red-100 text-red-700' : 
                        finding.severity === 'HIGH' ? 'bg-orange-100 text-orange-700' : 
                        finding.severity === 'MEDIUM' ? 'bg-yellow-100 text-yellow-700' : 
                        'bg-blue-100 text-blue-700'
                      }`}>
                        {finding.severity}
                      </span>
                    </td>
                    <td className="p-4 text-slate-600">
                      <div className="flex items-start gap-2">
                        {finding.severity === 'CRITICAL' && <AlertTriangle className="w-4 h-4 text-red-500 mt-0.5 shrink-0" />}
                        {finding.message}
                      </div>
                    </td>
                  </tr>
                ))}
                {scan.findings_count === 0 && (
                  <tr>
                    <td colSpan={3} className="p-8 text-center text-slate-500">
                      No vulnerabilities found. Code is secure.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </main>
  );
}