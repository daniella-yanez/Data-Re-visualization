import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Immigrants in the U.S. — Stories Behind the Numbers",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #f9f8f5; }
[data-testid="stSidebar"] { background: #ffffff; border-right: 1px solid #e8e4dc; }
h1 { font-size: 1.8rem !important; font-weight: 600 !important; color: #1a1a1a !important; }
h2 { font-size: 1.2rem !important; font-weight: 500 !important; color: #333 !important; }
.metric-card {
    background: white; border-radius: 10px; padding: 1rem 1.25rem;
    border: 1px solid #e8e4dc; margin-bottom: 0.5rem;
}
.metric-label { font-size: 0.72rem; color: #888; text-transform: uppercase; letter-spacing: .05em; margin-bottom: 2px; }
.metric-value { font-size: 1.6rem; font-weight: 600; color: #1a1a1a; }
.story-card {
    background: white; border-radius: 12px; padding: 1.25rem 1.5rem;
    border: 1px solid #e8e4dc; border-left: 5px solid #2471a3;
    margin-bottom: 1rem;
}
.story-card.humanitarian { border-left-color: #c0392b; }
.story-card.legal        { border-left-color: #2471a3; }
.story-card.mixed        { border-left-color: #d68910; }
.tag {
    display: inline-block; font-size: 0.7rem; padding: 2px 9px;
    border-radius: 12px; font-weight: 500; margin-right: 4px;
}
.tag-humanitarian { background: #fadbd8; color: #922b21; }
.tag-legal        { background: #d6eaf8; color: #1a5276; }
.tag-mixed        { background: #fdebd0; color: #9a6304; }
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    data = [
        {"country":"Afghanistan","immigrants":199000,"pathway_type":"Humanitarian","reason":"Conflict/War","pathways":"Humanitarian Parole; SIV; Refugee","context":"Post-2021 evacuation surge and status uncertainty. Tens of thousands arrived in Operation Allies Welcome after the fall of Kabul — many still navigating uncertain legal status.","lat":33.9,"lon":67.7},
        {"country":"Argentina","immigrants":212000,"pathway_type":"Legal","reason":"Economic","pathways":"Employment; Investor; Family","context":"Professionals fleeing hyperinflation and economic collapse. Many are highly educated — engineers, architects, doctors — drawn by stable U.S. wages.","lat":-34.6,"lon":-58.4},
        {"country":"Bangladesh","immigrants":358000,"pathway_type":"Mixed","reason":"Economic/Political","pathways":"Family; Asylum; Irregular","context":"A winding journey: many travel through South America, then walk the Darién Gap to reach the U.S. border. Economic hardship and political instability drive an increasingly dangerous route.","lat":23.7,"lon":90.4},
        {"country":"Brazil","immigrants":739000,"pathway_type":"Mixed","reason":"Economic","pathways":"Family; Work; Irregular","context":"'Yo-yo migration' — Brazilians often migrate, return home, then migrate again following U.S. labor demand cycles. A flexible diaspora responsive to two economies.","lat":-15.8,"lon":-47.9},
        {"country":"Cambodia","immigrants":171000,"pathway_type":"Humanitarian","reason":"Conflict","pathways":"Refugee; Family","context":"Khmer Rouge survivors and their descendants. Most arrived as refugees in the 1980s after the genocide; today their U.S.-born children are keeping communities alive.","lat":11.6,"lon":104.9},
        {"country":"Canada","immigrants":950000,"pathway_type":"Legal","reason":"Economic","pathways":"TN Visa; Work; Family","context":"Cross-border professional mobility — NAFTA/USMCA's TN visa makes skilled movement seamless. Canada's proximity and cultural similarity make the U.S. a natural destination.","lat":56.1,"lon":-106.3},
        {"country":"China","immigrants":2489000,"pathway_type":"Mixed","reason":"Economic/Political","pathways":"Student; Work; Asylum","context":"Dual streams: educated professionals and students through formal channels, and a rising wave of asylum seekers crossing at the southern border — fleeing censorship, repression, and hopelessness.","lat":35.9,"lon":104.2},
        {"country":"China, Hong Kong SAR","immigrants":269000,"pathway_type":"Mixed","reason":"Economic/Political","pathways":"Employment; Student; Family; Asylum","context":"Post-2020 political shift defines everything. After Beijing's crackdown on democracy protests, emigration surged. Many were professionals who had never considered leaving.","lat":22.3,"lon":114.2},
        {"country":"Colombia","immigrants":1009000,"pathway_type":"Legal","reason":"Family","pathways":"Family reunification","context":"High naturalization rates and chain migration. Decades of community-building mean each new immigrant has family already here. The U.S.-Colombia pipeline is now self-sustaining.","lat":4.7,"lon":-74.1},
        {"country":"Cuba","immigrants":1395000,"pathway_type":"Humanitarian","reason":"Political","pathways":"Humanitarian; Family","context":"The Cuban Adjustment Act grants unique legal status unavailable to other nationalities. A legacy of Cold War politics means Cubans have a faster path to residency than most.","lat":23.1,"lon":-82.4},
        {"country":"Dominican Republic","immigrants":1483000,"pathway_type":"Legal","reason":"Family","pathways":"Family reunification","context":"One of the oldest, most established Latino diasporas. Chain migration networks that go back generations — when one person gets a green card, an entire extended family follows.","lat":18.7,"lon":-70.2},
        {"country":"Ecuador","immigrants":562000,"pathway_type":"Mixed","reason":"Economic/Political","pathways":"Family; Irregular; Asylum","context":"Rising migration through the U.S.-Mexico border. Ecuador's violent crime surge and economic instability have pushed more Ecuadorians onto the dangerous overland route north.","lat":-1.8,"lon":-78.2},
        {"country":"Egypt","immigrants":263000,"pathway_type":"Legal","reason":"Economic","pathways":"Employment; Family; Diversity Visa","context":"Skilled professionals and visa lottery winners. Egypt is a consistent participant in the Diversity Visa program — giving ordinary people a genuine shot at immigration.","lat":26.8,"lon":30.8},
        {"country":"El Salvador","immigrants":1570000,"pathway_type":"Mixed","reason":"Economic/Violence","pathways":"Family; TPS; Irregular","context":"Temporary Protected Status (TPS) has kept hundreds of thousands in legal limbo for decades. Originally granted after a 2001 earthquake, TPS renewals have been politically contentious ever since.","lat":13.8,"lon":-88.9},
        {"country":"Ethiopia","immigrants":364000,"pathway_type":"Humanitarian","reason":"Conflict/Political","pathways":"Refugee; Asylum; Family","context":"Waves of refugees fleeing the Tigray conflict and political repression. Ethiopia sends some of the most highly educated African immigrants to the U.S. alongside those fleeing violence.","lat":9.1,"lon":40.5},
        {"country":"France","immigrants":253000,"pathway_type":"Legal","reason":"Economic","pathways":"Employment; Student","context":"Professional and educational mobility between two culturally close nations. Many are artists, academics, and business professionals drawn by U.S. opportunity.","lat":46.2,"lon":2.2},
        {"country":"Germany","immigrants":1138000,"pathway_type":"Legal","reason":"Economic","pathways":"Employment; Student","context":"A long history of skilled labor mobility — this community reflects both mid-20th-century postwar migration and modern professional movement.","lat":51.2,"lon":10.5},
        {"country":"Ghana","immigrants":258000,"pathway_type":"Legal","reason":"Economic","pathways":"Diversity Visa; Family; Employment","context":"Ghana punches above its weight in the Diversity Visa lottery. Highly educated Ghanaian immigrants — nurses, engineers, professors — are a cornerstone of African diaspora in the U.S.","lat":7.9,"lon":-1.0},
        {"country":"Greece","immigrants":131000,"pathway_type":"Legal","reason":"Economic","pathways":"Family; Employment","context":"A diaspora shaped by 20th-century labor migration. Greek communities in cities like Chicago and New York have been passing down citizenship for generations.","lat":39.1,"lon":21.8},
        {"country":"Guatemala","immigrants":1299000,"pathway_type":"Mixed","reason":"Economic/Violence","pathways":"Family; Irregular; Temporary Work","context":"Seasonal agricultural workers and families fleeing gang violence. Many are Indigenous Maya from highland communities — speaking Mam or K'iche' rather than Spanish — largely invisible in immigration statistics.","lat":15.8,"lon":-90.2},
        {"country":"Guyana","immigrants":315000,"pathway_type":"Legal","reason":"Economic","pathways":"Family; Employment","context":"Steady diaspora-driven migration since the 1970s. Guyanese-Americans are a tight-knit community — concentrated in New York — with high rates of homeownership and civic participation.","lat":4.9,"lon":-58.9},
        {"country":"Haiti","immigrants":798000,"pathway_type":"Humanitarian","reason":"Political/Disaster","pathways":"Humanitarian parole; TPS; Family","context":"Multiple catastrophes layered on top of each other: the 2010 earthquake, presidential assassination, gang takeovers. Each crisis sent a new wave. Haitian TPS is among the most politically contested.","lat":18.9,"lon":-72.3},
        {"country":"Honduras","immigrants":935000,"pathway_type":"Mixed","reason":"Economic/Violence","pathways":"Family; TPS; Irregular","context":"Among the world's highest homicide rates push families north. Many travel in caravans for safety — the journey itself is perilous, with exploitation and kidnapping at every border.","lat":15.2,"lon":-86.2},
        {"country":"India","immigrants":3165000,"pathway_type":"Legal","reason":"Economic","pathways":"H-1B; Student; Family","context":"The dominant story of H-1B visa backlogs: Indian professionals wait decades for green cards due to per-country limits. It is the world's longest documented employment-based immigration queue.","lat":20.6,"lon":78.9},
        {"country":"Iran","immigrants":431000,"pathway_type":"Mixed","reason":"Political","pathways":"Employment; Family; Asylum","context":"Migration shaped by political crises since 1979. The Iranian-American community includes Nobel laureates, Fortune 500 executives — and asylum seekers fleeing the Islamic Republic.","lat":32.4,"lon":53.7},
        {"country":"Iraq","immigrants":272000,"pathway_type":"Humanitarian","reason":"Conflict/War","pathways":"Refugee; Special Immigrant Visa","context":"Special Immigrant Visas for interpreters and embassy staff who risked their lives working with U.S. forces. A debt of honor — but one the U.S. has been slow to pay, with long waits and backlogs.","lat":33.2,"lon":43.7},
        {"country":"Ireland","immigrants":126000,"pathway_type":"Legal","reason":"Economic","pathways":"Employment; Student","context":"The Irish diaspora in America is among the oldest and most politically powerful. Modern Irish immigration is a trickle compared to the Famine era — but the cultural ties remain deep.","lat":53.4,"lon":-8.2},
        {"country":"Israel","immigrants":170000,"pathway_type":"Legal","reason":"Economic","pathways":"Family; Student; Employment","context":"High-skilled and education-based migration. Israeli-Americans are among the most highly educated immigrant groups — with a two-way brain circulation between Tel Aviv and Silicon Valley.","lat":31.5,"lon":34.8},
        {"country":"Italy","immigrants":361000,"pathway_type":"Legal","reason":"Economic","pathways":"Family; Employment","context":"Established diaspora networks from waves of 20th-century migration. Italian-Americans are one of America's largest ancestry groups — today's immigrants join a community already deeply woven into U.S. identity.","lat":42.8,"lon":12.8},
        {"country":"Jamaica","immigrants":911000,"pathway_type":"Legal","reason":"Economic","pathways":"Family; Employment","context":"Longstanding Caribbean migration systems — nurses, teachers, and domestic workers building families across two countries. Jamaica's remittance economy depends on those who left.","lat":18.1,"lon":-77.3},
        {"country":"Japan","immigrants":547000,"pathway_type":"Legal","reason":"Economic","pathways":"Employment; Student","context":"Corporate transfers and education pathways dominate. Japanese immigration has a different character — often temporary, often highly skilled, often tied to multinational companies.","lat":36.2,"lon":138.3},
        {"country":"Kenya","immigrants":211000,"pathway_type":"Legal","reason":"Economic","pathways":"Diversity Visa; Employment; Family","context":"Among the most highly educated African immigrant groups in the U.S. Kenyan doctors, nurses, and engineers are a significant export — and a significant loss for Kenya's own development.","lat":-0.0,"lon":37.9},
        {"country":"Korea, Rep.","immigrants":1083000,"pathway_type":"Legal","reason":"Economic","pathways":"Family; Employment; Student","context":"Long-established communities — Koreatown in LA is a city within a city. Korean immigration combines high professional achievement with vibrant small-business ownership across the country.","lat":36.0,"lon":127.7},
        {"country":"Lao PDR","immigrants":177000,"pathway_type":"Humanitarian","reason":"Conflict","pathways":"Refugee; Family","context":"Post-war refugee resettlement from the Vietnam War era. The Hmong and Lao communities in Minnesota and California are the living legacy of U.S. military intervention in Southeast Asia.","lat":17.9,"lon":102.6},
        {"country":"Lebanon","immigrants":150000,"pathway_type":"Legal","reason":"Economic/Political","pathways":"Family; Employment; Asylum","context":"A diaspora anchored in earlier waves — Lebanese-Americans have been here since the 1800s. Today, Lebanon's economic collapse is sending a new generation.","lat":33.9,"lon":35.5},
        {"country":"Mexico","immigrants":11280000,"pathway_type":"Mixed","reason":"Economic","pathways":"Family; Temporary Work; Irregular; DACA","context":"The world's single largest bilateral migration corridor. 11+ million people — about 1 in every 4 immigrants in the U.S. DACA protects ~580,000 Dreamers who grew up entirely American.","lat":23.6,"lon":-102.6},
        {"country":"Myanmar","immigrants":200000,"pathway_type":"Humanitarian","reason":"Conflict","pathways":"Refugee; Asylum","context":"Ongoing refugee resettlement from multiple waves of conflict. Rohingya genocide survivors sit alongside earlier Karen and Kachin refugees — communities separated by ethnicity but united by displacement.","lat":17.1,"lon":96.0},
        {"country":"Nepal","immigrants":264000,"pathway_type":"Legal","reason":"Economic","pathways":"Diversity Visa; Student; Family","context":"Heavy reliance on the visa lottery — Nepal has leveraged the Diversity Visa program more than almost any other country relative to its size. Education and family reunification follow.","lat":28.4,"lon":84.1},
        {"country":"Nicaragua","immigrants":295000,"pathway_type":"Mixed","reason":"Political","pathways":"Humanitarian parole; Asylum; Family","context":"Recent surge tied to authoritarian repression under Ortega. Dissidents, journalists, and clergy are among those seeking asylum — a politically charged community in a politically charged moment.","lat":12.9,"lon":-85.2},
        {"country":"Nigeria","immigrants":565000,"pathway_type":"Legal","reason":"Economic","pathways":"Employment; Student; Diversity Visa","context":"The fastest-growing African immigrant group in the U.S. Nigerian-Americans have the highest educational attainment of any immigrant group — and face the sharpest disconnect between credentials and recognition.","lat":9.1,"lon":8.7},
        {"country":"Pakistan","immigrants":453000,"pathway_type":"Mixed","reason":"Economic/Political","pathways":"Family; Employment; Asylum","context":"A mix of highly-skilled tech workers and asylum claims from those fleeing religious persecution or political violence. Pakistani-Americans navigate a complex relationship between two countries in tension.","lat":30.4,"lon":69.3},
        {"country":"Panama","immigrants":162000,"pathway_type":"Legal","reason":"Economic","pathways":"Employment; Family","context":"Smaller professional migration flows with deep historical ties — the Panama Canal era created lasting connections between Panamanian and American families.","lat":8.6,"lon":-80.1},
        {"country":"Peru","immigrants":512000,"pathway_type":"Legal","reason":"Economic","pathways":"Family; Employment; Student","context":"Urban and skilled migration patterns. Peruvians in the U.S. are concentrated in professional fields — a community that defies the homogenizing Latin America immigrant narrative.","lat":-9.2,"lon":-75.0},
        {"country":"Philippines","immigrants":2264000,"pathway_type":"Legal","reason":"Economic","pathways":"Family; Employment (Healthcare)","context":"The backbone of U.S. healthcare. Filipino nurses, doctors, and caregivers staff hospitals and nursing homes nationwide — a deliberate U.S. recruitment policy that began in the 1960s and never stopped.","lat":12.9,"lon":121.8},
        {"country":"Poland","immigrants":397000,"pathway_type":"Legal","reason":"Economic","pathways":"Employment; Diversity Visa","context":"Labor mobility and visa lottery. Polish-Americans have a long presence in Rust Belt cities — today's arrivals are professionals and trade workers joining established community networks.","lat":52.1,"lon":19.1},
        {"country":"Portugal","immigrants":142000,"pathway_type":"Legal","reason":"Economic","pathways":"Family; Employment","context":"Longstanding migration networks, especially in New England. Portuguese-American fishing and manufacturing communities in Massachusetts go back over a century.","lat":39.4,"lon":-8.2},
        {"country":"Puerto Rico","immigrants":1925000,"pathway_type":"Legal","reason":"Economic","pathways":"Internal migration (U.S. citizens)","context":"Not international immigration — Puerto Ricans are U.S. citizens moving within their own country. But they face unemployment, colonial status, and post-hurricane displacement that drives movement to the mainland.","lat":18.2,"lon":-66.5},
        {"country":"Romania","immigrants":178000,"pathway_type":"Legal","reason":"Economic","pathways":"Employment; Diversity Visa","context":"Post-EU mobility patterns — skilled IT workers and healthcare professionals feature prominently alongside visa lottery participants.","lat":45.9,"lon":24.9},
        {"country":"Russian Federation","immigrants":453000,"pathway_type":"Mixed","reason":"Political/Economic","pathways":"Asylum; Employment; Family","context":"Surge in asylum claims since 2022 Ukraine invasion and mobilization. Russians who opposed the war or feared conscription arrived at the U.S.-Mexico border in unprecedented numbers.","lat":61.5,"lon":105.3},
        {"country":"South Africa","immigrants":162000,"pathway_type":"Legal","reason":"Economic","pathways":"Employment; Family; Student","context":"Skilled migration with smaller flows. Both white and Black South African professionals are drawn by opportunity — sometimes pushed by violence or deep uncertainty about the future.","lat":-30.6,"lon":22.9},
        {"country":"Spain","immigrants":169000,"pathway_type":"Legal","reason":"Economic","pathways":"Employment; Student","context":"Professional and educational migration following Spain's economic crisis. Young Spaniards who couldn't find jobs in a 25%-unemployment economy turned to the U.S.","lat":40.5,"lon":-3.7},
        {"country":"Taiwan","immigrants":404000,"pathway_type":"Legal","reason":"Economic","pathways":"Student; Employment; Family","context":"High-skilled tech migration and education. Taiwan's contribution to Silicon Valley is outsized — engineers and entrepreneurs who built the semiconductor supply chain that powers the modern world.","lat":23.7,"lon":120.9},
        {"country":"Thailand","immigrants":308000,"pathway_type":"Legal","reason":"Economic","pathways":"Family; Employment","context":"Family reunification dominant — many Thai women married U.S. servicemen during the Vietnam War era, and their descendants have built lasting community networks.","lat":15.9,"lon":100.9},
        {"country":"Trinidad and Tobago","immigrants":242000,"pathway_type":"Legal","reason":"Economic","pathways":"Family; Employment","context":"Caribbean diaspora migration with high educational attainment. Trinidadian-Americans are among the most economically successful Caribbean immigrant groups in the U.S.","lat":10.7,"lon":-61.2},
        {"country":"Türkiye","immigrants":176000,"pathway_type":"Legal","reason":"Economic/Political","pathways":"Employment; Student; Family","context":"Skilled migration and political asylum combined. Turkish academics, journalists, and opposition figures have joined an already-established professional immigrant community.","lat":38.9,"lon":35.2},
        {"country":"Ukraine","immigrants":448000,"pathway_type":"Humanitarian","reason":"Conflict/War","pathways":"Humanitarian parole; TPS; Refugee","context":"War-driven displacement after Russia's 2022 full-scale invasion. The Uniting for Ukraine humanitarian parole program was created specifically for this crisis — by 2024 over 200,000 Ukrainians arrived.","lat":48.4,"lon":31.2},
        {"country":"United Kingdom","immigrants":895000,"pathway_type":"Legal","reason":"Economic","pathways":"Employment; Student; Family","context":"High-skilled and educational migration in both directions. British and American professionals move fluidly between two culturally close countries — but post-Brexit uncertainty has changed the calculus.","lat":55.4,"lon":-3.4},
        {"country":"Venezuela","immigrants":764000,"pathway_type":"Humanitarian","reason":"Political/Economic crisis","pathways":"TPS; Asylum; Humanitarian Parole","context":"Rapid growth due to national collapse under Maduro. A country that was once one of South America's wealthiest has seen millions flee hunger, blackouts, repression, and the world's largest hyperinflation.","lat":6.4,"lon":-66.6},
        {"country":"Vietnam","immigrants":1435000,"pathway_type":"Mixed","reason":"Conflict/Economic","pathways":"Family; Refugee legacy; Employment","context":"Post-war migration that never stopped. First came refugees from the Fall of Saigon; then Orderly Departure families; now economic migrants. Vietnamese-Americans carry the full arc of U.S. foreign policy history.","lat":14.1,"lon":108.3},
    ]
    return pd.DataFrame(data)

df = load_data()

COLORS = {"Humanitarian": "#c0392b", "Legal": "#2471a3", "Mixed": "#d68910"}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🌍 Immigrants in the U.S.")
    st.markdown("*Stories behind the numbers*")
    st.divider()

    pathway_filter = st.radio(
        "Filter by pathway type",
        ["All", "Humanitarian", "Legal", "Mixed"],
        index=0
    )

    st.divider()
    st.markdown("**Search for a country**")
    search = st.selectbox(
        "Select a country",
        ["— choose one —"] + sorted(df["country"].tolist()),
        label_visibility="collapsed"
    )

    st.divider()
    st.markdown(
        "<small style='color:#aaa'>Data covers 59 origin countries.<br>"
        "Hover map bubbles to explore.<br>"
        "Click a country in the list for its full story.</small>",
        unsafe_allow_html=True
    )

# ── Filter data ───────────────────────────────────────────────────────────────
filtered = df if pathway_filter == "All" else df[df["pathway_type"] == pathway_filter]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("## Immigrants in the United States")
st.markdown(
    "<p style='color:#666;font-size:0.95rem;margin-top:-0.5rem;margin-bottom:1.2rem'>"
    "Each bubble is a country. Each country is millions of stories — of conflict, opportunity, family, and survival."
    "</p>",
    unsafe_allow_html=True
)

# ── Metric row ────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Countries shown", len(filtered))
with c2:
    total = filtered["immigrants"].sum()
    st.metric("Total immigrants", f"{total/1e6:.1f}M")
with c3:
    largest = filtered.loc[filtered["immigrants"].idxmax(), "country"]
    st.metric("Largest origin", largest)
with c4:
    hum_pct = len(filtered[filtered["pathway_type"]=="Humanitarian"]) / max(len(filtered),1) * 100
    st.metric("Humanitarian pathways", f"{hum_pct:.0f}%")

st.divider()

# ── World bubble map ──────────────────────────────────────────────────────────
fig_map = go.Figure()

for pt, color in COLORS.items():
    sub = filtered[filtered["pathway_type"] == pt]
    if sub.empty:
        continue
    fig_map.add_trace(go.Scattergeo(
        lat=sub["lat"],
        lon=sub["lon"],
        mode="markers",
        name=pt,
        marker=dict(
            size=sub["immigrants"].apply(lambda x: max(6, min(55, (x**0.45) / 22))),
            color=color,
            opacity=0.75,
            line=dict(width=1, color=color),
            sizemode="diameter",
        ),
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "%{customdata[1]:,} immigrants<br>"
            "<i>%{customdata[2]}</i><br>"
            "<br>%{customdata[3]}<extra></extra>"
        ),
        customdata=sub[["country","immigrants","reason","context"]].values,
        showlegend=True,
    ))

fig_map.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=True,
        coastlinecolor="#c8dce8",
        showland=True,
        landcolor="#e8f4f8",
        showocean=True,
        oceancolor="#d0e8f2",
        showcountries=True,
        countrycolor="#b0ccd8",
        projection_type="natural earth",
        bgcolor="rgba(0,0,0,0)",
    ),
    legend=dict(
        title="Pathway type",
        orientation="h",
        yanchor="bottom", y=1.01,
        xanchor="left", x=0,
        font=dict(size=12),
    ),
    margin=dict(l=0, r=0, t=30, b=0),
    height=460,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
)

st.plotly_chart(fig_map, use_container_width=True)

st.divider()

# ── Bottom section: bar chart + country detail ────────────────────────────────
col_bar, col_detail = st.columns([1.2, 1])

with col_bar:
    st.markdown("#### Top countries by immigrant population")
    top_n = st.slider("Show top N countries", min_value=5, max_value=len(filtered), value=min(20, len(filtered)), step=1)
    top = filtered.nlargest(top_n, "immigrants")

    fig_bar = go.Figure(go.Bar(
        x=top["immigrants"],
        y=top["country"],
        orientation="h",
        marker_color=[COLORS[pt] for pt in top["pathway_type"]],
        hovertemplate="<b>%{y}</b><br>%{x:,} immigrants<extra></extra>",
        text=top["immigrants"].apply(lambda x: f"{x/1e6:.2f}M" if x>=1e6 else f"{x/1e3:.0f}K"),
        textposition="outside",
    ))
    fig_bar.update_layout(
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(autorange="reversed", tickfont=dict(size=11)),
        margin=dict(l=0, r=60, t=10, b=10),
        height=max(350, top_n * 28),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_detail:
    st.markdown("#### Country story")

    # Determine which country to show
    if search != "— choose one —":
        selected_country = search
    else:
        selected_country = filtered.nlargest(1, "immigrants").iloc[0]["country"] if not filtered.empty else None

    if selected_country:
        row = df[df["country"] == selected_country]
        if not row.empty:
            row = row.iloc[0]
            pt = row["pathway_type"]
            pt_class = pt.lower()

            st.markdown(f"""
            <div class="story-card {pt_class}">
                <div style="font-size:1.1rem;font-weight:600;color:#1a1a1a;margin-bottom:6px">{row['country']}</div>
                <div style="margin-bottom:10px">
                    <span class="tag tag-{pt_class}">{pt}</span>
                    <span style="font-size:0.75rem;color:#888">{row['reason']}</span>
                </div>
                <div style="font-size:1.6rem;font-weight:600;color:#1a1a1a;margin-bottom:10px">
                    {row['immigrants']:,}
                </div>
                <div style="font-size:0.8rem;color:#888;margin-bottom:10px">
                    <b>Main pathways:</b> {row['pathways']}
                </div>
                <div style="font-size:0.88rem;color:#444;line-height:1.65">
                    {row['context']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown(
        "<small style='color:#aaa'>Use the search dropdown on the left to explore any country's story.</small>",
        unsafe_allow_html=True
    )

# ── Reason breakdown chart ────────────────────────────────────────────────────
st.divider()
st.markdown("#### Why people leave — migration reason breakdown")

reason_totals = (
    filtered.groupby("reason")["immigrants"]
    .sum()
    .reset_index()
    .sort_values("immigrants", ascending=True)
)

color_map = {
    "Economic": "#2471a3",
    "Family": "#1a9e75",
    "Political": "#c0392b",
    "Conflict/War": "#922b21",
    "Economic/Violence": "#d68910",
    "Economic/Political": "#8e44ad",
    "Political/Disaster": "#e74c3c",
    "Conflict": "#e67e22",
    "Conflict/Political": "#a93226",
    "Conflict/Economic": "#ba4a00",
    "Political/Economic": "#7d6608",
    "Political/Economic crisis": "#b03a2e",
}
bar_colors = [color_map.get(r, "#888") for r in reason_totals["reason"]]

fig_reason = go.Figure(go.Bar(
    x=reason_totals["immigrants"],
    y=reason_totals["reason"],
    orientation="h",
    marker_color=bar_colors,
    text=reason_totals["immigrants"].apply(lambda x: f"{x/1e6:.1f}M" if x>=1e6 else f"{x/1e3:.0f}K"),
    textposition="outside",
    hovertemplate="<b>%{y}</b><br>%{x:,} immigrants<extra></extra>",
))
fig_reason.update_layout(
    xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
    yaxis=dict(tickfont=dict(size=11)),
    margin=dict(l=0, r=80, t=10, b=10),
    height=380,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    showlegend=False,
)
st.plotly_chart(fig_reason, use_container_width=True)

st.markdown(
    "<p style='font-size:0.78rem;color:#aaa;text-align:center;margin-top:-1rem'>"
    "Numbers represent immigrants in the U.S. by primary reason category for each origin country."
    "</p>",
    unsafe_allow_html=True
)
