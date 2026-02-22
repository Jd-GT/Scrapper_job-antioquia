"use client";

import { useMemo } from "react";
import { 
  TrendingUp, 
  TrendingDown,
  BarChart3,
  PieChart,
  Activity,
  Users,
  DollarSign,
  Briefcase
} from "lucide-react";
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart as RePieChart,
  Pie,
  Cell,
  LineChart,
  Line
} from "recharts";
import { mockOfertas, getSectorData, getModalidadData, getNivelData, getTopSkills } from "@/lib/mock-data";

const COLORS = ["#14b8a6", "#3b82f6", "#f59e0b", "#8b5cf6", "#ec4899", "#06b6d4", "#10b981", "#f97316"];

const experienciaData = [
  { name: "0-1 años", value: 15 },
  { name: "1-2 años", value: 25 },
  { name: "2-3 años", value: 30 },
  { name: "3-5 años", value: 20 },
  { name: "5+ años", value: 10 },
];

const educacionData = [
  { name: "Bachillerato", value: 5 },
  { name: "Técnico", value: 20 },
  { name: "Tecnólogo", value: 30 },
  { name: "Pregrado", value: 35 },
  { name: "Posgrado", value: 10 },
];

const contratacionData = [
  { mes: "Ene", ofertas: 45 },
  { mes: "Feb", ofertas: 52 },
  { mes: "Mar", ofertas: 48 },
  { mes: "Abr", ofertas: 61 },
  { mes: "May", ofertas: 55 },
  { mes: "Jun", ofertas: 67 },
];

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

