"use client";

import { useMemo } from "react";
import { 
  Briefcase, 
  Building2, 
  Globe2, 
  Code2, 
  TrendingUp,
  TrendingDown,
  Sparkles
} from "lucide-react";
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend
} from "recharts";
import { mockOfertas, getKPIs, getModalidadData, getNivelData, getTopSkills, getUbicacionData } from "@/lib/mock-data";

const COLORS = ["#14b8a6", "#3b82f6", "#f59e0b", "#8b5cf6", "#ec4899", "#06b6d4"];

const platformLogos: Record<string, string> = {
  LinkedIn: "https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/linkedin.svg",
  Computrabajo: "https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/indeed.svg",
  Indeed: "https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/indeed.svg",
  Magneto365: "https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/magnetodots.svg",
  Elempleo: "https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/briefcase.svg",
  MasEmpleo: "https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/briefcase.svg",
};

function formatCOP(value: number): string {
  return new Intl.NumberFormat("es-CO", {
    style: "currency",
    currency: "COP",
    maximumFractionDigits: 0,
  }).format(value);
}

function KpiCard({ 
  title, 
  value, 
  trend, 
  icon: Icon,
  format = "number",
  delay = 0
}: { 
  title: string; 
  value: number; 
  trend: number; 
  icon: any;
  format?: "number" | "currency" | "percent";
  delay?: number;
}) {
  const formattedValue = format === "currency" 
    ? formatCOP(value)
    : format === "percent"
    ? `${value}%`
    : value.toLocaleString("es-CO");

  return (
    <div 
      className="kpi-card group animate-slide-up" 
      style={{ animationDelay: `${delay}s`, opacity: 0 }}
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-slate-500 font-medium">{title}</p>
          <p className="text-2xl font-bold mt-2 font-display text-slate-100">{formattedValue}</p>
        </div>
        <div className="w-12 h-12 bg-slate-800 rounded-xl flex items-center justify-center border border-teal-900/40 group-hover:border-teal-500/50 transition-colors">
          <Icon className="w-6 h-6 text-teal-400" />
        </div>
      </div>
      <div className="flex items-center gap-1.5 mt-4">
        {trend >= 0 ? (
          <TrendingUp className="w-4 h-4 text-teal-400" />
        ) : (
          <TrendingDown className="w-4 h-4 text-rose-500" />
        )}
        <span className={trend >= 0 ? "text-teal-400" : "text-rose-500"}>
          {trend > 0 ? "+" : ""}{trend}%
        </span>
        <span className="text-slate-500 text-sm">vs semana anterior</span>
      </div>
    </div>
  );
}

function CustomTooltip({ active, payload, label }: any) {
  if (active && payload && payload.length) {
    return (
      <div className="bg-slate-900 border border-teal-900/50 rounded-xl p-3 shadow-lg">
        <p className="text-slate-200 font-medium">{label}</p>
        <p className="text-teal-400 text-sm">
          {payload[0].name}: <span className="font-mono">{payload[0].value}</span>
        </p>
      </div>
    );
  }
  return null;
}

