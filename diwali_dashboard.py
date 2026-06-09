import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Diwali Sales Analysis",
    page_icon="🪔",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --saffron: #FF6B00;
    --gold: #FFB800;
    --deep: #1A0A00;
    --warm: #2D1500;
    --cream: #FFF8EE;
    --accent: #FF3D00;
    --light-gold: #FFE0A3;
}

html, body, [class*="css"]  {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--deep);
    color: var(--cream);
}

.stApp {
    background: linear-gradient(135deg, #1A0A00 0%, #2D1500 50%, #1A0800 100%);
}

/* Hero Banner */
.hero {
    background: linear-gradient(135deg, #FF6B00 0%, #FFB800 50%, #FF3D00 100%);
    border-radius: 24px;
    padding: 48px 56px;
    margin-bottom: 40px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '🪔';
    position: absolute;
    font-size: 200px;
    opacity: 0.08;
    right: -20px;
    top: -20px;
}
.hero::after {
    content: '✨';
    position: absolute;
    font-size: 120px;
    opacity: 0.08;
    left: 10px;
    bottom: -20px;
}
.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: 3.2rem;
    font-weight: 900;
    color: #1A0A00;
    margin: 0 0 8px 0;
    line-height: 1.1;
}
.hero p {
    color: #3D1800;
    font-size: 1.1rem;
    margin: 0;
    font-weight: 500;
}

/* KPI Cards */
.kpi-card {
    background: linear-gradient(145deg, #2D1500, #3D1F00);
    border: 1px solid rgba(255, 184, 0, 0.2);
    border-radius: 16px;
    padding: 28px 24px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s;
}
.kpi-card:hover { transform: translateY(-3px); }
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #FF6B00, #FFB800);
}
.kpi-icon { font-size: 2rem; margin-bottom: 8px; }
.kpi-value {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: #FFB800;
    line-height: 1;
}
.kpi-label {
    font-size: 0.82rem;
    color: rgba(255, 248, 238, 0.6);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 6px;
}

/* Section Headers */
.section-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: #FFB800;
    border-left: 4px solid #FF6B00;
    padding-left: 16px;
    margin: 40px 0 20px 0;
}

/* Insight Cards */
.insight-box {
    background: linear-gradient(145deg, rgba(255,107,0,0.12), rgba(255,184,0,0.06));
    border: 1px solid rgba(255, 184, 0, 0.25);
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 16px;
}
.insight-title {
    font-weight: 700;
    color: #FFB800;
    font-size: 0.95rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 6px;
}
.insight-text {
    color: rgba(255, 248, 238, 0.85);
    font-size: 0.93rem;
    line-height: 1.6;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(45, 21, 0, 0.8);
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    border: 1px solid rgba(255,184,0,0.15);
}
.stTabs [data-baseweb="tab"] {
    color: rgba(255,248,238,0.6);
    border-radius: 10px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #FF6B00, #FFB800) !important;
    color: #1A0A00 !important;
    font-weight: 700;
}

/* Divider */
hr { border-color: rgba(255,184,0,0.15); }

