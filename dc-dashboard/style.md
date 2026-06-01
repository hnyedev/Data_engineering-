# CURSOR TASK — Restyle DC Dashboard (Hostaro Theme)

## Objetivo
Aplicar el design system del template Hostaro a **todos los archivos Python del dashboard**.
No toques la lógica, datos, ni charts. **Solo CSS y layout visual.**

---

## Design System — Tokens exactos

```
COLORES
──────────────────────────────────────────
--primary:        #3F5BD9   /* azul indigo hero */
--primary-dark:   #2A3AA8   /* gradiente oscuro */
--navy:           #1E2A6E   /* footer, headings */
--orange:         #F5821A   /* CTA, accents, links */
--bg:             #FFFFFF   /* body background */
--bg-light:       #F4F6FF   /* sidebar, alternos */
--border:         #E8E8E8   /* bordes de cards */
--text-main:      #222222   /* texto principal */
--text-muted:     #666666   /* texto secundario */
--success:        #28A745
--warning:        #FFC107
--danger:         #DC3545

TIPOGRAFÍA
──────────────────────────────────────────
font-family:  'Roboto', 'Open Sans', sans-serif
h1:           bold, 2rem,   color #FFFFFF (en hero) / #1E2A6E (en página)
h2:           bold, 1.4rem, color #1E2A6E
labels:       600 weight, 0.75rem, uppercase, letter-spacing 0.05em
body:         400, 0.95rem, color #222222
caption:      0.82rem, color #666666

COMPONENTES
──────────────────────────────────────────
card:         background #FFFFFF, border 1px solid #E8E8E8,
              border-radius 6px, box-shadow 0 2px 8px rgba(63,91,217,0.07)

metric-card:  igual que card + border-left 4px solid #3F5BD9

hero banner:  background linear-gradient(135deg, #3F5BD9 0%, #2A3AA8 100%)
              color #FFFFFF, border-radius 8px, padding 1.4rem 2rem

section-title: color #1E2A6E, font-size 0.85rem, font-weight 700,
               text-transform uppercase, letter-spacing 0.06em,
               border-bottom 2px solid #F5821A, padding-bottom 4px

button / badge CTA:  background #F5821A, color #FFFFFF,
                     border-radius 4px, padding 8px 20px, font-weight 600

badge-success: background #D4EDDA, color #1A5E2B
badge-warning: background #FFF3CD, color #856404
badge-danger:  background #F8D7DA, color #842029
badge-info:    background #D1ECF1, color #0C5460

sidebar:      background #F4F6FF
              nav links: color #1E2A6E, font-weight 600
              active:    color #3F5BD9, border-left 3px solid #F5821A
```

---

## Archivos a editar

```
app.py
pages/01_operations.py
pages/02_energy.py
pages/03_security.py
pages/04_market.py
pages/05_emerging_tech.py
.streamlit/config.toml
```

---

## Instrucciones por archivo

### `.streamlit/config.toml`
Reemplaza todo el bloque `[theme]` con:
```toml
[theme]
primaryColor              = "#F5821A"
backgroundColor           = "#FFFFFF"
secondaryBackgroundColor  = "#F4F6FF"
textColor                 = "#222222"
font                      = "sans serif"

[server]
port             = 8501
headless         = true
enableCORS       = false

[browser]
gatherUsageStats = false
```

---

### `app.py` y cada `pages/*.py`

En el bloque `st.markdown("""<style>...</style>""", unsafe_allow_html=True)` de cada archivo,
**reemplaza todo el contenido del bloque `<style>`** con el siguiente CSS unificado.
No agregues estilos extra. No dupliques. Solo pega esto exacto:

