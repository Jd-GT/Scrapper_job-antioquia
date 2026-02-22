export type PlataformaOrigen = 'LinkedIn' | 'Computrabajo' | 'Indeed' | 'Magneto365' | 'Elempleo' | 'MasEmpleo';

export type Modalidad = 'Presencial' | 'Remoto' | 'Híbrido';

export type NivelCargo = 'Junior' | 'Semi-senior' | 'Senior' | 'Gerente' | 'Director' | 'VP' | 'C-Level' | 'Analista' | 'Asistente' | 'Coordinador' | 'Supervisor' | 'Jefe' | 'Vicepresidente' | 'No especificado';

export type TamanoEmpresa = 'Microempresa' | 'Pequeña' | 'Mediana' | 'Gran empresa';

export type TipoContrato = 'Indefinido' | 'Término fijo' | 'Prestacion de servicios' | 'Obra labor' | 'Temporal' | 'Contrato por proyecto' | 'No especificado';

export type Jornada = 'Tiempo completo' | 'Medio tiempo' | 'Freelance' | 'Por horas';

export type EducacionMinima = 'Bachillerato' | 'Técnico' | 'Tecnólogo' | 'Pregrado' | 'Posgrado' | 'Doctorado' | 'No especificado';

export type EstadoOferta = 'Activa' | 'Cerrada' | 'Pausada';

export interface Empresa {
  nombre: string;
  sector: string;
  tamaño: TamanoEmpresa;
  ubicacion: string;
  verificada: boolean;
}

export interface Cargo {
  titulo: string;
  nivel: NivelCargo;
  area: string;
  modalidad: Modalidad;
  tipo_contrato: TipoContrato;
  jornada: Jornada;
}

export interface Compensacion {
  salario_min: number | null;
  salario_max: number | null;
  moneda: string;
  beneficios: string[];
}

export interface Requisitos {
  experiencia_anos: number;
  educacion_minima: EducacionMinima;
  habilidades_tecnicas: string[];
  habilidades_blandas: string[];
  idiomas: { idioma: string; nivel: string }[];
}

export interface Metadata {
  fecha_publicacion: string;
  fecha_scraping: string;
  url: string;
  estado: EstadoOferta;
}

export interface OfertaLaboral {
  id: string;
  plataforma_origen: PlataformaOrigen;
  empresa: Empresa;
  cargo: Cargo;
  compensacion: Compensacion;
  requisitos: Requisitos;
  metadata: Metadata;
}

export interface FilterState {
  plataformas: PlataformaOrigen[];
  sectores: string[];
  areas: string[];
  niveles: NivelCargo[];
  modalidad: Modalidad[];
  rangoSalarial: [number, number];
  experienciaMax: number;
  skillsRequeridas: string[];
  fechaDesde: string | null;
  fechaHasta: string | null;
  busquedaTexto: string;
  soloVerificadas: boolean;
  soloConSalario: boolean;
}

export interface KpiData {
  totalOfertas: number;
  tendenciaOfertas: number;
  salarioMediano: number;
  tendenciaSalario: number;
  empresasContratando: number;
  tendenciaEmpresas: number;
  ofertasRemotas: number;
  tendenciaRemotas: number;
  skillMasDemandada: string;
  tendenciaSkill: number;
  sectorLider: string;
  tendenciaSector: number;
}
