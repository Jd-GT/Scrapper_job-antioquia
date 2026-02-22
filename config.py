"""Configuration for the Antioquia job scraper."""

# ── Request Settings ──────────────────────────────────────────────
REQUEST_TIMEOUT = 15
RETRY_ATTEMPTS = 2
POLITE_DELAY = 1.5  # seconds between requests

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

# ── Antioquia Municipalities ─────────────────────────────────────────
ANTIOQUIA_MUNICIPALITIES = {
    "Medellín":           ["medellin", "medellín"],
    "Envigado":           ["envigado"],
    "Itagüí":             ["itagui", "itagüí", "itagui"],
    "Bello":              ["bello"],
    "Rionegro":           ["rionegro"],
    "Sabaneta":           ["sabaneta"],
    "Apartadó":           ["apartado", "apartadó"],
    "Turbo":              ["turbo"],
    "Urabá":              ["uraba", "urabá"],
}

# ── Contract Type Keywords ────────────────────────────────────────
TEMPORAL_KEYWORDS = [
    "temporal", "obra o labor", "prestación de servicios",
    "freelance", "contrato por obra", "tiempo parcial",
    "medio tiempo", "part-time", "proyecto", "pasantía",
    "practicante", "aprendiz", "suplencia",
]

PERMANENT_KEYWORDS = [
    "indefinido", "término indefinido", "planta",
    "permanente", "fijo", "tiempo completo", "full-time",
    "contrato a término indefinido",
]

# ── Benefits Keywords ─────────────────────────────────────────────
BENEFITS_MAP = {
    "Salud/EPS":        ["salud", "eps", "arl", "seguridad social"],
    "Pensión":          ["pensión", "pension", "fondo de pensiones"],
    "Bonificación":     ["bonificación", "bonificacion", "prima", "bono"],
    "Horario flexible": ["horario flexible", "flexible"],
    "Teletrabajo":      ["home office", "remoto", "teletrabajo", "trabajo remoto"],
    "Transporte":       ["transporte", "movilidad", "auxilio de transporte"],
    "Alimentación":     ["alimentación", "alimentacion", "almuerzo", "casino"],
    "Capacitación":     ["capacitación", "capacitacion", "formación", "curso"],
    "Comisiones":       ["comisión", "comision", "comisiones", "variable"],
}