export default function Home() {
  const kpis = useMemo(() => getKPIs(mockOfertas), []);
  const ubicacionData = useMemo(() => getUbicacionData(mockOfertas), []);
  const modalidadData = useMemo(() => getModalidadData(mockOfertas), []);
  const nivelData = useMemo(() => getNivelData(mockOfertas), []);
  const topSkills = useMemo(() => getTopSkills(mockOfertas, 8), []);

  return (
    <div className="space-y-8">
      <header className="animate-fade-in">
        <div className="flex-shrink-0">
          <div className="flex items-center gap-3">
            <h1 className="text-3xl font-display font-bold text-slate-100">Mercado Laboral Antioquia</h1>
            <span className="px-2 py-1 bg-teal-500/20 text-teal-300 text-xs rounded-full flex items-center gap-1">
              <Sparkles className="w-3 h-3" />
              Live
            </span>
          </div>
          <p className="text-slate-500 mt-1">Datos actualizados: 22 Feb 2026</p>
        </div>
      </header>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <KpiCard
          title="Total Ofertas"
          value={kpis.totalOfertas}
          trend={kpis.tendenciaOfertas}
          icon={Briefcase}
          delay={0.1}
        />
        <KpiCard
          title="Ofertas Remotas"
          value={Math.round((kpis.ofertasRemotas / kpis.totalOfertas) * 100)}
          trend={kpis.tendenciaRemotas}
          icon={Globe2}
          format="percent"
          delay={0.15}
        />
        <KpiCard
          title="Ofertas Presenciales"
          value={kpis.totalOfertas - kpis.ofertasRemotas}
          trend={-5}
          icon={Building2}
          delay={0.2}
        />
        <KpiCard
          title="Ofertas Híbridas"
          value={Math.round((kpis.totalOfertas - kpis.ofertasRemotas) * 0.3)}
          trend={10}
          icon={Code2}
          delay={0.25}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="chart-container animate-slide-up" style={{ animationDelay: "0.4s", opacity: 0 }}>
          <h3 className="text-lg font-display font-semibold mb-6 text-slate-100">Ofertas por Ciudad</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={ubicacionData} layout="vertical" margin={{ left: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(20, 184, 166, 0.1)" />
              <XAxis type="number" stroke="#78716c" fontSize={12} />
              <YAxis dataKey="name" type="category" width={100} stroke="#78716c" fontSize={12} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="value" fill="#14b8a6" radius={[0, 6, 6, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-container animate-slide-up" style={{ animationDelay: "0.45s", opacity: 0 }}>
          <h3 className="text-lg font-display font-semibold mb-6 text-slate-100">Modalidad de Trabajo</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={modalidadData}
                cx="50%"
                cy="50%"
                innerRadius={70}
                outerRadius={110}
                paddingAngle={4}
                dataKey="value"
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                labelLine={{ stroke: "#78716c" }}
              >
                {modalidadData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
              <Legend wrapperStyle={{ color: "#d6d3d1" }} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="chart-container animate-slide-up" style={{ animationDelay: "0.5s", opacity: 0 }}>
          <h3 className="text-lg font-display font-semibold mb-6 text-slate-100">Distribución por Nivel</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={nivelData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(20, 184, 166, 0.1)" />
              <XAxis dataKey="name" stroke="#78716c" fontSize={12} />
              <YAxis stroke="#78716c" fontSize={12} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="value" fill="#3b82f6" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-container animate-slide-up" style={{ animationDelay: "0.55s", opacity: 0 }}>
          <h3 className="text-lg font-display font-semibold mb-6 text-slate-100">Skills Más Demandados</h3>
          <div className="flex flex-wrap gap-2">
            {topSkills.map((skill, index) => (
              <div 
                key={skill.skill} 
                className="group px-4 py-3 bg-slate-800/80 rounded-xl border border-teal-900/40 hover:border-teal-500/50 transition-all cursor-default"
                style={{ animationDelay: `${0.6 + index * 0.05}s` }}
              >
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-teal-400 font-bold text-lg">{index + 1}</span>
                  <span className="text-slate-200 font-medium group-hover:text-teal-300 transition-colors">{skill.skill}</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="flex-1 h-1.5 bg-slate-700 rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-gradient-to-r from-teal-500 to-teal-400 rounded-full"
                      style={{ width: `${(skill.count / topSkills[0].count) * 100}%` }}
                    />
                  </div>
                  <span className="text-teal-400 text-sm font-mono whitespace-nowrap">{skill.count}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="chart-container animate-slide-up" style={{ animationDelay: "0.6s", opacity: 0 }}>
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-display font-semibold text-slate-100">Últimas Ofertas ({mockOfertas.length})</h3>
          <button className="text-teal-400 hover:text-teal-300 text-sm font-medium transition-colors">
            Ver todas →
          </button>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-teal-900/40">
                <th className="text-left py-3 px-4 font-semibold text-slate-400">Cargo</th>
                <th className="text-left py-3 px-4 font-semibold text-slate-400">Empresa</th>
                <th className="text-left py-3 px-4 font-semibold text-slate-400">Ubicación</th>
                <th className="text-left py-3 px-4 font-semibold text-slate-400">Salario</th>
                <th className="text-left py-3 px-4 font-semibold text-slate-400">Modalidad</th>
                <th className="text-left py-3 px-4 font-semibold text-slate-400">Plataforma</th>
              </tr>
            </thead>
            <tbody>
              {mockOfertas.slice(0, 5).map((oferta, idx) => (
                <tr key={oferta.id} className="table-row-hover" style={{ animationDelay: `${0.65 + idx * 0.05}s` }}>
                  <td className="py-4 px-4">
                    <div>
                      <p className="font-medium text-slate-100">{oferta.cargo.titulo}</p>
                      <p className="text-sm text-slate-500">{oferta.cargo.nivel}</p>
                    </div>
                  </td>
                  <td className="py-4 px-4">
                    <div className="flex items-center gap-2">
                      <span className="font-medium text-slate-200">{oferta.empresa.nombre}</span>
                      {oferta.empresa.verificada && (
                        <span className="w-2 h-2 bg-teal-400 rounded-full shadow-lg" title="Verificada" />
                      )}
                    </div>
                  </td>
                  <td className="py-4 px-4 text-slate-400">{oferta.empresa.ubicacion}</td>
                  <td className="py-4 px-4 font-mono text-teal-400">
                    {oferta.compensacion.salario_min 
                      ? `${formatCOP(oferta.compensacion.salario_min)} - ${formatCOP(oferta.compensacion.salario_max || oferta.compensacion.salario_min)}`
                      : "No especificado"
                    }
                  </td>
                  <td className="py-4 px-4">
                    <span className={`px-3 py-1.5 rounded-lg text-xs font-medium
                      ${oferta.cargo.modalidad === "Remoto" ? "modalidad-remoto" : 
                        oferta.cargo.modalidad === "Híbrido" ? "modalidad-hibrido" : "modalidad-presencial"
                      }`}
                    >
                      {oferta.cargo.modalidad}
                    </span>
                  </td>
                  <td className="py-4 px-4">
                    <div className="flex items-center gap-2">
                      <span className="px-2 py-1 bg-slate-800 rounded text-xs font-medium text-slate-300">
                        {oferta.plataforma_origen}
                      </span>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
