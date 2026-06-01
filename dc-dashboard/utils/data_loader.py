"""
data_loader.py
All dashboard data in one place.
Real benchmarks cited from: Uptime Institute 2024 Global Survey,
CBRE Mexico DC Report 2024, TIA-942, ISO 27001:2022.
"""
import pandas as pd
import numpy as np

# ─── 01 OPERATIONS ────────────────────────────────────────────────────────────

def get_sla_data():
    return pd.DataFrame([
        {"tier": "Tier I",  "label": "Basic",       "sla": 99.671, "downtime_hrs": 28.8, "redundancy": "N"},
        {"tier": "Tier II", "label": "Redundant",   "sla": 99.741, "downtime_hrs": 22.0, "redundancy": "N+1"},
        {"tier": "Tier III","label": "Concurrently Maintainable","sla": 99.982,"downtime_hrs": 1.6,"redundancy": "N+1"},
        {"tier": "Tier IV", "label": "Fault Tolerant","sla": 99.995,"downtime_hrs": 0.4,"redundancy": "2N"},
    ])

def get_incident_log():
    return pd.DataFrame([
        {"id":"INC-2401","date":"2024-01-08","severity":"P2","category":"Power","description":"UPS module B fault — switchover to redundant path","mttr_min":23,"status":"Resolved"},
        {"id":"INC-2402","date":"2024-02-14","severity":"P3","category":"Cooling","description":"CRAC unit 3 high-temp alarm — filter replacement","mttr_min":45,"status":"Resolved"},
        {"id":"INC-2403","date":"2024-03-02","severity":"P1","category":"Network","description":"Core switch uplink flap — BGP reconvergence","mttr_min":8,"status":"Resolved"},
        {"id":"INC-2404","date":"2024-03-19","severity":"P3","category":"Physical","description":"Access door sensor malfunction — badge reader replaced","mttr_min":120,"status":"Resolved"},
        {"id":"INC-2405","date":"2024-04-11","severity":"P2","category":"Power","description":"Generator test failure — fuel injector cleaned","mttr_min":210,"status":"Resolved"},
        {"id":"INC-2406","date":"2024-05-03","severity":"P4","category":"Cooling","description":"Humidity sensor drift — calibration performed","mttr_min":30,"status":"Resolved"},
        {"id":"INC-2407","date":"2024-06-22","severity":"P2","category":"Security","description":"CCTV zone 4 outage — NVR disk replaced","mttr_min":90,"status":"Resolved"},
        {"id":"INC-2408","date":"2024-07-15","severity":"P3","category":"Power","description":"PDU branch circuit breaker trip — load rebalanced","mttr_min":15,"status":"Resolved"},
        {"id":"INC-2409","date":"2024-08-01","severity":"P1","category":"Cooling","description":"Chiller primary compressor fault — redundant activated","mttr_min":5,"status":"Resolved"},
        {"id":"INC-2410","date":"2024-09-10","severity":"P4","category":"Network","description":"Port flap on ToR switch — SFP reseated","mttr_min":12,"status":"Open"},
    ])

def get_mac_table():
    return pd.DataFrame([
        {"mac_id":"MAC-441","type":"Move",   "rack":"A-12→B-07","description":"Relocate 2×Dell R750 servers","requested_by":"Ops Team","status":"Completed","date":"2024-09-01"},
        {"mac_id":"MAC-442","type":"Add",    "rack":"C-03",      "description":"Install 40U rack + 20kW PDU","requested_by":"Infra Team","status":"In Progress","date":"2024-09-12"},
        {"mac_id":"MAC-443","type":"Change", "rack":"D-15",      "description":"Upgrade patch panel Cat6→Cat6A","requested_by":"Network Team","status":"Pending","date":"2024-09-20"},
        {"mac_id":"MAC-444","type":"Add",    "rack":"B-09",      "description":"Deploy 4× GPU nodes for AI workloads","requested_by":"AI Division","status":"Approved","date":"2024-09-25"},
        {"mac_id":"MAC-445","type":"Move",   "rack":"A-05→A-08", "description":"Consolidate blade chassis","requested_by":"Ops Team","status":"Pending","date":"2024-10-03"},
        {"mac_id":"MAC-446","type":"Change", "rack":"E-01",      "description":"Reconfigure power feed 20A→30A","requested_by":"Facilities","status":"Completed","date":"2024-08-28"},
    ])

