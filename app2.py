"""
Global Migration Story: Where People Go — and Why
A Streamlit data visualization app following Tufte, Segel & Heer, Ware, and Mayer & Moreno principles.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ──────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Global Migration Story",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────────
# THEME / CSS
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Source+Sans+3:wght@300;400;600&display=swap');

  html, body, [class*="css"] {
      font-family: 'Source Sans 3', sans-serif;
      background-color: #0f1117;
      color: #e8e0d0;
  }

  /* Hero header */
  .hero-title {
      font-family: 'Playfair Display', serif;
      font-size: 3.2rem;
      font-weight: 900;
      letter-spacing: -1px;
      color: #f0e8d0;
      line-height: 1.1;
      margin-bottom: 0.2rem;
  }
  .hero-sub {
      font-family: 'Source Sans 3', sans-serif;
      font-size: 1.1rem;
      font-weight: 300;
      color: #a09888;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      margin-bottom: 1.5rem;
  }

  /* Pathway type badge colors */
  .badge-humanitarian {
      background: rgba(220,60,60,0.18);
      color: #e87070;
      border: 1px solid rgba(220,60,60,0.4);
      padding: 2px 10px;
      border-radius: 20px;
      font-size: 0.8rem;
      font-weight: 600;
      letter-spacing: 0.05em;
  }
  .badge-legal {
      background: rgba(60,120,220,0.18);
      color: #7ab0e8;
      border: 1px solid rgba(60,120,220,0.4);
      padding: 2px 10px;
      border-radius: 20px;
      font-size: 0.8rem;
      font-weight: 600;
      letter-spacing: 0.05em;
  }
  .badge-mixed {
      background: rgba(200,160,40,0.18);
      color: #e8c860;
      border: 1px solid rgba(200,160,40,0.4);
      padding: 2px 10px;
      border-radius: 20px;
      font-size: 0.8rem;
      font-weight: 600;
      letter-spacing: 0.05em;
  }

  /* Story card */
  .story-card {
      background: rgba(255,255,255,0.04);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 12px;
      padding: 1.2rem 1.4rem;
      margin-bottom: 0.8rem;
  }
  .story-card h4 {
      font-family: 'Playfair Display', serif;
      font-size: 1.15rem;
      color: #f0e8d0;
      margin-bottom: 0.3rem;
  }
  .story-card p {
      font-size: 0.93rem;
      color: #b0a898;
      line-height: 1.6;
      margin: 0;
  }

  /* Metric box */
  .metric-box {
      background: rgba(255,255,255,0.04);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 10px;
      padding: 1rem;
      text-align: center;
  }
  .metric-box .metric-value {
      font-family: 'Playfair Display', serif;
      font-size: 2rem;
      font-weight: 700;
      color: #f0e8d0;
  }
  .metric-box .metric-label {
      font-size: 0.78rem;
      color: #807870;
      text-transform: uppercase;
      letter-spacing: 0.1em;
  }

  /* Section title */
  .section-title {
      font-family: 'Playfair Display', serif;
      font-size: 1.6rem;
      font-weight: 700;
      color: #f0e8d0;
      border-bottom: 1px solid rgba(255,255,255,0.1);
      padding-bottom: 0.5rem;
      margin-bottom: 1rem;
  }

  .divider {
      border: none;
      border-top: 1px solid rgba(255,255,255,0.08);
      margin: 2rem 0;
  }

  /* Sidebar */
  [data-testid="stSidebar"] {
      background-color: #0a0d12 !important;
  }
  [data-testid="stSidebar"] label {
      font-family: 'Source Sans 3', sans-serif;
      font-size: 0.85rem;
      color: #a09888;
      text-transform: uppercase;
      letter-spacing: 0.08em;
  }

  /* Hide Streamlit branding */
  #MainMenu {visibility: hidden;}
  footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# COLOUR CONSTANTS  (Ware semiotics + Silva categorical encoding)
# ──────────────────────────────────────────────────────────────────────────────
COLORS = {
    "Humanitarian": "#dc3c3c",
    "Legal":        "#3c78dc",
    "Mixed":        "#c8a028",
}
LIGHT_COLORS = {
    "Humanitarian": "rgba(220,60,60,0.7)",
    "Legal":        "rgba(60,120,220,0.7)",
    "Mixed":        "rgba(200,160,40,0.7)",
}
BG    = "#0f1117"
PAPER = "#161920"
FONT  = "#e8e0d0"
MUTED = "#807870"

PLOTLY_THEME = dict(
    plot_bgcolor=BG,
    paper_bgcolor=PAPER,
    font=dict(family="Source Sans 3", color=FONT, size=12),
    margin=dict(l=40, r=20, t=50, b=40),
)


# ──────────────────────────────────────────────────────────────────────────────
# DATA  (load once, cache)
# ──────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    # Try the uploaded path first, fall back to local
    paths = [
        "full_migration_dataset_ess_final_project.xlsx",
        "data/full_migration_dataset_ess_final_project.xlsx",
    ]
    for p in paths:
        try:
            df = pd.read_excel(p)
            break
        except FileNotFoundError:
            continue
    else:
        st.error("⚠️ Could not find the Excel data file. "
                 "Place `full_migration_dataset_ess_final_project.xlsx` "
                 "in the same directory as app.py (or in a `data/` sub-folder).")
        st.stop()

    df = df.rename(columns={
        "migrants_in US":                "migrants_in_us",
        "sum_of_country's_immigrants":   "total_emigrants",
        "country's_population":          "population",
        "Latitude (generated)":          "lat",
        "Longitude (generated)":         "lon",
        "US_context":                    "us_context",
    })

    # Guarantee us_context exists — handle any capitalisation variant or missing column
    if "us_context" not in df.columns:
        # Try case-insensitive match against remaining columns
        col_map = {c.lower(): c for c in df.columns}
        candidate = col_map.get("us_context") or col_map.get("us context")
        if candidate:
            df = df.rename(columns={candidate: "us_context"})
        else:
            df["us_context"] = "N/A"

    US_POP = 335_000_000  # 2024 estimate

    # Derived metrics
    df["pct_of_us_pop"]        = df["migrants_in_us"] / US_POP * 100
    df["pct_of_country_pop"]   = df["total_emigrants"] / df["population"] * 100
    df["us_share_of_diaspora"] = df["migrants_in_us"] / df["total_emigrants"] * 100
    df["bubble_r"]             = np.sqrt(df["migrants_in_us"])   # Tufte graphical integrity

    # Normalised bubble size for Plotly (0–60 px range)
    mn, mx = df["bubble_r"].min(), df["bubble_r"].max()
    df["bubble_size"] = 6 + 54 * (df["bubble_r"] - mn) / (mx - mn)

    # Parse primary pathways into list
    df["pathways_list"] = df["primary_pathway"].apply(
        lambda x: [p.strip() for p in str(x).split(";")]
    )

    # Reason category — simplified grouping for colour axes
    df["reason_simple"] = df["reason_category"].apply(
        lambda x: x.split("/")[0] if isinstance(x, str) else x
    )

    return df


df = load_data()
ALL_COUNTRIES = sorted(df["origin_country"].tolist())


# ──────────────────────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────────────────────
def fmt_num(n):
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.0f}K"
    return str(int(n))


def badge(ptype):
    cls = f"badge-{ptype.lower()}"
    return f'<span class="{cls}">{ptype}</span>'


def plotly_defaults(fig):
    fig.update_layout(**PLOTLY_THEME)
    fig.update_xaxes(
        showgrid=False, zeroline=False,
        tickcolor=MUTED, linecolor=MUTED, color=MUTED,
    )
    fig.update_yaxes(
        showgrid=True, gridcolor="rgba(255,255,255,0.05)",
        zeroline=False, tickcolor=MUTED, linecolor=MUTED, color=MUTED,
    )
    return fig


# ──────────────────────────────────────────────────────────────────────────────
# SIDEBAR  — filters (Mayer & Moreno progressive disclosure)
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌍 Filters")

    sel_pathway = st.multiselect(
        "Pathway Type",
        options=["Humanitarian", "Legal", "Mixed"],
        default=["Humanitarian", "Legal", "Mixed"],
    )

    reason_opts = sorted(df["reason_category"].unique())
    sel_reason = st.multiselect(
        "Reason Category",
        options=reason_opts,
        default=reason_opts,
    )

    min_us = st.slider(
        "Min. migrants in US (thousands)",
        min_value=0,
        max_value=int(df["migrants_in_us"].max() / 1000),
        value=0,
        step=50,
    )

    sel_country = st.selectbox(
        "Deep-dive: Country",
        options=["— All countries —"] + ALL_COUNTRIES,
    )

    st.markdown("---")
    st.markdown(
        "<span style='font-size:0.75rem;color:#504840;'>"
        "Data: ESS Final Project Dataset · US pop. 335M (2024 est.)"
        "</span>",
        unsafe_allow_html=True,
    )

# Apply filters
mask = (
    df["pathway_type"].isin(sel_pathway)
    & df["reason_category"].isin(sel_reason)
    & (df["migrants_in_us"] >= min_us * 1000)
)
dff = df[mask].copy()


# ──────────────────────────────────────────────────────────────────────────────
# HERO HEADER
# ──────────────────────────────────────────────────────────────────────────────
st.markdown(
    '<p class="hero-title">Where People Go —<br>and Why They Leave</p>'
    '<p class="hero-sub">A global portrait of migration into the United States · 59 origin countries</p>',
    unsafe_allow_html=True,
)

# Global KPI row
c1, c2, c3, c4 = st.columns(4)
total_us   = dff["migrants_in_us"].sum()
total_dias = dff["total_emigrants"].sum()
n_hum  = (dff["pathway_type"] == "Humanitarian").sum()
n_leg  = (dff["pathway_type"] == "Legal").sum()
n_mix  = (dff["pathway_type"] == "Mixed").sum()

for col, val, lbl in [
    (c1, fmt_num(total_us),     "Migrants in US"),
    (c2, fmt_num(total_dias),   "Total diaspora (global)"),
    (c3, f"{n_hum} / {n_leg} / {n_mix}", "Humanitarian / Legal / Mixed"),
    (c4, f"{len(dff)}", "Countries shown"),
]:
    col.markdown(
        f'<div class="metric-box">'
        f'<div class="metric-value">{val}</div>'
        f'<div class="metric-label">{lbl}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 1 — GLOBAL MAP  (Tufte: graphical integrity, data-ink ratio)
# ──────────────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-title">Global Overview: Migrants in the US by Origin</p>', unsafe_allow_html=True)
st.caption(
    "Bubble size ∝ √(migrants in US) — square-root scaling keeps proportions honest "
    "while communicating magnitude. Color encodes pathway type."
)

hover_tpl = (
    "<b>%{customdata[0]}</b><br>"
    "━━━━━━━━━━━━━━━━━━━━<br>"
    "Migrants in US: <b>%{customdata[1]}</b><br>"
    "Total emigrants (global): %{customdata[2]}<br>"
    "% of country's pop. emigrated: %{customdata[3]:.1f}%<br>"
    "% of US pop.: %{customdata[4]:.2f}%<br>"
    "US share of diaspora: %{customdata[5]:.1f}%<br>"
    "Pathway: %{customdata[6]}<br>"
    "Reason: %{customdata[7]}<br>"
    "<i style='color:#c8a028'>%{customdata[8]}</i><br>"
    "<i style='color:#7ab0e8;font-size:0.85em'>🇺🇸 %{customdata[9]}</i>"
    "<extra></extra>"
)

fig_map = go.Figure()

for ptype, grp in dff.groupby("pathway_type"):
    fig_map.add_trace(go.Scattergeo(
        lat=grp["lat"],
        lon=grp["lon"],
        mode="markers",
        name=ptype,
        marker=dict(
            size=grp["bubble_size"],
            color=COLORS[ptype],
            opacity=0.82,
            line=dict(width=0.6, color="rgba(255,255,255,0.25)"),
        ),
        customdata=np.stack([
            grp["origin_country"],
            grp["migrants_in_us"].apply(fmt_num),
            grp["total_emigrants"].apply(fmt_num),
            grp["pct_of_country_pop"],
            grp["pct_of_us_pop"],
            grp["us_share_of_diaspora"],
            grp["pathway_type"],
            grp["reason_category"],
            grp["key_context"],
            grp["us_context"].fillna("No direct US policy connection documented."),
        ], axis=-1),
        hovertemplate=hover_tpl,
    ))

fig_map.update_layout(
    **PLOTLY_THEME,
    height=500,
    showlegend=True,
    legend=dict(
        orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0,
        font=dict(size=12, color=FONT),
        bgcolor="rgba(0,0,0,0)",
    ),
    geo=dict(
        bgcolor=BG,
        showframe=False,
        showcoastlines=True,
        coastlinecolor="rgba(255,255,255,0.1)",
        showland=True,
        landcolor="rgba(255,255,255,0.04)",
        showocean=True,
        oceancolor=BG,
        showlakes=False,
        showcountries=True,
        countrycolor="rgba(255,255,255,0.06)",
        projection_type="natural earth",
    ),
)
st.plotly_chart(fig_map, use_container_width=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 2 — PATHWAY TYPE BREAKDOWN
# ──────────────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-title">How They Arrive: Pathway Type Breakdown</p>', unsafe_allow_html=True)

col_pie, col_bar = st.columns([1, 2])

with col_pie:
    ptypes = dff.groupby("pathway_type")["migrants_in_us"].sum().reset_index()
    fig_pie = go.Figure(go.Pie(
        labels=ptypes["pathway_type"],
        values=ptypes["migrants_in_us"],
        marker_colors=[COLORS[p] for p in ptypes["pathway_type"]],
        hole=0.55,
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>%{value:,.0f} migrants<br>%{percent}<extra></extra>",
        textfont=dict(family="Source Sans 3", size=12, color=FONT),
    ))
    fig_pie.update_layout(
        **PLOTLY_THEME,
        height=320,
        showlegend=False,
        title=dict(text="Share of US migrants<br>by pathway type", font=dict(size=13, color=MUTED)),
        annotations=[dict(
            text=fmt_num(dff["migrants_in_us"].sum()),
            x=0.5, y=0.5, font_size=20, showarrow=False,
            font=dict(family="Playfair Display", color=FONT),
        )],
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col_bar:
    # Top 20 by migrants_in_us coloured by pathway
    top20 = dff.nlargest(20, "migrants_in_us")
    fig_hbar = go.Figure()
    for ptype, grp in top20.groupby("pathway_type"):
        fig_hbar.add_trace(go.Bar(
            y=grp["origin_country"],
            x=grp["migrants_in_us"],
            name=ptype,
            orientation="h",
            marker_color=COLORS[ptype],
            hovertemplate="%{y}: <b>%{x:,.0f}</b> migrants<extra></extra>",
        ))
    fig_hbar = plotly_defaults(fig_hbar)
    fig_hbar.update_layout(
        height=420,
        barmode="stack",
        title=dict(text="Top 20 Origin Countries — Migrants in US", font=dict(size=13, color=MUTED)),
        yaxis=dict(categoryorder="total ascending"),
        showlegend=False,
        xaxis_title="Migrants in US",
    )
    st.plotly_chart(fig_hbar, use_container_width=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 3 — REASON CATEGORY TREEMAP
# ──────────────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-title">Why They Leave: Reason Categories</p>', unsafe_allow_html=True)

reason_grp = dff.groupby(["reason_category", "pathway_type"])["migrants_in_us"].sum().reset_index()
fig_tree = px.treemap(
    reason_grp,
    path=["pathway_type", "reason_category"],
    values="migrants_in_us",
    color="pathway_type",
    color_discrete_map=COLORS,
    hover_data={"migrants_in_us": ":,.0f"},
    custom_data=["reason_category"],
)
fig_tree.update_traces(
    hovertemplate="<b>%{label}</b><br>Migrants: %{value:,.0f}<extra></extra>",
    textfont=dict(family="Source Sans 3", size=13),
)
fig_tree.update_layout(
    **PLOTLY_THEME,
    height=380,
    title=dict(text="Treemap: pathway type → reason category → migrant volume", font=dict(size=13, color=MUTED)),
)
st.plotly_chart(fig_tree, use_container_width=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 4 — PRIMARY PATHWAYS (exploded tags)
# ──────────────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-title">Primary Pathways: Which Visas & Routes Dominate?</p>', unsafe_allow_html=True)

# Explode pathway list, count weighted by migrants_in_us
pathway_rows = []
for _, row in dff.iterrows():
    for p in row["pathways_list"]:
        pathway_rows.append({"pathway": p, "migrants_in_us": row["migrants_in_us"], "pathway_type": row["pathway_type"]})
pw_df = pd.DataFrame(pathway_rows)
pw_agg = pw_df.groupby(["pathway", "pathway_type"])["migrants_in_us"].sum().reset_index()
pw_top = pw_agg.nlargest(25, "migrants_in_us")

fig_pw = px.bar(
    pw_top.sort_values("migrants_in_us"),
    x="migrants_in_us",
    y="pathway",
    color="pathway_type",
    color_discrete_map=COLORS,
    orientation="h",
    hover_data={"migrants_in_us": ":,.0f"},
    labels={"migrants_in_us": "Associated Migrant Volume", "pathway": ""},
)
fig_pw = plotly_defaults(fig_pw)
fig_pw.update_layout(
    height=500,
    title=dict(text="Top 25 Primary Pathways (weighted by migrant volume)", font=dict(size=13, color=MUTED)),
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0, bgcolor="rgba(0,0,0,0)"),
)
st.plotly_chart(fig_pw, use_container_width=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 5 — SCALE COMPARISONS (relative metrics)
# ──────────────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-title">Scale & Proportion: Migrants Relative to Home & Host Country</p>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs([
    "% of Country's Population Emigrated",
    "US Share of Global Diaspora",
    "% of US Population",
])

with tab1:
    fig_s1 = px.scatter(
        dff.sort_values("pct_of_country_pop", ascending=False).head(40),
        x="pct_of_country_pop",
        y="migrants_in_us",
        size="bubble_size",
        color="pathway_type",
        color_discrete_map=COLORS,
        hover_name="origin_country",
        hover_data={
            "pct_of_country_pop": ":.1f",
            "migrants_in_us": ":,.0f",
            "pathway_type": True,
            "reason_category": True,
            "bubble_size": False,
        },
        labels={
            "pct_of_country_pop": "% of Country's Population Emigrated (globally)",
            "migrants_in_us": "Migrants in US",
        },
        log_y=True,
    )
    fig_s1 = plotly_defaults(fig_s1)
    fig_s1.update_layout(
        height=420,
        title=dict(text="Nations with high emigration rates vs. US absorption — log scale", font=dict(size=13, color=MUTED)),
        showlegend=True,
    )
    # Add country labels for standouts
    standouts = dff.nlargest(8, "pct_of_country_pop")
    for _, row in standouts.iterrows():
        fig_s1.add_annotation(
            x=row["pct_of_country_pop"],
            y=np.log10(row["migrants_in_us"]),
            text=row["origin_country"],
            showarrow=False,
            font=dict(size=9, color=MUTED),
            xshift=6, yshift=4,
        )
    st.plotly_chart(fig_s1, use_container_width=True)
    st.caption(
        "Countries far to the right have lost a large share of their population to emigration globally. "
        "High y + high x = the US captures a major slice of a highly-mobile population."
    )

with tab2:
    fig_s2 = px.bar(
        dff.sort_values("us_share_of_diaspora", ascending=False).head(25),
        x="origin_country",
        y="us_share_of_diaspora",
        color="pathway_type",
        color_discrete_map=COLORS,
        labels={"us_share_of_diaspora": "US share of global diaspora (%)", "origin_country": ""},
        hover_data={"us_share_of_diaspora": ":.1f", "migrants_in_us": ":,.0f", "total_emigrants": ":,.0f"},
    )
    fig_s2 = plotly_defaults(fig_s2)
    fig_s2.update_layout(
        height=420,
        title=dict(text="The US captures X% of each country's global diaspora", font=dict(size=13, color=MUTED)),
        xaxis_tickangle=-40,
        showlegend=False,
    )
    st.plotly_chart(fig_s2, use_container_width=True)
    st.caption(
        "When the US share is very high (e.g. Mexico, El Salvador, Cuba), it signals a structural pull "
        "— geography, policy, or historical ties that funnel migrants specifically toward the US."
    )

with tab3:
    fig_s3 = px.bar(
        dff.sort_values("pct_of_us_pop", ascending=False).head(20),
        x="origin_country",
        y="pct_of_us_pop",
        color="pathway_type",
        color_discrete_map=COLORS,
        labels={"pct_of_us_pop": "% of US population", "origin_country": ""},
    )
    fig_s3 = plotly_defaults(fig_s3)
    fig_s3.update_layout(
        height=420,
        title=dict(text="Each origin country as % of the US total population", font=dict(size=13, color=MUTED)),
        xaxis_tickangle=-40,
        showlegend=False,
    )
    st.plotly_chart(fig_s3, use_container_width=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 6 — REASON × PATHWAY HEATMAP
# ──────────────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-title">Reason × Pathway: Where Causes Meet Routes</p>', unsafe_allow_html=True)

pivot = dff.pivot_table(
    index="reason_category",
    columns="pathway_type",
    values="migrants_in_us",
    aggfunc="sum",
    fill_value=0,
)
# Reorder columns if present
col_order = [c for c in ["Humanitarian", "Legal", "Mixed"] if c in pivot.columns]
pivot = pivot[col_order]

fig_heat = go.Figure(go.Heatmap(
    z=pivot.values / 1000,
    x=pivot.columns.tolist(),
    y=pivot.index.tolist(),
    colorscale=[
        [0.0,  "rgba(15,17,23,1)"],
        [0.15, "rgba(60,60,140,0.7)"],
        [0.5,  "rgba(80,120,200,0.85)"],
        [1.0,  "rgba(220,230,255,1)"],
    ],
    text=(pivot.values / 1000).round(0).astype(int),
    texttemplate="%{text}K",
    hoverongaps=False,
    hovertemplate="Reason: %{y}<br>Pathway: %{x}<br>Migrants: %{z:.0f}K<extra></extra>",
    colorbar=dict(title="Migrants (K)", tickfont=dict(color=MUTED)),
))
fig_heat = plotly_defaults(fig_heat)
fig_heat.update_layout(
    height=420,
    title=dict(text="Migrant volume (thousands) by reason category and pathway type", font=dict(size=13, color=MUTED)),
    xaxis_title="",
    yaxis_title="",
)
st.plotly_chart(fig_heat, use_container_width=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 7 — COUNTRY DEEP-DIVE + KEY CONTEXT NARRATIVE
# (Segel & Heer: martini glass — reader-driven exploration)
# ──────────────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-title">Country Deep-Dive & Story Panel</p>', unsafe_allow_html=True)

if sel_country != "— All countries —":
    row = df[df["origin_country"] == sel_country].iloc[0]
    ptype = row["pathway_type"]

    # Header
    st.markdown(
        f"### {row['origin_country']} &nbsp; {badge(ptype)}",
        unsafe_allow_html=True,
    )

    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    for col, val, lbl in [
        (m1, fmt_num(row["migrants_in_us"]),       "Migrants in US"),
        (m2, fmt_num(row["total_emigrants"]),       "Total emigrants (global)"),
        (m3, f"{row['pct_of_country_pop']:.1f}%",  "% of home country pop."),
        (m4, f"{row['us_share_of_diaspora']:.1f}%","US share of diaspora"),
    ]:
        col.markdown(
            f'<div class="metric-box">'
            f'<div class="metric-value">{val}</div>'
            f'<div class="metric-label">{lbl}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("")

    # Comparative bar: this country vs all others
    compare_df = pd.DataFrame({
        "Group": [sel_country, "All other countries"],
        "Migrants in US": [
            row["migrants_in_us"],
            df[df["origin_country"] != sel_country]["migrants_in_us"].sum(),
        ],
    })
    fig_cmp = px.bar(
        compare_df, x="Migrants in US", y="Group",
        orientation="h",
        color="Group",
        color_discrete_sequence=[COLORS[ptype], "rgba(255,255,255,0.1)"],
    )
    fig_cmp = plotly_defaults(fig_cmp)
    fig_cmp.update_layout(height=180, showlegend=False,
                           title=dict(text="Share of total migrants in dataset", font=dict(size=12, color=MUTED)))
    st.plotly_chart(fig_cmp, use_container_width=True)

    # Pathways tags
    st.markdown("**Primary pathways used:**")
    st.markdown("  &nbsp; ".join(
        [f'<span class="badge-{ptype.lower()}">{p}</span>' for p in row["pathways_list"]]
    ), unsafe_allow_html=True)

    st.markdown("")

    # KEY CONTEXT narrative card
    has_us_context = (
        isinstance(row.get("us_context"), str)
        and row["us_context"].strip().lower() not in ("", "n/a", "nan")
    )

    us_connection = has_us_context or any(
        kw in row["key_context"].lower()
        for kw in ["us ", "u.s.", "american", "united states", "foreign policy",
                   "cold war", "intervention", "treaty", "war on", "cia", "sanctions",
                   "occupation", "military"]
    )

    us_context_block = (
        f'<p style="margin-top:0.8rem;padding:0.6rem 0.8rem;'
        f'background:rgba(60,120,220,0.08);border-left:3px solid rgba(60,120,220,0.5);'
        f'border-radius:4px;font-size:0.9rem;color:#b8d0f0;">'
        f'🇺🇸 <b>US Context:</b> {row["us_context"]}</p>'
        if has_us_context else ""
    )

    st.markdown(
        f'<div class="story-card">'
        f'<h4>📖 Why {row["origin_country"]}? — The Story Behind the Numbers</h4>'
        f'<p><b>Reason category:</b> {row["reason_category"]}</p>'
        f'<p style="margin-top:0.6rem;">{row["key_context"]}</p>'
        + us_context_block
        + (
            f'<p style="margin-top:0.8rem;color:#e8c860;font-size:0.85rem;">'
            f'⚡ <b>US foreign policy connection detected</b> — this migration flow is linked to '
            f'direct or indirect US involvement in the origin country.</p>'
            if us_connection else ""
        )
        + '</div>',
        unsafe_allow_html=True,
    )

else:
    # All-countries story wall — sorted by migrants_in_us desc
    st.markdown(
        "Select a country in the sidebar for a deep-dive. "
        "Below: key context stories for all visible countries."
    )

    # US foreign policy flag
    show_us_link = st.checkbox("🔍 Highlight US foreign-policy-linked flows only", value=False)

    story_df = dff.copy()
    if show_us_link:
        us_kw = ["us ", "u.s.", "american", "united states", "foreign policy",
                 "cold war", "intervention", "cia", "sanctions", "occupation", "military", "war on"]
        def _has_us_link(row):
            ctx = str(row.get("us_context", "")).strip().lower()
            key = str(row.get("key_context", "")).lower()
            return (
                ctx not in ("", "n/a", "nan")
                or any(kw in key for kw in us_kw)
            )
        story_df = story_df[story_df.apply(_has_us_link, axis=1)]

    story_df = story_df.sort_values("migrants_in_us", ascending=False)

    for _, row in story_df.iterrows():
        ptype = row["pathway_type"]
        has_us_ctx = (
            isinstance(row.get("us_context"), str)
            and row["us_context"].strip().lower() not in ("", "n/a", "nan")
        )
        us_link = has_us_ctx or any(
            kw in row["key_context"].lower()
            for kw in ["us ", "u.s.", "american", "united states", "foreign policy",
                       "cold war", "intervention", "cia", "sanctions", "occupation", "military"]
        )
        flag = " ⚡" if us_link else ""

        us_ctx_html = (
            f'<p style="margin-top:0.6rem;padding:0.5rem 0.7rem;'
            f'background:rgba(60,120,220,0.08);border-left:3px solid rgba(60,120,220,0.4);'
            f'border-radius:4px;font-size:0.85rem;color:#b8d0f0;">'
            f'🇺🇸 {row["us_context"]}</p>'
            if has_us_ctx else ""
        )

        st.markdown(
            f'<div class="story-card">'
            f'<h4>{row["origin_country"]}{flag} &nbsp; {badge(ptype)}'
            f' &nbsp; <span style="font-size:0.85rem;color:{MUTED};font-weight:400;font-family:Source Sans 3">'
            f'{row["reason_category"]} · {fmt_num(row["migrants_in_us"])} in US</span></h4>'
            f'<p>{row["key_context"]}</p>'
            + us_ctx_html
            + '</div>',
            unsafe_allow_html=True,
        )

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 8 — METHODOLOGY / DESIGN PRINCIPLES NOTE
# ──────────────────────────────────────────────────────────────────────────────
with st.expander("ℹ️ Design Principles & Methodology"):
    st.markdown("""
**Graphical Integrity (Tufte)** — Bubble sizes are scaled by √(migrants in US), not raw counts.
Because the eye reads *area*, not radius, square-root scaling keeps proportional relationships honest
while still communicating magnitude.

**Data-Ink Ratio (Tufte)** — Every chart strips decorative elements. No grid-lines unless they carry
information, no tick marks unless needed for reading, muted country borders and ocean fills exist
only to orient the eye.

**Narrative Visualization (Segel & Heer)** — The app follows a *martini glass* structure: an
authored global overview (map, breakdown charts) that hands progressive control to the reader via
filters, the pathway/reason panels, and finally the story cards which surface the `key_context`
narrative layer.

**Semiotics & Color (Ware + Silva et al.)** — Three colors encode pathway type consistently across
every view: 🔴 Humanitarian, 🔵 Legal, 🟡 Mixed. Color carries emotional weight intentionally —
red signals urgency aligned with how audiences read crisis.

**Reducing Cognitive Load (Mayer & Moreno)** — Progressive disclosure via tabs, filters, and the
country selector prevents information overload. The story panel is the reward for narrowing focus.

**Data sources:** ESS Final Project Dataset (59 origin countries). US population denominator: 335M (2024 est.).
    """)
