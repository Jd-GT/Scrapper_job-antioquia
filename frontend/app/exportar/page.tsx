"use client";

import { useState } from "react";
import { 
  Download, 
  FileJson, 
  FileSpreadsheet, 
  FileText,
  Copy,
  Check,
  RefreshCw
} from "lucide-react";
import { mockOfertas } from "@/lib/mock-data";

type ExportFormat = "json" | "csv" | "xlsx";

export default function ExportarPage() {
  const [format, setFormat] = useState<ExportFormat>("json");
  const [copied, setCopied] = useState(false);
  const [exporting, setExporting] = useState(false);

  const formatData = () => {
    if (format === "json") {
      return JSON.stringify(mockOfertas, null, 2);
    }
    
    if (format === "csv") {
      const headers = [
        "id", "plataforma", "empresa", "sector", "ubicacion", 
        "cargo", "nivel", "modalidad", "salario_min", "salario_max",
        "experiencia", "educacion", "skills"
      ];
      
      const rows = mockOfertas.map(o => [
        o.id,
        o.plataforma_origen,
        o.empresa.nombre,
        o.empresa.sector,
        o.empresa.ubicacion,
        o.cargo.titulo,
        o.cargo.nivel,
        o.cargo.modalidad,
        o.compensacion.salario_min || "",
        o.compensacion.salario_max || "",
        o.requisitos.experiencia_anos,
        o.requisitos.educacion_minima,
        o.requisitos.habilidades_tecnicas.join("; ")
      ]);
      
      return [headers.join(","), ...rows.map(r => r.map(c => `"${c}"`).join(","))].join("\n");
    }
    
    return "";
  };

  const handleExport = async () => {
    setExporting(true);
    
    const data = formatData();
    const mimeTypes: Record<ExportFormat, string> = {
      json: "application/json",
      csv: "text/csv",
      xlsx: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    };
    
    const extensions: Record<ExportFormat, string> = {
      json: "json",
      csv: "csv",
      xlsx: "xlsx"
    };
    
    const blob = new Blob([data], { type: mimeTypes[format] });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `empleos-antioquia-${new Date().toISOString().split("T")[0]}.${extensions[format]}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    setTimeout(() => setExporting(false), 1000);
  };

  const handleCopy = () => {
    const data = formatData();
    navigator.clipboard.writeText(data);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const stats = {
    total: mockOfertas.length,
    remote: mockOfertas.filter(o => o.cargo.modalidad === "Remoto").length,
    hybrid: mockOfertas.filter(o => o.cargo.modalidad === "Híbrido").length,
    presencial: mockOfertas.filter(o => o.cargo.modalidad === "Presencial").length,
    conSalario: mockOfertas.filter(o => o.compensacion.salario_min).length,
    verificadas: mockOfertas.filter(o => o.empresa.verificada).length,
  };

  return (
    <div className="space-y-8">
      <header>
        <h1 className="text-3xl font-display font-bold text-slate-100">Exportar Datos</h1>
        <p className="text-slate-500 mt-1">Descarga los datos de ofertas de empleo en múltiples formatos</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="chart-container">
          <h3 className="text-lg font-display font-semibold mb-6 text-slate-100">Resumen de Datos</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-slate-800/50 rounded-xl">
              <span className="text-slate-400">Total de ofertas</span>
              <span className="text-2xl font-display font-bold text-teal-400">{stats.total}</span>
            </div>
            <div className="flex items-center justify-between p-4 bg-slate-800/50 rounded-xl">
              <span className="text-slate-400">Ofertas remotas</span>
              <span className="text-xl font-semibold text-purple-400">{stats.remote}</span>
            </div>
            <div className="flex items-center justify-between p-4 bg-slate-800/50 rounded-xl">
              <span className="text-slate-400">Ofertas híbridas</span>
              <span className="text-xl font-semibold text-amber-400">{stats.hybrid}</span>
            </div>
            <div className="flex items-center justify-between p-4 bg-slate-800/50 rounded-xl">
              <span className="text-slate-400">Presenciales</span>
              <span className="text-xl font-semibold text-blue-400">{stats.presencial}</span>
            </div>
            <div className="flex items-center justify-between p-4 bg-slate-800/50 rounded-xl">
              <span className="text-slate-400">Con salario publicado</span>
              <span className="text-xl font-semibold text-teal-400">{stats.conSalario}</span>
            </div>
            <div className="flex items-center justify-between p-4 bg-slate-800/50 rounded-xl">
              <span className="text-slate-400">Empresas verificadas</span>
              <span className="text-xl font-semibold text-emerald-400">{stats.verificadas}</span>
            </div>
          </div>
        </div>

        <div className="chart-container">
          <h3 className="text-lg font-display font-semibold mb-6 text-slate-100">Seleccionar Formato</h3>
          <div className="space-y-4">
            <button
              onClick={() => setFormat("json")}
              className={`w-full flex items-center gap-4 p-4 rounded-xl border transition-all ${
                format === "json" 
                  ? "bg-teal-500/20 border-teal-500/50" 
                  : "bg-slate-800/50 border-teal-900/40 hover:border-teal-500/30"
              }`}
            >
              <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${
                format === "json" ? "bg-teal-600" : "bg-slate-700"
              }`}>
                <FileJson className="w-6 h-6 text-white" />
              </div>
              <div className="text-left">
                <p className="font-medium text-slate-100">JSON</p>
                <p className="text-sm text-slate-400">Formato estructurado ideal para APIs</p>
              </div>
            </button>

            <button
              onClick={() => setFormat("csv")}
              className={`w-full flex items-center gap-4 p-4 rounded-xl border transition-all ${
                format === "csv" 
                  ? "bg-teal-500/20 border-teal-500/50" 
                  : "bg-slate-800/50 border-teal-900/40 hover:border-teal-500/30"
              }`}
            >
              <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${
                format === "csv" ? "bg-teal-600" : "bg-slate-700"
              }`}>
                <FileSpreadsheet className="w-6 h-6 text-white" />
              </div>
              <div className="text-left">
                <p className="font-medium text-slate-100">CSV</p>
                <p className="text-sm text-slate-400">Compatible con Excel y hojas de cálculo</p>
              </div>
            </button>

            <button
              onClick={() => setFormat("xlsx")}
              className={`w-full flex items-center gap-4 p-4 rounded-xl border transition-all ${
                format === "xlsx" 
                  ? "bg-teal-500/20 border-teal-500/50" 
                  : "bg-slate-800/50 border-teal-900/40 hover:border-teal-500/30"
              }`}
            >
              <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${
                format === "xlsx" ? "bg-teal-600" : "bg-slate-700"
              }`}>
                <FileText className="w-6 h-6 text-white" />
              </div>
              <div className="text-left">
                <p className="font-medium text-slate-100">Excel (XLSX)</p>
                <p className="text-sm text-slate-400">Formato de Microsoft Excel</p>
              </div>
            </button>
          </div>

          <div className="flex gap-3 mt-6">
            <button
              onClick={handleExport}
              disabled={exporting}
              className="flex-1 flex items-center justify-center gap-2 px-5 py-3 bg-teal-600 hover:bg-teal-500 text-white rounded-xl font-medium transition-all disabled:opacity-50"
            >
              {exporting ? (
                <RefreshCw className="w-5 h-5 animate-spin" />
              ) : (
                <Download className="w-5 h-5" />
              )}
              {exporting ? "Exportando..." : "Descargar"}
            </button>
            <button
              onClick={handleCopy}
              className="flex items-center justify-center gap-2 px-5 py-3 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl font-medium transition-all border border-teal-900/40"
            >
              {copied ? (
                <Check className="w-5 h-5 text-teal-400" />
              ) : (
                <Copy className="w-5 h-5" />
              )}
              {copied ? "Copiado!" : "Copiar"}
            </button>
          </div>
        </div>
      </div>

      <div className="chart-container">
        <h3 className="text-lg font-display font-semibold mb-4 text-slate-100">Vista Previa</h3>
        <pre className="bg-slate-950 rounded-xl p-4 text-sm text-slate-300 overflow-x-auto max-h-96 font-mono">
          {formatData().slice(0, 2000)}
          {formatData().length > 2000 && "\n\n... (truncado para vista previa)"}
        </pre>
      </div>
    </div>
  );
}
