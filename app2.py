import streamlit as st
import pandas as pd
import numpy as np
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
.us-flag { font-size: 0.75rem; background: #fff3cd; color: #7d5200;
           border: 1px solid #f0c040; border-radius: 8px;
           padding: 2px 8px; margin-left: 4px; }
.context-section { margin-top: 0.6rem; }
.context-label { font-size: 0.7rem; font-weight: 600; text-transform: uppercase;
                 letter-spacing: 0.07em; color: #999; margin-bottom: 2px; }
.context-body { font-size: 0.88rem; color: #444; line-height: 1.65; }
.us-context-box {
    margin-top: 0.75rem; background: #fffbf0; border-left: 3px solid #e6a817;
    border-radius: 0 8px 8px 0; padding: 0.6rem 0.9rem;
}
.us-context-box .context-label { color: #9a6304; }
.us-context-box .context-body  { color: #5a4010; font-size: 0.86rem; }
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
# NOTE: Coordinates are HARDCODED here with verified geographic centers.
# The Excel source file contains scrambled lat/lon values and must NOT be used
# for map placement. These values are ground-truthed against standard references.
@st.cache_data
def load_data():
    data = [
        {
            "country": "Afghanistan",
            "immigrants": 199000,
            "pathway_type": "Humanitarian",
            "reason": "Conflict/War",
            "pathways": "Humanitarian Parole; SIV; Refugee",
            "context": (
                "Post-2021 evacuation surge and deep legal uncertainty. When Kabul fell in August 2021, "
                "the U.S. conducted one of the largest airlifts in history — roughly 124,000 people evacuated "
                "in two weeks. Many arrived under Humanitarian Parole, a temporary status that does not "
                "automatically lead to a green card, leaving tens of thousands in a legal gray zone."
            ),
            "us_context": (
                "This migration is a direct consequence of 20 years of U.S. military presence in Afghanistan "
                "(2001–2021). Interpreters, embassy staff, and military contractors who worked alongside "
                "U.S. forces qualify for Special Immigrant Visas (SIVs) — a formal acknowledgment of U.S. "
                "obligation. The chaotic withdrawal and subsequent Taliban takeover created the crisis that "
                "drove the 2021 surge."
            ),
            "lat": 33.9, "lon": 67.7
        },
        {
            "country": "Argentina",
            "immigrants": 212000,
            "pathway_type": "Legal",
            "reason": "Economic",
            "pathways": "Employment; Investor; Family",
            "context": (
                "Professionals fleeing serial economic collapse. Argentina has experienced multiple currency "
                "crises, sovereign defaults, and hyperinflation cycles. Many immigrants are highly educated "
                "— engineers, architects, doctors — drawn by the stability of U.S. wages and a dollar-based "
                "economy. The Argentine-American community is concentrated in Miami and New York."
            ),
            "us_context": None,
            "lat": -38.4, "lon": -63.6
        },
        {
            "country": "Bangladesh",
            "immigrants": 358000,
            "pathway_type": "Mixed",
            "reason": "Economic/Political",
            "pathways": "Family; Asylum; Irregular",
            "context": (
                "A winding, dangerous route: many Bangladeshi migrants travel through the Middle East, "
                "then South America, then walk the Darién Gap to reach the U.S. southern border. "
                "Economic hardship, political instability, and limited formal visa options push an "
                "increasingly large cohort onto irregular pathways. New York City's Jackson Heights "
                "and the Bronx are home to large established Bangladeshi communities."
            ),
            "us_context": None,
            "lat": 23.7, "lon": 90.4
        },
        {
            "country": "Brazil",
            "immigrants": 739000,
            "pathway_type": "Mixed",
            "reason": "Economic",
            "pathways": "Family; Work; Irregular",
            "context": (
                "'Yo-yo migration' — Brazilians often migrate to the U.S., return home when the Brazilian "
                "economy improves, then migrate again when U.S. labor demand rises. This flexible pattern "
                "is unusually responsive to both countries' economic cycles. Concentrated in Massachusetts "
                "(especially Framingham), Florida, and New Jersey."
            ),
            "us_context": None,
            "lat": -14.2, "lon": -51.9
        },
        {
            "country": "Cambodia",
            "immigrants": 171000,
            "pathway_type": "Humanitarian",
            "reason": "Conflict",
            "pathways": "Refugee; Family",
            "context": (
                "Khmer Rouge survivors and their descendants — a community forged in genocide. Most "
                "Cambodian-Americans arrived as refugees in the 1980s after the fall of the Khmer Rouge "
                "regime (1975–1979), which killed an estimated 2 million people. Communities in Lowell, "
                "Massachusetts and Long Beach, California carry this history."
            ),
            "us_context": (
                "U.S. foreign policy is central to understanding this migration. The Nixon administration's "
                "secret bombing campaigns of Cambodia (1969–1973) destabilized the country, contributing "
                "to the conditions that allowed the Khmer Rouge to seize power. The U.S. resettled "
                "Cambodian refugees partly as acknowledgment of that role."
            ),
            "lat": 12.6, "lon": 104.9
        },
        {
            "country": "Canada",
            "immigrants": 950000,
            "pathway_type": "Legal",
            "reason": "Economic",
            "pathways": "TN Visa; Work; Family",
            "context": (
                "Cross-border professional mobility enabled by treaty. The NAFTA/USMCA TN visa allows "
                "Canadian professionals — engineers, accountants, scientists, nurses — to work in the U.S. "
                "without a lengthy visa process. Canada's proximity, cultural similarity, and shared "
                "language make the U.S. a natural destination for career advancement."
            ),
            "us_context": None,
            "lat": 56.1, "lon": -106.3
        },
        {
            "country": "China",
            "immigrants": 2489000,
            "pathway_type": "Mixed",
            "reason": "Economic/Political",
            "pathways": "Student; Work; Asylum",
            "context": (
                "Dual streams that tell two stories. One: highly educated professionals and graduate "
                "students arriving through formal channels — a major driver of U.S. STEM research and "
                "technology sectors. Two: a rising wave of asylum seekers crossing at the U.S.-Mexico "
                "border, fleeing censorship, political repression, zero-COVID policies, and economic "
                "stagnation. In 2023, Chinese nationals became one of the top nationalities at the "
                "U.S. southern border."
            ),
            "us_context": (
                "U.S.-China trade and educational ties created the foundation for skilled migration. "
                "The H-1B visa pipeline and top university admissions have made China the #1 source "
                "of international students for decades. Simultaneously, U.S. asylum law provides a "
                "legal opening for those fleeing political persecution — including Uyghurs and "
                "Falun Gong practitioners."
            ),
            "lat": 35.9, "lon": 104.2
        },
        {
            "country": "China, Hong Kong SAR",
            "immigrants": 269000,
            "pathway_type": "Mixed",
            "reason": "Economic/Political",
            "pathways": "Employment; Student; Family; Asylum",
            "context": (
                "Post-2020 political rupture defines everything. After Beijing imposed the National Security "
                "Law in June 2020 — criminalizing dissent and dismantling Hong Kong's autonomy — emigration "
                "surged dramatically. Many were professionals, lawyers, journalists, and educators who "
                "had never considered leaving. The U.S. extended TPS-like protections for Hong Kongers "
                "in 2021."
            ),
            "us_context": (
                "The U.S. played a role in framing Hong Kong as a democracy worth protecting — the "
                "Hong Kong Human Rights and Democracy Act (2019) tied U.S.-Hong Kong trade relations "
                "to democratic freedoms. When Beijing's crackdown came, the U.S. became an explicit "
                "refuge. The State Department extended deferred enforced departure for Hong Kong "
                "residents in 2021."
            ),
            "lat": 22.3, "lon": 114.2
        },
        {
            "country": "Colombia",
            "immigrants": 1009000,
            "pathway_type": "Legal",
            "reason": "Family",
            "pathways": "Family reunification",
            "context": (
                "High naturalization rates and chain migration that is now self-sustaining. Decades of "
                "community-building — shaped by 1980s–90s displacement from conflict and the drug trade "
                "— mean each new immigrant arrives with family already here. Colombian-Americans are "
                "concentrated in Miami and New York, with high civic participation and naturalization rates."
            ),
            "us_context": (
                "The U.S.-Colombia relationship is deep and complex. Plan Colombia (2000), a $10+ billion "
                "U.S. anti-drug and security aid program, militarized large parts of rural Colombia. "
                "Displacement caused by counterinsurgency operations and crop eradication pushed many "
                "Colombians northward. The U.S.-Colombia Free Trade Agreement (2012) further integrated "
                "the two economies."
            ),
            "lat": 4.1, "lon": -72.3
        },
        {
            "country": "Cuba",
            "immigrants": 1395000,
            "pathway_type": "Humanitarian",
            "reason": "Political",
            "pathways": "Humanitarian; Family",
            "context": (
                "A unique legal status with no parallel. The Cuban Adjustment Act (1966) gives Cuban "
                "nationals a faster path to permanent residency than virtually any other nationality — "
                "a legacy of Cold War politics that has outlasted the Cold War itself. Cuban-Americans, "
                "concentrated in Miami, have become one of the most politically powerful immigrant "
                "communities in the U.S., influencing presidential elections."
            ),
            "us_context": (
                "Cuban migration is inseparable from U.S. foreign policy. The U.S.-backed Bay of Pigs "
                "invasion (1961), the Cuban Missile Crisis (1962), and decades of economic embargo "
                "under the Helms-Burton Act shaped both the political character of the Cuban state and "
                "the waves of people fleeing it. The Cuban Adjustment Act was explicitly designed to "
                "embarrass the Castro government by welcoming its citizens."
            ),
            "lat": 21.5, "lon": -79.5
        },
        {
            "country": "Dominican Republic",
            "immigrants": 1483000,
            "pathway_type": "Legal",
            "reason": "Family",
            "pathways": "Family reunification",
            "context": (
                "One of the oldest and most established Latino diasporas in the U.S. Chain migration "
                "networks go back generations — when one person naturalized, an entire extended family "
                "followed. Dominican-Americans are concentrated in New York City (particularly Washington "
                "Heights), with among the highest rates of remittances back to the island of any "
                "immigrant group."
            ),
            "us_context": (
                "U.S. intervention in the Dominican Republic shaped migration patterns directly. The "
                "U.S. military occupied the country from 1916–1924, and again in 1965 (Operation "
                "Power Pack), when President Johnson sent 42,000 troops to prevent a perceived "
                "communist takeover. That occupation accelerated emigration and established the "
                "New York–Santo Domingo corridor that still defines Dominican migration today."
            ),
            "lat": 18.7, "lon": -70.2
        },
        {
            "country": "Ecuador",
            "immigrants": 562000,
            "pathway_type": "Mixed",
            "reason": "Economic/Political",
            "pathways": "Family; Irregular; Asylum",
            "context": (
                "A rising and increasingly dangerous migration flow. Ecuador's violent crime surge — "
                "driven by cartel activity and political instability — has dramatically increased "
                "emigration through the U.S.-Mexico border. More Ecuadorians are now making the "
                "overland journey through the Darién Gap, one of the world's most dangerous migration "
                "routes. Concentrated in New York and New Jersey."
            ),
            "us_context": None,
            "lat": -1.8, "lon": -78.2
        },
        {
            "country": "Egypt",
            "immigrants": 263000,
            "pathway_type": "Legal",
            "reason": "Economic",
            "pathways": "Employment; Family; Diversity Visa",
            "context": (
                "Skilled professionals and visa lottery winners building a quiet but significant "
                "diaspora. Egypt is a consistent participant in the Diversity Visa (DV) lottery — "
                "giving ordinary Egyptians a genuine shot at immigration without family or employer "
                "sponsorship. Egyptian-Americans are disproportionately represented in engineering, "
                "medicine, and academia."
            ),
            "us_context": None,
            "lat": 26.8, "lon": 30.8
        },
        {
            "country": "El Salvador",
            "immigrants": 1570000,
            "pathway_type": "Mixed",
            "reason": "Economic/Violence",
            "pathways": "Family; TPS; Irregular",
            "context": (
                "Temporary Protected Status (TPS) has kept hundreds of thousands in legal limbo for "
                "over two decades. Originally granted after a devastating 2001 earthquake, TPS renewals "
                "have become a political football — with the Trump administration attempting to end it "
                "in 2018 and courts repeatedly blocking termination. Many TPS holders have lived in "
                "the U.S. for 20+ years and have U.S.-born children."
            ),
            "us_context": (
                "The U.S. civil war connection is foundational. During El Salvador's civil war "
                "(1979–1992), the U.S. provided over $1 billion in military aid to the government "
                "fighting leftist guerrillas — a conflict that killed 75,000 people and displaced "
                "millions. Many of today's Salvadoran-Americans are descendants of that displacement. "
                "Additionally, MS-13 — the gang whose violence now drives migration — was founded "
                "in Los Angeles by Salvadoran refugees and deported back to El Salvador in the 1990s."
            ),
            "lat": 13.8, "lon": -88.9
        },
        {
            "country": "Ethiopia",
            "immigrants": 364000,
            "pathway_type": "Humanitarian",
            "reason": "Conflict/Political",
            "pathways": "Refugee; Asylum; Family",
            "context": (
                "Waves of refugees from layered crises. The Tigray conflict (2020–2022) — one of the "
                "world's deadliest wars — displaced over 2 million people. Ethiopia also sends some "
                "of the most highly educated African immigrants to the U.S., creating an unusual "
                "combination: brain drain alongside refugee resettlement. The Ethiopian diaspora is "
                "politically active and closely watches domestic politics."
            ),
            "us_context": None,
            "lat": 9.1, "lon": 40.5
        },
        {
            "country": "France",
            "immigrants": 253000,
            "pathway_type": "Legal",
            "reason": "Economic",
            "pathways": "Employment; Student",
            "context": (
                "Professional and educational mobility between two historically close nations. "
                "French immigrants are heavily concentrated in arts, academia, and business — "
                "New York's French community is one of the largest outside France. Many arrive "
                "through multinational corporate transfers or elite university partnerships. "
                "Movement is often bidirectional."
            ),
            "us_context": None,
            "lat": 46.2, "lon": 2.2
        },
        {
            "country": "Germany",
            "immigrants": 1138000,
            "pathway_type": "Legal",
            "reason": "Economic",
            "pathways": "Employment; Student",
            "context": (
                "A layered history: mid-20th century postwar migration merged with modern professional "
                "movement. German-Americans are among the largest ancestry groups in the U.S. — a "
                "testament to 19th and 20th century waves. Today's German immigrants are largely "
                "skilled professionals and academics moving through corporate and university channels."
            ),
            "us_context": None,
            "lat": 51.2, "lon": 10.5
        },
        {
            "country": "Ghana",
            "immigrants": 258000,
            "pathway_type": "Legal",
            "reason": "Economic",
            "pathways": "Diversity Visa; Family; Employment",
            "context": (
                "Ghana punches well above its weight in the Diversity Visa lottery. Highly educated "
                "Ghanaian immigrants — nurses, engineers, professors — are a cornerstone of the "
                "African diaspora in the U.S. Ghanaian-Americans have among the highest educational "
                "attainment rates of any African immigrant group, and high rates of sending remittances "
                "that constitute a significant share of Ghana's GDP."
            ),
            "us_context": None,
            "lat": 7.9, "lon": -1.0
        },
        {
            "country": "Greece",
            "immigrants": 131000,
            "pathway_type": "Legal",
            "reason": "Economic",
            "pathways": "Family; Employment",
            "context": (
                "A diaspora shaped by 20th-century labor migration — Greek communities in Chicago, "
                "New York, and Baltimore have been passing down citizenship for generations. Modern "
                "Greek immigration picked up again after Greece's severe 2010–2018 debt crisis, "
                "which produced 27% unemployment and pushed a new generation of educated Greeks "
                "to seek opportunities abroad."
            ),
            "us_context": None,
            "lat": 39.1, "lon": 21.8
        },
        {
            "country": "Guatemala",
            "immigrants": 1299000,
            "pathway_type": "Mixed",
            "reason": "Economic/Violence",
            "pathways": "Family; Irregular; Temporary Work",
            "context": (
                "A largely invisible population within immigration statistics. Many Guatemalan "
                "immigrants are Indigenous Maya — speaking Mam, K'iche', or Q'anjob'al rather than "
                "Spanish — from highland communities with deep subsistence poverty. Seasonal "
                "agricultural workers and families fleeing gang violence travel the same dangerous "
                "overland routes. They often lack interpreters who speak their languages at the border."
            ),
            "us_context": (
                "The 1954 CIA-backed coup that overthrew democratically-elected President Jacobo "
                "Árbenz (Operation PBSUCCESS) set off a 36-year civil war (1960–1996) that killed "
                "200,000 people and created the conditions of inequality and violence that still "
                "drive emigration today. U.S. Cold War policy framed Árbenz's land reforms as "
                "communist, and the resulting instability shaped modern Guatemala."
            ),
            "lat": 15.8, "lon": -90.2
        },
        {
            "country": "Guyana",
            "immigrants": 315000,
            "pathway_type": "Legal",
            "reason": "Economic",
            "pathways": "Family; Employment",
            "context": (
                "Steady diaspora-driven migration since the 1970s. Guyanese-Americans are a "
                "tight-knit community concentrated in New York City (particularly Queens and the "
                "Bronx) with high rates of homeownership and civic participation. Guyana's small "
                "population means its diaspora represents a disproportionately large share of the "
                "country's educated professionals."
            ),
            "us_context": None,
            "lat": 4.9, "lon": -58.9
        },
        {
            "country": "Haiti",
            "immigrants": 798000,
            "pathway_type": "Humanitarian",
            "reason": "Political/Disaster",
            "pathways": "Humanitarian parole; TPS; Family",
            "context": (
                "Multiple catastrophes layered on top of each other. The 2010 earthquake killed "
                "230,000 people. The 2021 presidential assassination destabilized governance. "
                "Gang control now covers large portions of Port-au-Prince, making Haiti nearly "
                "ungovernable. Each crisis produced a new migration wave. Haitian TPS is among "
                "the most politically contentious — the Biden administration extended it; the "
                "Trump administration repeatedly sought to end it."
            ),
            "us_context": (
                "The U.S. has intervened in Haiti repeatedly: occupation from 1915–1934, support "
                "for the Duvalier dictatorships (1957–1986), a 1994 military intervention to "
                "restore President Aristide, and a 2004 role in his removal. Critics argue U.S. "
                "policies created the institutional fragility that made Haiti so vulnerable to "
                "both natural disasters and political collapse."
            ),
            "lat": 18.9, "lon": -72.3
        },
        {
            "country": "Honduras",
            "immigrants": 935000,
            "pathway_type": "Mixed",
            "reason": "Economic/Violence",
            "pathways": "Family; TPS; Irregular",
            "context": (
                "Among the world's highest homicide rates push families north. The journey is "
                "perilous: Honduras is a transit corridor for Central American migrants, and "
                "many families travel in caravans for safety. Women and children face extreme "
                "vulnerability to trafficking and exploitation at every border crossing. TPS for "
                "Hondurans — originally granted after Hurricane Mitch in 1998 — has been "
                "renewed under political pressure ever since."
            ),
            "us_context": (
                "Honduras was a staging ground for U.S. Contra operations against Nicaragua "
                "in the 1980s — a policy that militarized the country and contributed to "
                "institutional corruption. The 2009 coup against President Manuel Zelaya, "
                "which the Obama State Department declined to call a coup, was seen by many "
                "analysts as tacitly endorsed by Washington. Political instability following "
                "the coup directly accelerated northward migration."
            ),
            "lat": 15.2, "lon": -86.2
        },
        {
            "country": "India",
            "immigrants": 3165000,
            "pathway_type": "Legal",
            "reason": "Economic",
            "pathways": "H-1B; Student; Family",
            "context": (
                "The world's longest documented employment-based immigration queue. Indian H-1B "
                "visa holders wait an average of 54–100+ years for a green card due to per-country "
                "caps — meaning many will die before getting permanent residency, even after "
                "decades of legal U.S. residency and tax-paying. Indian-Americans are among "
                "the most highly educated and highest-earning immigrant groups, with major "
                "representation in Silicon Valley, medicine, and finance."
            ),
            "us_context": None,
            "lat": 20.6, "lon": 78.9
        },
        {
            "country": "Iran",
            "immigrants": 431000,
            "pathway_type": "Mixed",
            "reason": "Political",
            "pathways": "Employment; Family; Asylum",
            "context": (
                "Migration shaped by political rupture since 1979. The Iranian revolution drove "
                "the first wave — educated, secular Iranians who fled the Islamic Republic. "
                "Subsequent waves followed the Green Movement crackdown (2009) and the Mahsa "
                "Amini protests (2022). The Iranian-American community includes Nobel laureates, "
                "Fortune 500 executives, and asylum seekers — extraordinary intellectual capital "
                "lost to Iran, gained by the U.S."
            ),
            "us_context": (
                "The 1953 CIA-MI6 coup that overthrew democratically-elected Prime Minister "
                "Mohammad Mosaddegh (Operation Ajax/Boot) and restored the Shah fundamentally "
                "shaped Iranian politics — contributing to the conditions that produced the "
                "1979 Islamic Revolution. The revolution itself, and U.S. hostage crisis, "
                "then produced the first major wave of Iranian immigration to the U.S."
            ),
            "lat": 32.4, "lon": 53.7
        },
        {
            "country": "Iraq",
            "immigrants": 272000,
            "pathway_type": "Humanitarian",
            "reason": "Conflict/War",
            "pathways": "Refugee; Special Immigrant Visa",
            "context": (
                "A debt of honor, slowly paid. The Special Immigrant Visa (SIV) program was created "
                "specifically for Iraqis who worked as interpreters, drivers, and embassy staff "
                "for U.S. forces — people who risked their lives and those of their families. "
                "The program has been plagued by backlogs, security vetting delays, and bureaucratic "
                "obstacles that have left tens of thousands stranded in danger while their "
                "applications process."
            ),
            "us_context": (
                "The 2003 U.S. invasion of Iraq — justified by claims of WMDs that proved false — "
                "triggered a civil war, the rise of ISIS, and the displacement of millions. Iraq "
                "had a population of 25 million before the invasion; by 2007, 2 million had "
                "fled as refugees and 2.7 million were internally displaced. Iraqi migration "
                "to the U.S. is a direct consequence of U.S. military action."
            ),
            "lat": 33.2, "lon": 43.7
        },
        {
            "country": "Ireland",
            "immigrants": 126000,
            "pathway_type": "Legal",
            "reason": "Economic",
            "pathways": "Employment; Student",
            "context": (
                "The Irish diaspora in America is among the oldest and most politically powerful. "
                "The Great Famine (1845–1852) sent over a million Irish to the U.S. in a single "
                "decade; descendants of those immigrants now number over 30 million. Modern Irish "
                "immigration is a trickle by comparison — young professionals and students — "
                "but the cultural and political bonds remain among the deepest of any bilateral relationship."
            ),
            "us_context": None,
            "lat": 53.4, "lon": -8.2
        },
        {
            "country": "Israel",
            "immigrants": 170000,
            "pathway_type": "Legal",
            "reason": "Economic",
            "pathways": "Family; Student; Employment",
            "context": (
                "High-skilled and education-based migration with a distinctive two-way character. "
                "Israeli-Americans are among the most highly educated immigrant groups. A notable "
                "'brain circulation' exists between Tel Aviv and Silicon Valley — Israeli "
                "entrepreneurs and engineers who help build U.S. tech companies, often while "
                "maintaining ties to Israel's own thriving startup ecosystem."
            ),
            "us_context": None,
            "lat": 31.5, "lon": 34.8
        },
        {
            "country": "Italy",
            "immigrants": 361000,
            "pathway_type": "Legal",
            "reason": "Economic",
            "pathways": "Family; Employment",
            "context": (
                "Established diaspora networks from waves of 20th-century migration — Italian-Americans "
                "are one of America's largest ancestry groups, numbering over 17 million. Today's "
                "Italian immigrants are a different stream: young professionals who cannot find "
                "opportunity in Italy's stagnant economy, joining a community already deeply woven "
                "into U.S. cultural identity through food, politics, and organized labor."
            ),
            "us_context": None,
            "lat": 42.8, "lon": 12.8
        },
        {
            "country": "Jamaica",
            "immigrants": 911000,
            "pathway_type": "Legal",
            "reason": "Economic",
            "pathways": "Family; Employment",
            "context": (
                "Longstanding Caribbean migration systems built around healthcare, education, and "
                "domestic work. Jamaican nurses, teachers, and caregivers have helped staff the "
                "U.S. healthcare and education systems for decades. The remittance economy is "
                "critical: Jamaican diaspora sends back roughly $3 billion annually — over 20% "
                "of Jamaica's GDP — sustaining families and communities at home."
            ),
            "us_context": None,
            "lat": 18.1, "lon": -77.3
        },
        {
            "country": "Japan",
            "immigrants": 547000,
            "pathway_type": "Legal",
            "reason": "Economic",
            "pathways": "Employment; Student",
            "context": (
                "Corporate transfers and education pathways dominate. Japanese immigration has a "
                "different character from most flows — often temporary, often highly skilled, "
                "often tied to multinational companies like Sony, Toyota, and Panasonic with "
                "major U.S. operations. Japanese-Americans also carry a historical memory of "
                "WWII incarceration, which continues to shape community identity."
            ),
            "us_context": None,
            "lat": 36.2, "lon": 138.3
        },
        {
            "country": "Kenya",
            "immigrants": 211000,
            "pathway_type": "Legal",
            "reason": "Economic",
            "pathways": "Diversity Visa; Employment; Family",
            "context": (
                "Among the most highly educated African immigrant groups in the U.S. Kenyan "
                "doctors, nurses, engineers, and professors represent significant human capital "
                "— and a significant loss for Kenya, which invests heavily in public education "
                "only to see graduates recruited abroad. This 'brain drain' has prompted "
                "serious policy debate in Nairobi about retaining skilled professionals."
            ),
            "us_context": None,
            "lat": -0.0, "lon": 37.9
        },
        {
            "country": "Korea, Rep.",
            "immigrants": 1083000,
            "pathway_type": "Legal",
            "reason": "Economic",
            "pathways": "Family; Employment; Student",
            "context": (
                "Long-established communities shaped by both postwar immigration and modern "
                "professional flows. Koreatown in Los Angeles is a city within a city — a "
                "thriving economic enclave. Korean immigration combines high professional "
                "achievement with vibrant small-business ownership. Education is culturally "
                "central: Korean-Americans have among the highest college graduation rates "
                "of any immigrant group."
            ),
            "us_context": (
                "The Korean War (1950–1953), where the U.S. intervened to defend South Korea, "
                "created lasting military and cultural ties. The U.S. still stations 28,500 "
                "troops in South Korea. These deep security ties, combined with the U.S.-Korea "
                "Free Trade Agreement and extensive educational partnerships, have made the "
                "U.S. the primary destination for Korean emigrants."
            ),
            "lat": 36.0, "lon": 127.7
        },
        {
            "country": "Lao PDR",
            "immigrants": 177000,
            "pathway_type": "Humanitarian",
            "reason": "Conflict",
            "pathways": "Refugee; Family",
            "context": (
                "Post-war refugee resettlement — the living legacy of a secret war. The Hmong "
                "and Lao communities in Minnesota (St. Paul) and California (Fresno, Sacramento) "
                "are the direct result of U.S. military intervention in Southeast Asia. These "
                "communities carry profound generational trauma alongside extraordinary resilience."
            ),
            "us_context": (
                "The CIA conducted a secret war in Laos from 1964–1973, recruiting Hmong "
                "tribespeople to fight against North Vietnamese supply lines along the "
                "Ho Chi Minh Trail. When the U.S. withdrew, Hmong fighters and their families "
                "faced brutal reprisals from the communist Pathet Lao government. The U.S. "
                "resettlement of Hmong refugees was a direct — if belated — acknowledgment "
                "of that obligation. Laos remains the most bombed country per capita in history "
                "from U.S. bombing during the Vietnam War era."
            ),
            "lat": 17.9, "lon": 102.6
        },
        {
            "country": "Lebanon",
            "immigrants": 150000,
            "pathway_type": "Legal",
            "reason": "Economic/Political",
            "pathways": "Family; Employment; Asylum",
            "context": (
                "A diaspora anchored in over a century of migration. Lebanese-Americans have "
                "been part of U.S. life since the 1880s — among the earliest Arab immigrants. "
                "Today, Lebanon's catastrophic economic collapse (the Lebanese pound lost 98% "
                "of its value since 2019), the Beirut port explosion (2020), and political "
                "paralysis are sending a new, highly educated generation toward emigration."
            ),
            "us_context": None,
            "lat": 33.9, "lon": 35.5
        },
        {
            "country": "Mexico",
            "immigrants": 11280000,
            "pathway_type": "Mixed",
            "reason": "Economic",
            "pathways": "Family; Temporary Work; Irregular; DACA",
            "context": (
                "The world's single largest bilateral migration corridor. Over 11 million "
                "Mexican-born people live in the U.S. — roughly 1 in 4 immigrants. DACA "
                "(Deferred Action for Childhood Arrivals) protects approximately 580,000 "
                "'Dreamers' who arrived as children and grew up entirely American. Mexican "
                "immigrants are the backbone of U.S. agriculture, construction, and food "
                "service — with an economic contribution that has been estimated in the "
                "hundreds of billions annually."
            ),
            "us_context": (
                "The U.S.-Mexico migration relationship is inseparable from history and policy. "
                "NAFTA (1994) opened Mexico to cheap U.S. corn imports, displacing millions of "
                "subsistence farmers and triggering a wave of rural-to-U.S. migration. The "
                "Bracero Program (1942–1964) deliberately recruited Mexican labor, establishing "
                "migration networks that persisted for decades. The U.S. demand for low-wage "
                "labor and Mexico's wage differential create structural pull that no wall "
                "has historically eliminated."
            ),
            "lat": 23.6, "lon": -102.6
        },
        {
            "country": "Myanmar",
            "immigrants": 200000,
            "pathway_type": "Humanitarian",
            "reason": "Conflict",
            "pathways": "Refugee; Asylum",
            "context": (
                "Multiple waves of conflict-driven displacement. Rohingya genocide survivors "
                "(2017 military crackdown killed thousands and displaced 700,000) sit alongside "
                "earlier Karen and Kachin refugees who fled decades of civil war. After the "
                "2021 military coup, a new wave of urban professionals joined the refugee "
                "pipeline. These communities are separated by ethnicity but united by "
                "displacement from the same military."
            ),
            "us_context": None,
            "lat": 17.1, "lon": 96.0
        },
        {
            "country": "Nepal",
            "immigrants": 264000,
            "pathway_type": "Legal",
            "reason": "Economic",
            "pathways": "Diversity Visa; Student; Family",
            "context": (
                "Heavy reliance on the Diversity Visa lottery — Nepal has leveraged the DV program "
                "more than almost any other country relative to its size. Nepali-Americans are a "
                "rapidly growing community, with education and family reunification following "
                "initial lottery-based entry. Remittances from abroad are critical to the "
                "Nepali economy, representing over 25% of GDP."
            ),
            "us_context": None,
            "lat": 28.4, "lon": 84.1
        },
        {
            "country": "Nicaragua",
            "immigrants": 295000,
            "pathway_type": "Mixed",
            "reason": "Political",
            "pathways": "Humanitarian parole; Asylum; Family",
            "context": (
                "A recent surge tied to authoritarian repression under President Daniel Ortega. "
                "Dissidents, journalists, clergy, and opposition figures are among those seeking "
                "asylum — including Catholic bishops and university rectors arrested for "
                "criticizing the government. In 2023, Nicaragua stripped citizenship from "
                "hundreds of opposition figures, including over 200 who were already in exile "
                "or had emigrated."
            ),
            "us_context": (
                "Nicaragua's complex relationship with the U.S. is central to understanding "
                "its political situation. The Contra War of the 1980s — secretly funded by "
                "the Reagan administration through the Iran-Contra affair — pitted U.S.-backed "
                "rebels against the Sandinista government. Ortega, who fought as a Sandinista, "
                "returned to power in 2006 and has increasingly governed as an authoritarian, "
                "partly defined by anti-Americanism."
            ),
            "lat": 12.9, "lon": -85.2
        },
        {
            "country": "Nigeria",
            "immigrants": 565000,
            "pathway_type": "Legal",
            "reason": "Economic",
            "pathways": "Employment; Student; Diversity Visa",
            "context": (
                "The fastest-growing African immigrant group in the U.S., and a study in "
                "contradictions. Nigerian-Americans have the highest educational attainment "
                "of any immigrant group in the country — yet face a sharp disconnect between "
                "their credentials and social recognition. Concentrated in Houston, Atlanta, "
                "and the New York metro area, they send billions in annual remittances and "
                "are a major force in U.S. medicine and engineering."
            ),
            "us_context": None,
            "lat": 9.1, "lon": 8.7
        },
        {
            "country": "Pakistan",
            "immigrants": 453000,
            "pathway_type": "Mixed",
            "reason": "Economic/Political",
            "pathways": "Family; Employment; Asylum",
            "context": (
                "A community navigating a complex bilateral relationship. Highly-skilled tech "
                "workers and professionals enter through employment-based pathways alongside "
                "asylum claims from those fleeing religious persecution (particularly Ahmadis "
                "and Christians) or political violence. Pakistani-Americans are concentrated "
                "in New York, Houston, and Chicago, with strong professional networks and "
                "significant political engagement."
            ),
            "us_context": (
                "Pakistan has been a central U.S. strategic partner since the Cold War — first "
                "as a base for CIA operations in Afghanistan, then as a front-line state in "
                "the War on Terror after 9/11. The U.S. provided over $33 billion in aid to "
                "Pakistan between 2002–2018. The relationship is deeply ambivalent: Pakistan "
                "hosted Osama bin Laden while receiving U.S. counterterrorism funding, and U.S. "
                "drone strikes in Pakistani territory killed thousands and generated significant "
                "anti-American sentiment driving asylum claims."
            ),
            "lat": 30.4, "lon": 69.3
        },
        {
            "country": "Panama",
            "immigrants": 162000,
            "pathway_type": "Legal",
            "reason": "Economic",
            "pathways": "Employment; Family",
            "context": (
                "Smaller professional migration flows with historically deep ties. The Panama "
                "Canal Zone was U.S. territory from 1903–1999 — creating a unique shared "
                "history where many Panamanians grew up with American schools, culture, and "
                "family connections. Canal Zone 'Zonians' and their descendants blur the "
                "line between migration and citizenship."
            ),
            "us_context": (
                "The U.S. controlled the Canal Zone for nearly a century, creating a lasting "
                "demographic and cultural imprint. The 1989 U.S. invasion to remove Manuel "
                "Noriega (Operation Just Cause) further entangled the countries. Many "
                "Panamanian immigrants have direct family connections to Americans who "
                "worked or served in the Canal Zone."
            ),
            "lat": 8.6, "lon": -80.1
        },
        {
            "country": "Peru",
            "immigrants": 512000,
            "pathway_type": "Legal",
            "reason": "Economic",
            "pathways": "Family; Employment; Student",
            "context": (
                "Urban and skilled migration patterns that defy the homogenizing Latin American "
                "immigrant narrative. Peruvians in the U.S. are concentrated in professional "
                "fields — medicine, engineering, finance. The community is also notable for its "
                "culinary influence: Peruvian restaurants have become a significant presence in "
                "major U.S. cities, reflecting high-skilled service migration alongside "
                "professional flows."
            ),
            "us_context": None,
            "lat": -9.2, "lon": -75.0
        },
        {
            "country": "Philippines",
            "immigrants": 2264000,
            "pathway_type": "Legal",
            "reason": "Economic",
            "pathways": "Family; Employment (Healthcare)",
            "context": (
                "The backbone of U.S. healthcare. Filipino nurses, doctors, and caregivers staff "
                "hospitals and nursing homes nationwide — a deliberate U.S. recruitment policy "
                "that began in the 1960s and never stopped. The Philippines trains nurses "
                "specifically for export, and U.S. hospitals actively recruit from Filipino "
                "nursing schools. Remittances back to the Philippines — over $10 billion annually "
                "from the U.S. alone — are a pillar of the Philippine economy."
            ),
            "us_context": (
                "The Philippines was a U.S. colony from 1898–1946, following the Spanish-American "
                "War. The U.S. established English-language education, American institutions, "
                "and deep cultural ties that persist. The Philippine-American War (1899–1902) "
                "killed 200,000–600,000 Filipinos. Post-independence, the U.S. maintained "
                "military bases (Clark Air Base, Subic Bay Naval Base) until 1992, and the "
                "Visiting Forces Agreement still governs U.S. military presence. This colonial "
                "relationship is the foundation of Filipino migration to the U.S."
            ),
            "lat": 12.9, "lon": 121.8
        },
        {
            "country": "Poland",
            "immigrants": 397000,
            "pathway_type": "Legal",
            "reason": "Economic",
            "pathways": "Employment; Diversity Visa",
            "context": (
                "Labor mobility and visa lottery, joining a century-old community. Polish-Americans "
                "have a long presence in Rust Belt cities — Chicago's Polish community (once the "
                "largest outside Warsaw) reflects 20th-century industrial migration. Today's "
                "arrivals are professionals and trade workers, supplemented by DV lottery "
                "participants, joining established networks in Chicago, New York, and New Jersey."
            ),
            "us_context": None,
            "lat": 52.1, "lon": 19.1
        },
        {
            "country": "Portugal",
            "immigrants": 142000,
            "pathway_type": "Legal",
            "reason": "Economic",
            "pathways": "Family; Employment",
            "context": (
                "Longstanding migration networks, especially in New England. Portuguese-American "
                "fishing and manufacturing communities in Massachusetts (New Bedford, Fall River) "
                "and Rhode Island go back over a century — built by waves of immigration from "
                "the Azores and mainland Portugal. These tight-knit communities have been "
                "passing down language, culture, and chain migration for generations."
            ),
            "us_context": None,
            "lat": 39.4, "lon": -8.2
        },
        {
            "country": "Puerto Rico",
            "immigrants": 1925000,
            "pathway_type": "Legal",
            "reason": "Economic",
            "pathways": "Internal migration (U.S. citizens)",
            "context": (
                "Not international immigration — Puerto Ricans are U.S. citizens moving within "
                "their own sovereign territory. But 'internal migration' obscures a profound "
                "story: Puerto Rico is a U.S. territory with no voting representation in Congress "
                "and no electoral college votes. Decades of colonial economic policy, a 2006 "
                "fiscal crisis, and Hurricane Maria (2017) — which killed an estimated 3,000 "
                "people and destroyed the power grid — drove mass migration to Florida and the "
                "Northeast. Puerto Ricans vote in U.S. elections only after moving to the mainland."
            ),
            "us_context": (
                "Puerto Rico became a U.S. territory in 1898 after the Spanish-American War. "
                "The Jones-Shafroth Act (1917) granted citizenship but not statehood. PROMESA "
                "(2016) imposed a fiscal oversight board — critics call it a 'colonial control "
                "board' — that oversaw austerity measures including public school closures and "
                "pension cuts. The unresolved question of Puerto Rican statehood or independence "
                "shapes every aspect of its residents' relationship with migration."
            ),
            "lat": 18.2, "lon": -66.5
        },
        {
            "country": "Romania",
            "immigrants": 178000,
            "pathway_type": "Legal",
            "reason": "Economic",
            "pathways": "Employment; Diversity Visa",
            "context": (
                "Post-communist mobility patterns — skilled IT workers and healthcare "
                "professionals feature prominently alongside DV lottery participants. Romanian "
                "professionals have built notable communities in Chicago, New York, and Los "
                "Angeles. Romania's integration into the EU created alternative destinations "
                "in Western Europe, making U.S.-bound migration a self-selected, often "
                "highly skilled stream."
            ),
            "us_context": None,
            "lat": 45.9, "lon": 24.9
        },
        {
            "country": "Russian Federation",
            "immigrants": 453000,
            "pathway_type": "Mixed",
            "reason": "Political/Economic",
            "pathways": "Asylum; Employment; Family",
            "context": (
                "A community transformed by the 2022 full-scale invasion of Ukraine. Russians "
                "who opposed the war, feared conscription, or simply wanted to leave an "
                "increasingly repressive state began arriving at the U.S.-Mexico border in "
                "unprecedented numbers — a phenomenon sometimes called the 'back-door' to "
                "U.S. asylum. Earlier waves included Jewish refugees (1980s–90s), post-Soviet "
                "economic migrants, and political dissidents."
            ),
            "us_context": None,
            "lat": 61.5, "lon": 105.3
        },
        {
            "country": "South Africa",
            "immigrants": 162000,
            "pathway_type": "Legal",
            "reason": "Economic",
            "pathways": "Employment; Family; Student",
            "context": (
                "Skilled migration with complex motivations. Both white and Black South African "
                "professionals emigrate — pushed by crime, economic uncertainty, power outages "
                "(loadshedding), and deep anxiety about South Africa's future. The phenomenon "
                "of white South African emigration has attracted particular attention, while "
                "the parallel brain drain of Black professionals receives less coverage. "
                "South African doctors and engineers are particularly sought in the U.S."
            ),
            "us_context": None,
            "lat": -30.6, "lon": 22.9
        },
        {
            "country": "Spain",
            "immigrants": 169000,
            "pathway_type": "Legal",
            "reason": "Economic",
            "pathways": "Employment; Student",
            "context": (
                "Professional and educational migration shaped by Spain's economic crisis. "
                "Following the 2008–2014 period when unemployment reached 27%, a generation "
                "of highly educated young Spaniards left for opportunity abroad — the U.S., "
                "Germany, and the UK among primary destinations. This 'brain drain' has been "
                "a major policy concern in Spain, where public universities trained graduates "
                "who then built careers elsewhere."
            ),
            "us_context": None,
            "lat": 40.5, "lon": -3.7
        },
        {
            "country": "Taiwan",
            "immigrants": 404000,
            "pathway_type": "Legal",
            "reason": "Economic",
            "pathways": "Student; Employment; Family",
            "context": (
                "High-skilled tech migration with an outsized global impact. Taiwan's contribution "
                "to Silicon Valley is extraordinary — engineers and entrepreneurs who built the "
                "semiconductor supply chain that powers the modern world. TSMC (Taiwan "
                "Semiconductor Manufacturing Company), partly founded with U.S. links, now "
                "builds chips that the global economy depends on. Many Taiwanese-Americans "
                "maintain deep professional and personal ties to both countries."
            ),
            "us_context": (
                "The U.S.-Taiwan relationship is a unique geopolitical dynamic. The U.S. "
                "maintains unofficial relations with Taiwan while formally recognizing the "
                "People's Republic of China — a deliberate ambiguity established by the "
                "Taiwan Relations Act (1979). U.S. arms sales to Taiwan and the implicit "
                "security commitment create strong ties. The CHIPS Act (2022), which incentivized "
                "TSMC to build fabs in Arizona, is the latest chapter in deep economic interdependence."
            ),
            "lat": 23.7, "lon": 120.9
        },
        {
            "country": "Thailand",
            "immigrants": 308000,
            "pathway_type": "Legal",
            "reason": "Economic",
            "pathways": "Family; Employment",
            "context": (
                "Family reunification dominant — a network built by the Vietnam War era. Many "
                "Thai women married U.S. servicemen stationed at Royal Thai Air Force Bases "
                "during the Vietnam War, establishing the family connections that seeded "
                "today's Thai-American community. Their U.S.-born children and grandchildren "
                "sponsor further immigration. Communities are concentrated in California, "
                "Texas, and New York."
            ),
            "us_context": (
                "Thailand was a major base for U.S. operations during the Vietnam War — "
                "U-Tapao, Korat, and other Royal Thai Air Force Bases launched B-52 bombing "
                "missions over Vietnam, Laos, and Cambodia. The U.S. stationed up to 50,000 "
                "troops in Thailand. The resulting social connections, family formations, and "
                "cultural exchange created migration networks that have continued for 50+ years."
            ),
            "lat": 15.9, "lon": 100.9
        },
        {
            "country": "Trinidad and Tobago",
            "immigrants": 242000,
            "pathway_type": "Legal",
            "reason": "Economic",
            "pathways": "Family; Employment",
            "context": (
                "Caribbean diaspora migration with high educational attainment. Trinidadian- "
                "and Tobagonian-Americans are among the most economically successful Caribbean "
                "immigrant groups, with high rates of professional employment and homeownership. "
                "The community is concentrated in New York (the Bronx, Brooklyn) and South "
                "Florida. Strong cultural presence through calypso, soca, and Carnival traditions."
            ),
            "us_context": None,
            "lat": 10.7, "lon": -61.2
        },
        {
            "country": "Türkiye",
            "immigrants": 176000,
            "pathway_type": "Legal",
            "reason": "Economic/Political",
            "pathways": "Employment; Student; Family",
            "context": (
                "Skilled migration and political asylum combined. Turkish academics, journalists, "
                "and opposition figures have joined an already-established professional immigrant "
                "community — particularly following the post-2016 coup attempt crackdown, which "
                "purged 150,000 people from the civil service. Turkish-Americans are "
                "concentrated in New York, New Jersey, and California, with strong representation "
                "in engineering and academia."
            ),
            "us_context": None,
            "lat": 38.9, "lon": 35.2
        },
        {
            "country": "Ukraine",
            "immigrants": 448000,
            "pathway_type": "Humanitarian",
            "reason": "Conflict/War",
            "pathways": "Humanitarian parole; TPS; Refugee",
            "context": (
                "War-driven displacement after Russia's 2022 full-scale invasion. The Biden "
                "administration created the Uniting for Ukraine (U4U) humanitarian parole "
                "program specifically for this crisis — and by mid-2024, over 240,000 "
                "Ukrainians had arrived through it. Ukrainians also received Temporary "
                "Protected Status. The speed and scale of the U.S. response — contrasted with "
                "the treatment of other conflict-zone populations — sparked significant "
                "debate about immigration equity."
            ),
            "us_context": (
                "The U.S. has provided over $175 billion in total Ukraine aid since the "
                "2022 invasion — military, economic, and humanitarian. U.S. intelligence, "
                "weapons systems, and training have been central to Ukraine's war effort. "
                "The U.S. humanitarian response to Ukrainian displacement reflects this deep "
                "geopolitical commitment, which critics contrast with the U.S. response to "
                "displacement from other U.S.-involved conflicts."
            ),
            "lat": 48.4, "lon": 31.2
        },
        {
            "country": "United Kingdom",
            "immigrants": 895000,
            "pathway_type": "Legal",
            "reason": "Economic",
            "pathways": "Employment; Student; Family",
            "context": (
                "High-skilled and educational migration in both directions — the 'Special "
                "Relationship' in human form. British and American professionals move fluidly "
                "between two deeply connected cultures with shared language, legal traditions, "
                "and institutional ties. Post-Brexit, the UK has lost easy access to European "
                "labor markets, making the U.S. a relatively more attractive destination for "
                "skilled British emigrants."
            ),
            "us_context": None,
            "lat": 55.4, "lon": -3.4
        },
        {
            "country": "Venezuela",
            "immigrants": 764000,
            "pathway_type": "Humanitarian",
            "reason": "Political/Economic crisis",
            "pathways": "TPS; Asylum; Humanitarian Parole",
            "context": (
                "Rapid growth driven by national collapse. Venezuela — once one of South "
                "America's wealthiest countries with the world's largest proven oil reserves "
                "— experienced the largest economic contraction in modern Latin American "
                "history under Maduro. Over 7 million Venezuelans have left the country since "
                "2015 — the largest displacement crisis in the Western Hemisphere. Those "
                "reaching the U.S. are often the fortunate ones; millions more are in "
                "Colombia, Peru, and Ecuador."
            ),
            "us_context": (
                "U.S. policy toward Venezuela has been highly interventionist. Sweeping "
                "U.S. sanctions on Venezuela's oil sector — intended to pressure Maduro — "
                "have had humanitarian consequences that critics argue worsened the economic "
                "crisis driving emigration. The Trump administration's attempt to recognize "
                "opposition leader Juan Guaidó as president (2019) and its failed support "
                "for a coup attempt deepened Venezuela's political crisis without resolving it."
            ),
            "lat": 6.4, "lon": -66.6
        },
        {
            "country": "Vietnam",
            "immigrants": 1435000,
            "pathway_type": "Mixed",
            "reason": "Conflict/Economic",
            "pathways": "Family; Refugee legacy; Employment",
            "context": (
                "Post-war migration that never stopped. First came refugees from the Fall of "
                "Saigon (1975) — Vietnam War veterans and their families, many arriving by "
                "boat as 'boat people.' Then the Orderly Departure Program reunited families "
                "through the 1980s–90s. Now economic migrants and skilled professionals add "
                "new layers. Vietnamese-Americans carry the full arc of U.S. foreign policy "
                "history — from military ally to refugee to successful immigrant community."
            ),
            "us_context": (
                "The Vietnam War (U.S. involvement 1955–1975) is the foundational event for "
                "Vietnamese-American immigration. The U.S. dropped more bombs on Vietnam, "
                "Laos, and Cambodia than it dropped in all of WWII. Agent Orange defoliation "
                "affected millions; its health effects continue to the present. The Fall of "
                "Saigon triggered the first refugee wave; subsequent Amerasian children — "
                "born to Vietnamese mothers and American GIs — were later brought to the "
                "U.S. through the Amerasian Homecoming Act (1987)."
            ),
            "lat": 14.1, "lon": 108.3
        },
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
# Coordinates are verified geographic centers hardcoded in load_data() above.
# Do NOT substitute coordinates from the Excel source file — those values are
# scrambled and will place every country on the wrong location.
fig_map = go.Figure()

for pt, color in COLORS.items():
    sub = filtered[filtered["pathway_type"] == pt]
    if sub.empty:
        continue
    # Build a short hover text that shows the opening line of context
    hover_context = sub["context"].apply(lambda c: c[:120] + "…" if len(c) > 120 else c)
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
            "%{customdata[1]:,} immigrants · <i>%{customdata[2]}</i><br>"
            "<br><span style='font-size:11px'>%{customdata[3]}</span><extra></extra>"
        ),
        customdata=np.column_stack([
            sub["country"].values,
            sub["immigrants"].values,
            sub["reason"].values,
            hover_context.values,
        ]),
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
            has_us_context = (
                row.get("us_context") is not None
                and str(row.get("us_context", "")).strip() not in ("", "None")
            )

            st.markdown(f"""
            <div class="story-card {pt_class}">
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px">
                    <span style="font-size:1.1rem;font-weight:600;color:#1a1a1a">{row['country']}</span>
                    {"<span class='us-flag'>⚡ US policy link</span>" if has_us_context else ""}
                </div>
                <div style="margin-bottom:10px">
                    <span class="tag tag-{pt_class}">{pt}</span>
                    <span style="font-size:0.75rem;color:#888">{row['reason']}</span>
                </div>
                <div style="font-size:1.6rem;font-weight:600;color:#1a1a1a;margin-bottom:4px">
                    {row['immigrants']:,}
                </div>
                <div style="font-size:0.72rem;color:#aaa;margin-bottom:10px;text-transform:uppercase;letter-spacing:.04em">
                    immigrants in the U.S.
                </div>
                <div style="font-size:0.78rem;color:#888;margin-bottom:12px">
                    <b>Main pathways:</b> {row['pathways']}
                </div>
                <div class="context-section">
                    <div class="context-label">Why they came</div>
                    <div class="context-body">{row['context']}</div>
                </div>
                {f'''
                <div class="us-context-box">
                    <div class="context-label">🇺🇸 U.S. foreign policy connection</div>
                    <div class="context-body">{row["us_context"]}</div>
                </div>
                ''' if has_us_context else ""}
            </div>
            """, unsafe_allow_html=True)

# ── Full story wall ───────────────────────────────────────────────────────────
st.divider()
st.markdown("#### All country stories")

us_only = st.checkbox("🔍 Show only countries with a U.S. foreign policy connection", value=False)

col_left, col_right = st.columns(2)
story_df = filtered.sort_values("immigrants", ascending=False).copy()

if us_only:
    story_df = story_df[
        story_df["us_context"].notna() &
        (story_df["us_context"].astype(str).str.strip() != "") &
        (story_df["us_context"].astype(str).str.strip() != "None")
    ]

for i, (_, row) in enumerate(story_df.iterrows()):
    pt = row["pathway_type"]
    pt_class = pt.lower()
    has_us = (
        row.get("us_context") is not None
        and str(row.get("us_context", "")).strip() not in ("", "None")
    )
    col = col_left if i % 2 == 0 else col_right

    col.markdown(f"""
    <div class="story-card {pt_class}">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px">
            <span style="font-size:1.05rem;font-weight:600;color:#1a1a1a">{row['country']}</span>
            {"<span class='us-flag'>⚡ US policy link</span>" if has_us else ""}
        </div>
        <div style="margin-bottom:8px">
            <span class="tag tag-{pt_class}">{pt}</span>
            <span style="font-size:0.72rem;color:#888">{row['reason']}</span>
        </div>
        <div style="font-size:1.4rem;font-weight:600;color:#1a1a1a;margin-bottom:4px">
            {row['immigrants']:,}
        </div>
        <div style="font-size:0.68rem;color:#aaa;margin-bottom:8px;text-transform:uppercase;letter-spacing:.04em">
            immigrants in the U.S.
        </div>
        <div style="font-size:0.8rem;color:#888;margin-bottom:10px">
            <b>Pathways:</b> {row['pathways']}
        </div>
        <div class="context-section">
            <div class="context-label">Why they came</div>
            <div class="context-body">{row['context']}</div>
        </div>
        {f'''
        <div class="us-context-box">
            <div class="context-label">🇺🇸 U.S. foreign policy connection</div>
            <div class="context-body">{row["us_context"]}</div>
        </div>
        ''' if has_us else ""}
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