# ─── 02 ENERGY ────────────────────────────────────────────────────────────────

def get_pue_trend():
    months = pd.date_range("2022-01", "2024-09", freq="MS")
    np.random.seed(42)
    pue_vals = np.linspace(1.72, 1.55, len(months)) + np.random.normal(0, 0.02, len(months))
    return pd.DataFrame({
        "month": months,
        "pue": pue_vals.round(3),
        "global_avg": [1.58]*len(months),
        "hyperscaler": [1.20]*len(months),
        "target": [1.40]*len(months),
    })

def get_energy_breakdown():
    return pd.DataFrame([
        {"system": "IT Equipment",       "mw": 4.20, "pct": 53.2},
        {"system": "Cooling (CRAC/CRAH)","mw": 2.45, "pct": 31.0},
        {"system": "UPS Losses",         "mw": 0.55, "pct": 7.0},
        {"system": "Lighting & Other",   "mw": 0.32, "pct": 4.1},
        {"system": "Power Distribution", "mw": 0.37, "pct": 4.7},
    ])

def get_monthly_energy():
    months = pd.date_range("2024-01", "2024-09", freq="MS")
    np.random.seed(7)
    return pd.DataFrame({
        "month": months,
        "it_load_kw":      [4100,4150,4200,4180,4220,4260,4300,4280,4200],
        "total_load_kw":   [6478,6523,6594,6568,6628,6697,6753,6712,6594],
        "renewable_pct":   [12,12,14,15,15,18,18,20,20],
    })

# ─── 03 SECURITY ──────────────────────────────────────────────────────────────

def get_tia942_checklist():
    return pd.DataFrame([
        {"domain":"Site Location",      "control":"Flood/seismic zone assessment",            "status":"Pass","risk":"Low",   "tier_req":"All"},
        {"domain":"Site Location",      "control":"Perimeter setback ≥ 30m from road",         "status":"Pass","risk":"Low",   "tier_req":"III+"},
        {"domain":"Architectural",      "control":"Reinforced concrete structure",              "status":"Pass","risk":"Low",   "tier_req":"All"},
        {"domain":"Architectural",      "control":"Separate security zones (MDF/IDF/NOC)",     "status":"Pass","risk":"Low",   "tier_req":"II+"},
        {"domain":"Architectural",      "control":"Mantrap / airlock entry system",            "status":"Pass","risk":"Low",   "tier_req":"III+"},
        {"domain":"Electrical",         "control":"Redundant utility feeds (2N)",              "status":"Pass","risk":"Low",   "tier_req":"III+"},
        {"domain":"Electrical",         "control":"On-site generator ≥ 96h fuel",             "status":"Pass","risk":"Low",   "tier_req":"II+"},
        {"domain":"Electrical",         "control":"UPS with <10ms transfer time",             "status":"Pass","risk":"Low",   "tier_req":"All"},
        {"domain":"Mechanical",         "control":"N+1 cooling redundancy",                   "status":"Pass","risk":"Low",   "tier_req":"II+"},
        {"domain":"Mechanical",         "control":"Hot/cold aisle containment",               "status":"Partial","risk":"Med","tier_req":"All"},
        {"domain":"Mechanical",         "control":"Free cooling / economizer mode",           "status":"Partial","risk":"Med","tier_req":"III+"},
        {"domain":"Fire Suppression",   "control":"FM-200 / clean agent system",             "status":"Pass","risk":"Low",   "tier_req":"All"},
        {"domain":"Fire Suppression",   "control":"VESDA early smoke detection",             "status":"Pass","risk":"Low",   "tier_req":"II+"},
        {"domain":"Security Systems",   "control":"24/7 CCTV coverage (≥90 day retention)", "status":"Pass","risk":"Low",   "tier_req":"All"},
        {"domain":"Security Systems",   "control":"Biometric + badge dual-factor entry",    "status":"Pass","risk":"Low",   "tier_req":"II+"},
        {"domain":"Security Systems",   "control":"Man-trap with weight sensors",           "status":"Fail","risk":"High",  "tier_req":"III+"},
        {"domain":"Security Systems",   "control":"SOC staffed 24/7",                       "status":"Pass","risk":"Low",   "tier_req":"III+"},
        {"domain":"Telecom",            "control":"Diverse carrier entry points",           "status":"Pass","risk":"Low",   "tier_req":"II+"},
        {"domain":"Telecom",            "control":"Meet-me room with cage separation",      "status":"Pass","risk":"Low",   "tier_req":"All"},
    ])