/* Sidebar */
.css-1d391kg, [data-testid="stSidebar"] {
    background: #2D1500;
}
</style>
""", unsafe_allow_html=True)


# ─── DATA (embedded from analysis results) ──────────────────────────────────────

# Gender data
gender_count = pd.DataFrame({'Gender': ['Female', 'Male'], 'Count': [7832, 3407]})
gender_revenue = pd.DataFrame({'Gender': ['Female', 'Male'], 'Amount': [74000000, 32000000]})

# Age group data
age_count = pd.DataFrame({
    'Age Group': ['26-35', '36-45', '18-25', '46-50', '51-55', '55+', '0-17'],
    'Count': [4541, 2283, 1879, 983, 830, 427, 296],
    'Revenue': [42600000, 22100000, 17200000, 9200000, 7500000, 4100000, 2500000]
})
age_gender = pd.DataFrame({
    'Age Group': ['26-35', '26-35', '36-45', '36-45', '18-25', '18-25', '46-50', '46-50'],
    'Gender': ['Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male'],
    'Count': [3269, 1272, 1540, 743, 1340, 539, 680, 303]
})

# State data
state_orders = pd.DataFrame({
    'State': ['Uttar Pradesh', 'Maharashtra', 'Karnataka', 'Delhi', 'Madhya Pradesh',
              'Andhra Pradesh', 'Himachal Pradesh', 'Gujarat', 'Rajasthan', 'Tamil Nadu'],
    'Orders': [4800, 3800, 3200, 2700, 2200, 1900, 1600, 1400, 1200, 1000]
})
state_revenue = pd.DataFrame({
    'State': ['Uttar Pradesh', 'Maharashtra', 'Karnataka', 'Delhi', 'Madhya Pradesh',
              'Andhra Pradesh', 'Himachal Pradesh', 'Gujarat', 'Rajasthan', 'Tamil Nadu'],
    'Amount': [19000000, 14000000, 13000000, 11000000, 8000000, 7900000, 6500000, 5800000, 5200000, 4800000]
})

# Marital status data
marital_count = pd.DataFrame({'Status': ['Unmarried', 'Married'], 'Count': [6518, 4721]})
marital_revenue = pd.DataFrame({
    'Status': ['Unmarried Female', 'Married Female', 'Unmarried Male', 'Married Male'],
    'Amount': [44000000, 30000000, 18000000, 13000000],
    'Gender': ['Female', 'Female', 'Male', 'Male'],
    'Marital': ['Unmarried', 'Married', 'Unmarried', 'Married']
})

# Occupation data
occ_count = pd.DataFrame({
    'Occupation': ['IT Sector', 'Healthcare', 'Aviation', 'Banking', 'Government',
                   'Hospitality', 'Media', 'Retail', 'Textile', 'Construction'],
    'Count': [1683, 1408, 1310, 1137, 954, 890, 820, 740, 680, 610],
    'Revenue': [14000000, 12000000, 11000000, 10000000, 8000000, 7000000, 6500000, 5800000, 5200000, 4800000]
})

# Product category data
cat_orders = pd.DataFrame({
    'Category': ['Clothing & Apparel', 'Food', 'Electronics & Gadgets', 'Footwear & Shoes',
                 'Beauty Products', 'Games & Toys', 'Home & Furniture', 'Decor', 'Sports', 'Books'],
    'Orders': [2656, 2420, 2047, 1059, 620, 590, 540, 480, 430, 390],
    'Revenue': [18000000, 35000000, 16000000, 14000000, 4800000, 4200000, 5200000, 3800000, 3500000, 2900000]
})

# Top products
top_products = pd.DataFrame({
    'Product_ID': ['P00265242', 'P00110942', 'P00237542', 'P00184942', 'P00011442',
                   'P00059442', 'P00173442', 'P00117542', 'P00140742', 'P00193542'],
    'Orders': [130, 115, 91, 82, 79, 76, 75, 74, 73, 72]
})

# ─── CHART COLOR PALETTE ────────────────────────────────────────────────────────
SAFFRON_SCALE = ['#FF3D00', '#FF6B00', '#FF8C00', '#FFB800', '#FFD060', '#FFE0A3', '#FFF8EE']
GENDER_COLORS = {'Female': '#FF6B00', 'Male': '#FFB800'}
PLOTLY_TEMPLATE = "plotly_dark"

def styled_fig(fig, height=380):
    fig.update_layout(
        height=height,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='DM Sans', color='#FFF8EE', size=12),
        title_font=dict(family='Playfair Display', color='#FFB800', size=16),
        legend=dict(bgcolor='rgba(45,21,0,0.8)', bordercolor='rgba(255,184,0,0.2)', borderwidth=1),
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis=dict(gridcolor='rgba(255,184,0,0.08)', tickfont=dict(color='rgba(255,248,238,0.7)')),
        yaxis=dict(gridcolor='rgba(255,184,0,0.08)', tickfont=dict(color='rgba(255,248,238,0.7)')),
    )
    return fig


# ─── HERO BANNER ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🪔 Diwali Sales Analysis</h1>
    <p>11,239 transactions · 15 dimensions · Deep-dive insights across gender, geography, occupation & products</p>
</div>
""", unsafe_allow_html=True)