```css
/* ── FONTS ───────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;600;700&display=swap');

* { font-family: 'Roboto', sans-serif; }

/* ── SIDEBAR ─────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #F4F6FF;
    border-right: 1px solid #E8E8E8;
}
[data-testid="stSidebarNav"] a {
    color: #1E2A6E;
    font-weight: 600;
    font-size: 0.92rem;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    display: block;
}
[data-testid="stSidebarNav"] a:hover {
    color: #3F5BD9;
    background: #E8EDFF;
}

/* ── METRIC CARDS ────────────────────────────────── */
div[data-testid="metric-container"] {
    background: #FFFFFF;
    border: 1px solid #E8E8E8;
    border-left: 4px solid #3F5BD9;
    border-radius: 6px;
    padding: 1rem 1.2rem;
    box-shadow: 0 2px 8px rgba(63,91,217,0.07);
}
div[data-testid="metric-container"] label {
    color: #666666 !important;
    font-weight: 600;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #1E2A6E !important;
    font-size: 1.6rem;
    font-weight: 700;
}
div[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    color: #28A745;
    font-size: 0.82rem;
}

/* ── PAGE HERO BANNER ────────────────────────────── */
.page-header {
    background: linear-gradient(135deg, #3F5BD9 0%, #2A3AA8 100%);
    color: #FFFFFF;
    padding: 1.4rem 2rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
}
.page-header h1 {
    color: #FFFFFF;
    margin: 0;
    font-size: 1.6rem;
    font-weight: 700;
}
.page-header p {
    color: #C5D0FF;
    margin: 0.3rem 0 0;
    font-size: 0.88rem;
}

/* ── SECTION TITLES ──────────────────────────────── */
.section-title {
    color: #1E2A6E;
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    border-bottom: 2px solid #F5821A;
    padding-bottom: 4px;
    margin: 1.5rem 0 1rem;
}

/* ── GENERIC CARD ────────────────────────────────── */
.card {
    background: #FFFFFF;
    border: 1px solid #E8E8E8;
    border-radius: 6px;
    padding: 1.2rem;
    box-shadow: 0 2px 8px rgba(63,91,217,0.07);
    margin-bottom: 1rem;
}

/* ── BADGES ──────────────────────────────────────── */
.badge-ok   { background:#D4EDDA; color:#1A5E2B; padding:2px 10px; border-radius:12px; font-size:0.78rem; font-weight:600; }
.badge-warn { background:#FFF3CD; color:#856404; padding:2px 10px; border-radius:12px; font-size:0.78rem; font-weight:600; }
.badge-crit { background:#F8D7DA; color:#842029; padding:2px 10px; border-radius:12px; font-size:0.78rem; font-weight:600; }
.badge-info { background:#D1ECF1; color:#0C5460; padding:2px 10px; border-radius:12px; font-size:0.78rem; font-weight:600; }

/* ── ORANGE ACCENT BUTTON ────────────────────────── */
.btn-orange {
    background: #F5821A;
    color: #FFFFFF;
    border: none;
    border-radius: 4px;
    padding: 10px 24px;
    font-weight: 600;
    font-size: 0.9rem;
    cursor: pointer;
}

/* ── DATAFRAME OVERRIDES ─────────────────────────── */
[data-testid="stDataFrame"] thead tr th {
    background-color: #3F5BD9 !important;
    color: #FFFFFF !important;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
[data-testid="stDataFrame"] tbody tr:hover {
    background-color: #F4F6FF !important;
}

/* ── DIVIDER ─────────────────────────────────────── */
hr {
    border: none;
    border-top: 1px solid #E8E8E8;
    margin: 1.2rem 0;
}

/* ── EXPANDER ────────────────────────────────────── */
[data-testid="stExpander"] {
    border: 1px solid #E8E8E8;
    border-radius: 6px;
}

/* ── MULTISELECT TAGS ────────────────────────────── */
[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
    background-color: #3F5BD9;
    color: #FFFFFF;
}

/* ── INFO / WARNING BOXES ────────────────────────── */
[data-testid="stInfo"]    { border-left: 4px solid #3F5BD9; }
[data-testid="stWarning"] { border-left: 4px solid #F5821A; }
[data-testid="stError"]   { border-left: 4px solid #DC3545; }
[data-testid="stSuccess"] { border-left: 4px solid #28A745; }
```

---

## Reglas para Cursor

1. **El bloque `<style>` va UNA sola vez por archivo**, justo después de `st.set_page_config(...)`.
2. **No repitas estilos inline** en los `st.markdown()` de cards o banners — usa las clases definidas arriba (`.page-header`, `.section-title`, `.card`, `.badge-*`).
3. **No toques** `utils/data_loader.py`, `utils/charts.py`, ni los archivos de infra.
4. **No cambies colores en `charts.py`** — esos tokens ya están alineados.
5. Cada `pages/*.py` debe importar la misma función helper si la creas — **DRY**.
6. El `config.toml` es la fuente de verdad para Streamlit theme. No pongas `backgroundColor` inline.
7. Después de editar, verifica que `streamlit run app.py` corre sin errores antes de hacer commit.

---

## Verificación final

```bash
cd ~/aws/dc-d
streamlit run app.py
# Checklist visual:
# [ ] Hero banner azul gradiente en todas las páginas
# [ ] Metric cards con borde izquierdo azul
# [ ] Section titles con underline naranja
# [ ] Sidebar fondo #F4F6FF
# [ ] Tablas con header azul
# [ ] Badges de colores correctos en Operations y Security
```