def get_iso27001_controls():
    return pd.DataFrame([
        {"clause":"A.7  Physical Controls", "control":"Secure perimeter definition",     "status":"Implemented","score":95},
        {"clause":"A.7  Physical Controls", "control":"Physical entry controls",         "status":"Implemented","score":90},
        {"clause":"A.7  Physical Controls", "control":"Securing offices & facilities",   "status":"Implemented","score":88},
        {"clause":"A.7  Physical Controls", "control":"Physical security monitoring",    "status":"Implemented","score":92},
        {"clause":"A.7  Physical Controls", "control":"Protection against environmental threats","status":"Partial","score":75},
        {"clause":"A.8  Tech Controls",     "control":"User endpoint devices",           "status":"Implemented","score":85},
        {"clause":"A.8  Tech Controls",     "control":"Privileged access rights",        "status":"Implemented","score":90},
        {"clause":"A.8  Tech Controls",     "control":"Information access restriction",  "status":"Implemented","score":88},
        {"clause":"A.8  Tech Controls",     "control":"Malware protection",              "status":"Implemented","score":95},
        {"clause":"A.8  Tech Controls",     "control":"Capacity management",             "status":"Partial","score":70},
        {"clause":"A.6  Org Controls",      "control":"Screening",                       "status":"Implemented","score":80},
        {"clause":"A.6  Org Controls",      "control":"Information security in projects","status":"Partial","score":65},
    ])

# ─── 04 MARKET INTELLIGENCE ───────────────────────────────────────────────────

def get_mexico_market():
    return pd.DataFrame([
        {"city":"Ciudad de México","region":"CDMX",       "capacity_mw":210,"utilization_pct":78,"yoy_growth_pct":14,"avg_rack_price_usd":350,"operators":"KIO, Telmex, IXmetro, Equinix","lat":19.43,"lon":-99.13},
        {"city":"Querétaro",       "region":"Bajío",      "capacity_mw":95, "utilization_pct":65,"yoy_growth_pct":32,"avg_rack_price_usd":280,"operators":"Equinix QRO1/QRO2, CyrusOne, KIO","lat":20.59,"lon":-100.39},
        {"city":"Guadalajara",     "region":"Jalisco",    "capacity_mw":55, "utilization_pct":60,"yoy_growth_pct":18,"avg_rack_price_usd":260,"operators":"Telmex, IXmetro","lat":20.66,"lon":-103.35},
        {"city":"Monterrey",       "region":"Noreste",    "capacity_mw":38, "utilization_pct":55,"yoy_growth_pct":22,"avg_rack_price_usd":270,"operators":"KIO, Neutral DC","lat":25.67,"lon":-100.31},
        {"city":"Mérida",          "region":"Sureste",    "capacity_mw":14, "utilization_pct":45,"yoy_growth_pct":40,"avg_rack_price_usd":240,"operators":"Telmex, local ISPs","lat":20.97,"lon":-89.62},
    ])