# ─── KPI STRIP ──────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
kpis = [
    ("📦", "11,239", "Total Transactions"),
    ("💰", "₹106M+", "Total Revenue"),
    ("🛒", "₹9,454", "Avg Order Value"),
    ("👩", "70%", "Female Buyers"),
    ("🏆", "UP", "Top State"),
]
for col, (icon, val, label) in zip([k1, k2, k3, k4, k5], kpis):
    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-value">{val}</div>
        <div class="kpi-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


# ─── TABS ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "👤 Demographics", "🗺️ Geography", "💍 Marital Status",
    "💼 Occupation", "🛍️ Products", "📋 Summary"
])


# ══════════════════════════════════════════════════════════
# TAB 1 — DEMOGRAPHICS (Gender + Age)
# ══════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-header">Gender Analysis</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1.2, 1.2, 1])

    with c1:
        fig = px.bar(gender_count, x='Gender', y='Count', color='Gender',
                     color_discrete_map=GENDER_COLORS,
                     title='Buyers by Gender', text='Count')
        fig.update_traces(textposition='outside', textfont=dict(color='#FFB800', size=14))
        fig.update_layout(showlegend=False)
        st.plotly_chart(styled_fig(fig), use_container_width=True)

    with c2:
        fig = px.bar(gender_revenue, x='Gender', y='Amount', color='Gender',
                     color_discrete_map=GENDER_COLORS,
                     title='Revenue by Gender (₹)',
                     text=gender_revenue['Amount'].apply(lambda x: f"Rs.{x/1e6:.0f}M"))
        fig.update_traces(textposition='outside', textfont=dict(color='#FFB800', size=14))
        fig.update_layout(showlegend=False)
        st.plotly_chart(styled_fig(fig), use_container_width=True)

    with c3:
        fig = go.Figure(data=[go.Pie(
            labels=['Female', 'Male'],
            values=[74, 26],
            hole=0.6,
            marker=dict(colors=['#FF6B00', '#FFB800']),
        )])
        fig.update_traces(textinfo='percent+label', textfont_size=13)
        fig.add_annotation(text="Revenue<br>Share", x=0.5, y=0.5,
                           font_size=13, showarrow=False, font_color='#FFF8EE')
        fig.update_layout(title='Revenue Share', showlegend=False)
        st.plotly_chart(styled_fig(fig, height=380), use_container_width=True)

    st.markdown('<div class="section-header">Age Group Analysis</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        fig = px.bar(age_count.sort_values('Count', ascending=True),
                     x='Count', y='Age Group', orientation='h',
                     color='Count', color_continuous_scale=SAFFRON_SCALE,
                     title='Buyers by Age Group', text='Count')
        fig.update_traces(textposition='outside')
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(styled_fig(fig, height=420), use_container_width=True)

    with c2:
        fig = px.bar(age_gender, x='Age Group', y='Count', color='Gender',
                     color_discrete_map=GENDER_COLORS, barmode='group',
                     title='Age Group × Gender Breakdown')
        st.plotly_chart(styled_fig(fig, height=420), use_container_width=True)

    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">💡 Key Insight — Demographics</div>
        <div class="insight-text">
            Women represent <strong>70% of all buyers</strong> and drive <strong>70% of total revenue</strong>.
            The <strong>26–35 age group</strong> is the dominant segment with 4,541 buyers and ₹42.6M revenue — 
            mostly working-age women with high disposable income and festive spending intent.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# TAB 2 — GEOGRAPHY
