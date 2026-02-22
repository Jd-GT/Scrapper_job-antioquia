LINKEDIN_SELECTORS = {
    "job_card": "li.job-card-container, .job-card-list__entity",
    "job_title": ".job-card-list__title, .job-card-container__title",
    "company_name": ".job-card-container__company-name, .job-card-list__company-name",
    "company_location": ".job-card-container__metadata-item, .job-card-list__location",
    "job_url": "a.job-card-list__cta--inline",
    "salary": ".job-card-container__salary-info, .job-card-list__salary",
    "job_details_link": "a.job-card-list__title",
    "description": ".jobs-description__content, .job-view-layout",
    "posted_date": ".job-card-container__listed-time, .job-card-list__listed-time",
    "modalidad": ".job-card-container__workstyle-type-name",
    "nivel": ".job-card-container__jobseniority-level-name",
    "pagination_next": "button[aria-label='Ver más empleos']",
    "pagination": ".artdeco-pagination__pages li",
}

COMPUTRABAJO_SELECTORS = {
    "job_card": ".box_of",
    "job_title": "h1.t1",
    "company_name": ".company a",
    "company_location": ".location",
    "job_url": "a.button_full",
    "salary": ".salary",
    "description": ".description",
    "posted_date": ".date",
    "tipo_contrato": ".contract",
    "modalidad": ".modality",
    "pagination": ".pagination a",
    "next_button": "a.next",
}

INDEED_SELECTORS = {
    "job_card": ".jobsearch-ResultsList > li",
    "job_title": ".jobTitle a",
    "company_name": ".companyName",
    "company_location": ".companyLocation",
    "job_url": ".jobTitle a",
    "salary": ".salaryText",
    "description": ".jobsearch-JobComponent-embeddedDescription",
    "posted_date": ".date",
    "job_details_container": ".jobsearch-JobInfo",
    "pagination": ".pagination a",
    "next_button": "a[aria-label='Next']",
}

MAGNETO365_SELECTORS = {
    "job_card": ".job-item, .MuiCard-root",
    "job_title": ".job-title, .MuiTypography-h6",
    "company_name": ".company-name, .companyInfo",
    "company_location": ".location, .MuiChip-label",
    "job_url": "a.job-title",
    "salary": ".salary, .salary-range",
    "description": ".job-description, .description",
    "posted_date": ".posted-date, .datePosted",
    "modalidad": ".work-mode, .modality",
    "tipo_contrato": ".contract-type",
    "pagination": ".pagination a, .MuiPagination-ul li",
    "next_button": "button[aria-label='next']",
}

ELEMPLEO_SELECTORS = {
    "job_card": ".job-item, .job-box",
    "job_title": ".title, .job-title, h2",
    "company_name": ".company, .company-name",
    "company_location": ".location, .city",
    "job_url": "a.title, a.job-title",
    "salary": ".salary, .remuneration",
    "description": ".description, .job-description",
    "posted_date": ".date, .published",
    "tipo_contrato": ".contract-type",
    "modalidad": ".work-mode",
    "pagination": ".pagination a, .pager a",
    "next_button": ".next a",
}

MASEMPLEO_SELECTORS = {
    "job_card": ".job_listing, .job-item",
    "job_title": ".job_title, .position",
    "company_name": ".company_name, .company",
    "company_location": ".location, .city",
    "job_url": "a.job_title, a[rel='job']",
    "salary": ".salary, .wage",
    "description": ".description, .details",
    "posted_date": ".date, .posted",
    "tipo_contrato": ".contract",
    "modalidad": ".work_type",
    "pagination": ".pagination a",
    "next_button": ".next",
}

SELECTORS_MAP = {
    "linkedin": LINKEDIN_SELECTORS,
    "computrabajo": COMPUTRABAJO_SELECTORS,
    "indeed": INDEED_SELECTORS,
    "magneto365": MAGNETO365_SELECTORS,
    "elempleo": ELEMPLEO_SELECTORS,
    "masempleo": MASEMPLEO_SELECTORS,
}


def get_selectors(platform: str) -> dict:
    return SELECTORS_MAP.get(platform, {})