export default function AnalisisPage() {
  const sectorData = useMemo(() => getSectorData(mockOfertas), []);
  const modalidadData = useMemo(() => getModalidadData(mockOfertas), []);
  const nivelData = useMemo(() => getNivelData(mockOfertas), []);
  const topSkills = useMemo(() => getTopSkills(mockOfertas, 8), []);

  const stats = useMemo(() => {
    const salarios = mockOfertas
      .filter(o => o.compensacion.salario_min)
      .map(o => o.compensacion.salario_min!);
    
    const avgSalary = salarios.length ? Math.round(salarios.reduce((a, b) => a + b, 0) / salarios.length) : 0;
    const minSalary = salarios.length ? Math.min(...salarios) : 0;
    const maxSalary = salarios.length ? Math.max(...salarios) : 0;

    const remoteCount = mockOfertas.filter(o => o.cargo.modalidad === "Remoto").length;
    const hybridCount = mockOfertas.filter(o => o.cargo.modalidad === "Híbrido").length;
    
    const experienceYears = mockOfertas.map(o => o.requisitos.experiencia_anos);
    const avgExperience = experienceYears.length ? (experienceYears.reduce((a, b) => a + b, 0) / experienceYears.length).toFixed(1) : "0";

    return { avgSalary, minSalary, maxSalary, remoteCount, hybridCount, avgExperience };
  }, []);

  return (
    <div className="space-y-8">
      <header>
        <h1 className="text-3xl font-display font-bold text-slate-100">Análisis Profundo</h1>
        <p className="text-slate-500 mt-1">Insights detallados del mercado laboral en Antioquia</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-slate-900/80 rounded-xl border border-teal-900/40 p-5">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 bg-teal-500/20 rounded-lg flex items-center justify-center">
              <DollarSign className="w-5 h-5 text-teal-400" />
            </div>
            <span className="text-slate-400 text-sm">Rango Salarial</span>
          </div>
          {stats.avgSalary > 0 ? (
            <>
              <p className="text-2xl font-display font-bold text-slate-100">
                ${(stats.minSalary / 1000000).toFixed(1)}M - ${(stats.maxSalary / 1000000).toFixed(1)}M
              </p>
              <p className="text-sm text-teal-400 mt-1">Promedio: ${(stats.avgSalary / 1000000).toFixed(1)}M COP</p>
            </>
          ) : (
            <p className="text-2xl font-display font-bold text-slate-500">No disponible</p>
          )}
        </div>

        <div className="bg-slate-900/80 rounded-xl border border-teal-900/40 p-5">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 bg-blue-500/20 rounded-lg flex items-center justify-center">
              <Activity className="w-5 h-5 text-blue-400" />
            </div>
            <span className="text-slate-400 text-sm">Experiencia Requerida</span>
          </div>
          {parseFloat(stats.avgExperience) > 0 ? (
            <>
              <p className="text-2xl font-display font-bold text-slate-100">{stats.avgExperience} años</p>
              <p className="text-sm text-blue-400 mt-1">Promedio del mercado</p>
            </>
          ) : (
            <p className="text-2xl font-display font-bold text-slate-500">No disponible</p>
          )}
        </div>

        <div className="bg-slate-900/80 rounded-xl border border-teal-900/40 p-5">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 bg-purple-500/20 rounded-lg flex items-center justify-center">
              <Users className="w-5 h-5 text-purple-400" />
            </div>
            <span className="text-slate-400 text-sm">Modalidad</span>
          </div>
          <p className="text-2xl font-display font-bold text-slate-100">
            {stats.remoteCount + stats.hybridCount}/{mockOfertas.length}
          </p>
          <p className="text-sm text-purple-400 mt-1">Remoto o Híbrido</p>
        </div>

        <div className="bg-slate-900/80 rounded-xl border border-teal-900/40 p-5">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 bg-amber-500/20 rounded-lg flex items-center justify-center">
              <Briefcase className="w-5 h-5 text-amber-400" />
            </div>
            <span className="text-slate-400 text-sm">Sectores Activos</span>
          </div>
          <p className="text-2xl font-display font-bold text-slate-100">{sectorData.length}</p>
          <p className="text-sm text-amber-400 mt-1">Industrias diferentes</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="chart-container">
            <h3 className="text-lg font-display font-semibold mb-6 text-slate-100">Tendencia de Contratación (2025-2026)</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={contratacionData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(20, 184, 166, 0.1)" />
                <XAxis dataKey="mes" stroke="#78716c" fontSize={12} />
                <YAxis stroke="#78716c" fontSize={12} />
                <Tooltip content={<CustomTooltip />} />
                <Line 
                  type="monotone" 
                  dataKey="ofertas" 
                  stroke="#14b8a6" 
                  strokeWidth={3}
                  dot={{ fill: "#14b8a6", strokeWidth: 2, r: 4 }}
                  activeDot={{ r: 6, fill: "#2dd4bf" }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="chart-container">
          <h3 className="text-lg font-display font-semibold mb-6 text-slate-100">Por Nivel de Experiencia</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={experienciaData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(20, 184, 166, 0.1)" />
              <XAxis type="number" stroke="#78716c" fontSize={12} />
              <YAxis dataKey="name" type="category" width={80} stroke="#78716c" fontSize={11} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="value" fill="#3b82f6" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-container">
          <h3 className="text-lg font-display font-semibold mb-6 text-slate-100">Educación Mínima</h3>
          <ResponsiveContainer width="100%" height={250}>
            <RePieChart>
              <Pie
                data={educacionData}
                cx="50%"
                cy="50%"
                innerRadius={50}
                outerRadius={90}
                paddingAngle={3}
                dataKey="value"
              >
                {educacionData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
            </RePieChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-container">
          <h3 className="text-lg font-display font-semibold mb-6 text-slate-100">Distribución por Sector</h3>
          <ResponsiveContainer width="100%" height={250}>
            <RePieChart>
              <Pie
                data={sectorData.slice(0, 5)}
                cx="50%"
                cy="50%"
                outerRadius={90}
                dataKey="value"
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                labelLine={{ stroke: "#78716c" }}
              >
                {sectorData.slice(0, 5).map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
            </RePieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="chart-container">
        <h3 className="text-lg font-display font-semibold mb-6 text-slate-100">Comparativa: Platforms</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={nivelData}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(20, 184, 166, 0.1)" />
            <XAxis dataKey="name" stroke="#78716c" fontSize={12} />
            <YAxis stroke="#78716c" fontSize={12} />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="value" fill="#8b5cf6" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