# ══════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">State-wise Performance</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        fig = px.bar(state_orders.sort_values('Orders', ascending=True),
                     x='Orders', y='State', orientation='h',
                     color='Orders', color_continuous_scale=SAFFRON_SCALE,
                     title='Top 10 States by Orders', text='Orders')
        fig.update_traces(textposition='outside')
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(styled_fig(fig, height=460), use_container_width=True)

    with c2:
        state_rev_sorted = state_revenue.sort_values('Amount', ascending=True).copy()
        state_rev_sorted['text'] = state_rev_sorted['Amount'].apply(lambda x: f"Rs.{x/1e6:.0f}M")
        fig = px.bar(state_rev_sorted,
                     x='Amount', y='State', orientation='h',
                     color='Amount', color_continuous_scale=['#FF3D00', '#FFB800'],
                     title='Top 10 States by Revenue (₹)', text='text')
        fig.update_traces(textposition='outside')
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(styled_fig(fig, height=460), use_container_width=True)

    # Treemap
    fig = px.treemap(state_revenue, path=['State'], values='Amount',
                     color='Amount', color_continuous_scale=SAFFRON_SCALE,
                     title='Revenue Distribution Across Top States')
    fig.update_traces(textinfo='label+percent parent', textfont_size=14)
    fig.update_coloraxes(showscale=False)
    st.plotly_chart(styled_fig(fig, height=340), use_container_width=True)

    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">💡 Key Insight — Geography</div>
        <div class="insight-text">
            <strong>Uttar Pradesh, Maharashtra & Karnataka</strong> together account for ~45% of all orders and revenue.
            UP alone generates ₹19M+, nearly <strong>40% more than Maharashtra</strong> in 2nd place.
            These three states should receive the largest share of marketing budget and inventory allocation.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# TAB 3 — MARITAL STATUS
# ══════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">Marital Status Analysis</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.4, 1.2])

    with c1:
        fig = go.Figure(data=[go.Pie(
            labels=['Unmarried', 'Married'],
            values=[6518, 4721],
            hole=0.55,
            marker=dict(colors=['#FF6B00', '#FFB800']),
        )])
        fig.update_traces(textinfo='percent+label', textfont_size=13)
        fig.update_layout(title='Customer Split', showlegend=False)
        st.plotly_chart(styled_fig(fig, height=360), use_container_width=True)

    with c2:
        fig = px.bar(marital_revenue, x='Status', y='Amount',
                     color='Gender', color_discrete_map=GENDER_COLORS,
                     title='Revenue by Marital Status & Gender',
                     text=marital_revenue['Amount'].apply(lambda x: f"Rs.{x/1e6:.0f}M"))
        fig.update_traces(textposition='outside')
        st.plotly_chart(styled_fig(fig, height=360), use_container_width=True)

    with c3:
        # Waterfall
        fig = go.Figure(go.Waterfall(
            name='Revenue',
            orientation='v',
            x=['Unmarried F', 'Married F', 'Unmarried M', 'Married M'],
            y=[44, 30, 18, 13],
            connector={"line": {"color": "rgba(255,184,0,0.4)"}},
            increasing={"marker": {"color": "#FF6B00"}},
            decreasing={"marker": {"color": "#FF3D00"}},
            totals={"marker": {"color": "#FFB800"}},
            textposition='outside',
            text=['Rs.44M', 'Rs.30M', 'Rs.18M', 'Rs.13M'],
        ))
        fig.update_layout(title='Revenue Waterfall (₹M)', showlegend=False)
        st.plotly_chart(styled_fig(fig, height=360), use_container_width=True)

    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">💡 Key Insight — Marital Status</div>
        <div class="insight-text">
            <strong>Unmarried females</strong> are the single biggest segment at ₹44M.
            Married women contribute ₹30M — giving women a combined ₹74M vs men's ₹31M.
            Unmarried buyers (58%) are slightly more numerous, but married segments show higher per-capita spend.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# TAB 4 — OCCUPATION