def get_deployment_models():
    return pd.DataFrame([
        {"model":"Colocation",     "capex":"Low",   "opex":"Medium","control":"Low",   "scalability":"Medium","best_for":"SME / regional enterprises"},
        {"model":"Hyperscale",     "capex":"High",  "opex":"Low",   "control":"High",  "scalability":"High",  "best_for":"Cloud providers / AI clusters"},
        {"model":"Edge DC",        "capex":"Medium","opex":"Medium","control":"Medium","scalability":"Low",   "best_for":"Latency-sensitive / IoT workloads"},
        {"model":"Wholesale",      "capex":"Low",   "opex":"Medium","control":"Medium","scalability":"High",  "best_for":"Large enterprise / gov outsourcing"},
        {"model":"On-Premises",    "capex":"High",  "opex":"High",  "control":"Full",  "scalability":"Low",   "best_for":"Regulated sectors (banking, gov)"},
    ])

def get_market_growth():
    years = list(range(2020, 2027))
    return pd.DataFrame({
        "year":         years,
        "capacity_mw":  [210, 245, 280, 320, 412, 510, 630],
        "investment_musd":[380,440,520,610,780,960,1180],
        "forecast":     [False,False,False,False,False,True,True],
    })

# ─── 05 EMERGING TECH ─────────────────────────────────────────────────────────

def get_tech_radar():
    return pd.DataFrame([
        {"technology":"Liquid Cooling (Direct-to-Chip)", "category":"Infrastructure","maturity":"Adopt",  "horizon_yr":2025,"impact":"High",  "readiness":4},
        {"technology":"AI-Driven DCIM",                  "category":"Operations",   "maturity":"Trial",  "horizon_yr":2025,"impact":"High",  "readiness":3},
        {"technology":"400G / 800G Networking",          "category":"Network",      "maturity":"Adopt",  "horizon_yr":2024,"impact":"High",  "readiness":4},
        {"technology":"Immersion Cooling",               "category":"Infrastructure","maturity":"Trial",  "horizon_yr":2026,"impact":"High",  "readiness":2},
        {"technology":"Renewable PPA (Solar/Wind)",      "category":"Energy",       "maturity":"Adopt",  "horizon_yr":2025,"impact":"Medium","readiness":4},
        {"technology":"Modular / Prefab DC",             "category":"Infrastructure","maturity":"Adopt",  "horizon_yr":2024,"impact":"Medium","readiness":5},
        {"technology":"NVMe-oF Storage Fabric",         "category":"Storage",      "maturity":"Trial",  "horizon_yr":2026,"impact":"Medium","readiness":3},
        {"technology":"Hydrogen Fuel Cells",             "category":"Energy",       "maturity":"Assess", "horizon_yr":2027,"impact":"High",  "readiness":1},
        {"technology":"Digital Twin (DC)",               "category":"Operations",   "maturity":"Trial",  "horizon_yr":2026,"impact":"Medium","readiness":2},
        {"technology":"Neuromorphic Computing",          "category":"Compute",      "maturity":"Hold",   "horizon_yr":2029,"impact":"High",  "readiness":1},
        {"technology":"Quantum-Safe Encryption",         "category":"Security",     "maturity":"Assess", "horizon_yr":2027,"impact":"High",  "readiness":2},
        {"technology":"Software-Defined Power",          "category":"Power",        "maturity":"Assess", "horizon_yr":2027,"impact":"Medium","readiness":2},
    ])

def get_adoption_timeline():
    return pd.DataFrame([
        {"technology":"Modular / Prefab DC",            "start":2022,"peak":2024,"end":2028},
        {"technology":"400G / 800G Networking",         "start":2023,"peak":2025,"end":2029},
        {"technology":"Liquid Cooling (DtC)",           "start":2023,"peak":2026,"end":2030},
        {"technology":"AI-Driven DCIM",                 "start":2024,"peak":2026,"end":2030},
        {"technology":"Renewable PPA",                  "start":2023,"peak":2025,"end":2030},
        {"technology":"Immersion Cooling",              "start":2025,"peak":2027,"end":2030},
        {"technology":"Digital Twin (DC)",              "start":2025,"peak":2027,"end":2030},
        {"technology":"Quantum-Safe Encryption",        "start":2026,"peak":2028,"end":2030},
        {"technology":"Hydrogen Fuel Cells",            "start":2027,"peak":2029,"end":2030},
    ])