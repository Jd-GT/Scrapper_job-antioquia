"use client";

import { useState, useMemo } from "react";
import { 
  Search, 
  Filter, 
  MapPin, 
  DollarSign, 
  Building2, 
  Clock,
  ExternalLink,
  ChevronDown,
  X
} from "lucide-react";
import { mockOfertas } from "@/lib/mock-data";
import { OfertaLaboral } from "@/types";

const plataformas = ["Computrabajo"];
const modalidades = ["Presencial", "Remoto", "Híbrido"];
const niveles = ["Junior", "Semi-senior", "Senior"];
const ubicaciones = ["Medellín", "Envigado", "Itagüí", "Bello", "Rionegro"];

const platformColors: Record<string, string> = {
  LinkedIn: "bg-blue-600",
  Computrabajo: "bg-green-600",
  Indeed: "bg-indigo-600",
  Magneto365: "bg-purple-600",
  Elempleo: "bg-orange-600",
  MasEmpleo: "bg-pink-600",
};

function formatCOP(value: number): string {
  return new Intl.NumberFormat("es-CO", {
    style: "currency",
    currency: "COP",
    maximumFractionDigits: 0,
  }).format(value);
}

function OfertaCard({ oferta }: { oferta: OfertaLaboral }) {
  return (
    <div className="bg-slate-900/80 rounded-xl border border-teal-900/40 p-5 hover:border-teal-500/50 transition-all group">
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <h3 className="font-display font-semibold text-lg text-slate-100 truncate">
              {oferta.cargo.titulo}
            </h3>
            {oferta.empresa.verificada && (
              <span className="w-2 h-2 bg-teal-400 rounded-full flex-shrink-0" title="Empresa verificada" />
            )}
          </div>
          <p className="text-teal-400 font-medium mt-1">{oferta.empresa.nombre}</p>
          
          <div className="flex flex-wrap items-center gap-4 mt-3 text-sm text-slate-400">
            <span className="flex items-center gap-1">
              <MapPin className="w-4 h-4" />
              {oferta.empresa.ubicacion}
            </span>
            <span className="flex items-center gap-1">
              <Building2 className="w-4 h-4" />
              {oferta.empresa.sector}
            </span>
            <span className="flex items-center gap-1">
              <Clock className="w-4 h-4" />
              {oferta.cargo.nivel}
            </span>
            {oferta.requisitos.experiencia_anos > 0 && (
              <span className="text-amber-400 text-xs">
                {oferta.requisitos.experiencia_anos} {oferta.requisitos.experiencia_anos === 1 ? 'año' : 'años'} exp.
              </span>
            )}
          </div>

          <div className="flex flex-wrap gap-2 mt-4">
            <span className={`px-2 py-1 rounded-lg text-xs font-medium
              ${oferta.cargo.modalidad === "Remoto" ? "modalidad-remoto" : 
                oferta.cargo.modalidad === "Híbrido" ? "modalidad-hibrido" : "modalidad-presencial"
              }`}
            >
              {oferta.cargo.modalidad}
            </span>
            <span className="px-2 py-1 rounded-lg text-xs font-medium bg-slate-800 text-slate-300 border border-teal-900/40">
              {oferta.cargo.tipo_contrato}
            </span>
            <span className="px-2 py-1 rounded-lg text-xs font-medium bg-slate-800 text-slate-300 border border-teal-900/40">
              {oferta.cargo.jornada}
            </span>
          </div>

          <div className="flex flex-wrap gap-2 mt-3">
            {oferta.requisitos.habilidades_tecnicas.slice(0, 4).map((skill) => (
              <span key={skill} className="skill-badge text-xs">
                {skill}
              </span>
            ))}
            {oferta.requisitos.habilidades_tecnicas.length > 4 && (
              <span className="text-xs text-slate-500">+{oferta.requisitos.habilidades_tecnicas.length - 4} más</span>
            )}
          </div>
        </div>

        <div className="flex flex-col items-end gap-3">
          <span className="font-mono text-lg text-teal-400 font-semibold">
            {oferta.compensacion.salario_min 
              ? `${formatCOP(oferta.compensacion.salario_min)} - ${formatCOP(oferta.compensacion.salario_max || oferta.compensacion.salario_min)}`
              : "No especificado"
            }
          </span>
          <span className={`px-2 py-1 ${platformColors[oferta.plataforma_origen] || "bg-slate-600"} text-white rounded text-xs font-medium`}>
            {oferta.plataforma_origen}
          </span>
          <a 
            href={oferta.metadata.url} 
            target="_blank" 
            rel="noopener noreferrer"
            className="flex items-center gap-1 px-3 py-1.5 bg-teal-600 hover:bg-teal-500 text-white rounded-lg text-sm font-medium transition-colors"
          >
            Ver oferta <ExternalLink className="w-3 h-3" />
          </a>
        </div>
      </div>
    </div>
  );
}