# ══════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">Occupation-wise Analysis</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        fig = px.bar(occ_count.sort_values('Count'),
                     x='Count', y='Occupation', orientation='h',
                     color='Count', color_continuous_scale=SAFFRON_SCALE,
                     title='Customers by Occupation', text='Count')
        fig.update_traces(textposition='outside')
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(styled_fig(fig, height=440), use_container_width=True)

    with c2:
        occ_rev_sorted = occ_count.sort_values('Revenue').copy()
        occ_rev_sorted['text'] = occ_rev_sorted['Revenue'].apply(lambda x: f"Rs.{x/1e6:.0f}M")
        fig = px.bar(occ_rev_sorted,
                     x='Revenue', y='Occupation', orientation='h',
                     color='Revenue', color_continuous_scale=['#FF3D00', '#FFB800'],
                     title='Revenue by Occupation (₹)', text='text')
        fig.update_traces(textposition='outside')
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(styled_fig(fig, height=440), use_container_width=True)

    # Scatter: count vs revenue
    fig = px.scatter(occ_count, x='Count', y='Revenue', text='Occupation',
                     size='Revenue', color='Revenue',
                     color_continuous_scale=SAFFRON_SCALE,
                     title='Customer Count vs Revenue by Occupation')
    fig.update_traces(textposition='top center', textfont=dict(color='#FFB800', size=11))
    fig.update_coloraxes(showscale=False)
    st.plotly_chart(styled_fig(fig, height=360), use_container_width=True)

    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">💡 Key Insight — Occupation</div>
        <div class="insight-text">
            <strong>IT, Healthcare & Aviation</strong> professionals are the top 3 customer segments by both headcount and revenue.
            These white-collar, high-income professionals show strong festive purchasing power.
            Targeted campaigns and exclusive bundles for these segments can significantly lift average order value.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# TAB 5 — PRODUCTS
# ══════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-header">Product Category Analysis</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        fig = px.bar(cat_orders.sort_values('Orders', ascending=False).head(8),
                     x='Orders', y='Category', orientation='h',
                     color='Orders', color_continuous_scale=SAFFRON_SCALE,
                     title='Orders by Category', text='Orders')
        fig.update_traces(textposition='outside')
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(styled_fig(fig, height=420), use_container_width=True)

    with c2:
        cat_rev_sorted = cat_orders.sort_values('Revenue', ascending=False).head(8).copy()
        cat_rev_sorted['text'] = cat_rev_sorted['Revenue'].apply(lambda x: f"Rs.{x/1e6:.0f}M")
        fig = px.bar(cat_rev_sorted,
                     x='Revenue', y='Category', orientation='h',
                     color='Revenue', color_continuous_scale=['#FF3D00', '#FFB800'],
                     title='Revenue by Category (Rs.)',
                     text='text')
        fig.update_traces(textposition='outside')
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(styled_fig(fig, height=420), use_container_width=True)

    # Bubble chart — orders vs revenue
    fig = px.scatter(cat_orders, x='Orders', y='Revenue',
                     size='Revenue', color='Category', text='Category',
                     color_discrete_sequence=px.colors.sequential.Oranges_r,
                     title='Orders vs Revenue by Category (bubble size = revenue)')
    fig.update_traces(textposition='top center', textfont=dict(size=10))
    st.plotly_chart(styled_fig(fig, height=380), use_container_width=True)

    st.markdown('<div class="section-header">Top 10 Best-Selling Products</div>', unsafe_allow_html=True)
    fig = px.bar(top_products.sort_values('Orders', ascending=True),
                 x='Orders', y='Product_ID', orientation='h',
                 color='Orders', color_continuous_scale=SAFFRON_SCALE,
                 title='Top 10 Products by Order Volume', text='Orders')
    fig.update_traces(textposition='outside')
    fig.update_coloraxes(showscale=False)
    st.plotly_chart(styled_fig(fig, height=360), use_container_width=True)

    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">💡 Key Insight — Products</div>
        <div class="insight-text">
            <strong>Food</strong> generates the highest revenue (₹35M) despite ranking 2nd in orders — 
            indicating high average transaction value. <strong>Clothing & Apparel</strong> leads in order count.
            The <strong>top 3 categories (Food, Clothing, Electronics)</strong> together account for 65%+ of all revenue.
            Product <strong>P00265242</strong> is the runaway bestseller — ensure robust stock levels.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# TAB 6 — EXECUTIVE SUMMARY
