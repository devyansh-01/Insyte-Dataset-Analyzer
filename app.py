import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit.components.v1 as components
import io
from fpdf import FPDF

st.set_page_config(page_title="Insyte | Smart Data Pro", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 4rem !important;
    }

    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #f1f5f9;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        border-bottom: 1px solid #f1f5f9;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #f8fafc;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 600;
        color: #64748b;
    }

    .stTabs [aria-selected="true"] {
        background-color: #4f46e5 !important;
        color: white !important;
    }

    div[data-baseweb="select"] input {
        caret-color: transparent !important;
        pointer-events: none !important;
    }

    #MainMenu,
    footer,
    header,
    .stAppDeployButton {
        visibility: hidden;
        display: none;
    }

    /* Updated feature grid cards for uniform size and spacing */
    .feature-grid-container {
        margin-top: 20px;
    }
    .feature-card { 
        background: #ffffff; 
        border: 1px solid #e2e8f0; 
        padding: 24px; 
        border-radius: 16px; 
        margin-bottom: 24px; 
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05); 
        min-height: 280px; 
        overflow: hidden;
    }
    .feature-title { 
        color: #1e293b; 
        font-weight: 800; 
        font-size: 18px; 
        margin-bottom: 8px; 
    }
    .feature-tagline {
        color: #64748b; 
        font-size: 14px; 
        margin-bottom: 16px; 
        line-height: 1.4;
    }
    .feature-list { 
        color: #475569; 
        font-size: 13px; 
        line-height: 1.6; 
        list-style: none; 
        padding-left: 0; 
        margin: 0;
    }
    .feature-list li { 
        margin-bottom: 4px; 
    }

    /* Navigation buttons styling - tightly spaced side-by-side */
    div[data-testid="stHorizontalBlock"] button {
        background: none !important;
        border: none !important;
        color: #4b5563 !important;
        font-weight: 600 !important;
        font-size: 18px !important;
        padding: 8px 10px !important;
        cursor: pointer !important;
        border-radius: 50px !important;
    }

    div[data-testid="stHorizontalBlock"] button:hover {
        color: #2563eb !important;
        background: #eff6ff !important;
    }
    
    /* Solid Blue Pill design applied only to the 5th column container (Contact Us) */
    div[data-testid="stHorizontalBlock"] div:nth-child(5) button {
        background: #2563eb !important;
        border: 2px solid #2563eb !important;
        color: white !important;
        padding: 6px 16px !important;
        border-radius: 50px !important;
        font-weight: 600 !important;
        font-size: 18px !important;
        transition: all 0.2s ease-in-out;
    }
    
    div[data-testid="stHorizontalBlock"] div:nth-child(5) button:hover {
        background: #1d4ed8 !important;
        border-color: #1d4ed8 !important;
    }

    /* MOBILE FIX: force navbar into a tight single row */
    @media (max-width: 768px) {
        /* Hide the logo column's default large text and the Streamlit column layout */
        div[data-testid="stHorizontalBlock"] {
            display: none !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- NAVIGATION STATE ---
if "nav" not in st.session_state:
    st.session_state.nav = "home"

# --- DESKTOP NAVBAR (original, hidden on mobile via CSS) ---
col_logo, col_home, col_feat, col_about, col_contact, col_theme = st.columns([6.5, 0.8, 1.0, 0.8, 1.5, 0.4])

with col_logo:
    st.markdown("<p style='font-weight:800; font-size:28px; color:black; letter-spacing:-1px; padding:0; margin: 2px 0 0 var(--logo-margin, 0px); line-height: 42px;'>Insyte<span style=\"color:#2563eb\">.</span></p><style>@media(min-width:769px){:root{--logo-margin: 100px;}}</style>", unsafe_allow_html=True)
with col_home:
    if st.button("Home", key="nav_home"):
        st.session_state.nav = "home"; st.rerun()
with col_feat:
    if st.button("Features", key="nav_feat"):
        st.session_state.nav = "features"; st.rerun()
with col_about:
    if st.button("About", key="nav_about"):
        st.session_state.nav = "about"; st.rerun()
with col_contact:
    if st.button("Contact Us", key="nav_contact"):
        st.session_state.nav = "contact"; st.rerun()

# --- MOBILE NAVBAR (shown only on mobile via CSS) ---
st.markdown("""
<style>
.mobile-nav {
    display: none;
}
@media (max-width: 768px) {
    .mobile-nav {
        display: flex !important;
        align-items: center;
        justify-content: space-between;
        padding: 4px 0 10px 0;
        flex-wrap: nowrap;
        gap: 2px;
    }
    .mobile-logo {
        font-weight: 800;
        font-size: 22px;
        color: black;
        letter-spacing: -1px;
        white-space: nowrap;
        flex-shrink: 0;
        font-family: system-ui, -apple-system, sans-serif;
        line-height: 1;
    }
    .mobile-logo span { color: #2563eb; }
    .mobile-links {
        display: flex;
        align-items: center;
        gap: 1px;
        flex-wrap: nowrap;
    }
    .mobile-nav-btn {
        background: none;
        border: none;
        color: #4b5563;
        font-weight: 600;
        font-size: 12px;
        padding: 5px 7px;
        cursor: pointer;
        border-radius: 50px;
        white-space: nowrap;
        font-family: system-ui, -apple-system, sans-serif;
        text-decoration: none;
        display: inline-block;
    }
    .mobile-nav-cta {
        background: #2563eb;
        border: 2px solid #2563eb;
        color: white !important;
        font-weight: 600;
        font-size: 12px;
        padding: 5px 11px;
        cursor: pointer;
        border-radius: 50px;
        white-space: nowrap;
        font-family: system-ui, -apple-system, sans-serif;
        text-decoration: none;
        display: inline-block;
    }
}
</style>
<div class="mobile-nav">
    <div class="mobile-logo">Insyte<span>.</span></div>
    <div class="mobile-links">
        <a class="mobile-nav-btn" href="?nav=home">Home</a>
        <a class="mobile-nav-btn" href="?nav=features">Features</a>
        <a class="mobile-nav-btn" href="?nav=about">About</a>
        <a class="mobile-nav-cta" href="?nav=contact">Contact Us</a>
    </div>
</div>
""", unsafe_allow_html=True)

# --- READ NAV FROM URL QUERY PARAMS (for mobile anchor links) ---
query_params = st.query_params
if "nav" in query_params:
    st.session_state.nav = query_params["nav"]

st.markdown("<div style='border-bottom: 1px solid #cbd5e1; margin-top: -2px; margin-bottom: 20px;'></div>", unsafe_allow_html=True)

nav = st.session_state.nav

# --- HOME ---
if nav == "home":
    hero_body = """
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Plus Jakarta Sans', sans-serif; margin: 0; padding: 0; background: white; overflow-x: hidden; }
        .hero { text-align: center; padding: 80px 15% 30px 15%; position: relative; width: 100%; box-sizing: border-box; }
        .badge { background: #eff6ff; color: #2563eb; border: 1px solid #dbeafe; padding: 6px 15px; border-radius: 20px; font-size: 11px; font-weight: 800; text-transform: uppercase; display: inline-block; margin-bottom: 25px; letter-spacing: 1px; }
        h1 { font-size: 64px; font-weight: 800; line-height: 1.1; color: #111827; margin: 0 0 25px 0; letter-spacing: -2px; }
        h1 span { color: #4f46e5; }
        p { color: #6b7280; font-size: 18px; max-width: 700px; margin: 0 auto 40px auto; line-height: 1.6; }
        .float-card { position: absolute; background: white; padding: 20px; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.06); border: 1px solid #f1f5f9; animation: float 5s ease-in-out infinite; z-index: 10; text-align: left; min-width: 170px; }
        .c1 { top: 10%; left: 3%; } .c2 { top: 15%; right: 3%; animation-delay: 1s; }
        .c3 { bottom: 0%; left: 5%; animation-delay: 2s; }
        .c4 { bottom: 2%; right: 3%; animation-delay: 1.5s; }
        @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-20px); } }
        .btn-main { background: #2563eb; color: white; padding: 18px 45px; border-radius: 50px; border: none; font-size: 18px; font-weight: 700; cursor: pointer; box-shadow: 0 10px 20px rgba(37,99,235,0.3); }
        .bar-container { display: flex; align-items: flex-end; gap: 4px; height: 35px; margin-bottom: 10px; }
        .bar { width: 8px; border-radius: 2px; }
        .icon-stack { background: #e0e7ff; width: 35px; height: 35px; border-radius: 10px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 2px; margin-bottom: 12px; }
        .stack-line { width: 16px; height: 3px; background: #4338ca; border-radius: 1px; }

        @media (max-width: 768px) {
            .hero { padding: 30px 6% 30px 6%; }
            h1 { font-size: 36px; letter-spacing: -1px; }
            p { font-size: 15px; }
            .float-card { display: none; }
            .btn-main { font-size: 15px; padding: 14px 32px; }
        }
    </style>
    <div class="hero">
        <div class="float-card c1">
            <div class="icon-stack"><div class="stack-line"></div><div class="stack-line"></div><div class="stack-line"></div></div>
            <div style="font-weight:800; font-size:20px; color:#1e1b4b">1,000+ Rows</div>
            <div style="color:#64748b; font-size:11px; font-weight:600;">STATISTICAL SUMMARIES</div>
        </div>
        <div class="float-card c2">
            <div class="bar-container">
                <div class="bar" style="height:40%; background:#dbeafe"></div>
                <div class="bar" style="height:80%; background:#2563eb"></div>
                <div class="bar" style="height:55%; background:#93c5fd"></div>
                <div class="bar" style="height:100%; background:#4f46e5"></div>
            </div>
            <div style="font-weight:800; font-size:18px; color:#1e293b">5+ Visuals</div>
            <div style="color:#94a3b8; font-size:10px; font-weight:700;">INTERACTIVE CHARTS</div>
        </div>
        <div class="float-card c3">
            <div style="font-size:24px; margin-bottom:8px;">⏱</div>
            <div style="font-weight:800; font-size:18px; color:#4f46e5">40% Faster Analysis</div>
            <div style="color:#64748b; font-size:9px; font-weight:600;">AUTOMATED INSIGHT GENERATION</div>
        </div>
        <div class="float-card c4">
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:10px">
                <div style="font-size:22px;">🧹</div>
                <div style="font-weight:800; font-size:14px; color:#1e293b">Data Quality</div>
            </div>
            <div style="color:#16a34a; font-weight:800; font-size:18px">30% Less Manual Work</div>
            <div style="color:#94a3b8; font-size:10px; font-weight:700;">CLEANING AUTOMATION</div>
        </div>
        <div class="badge">📊 Analyze, Clean, Visualize.</div>
        <h1>Turn Raw Data Into <br><span>Actionable Insights.</span></h1>
        <p>A professional system designed to handle large-scale datasets, automate rigorous cleaning, and generate visual narratives in seconds.</p>
        <button class="btn-main" onclick="window.parent.document.querySelector('#upload_area').scrollIntoView({behavior:'smooth'})">Analyze Data →</button>
    </div>
    """
    components.html(hero_body, height=620)

# --- FEATURES ---
elif nav == "features":
    st.markdown("<div style='padding: 20px 5%;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color: #1e293b; font-weight: 800; margin-bottom: 10px;'>Platform Features</h1>", unsafe_allow_html=True)
    
    features = [
        {"icon": "", "title": "Automated Statistical Analysis", "tagline": "Generate detailed statistical summaries instantly.", "items": ["Mean, Median, Mode", "Standard Deviation", "Distribution Analysis", "Column Profiling", "Numerical & Categorical Statistics"]},
        {"icon": "", "title": "Intelligent Data Cleaning", "tagline": "Improve data quality automatically.", "items": ["Missing Value Detection", "Duplicate Detection", "Inconsistency Checks", "Data Quality Assessment", "Cleaning Recommendations"]},
        {"icon": "", "title": "Interactive Visualizations", "tagline": "Understand data through dynamic charts.", "items": ["Bar Charts", "Line Charts", "Histograms", "Pie Charts", "Scatter Plots"]},
        {"icon": "", "title": "AI-Powered Insights", "tagline": "Discover patterns without manual analysis.", "items": ["Trend Detection", "Correlation Discovery", "Key Findings", "Business Insights", "Automated Recommendations"]},
        {"icon": "", "title": "Fast Performance", "tagline": "Built for efficient analysis.", "items": ["Process 1000+ Rows", "Instant Results", "Optimized Calculations", "Interactive Dashboard"]},
        {"icon": "", "title": "Export & Reporting", "tagline": "Share your findings effortlessly.", "items": ["Download Cleaned Data", "Export Reports", "Save Visualizations", "PDF & Excel Support"]},
    ]
    
    st.markdown("<div class='feature-grid-container'>", unsafe_allow_html=True)
    
    for i in range(0, len(features), 3):
        row_features = features[i:i+3]
        cols = st.columns(3)
        
        for col, feature in zip(cols, row_features):
            with col:
                st.markdown(f"""
                <div class="feature-card">
                    <div class="feature-title">{feature['icon']} {feature['title']}</div>
                    <div class="feature-tagline">{feature['tagline']}</div>
                    <ul class="feature-list">
                        {''.join(f"<li>• {item}</li>" for item in feature['items'])}
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# --- ABOUT ---
elif nav == "about":
    about_html = """
    <div style="padding: 20px 0; max-width: 1000px; margin: auto; font-family: system-ui, -apple-system, sans-serif;">
        <h1 style="color:#1e293b; margin-bottom:25px; font-size: 32px; font-weight: 800;">
            About Insyte
        </h1>

        <p style="font-size:17px; color:#64748b; line-height:1.8; margin-bottom: 20px;">
            Insyte is a smart data analysis platform built to simplify the way
            people explore and understand data. Instead of spending hours writing
            code or manually analyzing spreadsheets, users can upload their datasets
            and instantly uncover meaningful insights through statistics,
            visualizations, and AI-powered analysis.
        </p>

        <p style="font-size:17px; color:#64748b; line-height:1.8; margin-bottom: 20px;">
            Whether you're a student working on a project, a researcher studying
            trends, or a professional looking for quick insights, Insyte provides
            an intuitive environment for exploring data with confidence.
        </p>

        <p style="font-size:17px; color:#64748b; line-height:1.8; margin-bottom: 30px;">
            Built using Python, Pandas, NumPy, Matplotlib, and Streamlit,
            the platform combines powerful analytics with a clean and
            user-friendly interface.
        </p>

        <div style="
            padding:20px;
            background:#f8fafc;
            border-radius:12px;
            border:1px solid #e2e8f0;
        ">
            <h3 style="margin-top:0; margin-bottom:15px; color:#1e293b; font-size: 20px; font-weight: 700;">
                Our Mission
            </h3>

            <p style="color:#64748b; line-height:1.7; margin:0; font-size:16px;">
                To make data analysis accessible, interactive, and insightful
                for everyone, regardless of their technical background.
            </p>
        </div>
    </div>
    """
    components.html(about_html, height=550, scrolling=False)
    st.stop()

# --- CONTACT ---
elif nav == "contact":
    contact_html = """
    <div style="padding: 20px 0; max-width: 1000px; margin: auto; font-family: system-ui, -apple-system, sans-serif;">
        
        <h1 style="color:#1e293b; margin-bottom:10px; font-size: 32px; font-weight: 800;">
            Contact Us
        </h1>
        <p style="font-size:16px; color:#64748b; margin-bottom: 40px; margin-top: 0;">
            Have questions about the project, want to collaborate, or discuss data analytics opportunities? Drop a line below!
        </p>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(450px, 1fr)); gap: 24px;">
            
            <div style="padding: 24px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);">
                <div style="font-weight: 700; font-size: 18px; color: #1e293b; margin-bottom: 6px;">Email</div>
                <div style="font-size: 14px; color: #64748b; margin-bottom: 12px;">Feel free to reach out directly for project inquiries or feedback.</div>
                <a href="mailto:devyanshsingh05@gmail.com" style="color: #2563eb; font-weight: 600; text-decoration: none; font-size: 15px;">devyanshsingh05@gmail.com →</a>
            </div>

            <div style="padding: 24px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);">
                <div style="font-weight: 700; font-size: 18px; color: #1e293b; margin-bottom: 6px;">Phone Number</div>
                <div style="font-size: 14px; color: #64748b; margin-bottom: 12px;">Let's connect directly via call or message.</div>
                <a href="tel:+917055530007" style="color: #2563eb; font-weight: 600; text-decoration: none; font-size: 15px;">+91 70555 30007 →</a>
            </div>

            <div style="padding: 24px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);">
                <div style="font-weight: 700; font-size: 18px; color: #1e293b; margin-bottom: 6px;">LinkedIn Profile</div>
                <div style="font-size: 14px; color: #64748b; margin-bottom: 12px;">Let's connect! I post about my software developments and technical milestones.</div>
                <a href="https://linkedin.com/in/devyanshsingh05" target="_blank" style="color: #2563eb; font-weight: 600; text-decoration: none; font-size: 15px;">linkedin.com/in/devyanshsingh05 →</a>
            </div>

            <div style="padding: 24px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);">
                <div style="font-weight: 700; font-size: 18px; color: #1e293b; margin-bottom: 6px;">Source Code & Contributions (GitHub)</div>
                <div style="font-size: 14px; color: #64748b; margin-bottom: 12px;">Check out source repositories, builds, and development contributions.</div>
                <a href="https://github.com/devyansh-01" target="_blank" style="color: #2563eb; font-weight: 600; text-decoration: none; font-size: 15px;">github.com/devyansh-01 →</a>
            </div>

        </div>
    </div>
    """
    components.html(contact_html, height=600, scrolling=False)
    st.stop()

# --- UPLOAD SECTION (home only) ---
st.markdown('<div id="upload_area"></div>', unsafe_allow_html=True)
with st.container():
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<h2 style='text-align: center; color: #1e293b; margin-top: 10px;'>Upload Your Dataset</h2>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("", type=["csv", "xlsx", "txt"])

# --- DASHBOARD ---
if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'): df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'): df = pd.read_excel(uploaded_file)
        else: df = pd.read_csv(uploaded_file, sep=None, engine='python')

        st.markdown("---")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Rows Processed", f"{df.shape[0]:,}")
        m2.metric("Features", df.shape[1])
        m3.metric("Status", "Optimized")
        m4.metric("Time Saved", "40%")

        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Stats Summary", "🧹 Health Audit", "📈 Visual Lab", "🤖 AI Insights", "📥 Download Report"])

        with tab1:
            st.dataframe(df.describe(include='all').fillna('-'), use_container_width=True)
            with st.expander("View Raw Data"):
                st.dataframe(df.head(50), use_container_width=True)

        with tab2:
            st.subheader("Data Integrity Scan")
            col_a, col_b = st.columns([2, 1])
            with col_a:
                st.plotly_chart(px.imshow(df.isnull(), color_continuous_scale=['#f8fafc', '#4f46e5']), use_container_width=True)
            with col_b:
                st.write(f"**Missing Values:** {df.isnull().sum().sum()}")
                st.write(f"**Duplicates:** {df.duplicated().sum()}")

        with tab3:
            st.subheader("Interactive Visual Library")
            num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            cat_cols = df.select_dtypes(include=['object']).columns.tolist()
            selection = st.selectbox("Choose a Visualization Type:", [
                "1. Numerical Distribution (Histogram & Box Plot)",
                "2. Correlation Heatmap (Feature Relationships)",
                "3. Scatter Plot (Bivariate Analysis)",
                "4. Categorical Breakdown (Pie Chart)",
                "5. Outlier Scanning (Violin Plot)"
            ])
            st.markdown("---")
            if "1." in selection and num_cols:
                col = st.selectbox("Select Column:", num_cols)
                st.plotly_chart(px.histogram(df, x=col, marginal="box", template="plotly_white", color_discrete_sequence=['#4f46e5']), use_container_width=True)
            elif "2." in selection and len(num_cols) > 1:
                st.plotly_chart(px.imshow(df[num_cols].corr(), text_auto=True, color_continuous_scale="RdBu_r"), use_container_width=True)
            elif "3." in selection and len(num_cols) >= 2:
                col_x = st.selectbox("X Axis:", num_cols, index=0)
                col_y = st.selectbox("Y Axis:", num_cols, index=1)
                st.plotly_chart(px.scatter(df, x=col_x, y=col_y, template="plotly_white", color_discrete_sequence=['#4f46e5']), use_container_width=True)
            elif "4." in selection and cat_cols:
                col = st.selectbox("Category Column:", cat_cols)
                st.plotly_chart(px.pie(df, names=col, hole=0.4), use_container_width=True)
            elif "5." in selection and num_cols:
                col = st.selectbox("Select Column to Scan:", num_cols)
                st.plotly_chart(px.violin(df, y=col, box=True, points="all", color_discrete_sequence=['#818cf8']), use_container_width=True)

        with tab4:
            num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            insights = [f"🔍 **Scale:** {df.shape[0]} observations across {df.shape[1]} variables."]
            if df.isnull().sum().sum() > 0:
                insights.append(f"⚠️ **Alert:** Found {df.isnull().sum().sum()} empty cells.")
            else:
                insights.append("✅ **Clean Slate:** No missing data detected.")
            if len(num_cols) > 1:
                corr = df[num_cols].corr().unstack().sort_values(ascending=False)
                top_corr = corr[corr < 1].idxmax()
                insights.append(f"📈 **Trend:** Strongest link found between '{top_corr[0]}' and '{top_corr[1]}'.")
            for item in insights:
                st.info(item)

        with tab5:
            st.subheader("Export Analysis Report")
            col1, col2 = st.columns(2)
            with col1:
                buffer = io.BytesIO()
                try:
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                        df.to_excel(writer, index=False)
                    st.download_button("Download Excel Report", buffer.getvalue(), "report.xlsx", "application/vnd.ms-excel")
                except:
                    st.warning("Excel module issue. Downloading as CSV instead.")
                    st.download_button("Download CSV Data", df.to_csv(index=False), "data.csv", "text/csv")
            with col2:
                try:
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", 'B', 16)
                    pdf.cell(200, 10, "Insyte Data Analysis Report", ln=True, align='C')
                    pdf.set_font("Arial", '', 12)
                    pdf.ln(10)
                    pdf.cell(200, 10, f"Total Rows: {df.shape[0]}", ln=True)
                    pdf.cell(200, 10, f"Total Columns: {df.shape[1]}", ln=True)
                    pdf_data = pdf.output(dest='S').encode('latin-1')
                    st.download_button("Download PDF Report", pdf_data, "report.pdf", "application/pdf")
                except:
                    st.error("Please install fpdf (pip install fpdf) to enable PDF exports.")

    except Exception as e:
        st.error(f"Error: {e}")