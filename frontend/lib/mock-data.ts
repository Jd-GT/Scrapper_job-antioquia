import type { OfertaLaboral } from '@/types';
import realData from './real-data.json';

export const mockOfertas: OfertaLaboral[] = realData as unknown as OfertaLaboral[];

export interface KPIData {
  totalOfertas: number;
  tendenciaOfertas: number;
  salarioMediano: number;
  tendenciaSalario: number;
  empresasContratando: number;
  tendenciaEmpresas: number;
  ofertasRemotas: number;
  tendenciaRemotas: number;
  tendenciaSkill: number;
  tendenciaSector: number;
}

export interface ChartData {
  name: string;
  value: number;
}

export interface SkillData {
  skill: string;
  count: number;
}

export function getKPIs(ofertas: OfertaLaboral[]): KPIData {
  const uniqueEmpresas = new Set(ofertas.map(o => o.empresa.nombre));
  const ofertasRemotas = ofertas.filter(o => o.cargo.modalidad === "Remoto").length;
  
  const salarios = ofertas
    .filter(o => o.compensacion.salario_min)
    .map(o => o.compensacion.salario_min!);
  
  const salarioMediano = salarios.length 
    ? salarios.sort((a, b) => a - b)[Math.floor(salarios.length / 2)]
    : 5000000;

  return {
    totalOfertas: ofertas.length,
    tendenciaOfertas: 5.2,
    salarioMediano,
    tendenciaSalario: 3.1,
    empresasContratando: uniqueEmpresas.size,
    tendenciaEmpresas: 8.4,
    ofertasRemotas,
    tendenciaRemotas: 12.3,
    tendenciaSkill: 15.2,
    tendenciaSector: 4.8
  };
}

export function getSectorData(ofertas: OfertaLaboral[]): ChartData[] {
  const sectores: Record<string, number> = {};
  ofertas.forEach(oferta => {
    const sector = oferta.empresa.sector || "Otro";
    sectores[sector] = (sectores[sector] || 0) + 1;
  });
  
  return Object.entries(sectores)
    .map(([name, value]) => ({ name, value }))
    .sort((a, b) => b.value - a.value);
}

export function getUbicacionData(ofertas: OfertaLaboral[]): ChartData[] {
  const ubicaciones: Record<string, number> = {};
  ofertas.forEach(oferta => {
    const ciudad = oferta.empresa.ubicacion || "Otro";
    ubicaciones[ciudad] = (ubicaciones[ciudad] || 0) + 1;
  });
  
  return Object.entries(ubicaciones)
    .map(([name, value]) => ({ name, value }))
    .sort((a, b) => b.value - a.value);
}

export function getModalidadData(ofertas: OfertaLaboral[]): ChartData[] {
  const modalidades: Record<string, number> = {};
  ofertas.forEach(oferta => {
    const modalidad = oferta.cargo.modalidad || "Otro";
    modalidades[modalidad] = (modalidades[modalidad] || 0) + 1;
  });
  
  return Object.entries(modalidades)
    .map(([name, value]) => ({ name, value }))
    .sort((a, b) => b.value - a.value);
}

export function getNivelData(ofertas: OfertaLaboral[]): ChartData[] {
  const niveles: Record<string, number> = {};
  ofertas.forEach(oferta => {
    const nivel = oferta.cargo.nivel || "Otro";
    niveles[nivel] = (niveles[nivel] || 0) + 1;
  });
  
  return Object.entries(niveles)
    .map(([name, value]) => ({ name, value }))
    .sort((a, b) => b.value - a.value);
}

export function getTopSkills(ofertas: OfertaLaboral[], limit: number = 10): SkillData[] {
  const skills: Record<string, number> = {};
  
  ofertas.forEach(oferta => {
    oferta.requisitos.habilidades_tecnicas.forEach(skill => {
      skills[skill] = (skills[skill] || 0) + 1;
    });
  });
  
  return Object.entries(skills)
    .map(([skill, count]) => ({ skill, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, limit);
}

interface ScrapedJob {
  title: string;
  company: string;
  location: string;
  salary_raw: string;
  url: string;
  source: string;
  date_posted: string | null;
}

export function transformScrapedData(scrapedJobs: ScrapedJob[]): OfertaLaboral[] {
  const itKeywords = [
    'desarrollador', 'developer', 'programador', 'ingeniero', 'engineer',
    'analista', 'analyst', 'soporte', 'support', 'datos', 'data',
    'devops', 'fullstack', 'frontend', 'backend', 'python', 'java',
    'javascript', 'react', 'angular', 'vue', 'node', 'sql', 'aws',
    'cloud', 'security', 'software', 'web', 'móvil', 'mobile',
    'tester', 'qa', 'ux', 'ui', 'product', 'scrum', 'agile'
  ];

  return scrapedJobs
    .filter(job => {
      const titleLower = (job.title || '').toLowerCase();
      return itKeywords.some(keyword => titleLower.includes(keyword.toLowerCase()));
    })
    .map((job, index): OfertaLaboral => ({
      id: String(index + 1),
      plataforma_origen: (job.source || 'Computrabajo') as OfertaLaboral['plataforma_origen'],
      empresa: {
        nombre: job.company || 'No especificada',
        sector: 'Tecnología',
        tamaño: 'Gran empresa',
        ubicacion: job.location?.replace(', Antioquia', '') || 'Medellín',
        verificada: false
      },
      cargo: {
        titulo: job.title,
        nivel: 'No especificado',
        area: 'IT',
        modalidad: (job.location?.toLowerCase().includes('remoto') ? 'Remoto' : 'Presencial') as OfertaLaboral['cargo']['modalidad'],
        tipo_contrato: 'No especificado',
        jornada: 'Tiempo completo'
      },
      compensacion: {
        salario_min: null,
        salario_max: null,
        moneda: 'COP',
        beneficios: []
      },
      requisitos: {
        experiencia_anos: 0,
        educacion_minima: 'No especificado',
        habilidades_tecnicas: [],
        habilidades_blandas: [],
        idiomas: []
      },
      metadata: {
        fecha_publicacion: job.date_posted || new Date().toISOString().split('T')[0],
        fecha_scraping: new Date().toISOString().split('T')[0],
        url: job.url,
        estado: 'Activa'
      }
    }));
}