# ══════════════════════════════════════════════════════════
with tab6:
    st.markdown('<div class="section-header">Executive Summary & Recommendations</div>', unsafe_allow_html=True)

    # Target customer profile
    st.markdown("""
    <div class="insight-box" style="background: linear-gradient(135deg,rgba(255,107,0,0.2),rgba(255,184,0,0.1)); border-color: rgba(255,184,0,0.5);">
        <div class="insight-title" style="font-size:1.1rem;">🎯 Ideal Target Customer Profile</div>
        <div class="insight-text" style="font-size:1rem;">
            <strong>Married woman, aged 26–35</strong>, living in <strong>Uttar Pradesh, Maharashtra, or Karnataka</strong>,
            working in <strong>IT, Healthcare, or Aviation</strong> — with a high propensity to purchase
            <strong>Food, Clothing & Apparel, and Electronics</strong>.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        findings = [
            ("👩", "Gender", "70% of buyers are female, contributing 70% of total revenue (₹74M vs ₹32M for men)"),
            ("🎂", "Age Group", "26–35 is the #1 segment with 4,541 buyers and ₹42.6M revenue — primarily females"),
            ("🗺️", "Geography", "Top 3 states (UP, Maharashtra, Karnataka) account for ~45% of all orders & revenue"),
        ]
        for icon, title, text in findings:
            st.markdown(f"""
            <div class="insight-box">
                <div class="insight-title">{icon} {title}</div>
                <div class="insight-text">{text}</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        findings2 = [
            ("💼", "Occupation", "IT, Healthcare & Aviation professionals are the top 3 segments by count and spend"),
            ("🛍️", "Products", "Food (₹35M), Clothing (₹18M), Electronics (₹16M) make up 65%+ of total revenue"),
            ("📦", "Top Product", "P00265242 is the #1 bestseller with 130+ orders — stock deeply for peak season"),
        ]
        for icon, title, text in findings2:
            st.markdown(f"""
            <div class="insight-box">
                <div class="insight-title">{icon} {title}</div>
                <div class="insight-text">{text}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Strategic Recommendations</div>', unsafe_allow_html=True)

    recs = [
        ("📣", "Marketing", "Run women-centric Diwali campaigns targeting the 26–35 age group on social media. Focus ad budget on UP, Maharashtra & Karnataka."),
        ("📦", "Inventory", "Prioritize deep stock of Food, Clothing & Electronics. Ensure P00265242 and the top 10 products are well-stocked before the festive season."),
        ("💡", "Promotions", "Create exclusive bundles for IT/Healthcare/Aviation professionals. Offer loyalty rewards for married women who are repeat purchasers."),
        ("📈", "Revenue Growth", "Upsell Food products which have the highest avg. transaction value. Bundle with Clothing for cross-category cart growth."),
        ("🎁", "Loyalty", "Build a loyalty program targeting female repeat buyers — they represent the highest LTV segment."),
    ]
    for icon, title, text in recs:
        st.markdown(f"""
        <div class="insight-box" style="display:flex; gap:16px; align-items:flex-start;">
            <div style="font-size:1.8rem; line-height:1;">{icon}</div>
            <div>
                <div class="insight-title">{title}</div>
                <div class="insight-text">{text}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Final mini chart — revenue by category donut
    fig = px.pie(cat_orders.head(6), values='Revenue', names='Category',
                 hole=0.5, color_discrete_sequence=px.colors.sequential.Oranges_r,
                 title='Revenue Share by Top Product Categories')
    fig.update_traces(textinfo='percent+label', textfont_size=12)
    st.plotly_chart(styled_fig(fig, height=380), use_container_width=True)

# ─── FOOTER ──────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:rgba(255,248,238,0.35); font-size:0.8rem; padding: 12px 0;">
    🪔 Diwali Sales Analysis Dashboard &nbsp;·&nbsp; 11,239 Records &nbsp;·&nbsp; Built with Streamlit & Plotly
</div>
""", unsafe_allow_html=True)
