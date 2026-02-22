import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { FilterState, PlataformaOrigen, Modalidad, NivelCargo } from '@/types';

interface FilterStore extends FilterState {
  setPlataformas: (plataformas: PlataformaOrigen[]) => void;
  setSectores: (sectores: string[]) => void;
  setAreas: (areas: string[]) => void;
  setNiveles: (niveles: NivelCargo[]) => void;
  setModalidad: (modalidad: Modalidad[]) => void;
  setRangoSalarial: (rango: [number, number]) => void;
  setExperienciaMax: (experiencia: number) => void;
  setSkillsRequeridas: (skills: string[]) => void;
  setFechaDesde: (fecha: string | null) => void;
  setFechaHasta: (fecha: string | null) => void;
  setBusquedaTexto: (texto: string) => void;
  setSoloVerificadas: (solo: boolean) => void;
  setSoloConSalario: (solo: boolean) => void;
  resetFilters: () => void;
  setPreset: (preset: string) => void;
}

const defaultFilters: FilterState = {
  plataformas: [],
  sectores: [],
  areas: [],
  niveles: [],
  modalidad: [],
  rangoSalarial: [0, 20000000],
  experienciaMax: 10,
  skillsRequeridas: [],
  fechaDesde: null,
  fechaHasta: null,
  busquedaTexto: '',
  soloVerificadas: false,
  soloConSalario: false,
};

export const useFilterStore = create<FilterStore>()(
  persist(
    (set) => ({
      ...defaultFilters,
      
      setPlataformas: (plataformas) => set({ plataformas }),
      setSectores: (sectores) => set({ sectores }),
      setAreas: (areas) => set({ areas }),
      setNiveles: (niveles) => set({ niveles }),
      setModalidad: (modalidad) => set({ modalidad }),
      setRangoSalarial: (rangoSalarial) => set({ rangoSalarial }),
      setExperienciaMax: (experienciaMax) => set({ experienciaMax }),
      setSkillsRequeridas: (skillsRequeridas) => set({ skillsRequeridas }),
      setFechaDesde: (fechaDesde) => set({ fechaDesde }),
      setFechaHasta: (fechaHasta) => set({ fechaHasta }),
      setBusquedaTexto: (busquedaTexto) => set({ busquedaTexto }),
      setSoloVerificadas: (soloVerificadas) => set({ soloVerificadas }),
      setSoloConSalario: (soloConSalario) => set({ soloConSalario }),
      
      resetFilters: () => set(defaultFilters),
      
      setPreset: (preset) => {
        switch (preset) {
          case 'primer-empleo':
            set({
              experienciaMax: 1,
              niveles: ['Junior', 'Asistente'],
              soloConSalario: false,
            });
            break;
          case 'tech-senior':
            set({
              sectores: ['Tecnología'],
              niveles: ['Senior', 'Gerente', 'Director'],
              experienciaMax: 5,
            });
            break;
          case 'remoto':
            set({
              modalidad: ['Remoto'],
            });
            break;
          default:
            break;
        }
      },
    }),
    {
      name: 'empleos-filters',
    }
  )
);