export default function OfertasPage() {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedUbicaciones, setSelectedUbicaciones] = useState<string[]>([]);
  const [selectedModalidades, setSelectedModalidades] = useState<string[]>([]);
  const [selectedNiveles, setSelectedNiveles] = useState<string[]>([]);
  const [showFilters, setShowFilters] = useState(false);

  const filteredOfertas = useMemo(() => {
    return mockOfertas.filter((oferta) => {
      if (searchTerm) {
        const term = searchTerm.toLowerCase();
        const matchesSearch = 
          oferta.cargo.titulo.toLowerCase().includes(term) ||
          oferta.empresa.nombre.toLowerCase().includes(term) ||
          oferta.requisitos.habilidades_tecnicas.some(s => s.toLowerCase().includes(term));
        if (!matchesSearch) return false;
      }
      if (selectedUbicaciones.length && !selectedUbicaciones.includes(oferta.empresa.ubicacion)) {
        return false;
      }
      if (selectedModalidades.length && !selectedModalidades.includes(oferta.cargo.modalidad)) {
        return false;
      }
      if (selectedNiveles.length && !selectedNiveles.includes(oferta.cargo.nivel)) {
        return false;
      }
      return true;
    });
  }, [searchTerm, selectedUbicaciones, selectedModalidades, selectedNiveles]);

  const toggleFilter = <T extends string>(item: T, selected: T[], setSelected: (v: T[]) => void) => {
    if (selected.includes(item)) {
      setSelected(selected.filter(i => i !== item));
    } else {
      setSelected([...selected, item]);
    }
  };

  const clearFilters = () => {
    setSelectedUbicaciones([]);
    setSelectedModalidades([]);
    setSelectedNiveles([]);
    setSearchTerm("");
  };

  const hasActiveFilters = selectedUbicaciones.length || selectedModalidades.length || selectedNiveles.length || searchTerm;

  return (
    <div className="space-y-6">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-display font-bold text-slate-100">Ofertas de Empleo</h1>
          <p className="text-slate-500 mt-1">{filteredOfertas.length} vacantes encontradas</p>
        </div>
      </header>

      <div className="flex items-center gap-4">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
          <input
            type="text"
            placeholder="Buscar por cargo, empresa o skill..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="input-glow w-full pl-10"
          />
        </div>
        
        <button 
          onClick={() => setShowFilters(!showFilters)}
          className={`flex items-center gap-2 px-5 py-2.5 rounded-xl font-medium transition-all ${
            showFilters || hasActiveFilters 
              ? "bg-teal-600 text-white" 
              : "bg-slate-800 text-slate-300 border border-teal-900/40 hover:border-teal-500/50"
          }`}
        >
          <Filter className="w-4 h-4" />
          Filtros
          {hasActiveFilters && (
            <span className="ml-1 px-1.5 py-0.5 bg-white/20 rounded text-xs">
              {selectedUbicaciones.length + selectedModalidades.length + selectedNiveles.length}
            </span>
          )}
        </button>

        {hasActiveFilters && (
          <button 
            onClick={clearFilters}
            className="flex items-center gap-1 px-3 py-2 text-slate-400 hover:text-teal-400 transition-colors"
          >
            <X className="w-4 h-4" />
            Limpiar
          </button>
        )}
      </div>

      {showFilters && (
        <div className="bg-slate-900/80 rounded-xl border border-teal-900/40 p-5 animate-slide-up">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <h4 className="text-sm font-medium text-slate-300 mb-3">Ubicación</h4>
              <div className="flex flex-wrap gap-2">
                {ubicaciones.map((u) => (
                  <button
                    key={u}
                    onClick={() => toggleFilter(u, selectedUbicaciones, setSelectedUbicaciones)}
                    className={`px-3 py-1.5 rounded-lg text-sm transition-all ${
                      selectedUbicaciones.includes(u)
                        ? "bg-teal-600 text-white"
                        : "bg-slate-800 text-slate-400 hover:text-slate-200 border border-teal-900/40"
                    }`}
                  >
                    {u}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <h4 className="text-sm font-medium text-slate-300 mb-3">Modalidad</h4>
              <div className="flex flex-wrap gap-2">
                {modalidades.map((m) => (
                  <button
                    key={m}
                    onClick={() => toggleFilter(m, selectedModalidades, setSelectedModalidades)}
                    className={`px-3 py-1.5 rounded-lg text-sm transition-all ${
                      selectedModalidades.includes(m)
                        ? "bg-teal-600 text-white"
                        : "bg-slate-800 text-slate-400 hover:text-slate-200 border border-teal-900/40"
                    }`}
                  >
                    {m}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <h4 className="text-sm font-medium text-slate-300 mb-3">Nivel</h4>
              <div className="flex flex-wrap gap-2">
                {niveles.map((n) => (
                  <button
                    key={n}
                    onClick={() => toggleFilter(n, selectedNiveles, setSelectedNiveles)}
                    className={`px-3 py-1.5 rounded-lg text-sm transition-all ${
                      selectedNiveles.includes(n)
                        ? "bg-teal-600 text-white"
                        : "bg-slate-800 text-slate-400 hover:text-slate-200 border border-teal-900/40"
                    }`}
                  >
                    {n}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="space-y-4">
        {filteredOfertas.map((oferta) => (
          <OfertaCard key={oferta.id} oferta={oferta} />
        ))}
        
        {filteredOfertas.length === 0 && (
          <div className="text-center py-12">
            <p className="text-slate-400 text-lg">No se encontraron ofertas con los filtros seleccionados</p>
            <button 
              onClick={clearFilters}
              className="mt-4 text-teal-400 hover:text-teal-300"
            >
              Limpiar filtros
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
