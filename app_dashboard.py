import os
import requests
import streamlit as st
from streamlit_autorefresh import st_autorefresh

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

if not API_URL:
    raise ValueError("Environment variable 'API_URL' is not set")

st.set_page_config(
    page_title="SupportFlow AI — Customer Support",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ══ TOKENS — Modern Enterprise ══ */
:root {
    --bg-page: #F8FAFC;
    --bg-surface: #FFFFFF;
    --border-color: #E2E8F0;
    --text-main: #0F172A;
    --text-muted: #64748B;
    --primary: #2563EB;
    --primary-hover: #1D4ED8;
    --success: #10B981;
    --success-bg: #ECFDF5;
    --warning: #F59E0B;
    --warning-bg: #FEF3C7;
    --danger: #EF4444;
    --danger-bg: #FEF2F2;
    --info-bg: #EFF6FF;
    --info-text: #1E3A8A;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

[data-testid="stAppViewContainer"] { background: var(--bg-page) !important; color: var(--text-main) !important; }
[data-testid="stHeader"]  { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }
.block-container { padding: 2rem 3rem 4rem !important; max-width: 1200px !important; }

body, h1,h2,h3,h4,p,label,div,span,button,input,textarea {
    font-family: 'Outfit', sans-serif !important;
}

/* ── Topbar ── */
.topbar {
    display: flex; align-items: center; justify-content: space-between;
    padding-bottom: 1.5rem; border-bottom: 1px solid var(--border-color); margin-bottom: 2rem;
}
.tb-brand { display: flex; align-items: center; gap: 14px; }
.tb-logo {
    width: 42px; height: 42px; border-radius: 12px; background: var(--primary);
    display: flex; align-items: center; justify-content: center; flex-shrink: 0;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}
.tb-name { font-size: 18px !important; font-weight: 700 !important; color: var(--text-main) !important; letter-spacing: -0.01em; line-height: 1.2; }
.tb-sub  { font-size: 13px !important; color: var(--text-muted) !important; margin-top: 2px !important; }
.tb-online {
    display: inline-flex; align-items: center; gap: 8px;
    background: var(--success-bg); border: 1px solid rgba(16, 185, 129, 0.2); color: #047857;
    font-size: 12px; font-weight: 600; padding: 6px 14px; border-radius: 99px;
    font-family: 'JetBrains Mono', monospace !important; letter-spacing: 0.03em;
}
.tb-online::before {
    content: ''; width: 8px; height: 8px; border-radius: 50%; background: var(--success);
    box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2); display: block;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px !important; background: transparent !important;
    padding: 0 !important; margin-bottom: 2rem !important; border: none !important;
}
.stTabs [data-baseweb="tab"] {
    font-size: 15px !important; font-weight: 600 !important;
    padding: 10px 24px !important; color: var(--text-muted) !important;
    border-radius: 99px !important; border: 1px solid transparent !important; 
    transition: all 0.2s ease !important; background: transparent !important;
}
.stTabs [data-baseweb="tab"]:hover { background: #F1F5F9 !important; color: var(--text-main) !important; }
.stTabs [aria-selected="true"] { 
    background: var(--bg-surface) !important; 
    color: var(--primary) !important; 
    border-color: var(--border-color) !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* ── Section label ── */
.slabel {
    font-size: 11px !important; font-weight: 700 !important; color: var(--text-muted) !important;
    text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.75rem !important; display: block;
}

/* ── Landing ── */
.land-hero { text-align: center; padding: 4rem 1rem 3rem; }
.land-logo-wrap {
    width: 64px; height: 64px; border-radius: 16px; background: var(--primary);
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 1.5rem;
    box-shadow: 0 8px 24px rgba(37, 99, 235, 0.25);
}
.land-h   { font-size: 28px !important; font-weight: 700 !important; color: var(--text-main) !important; letter-spacing: -0.02em; margin-bottom: 12px !important; }
.land-sub { font-size: 15px !important; color: var(--text-muted) !important; margin-bottom: 3rem !important; }

.choice-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; max-width: 560px; margin: 0 auto; }
.choice-card {
    background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: 16px;
    padding: 1.75rem 1.5rem; text-align: left; cursor: pointer;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}
.choice-card:hover { 
    border-color: var(--primary); 
    box-shadow: 0 12px 24px -8px rgba(37, 99, 235, 0.15); 
    transform: translateY(-4px);
}
.choice-card-icon  { font-size: 28px; margin-bottom: 14px; }
.choice-card-title { font-size: 16px !important; font-weight: 700 !important; color: var(--text-main) !important; margin-bottom: 6px !important; }
.choice-card-desc  { font-size: 13px !important; color: var(--text-muted) !important; line-height: 1.6; }

/* ── Ticket chip ── */
.tkt-block { margin-bottom: 2rem; }
.tkt-chip {
    display: inline-flex; align-items: center; gap: 10px;
    background: var(--primary); color: #FFFFFF;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 18px; font-weight: 500; letter-spacing: 0.05em;
    padding: 12px 20px; border-radius: 12px;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}
.tkt-dot {
    width: 8px; height: 8px; border-radius: 50%; background: #60A5FA;
    box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.3); flex-shrink: 0;
}

/* ── Banners ── */
.banner-created {
    display: flex; align-items: flex-start; gap: 14px;
    background: var(--success-bg); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 12px;
    padding: 18px 22px; margin-bottom: 1.5rem; animation: rise 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
.banner-submit {
    display: flex; align-items: center; gap: 12px;
    background: var(--success-bg); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 10px;
    padding: 14px 18px; margin: 1rem 0; animation: rise 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.banner-warn {
    background: var(--warning-bg); border: 1px solid rgba(245, 158, 11, 0.2); border-radius: 10px;
    padding: 12px 16px; font-size: 13.5px; color: #92400E; font-weight: 500; margin: 1rem 0;
}
.banner-info {
    background: var(--info-bg); border: 1px solid rgba(37, 99, 235, 0.2); border-radius: 10px;
    padding: 12px 16px; font-size: 13.5px; color: var(--info-text); margin: 1rem 0; font-weight: 500;
}
@keyframes rise { from { opacity:0; transform:translateY(8px); } to { opacity:1; transform:translateY(0); } }

.check-ring {
    flex-shrink: 0; width: 32px; height: 32px; border-radius: 50%;
    background: var(--success); display: flex; align-items: center; justify-content: center;
    color: #fff; font-size: 16px; font-weight: 700;
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
}
.check-ring-sm {
    flex-shrink: 0; width: 24px; height: 24px; border-radius: 50%;
    background: var(--success); display: flex; align-items: center; justify-content: center;
    color: #fff; font-size: 12px; font-weight: 700;
}
.banner-created-title { font-size: 15px !important; font-weight: 700 !important; color: #065F46 !important; margin-bottom: 4px !important; }
.banner-created-sub   { font-size: 13px !important; color: #047857 !important; line-height: 1.5; }
.banner-submit-text   { font-size: 14px !important; font-weight: 600 !important; color: #065F46 !important; }
.banner-submit-sub    { font-size: 12.5px !important; color: #047857 !important; }

/* ── Conversation ── */
.conv-wrap { display: flex; flex-direction: column; gap: 12px; margin-bottom: 2rem; }
.bubble { padding: 14px 18px; border-radius: 16px; position: relative; }
.bubble-customer { background: var(--bg-surface); border: 1px solid var(--border-color); box-shadow: 0 2px 8px rgba(0,0,0,0.02); align-self: flex-end; max-width: 85%; border-bottom-right-radius: 4px; }
.bubble-support  { background: #F0F9FF; border: 1px solid #BAE6FD; align-self: flex-start; max-width: 85%; border-bottom-left-radius: 4px; }
.bubble-role { font-size: 11px !important; font-weight: 700 !important; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px !important; }
.bubble-role-c { color: var(--text-muted) !important; }
.bubble-role-s { color: #0284C7 !important; }
.bubble-text   { font-size: 14.5px !important; color: var(--text-main) !important; line-height: 1.6; }
.bubble-time   { font-size: 11px !important; color: #94A3B8 !important; margin-top: 8px !important; font-family: 'JetBrains Mono', monospace !important; }
.conv-sep { display: none; }

/* ── Stats ── */
.stats-row { display: grid; grid-template-columns: repeat(3,1fr); gap: 16px; margin-bottom: 2rem; }
.stat-box {
    background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: 16px; padding: 1.25rem 1.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02);
}
.stat-label { font-size: 11px !important; color: var(--text-muted) !important; font-weight: 700 !important; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px !important; }
.stat-val   { font-family: 'JetBrains Mono', monospace !important; font-size: 32px !important; font-weight: 600 !important; color: var(--text-main) !important; }

/* ── Customer info ── */
.cust-info {
    background: var(--bg-surface); border: 1px solid var(--border-color); border-left: 4px solid var(--primary);
    border-radius: 12px; padding: 1.25rem 1.5rem; margin-bottom: 1.5rem;
    display: flex; gap: 3rem; flex-wrap: wrap; box-shadow: 0 2px 8px rgba(0,0,0,0.02);
}
.cf-label { font-size: 11px !important; font-weight: 700 !important; color: var(--text-muted) !important; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px !important; }
.cf-val   { font-size: 15px !important; font-weight: 600 !important; color: var(--text-main) !important; }
.cf-mono  { font-family: 'JetBrains Mono', monospace !important; color: var(--primary) !important; }

/* ── Result banners ── */
.res-banner { display:flex; align-items:flex-start; gap:14px; border-radius:12px; padding:16px 20px; margin-bottom:1.5rem; animation: rise 0.4s cubic-bezier(0.16, 1, 0.3, 1); }
.res-icon   { flex-shrink:0; width:28px; height:28px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:14px; font-weight:700; color:#fff; }
.res-title  { font-size:15px !important; font-weight:700 !important; margin-bottom:4px; }
.res-detail { font-size:13px !important; line-height:1.6; }
.res-ok  { background:var(--success-bg); border:1px solid rgba(16,185,129,0.2); }
.res-ok  .res-icon   { background:var(--success); box-shadow: 0 4px 12px rgba(16,185,129,0.2); }
.res-ok  .res-title  { color:#065F46 !important; }
.res-ok  .res-detail { color:#047857 !important; }
.res-bad { background:var(--danger-bg); border:1px solid rgba(239,68,68,0.2); }
.res-bad .res-icon   { background:var(--danger); box-shadow: 0 4px 12px rgba(239,68,68,0.2); }
.res-bad .res-title  { color:#991B1B !important; }
.res-bad .res-detail { color:#B91C1C !important; }

.divider { border:none; border-top:1px solid var(--border-color); margin:2rem 0; }

/* ══ Streamlit overrides ══ */
.stTextInput > div > div > input {
    border-radius: 10px !important; border: 1px solid var(--border-color) !important;
    font-size: 14.5px !important; padding: 12px 16px !important;
    background: var(--bg-surface) !important; color: var(--text-main) !important;
    -webkit-text-fill-color: var(--text-main) !important;
    font-family: 'Outfit', sans-serif !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02) !important;
}
.stTextInput > div > div > input::placeholder { color: #94A3B8 !important; opacity: 1 !important; }
.stTextInput > div > div > input:focus {
    border-color: var(--primary) !important; box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.1) !important; outline: none !important;
}
.stTextInput > div > div > input:disabled {
    background: #F1F5F9 !important; color: #94A3B8 !important; -webkit-text-fill-color: #94A3B8 !important; opacity: 1 !important;
}
.stTextArea > div > div > textarea {
    border-radius: 12px !important; border: 1px solid var(--border-color) !important;
    font-size: 14.5px !important; background: var(--bg-surface) !important;
    color: var(--text-main) !important; -webkit-text-fill-color: var(--text-main) !important;
    line-height: 1.65 !important; font-family: 'Outfit', sans-serif !important;
    transition: all 0.2s ease !important; padding: 16px !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02) !important;
}
.stTextArea > div > div > textarea:focus {
    border-color: var(--primary) !important; box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.1) !important; outline: none !important;
}
.stTextArea > div > div > textarea:disabled {
    background: #F1F5F9 !important; color: #94A3B8 !important; -webkit-text-fill-color: #94A3B8 !important; opacity: 1 !important;
}
.stTextArea > div > div > textarea::placeholder { color: #94A3B8 !important; opacity: 1 !important; }
.stButton > button {
    border-radius: 10px !important; font-size: 14.5px !important; font-weight: 600 !important;
    padding: 12px 24px !important; transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    font-family: 'Outfit', sans-serif !important; letter-spacing: 0.02em;
}
.stButton > button[kind="primary"] {
    background: var(--primary) !important; color: #FFFFFF !important; border: none !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2) !important;
}
.stButton > button[kind="primary"]:hover {
    background: var(--primary-hover) !important;
    transform: translateY(-2px) !important; box-shadow: 0 6px 16px rgba(37, 99, 235, 0.3) !important;
}
.stButton > button[kind="secondary"] {
    background: var(--bg-surface) !important; color: var(--text-main) !important; border: 1px solid var(--border-color) !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
}
.stButton > button[kind="secondary"]:hover { 
    background: #F8FAFC !important; border-color: #CBD5E1 !important; 
    transform: translateY(-2px) !important;
}

div[data-testid="stVerticalBlock"]:has(> div.st-key-approve-action) button[kind="primary"] {
    background: var(--success) !important; border: none !important;
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2) !important;
}
div[data-testid="stVerticalBlock"]:has(> div.st-key-approve-action) button[kind="primary"]:hover {
    background: #059669 !important; box-shadow: 0 6px 16px rgba(16, 185, 129, 0.3) !important;
}
div[data-testid="stVerticalBlock"]:has(> div.st-key-reject-action) button[kind="secondary"] {
    color: var(--danger) !important; border-color: rgba(239, 68, 68, 0.3) !important; background: var(--danger-bg) !important;
}
div[data-testid="stVerticalBlock"]:has(> div.st-key-reject-action) button[kind="secondary"]:hover {
    background: #FEE2E2 !important; border-color: var(--danger) !important;
}

[data-testid="stCheckboxLabelText"], [data-testid="stCheckboxLabelText"] p,
[data-testid="stCheckbox"] label, [data-testid="stCheckbox"] label p,
[data-testid="stCheckbox"] label span, [data-testid="stCheckbox"] * {
    color: var(--text-main) !important; -webkit-text-fill-color: var(--text-main) !important;
    font-size: 14.5px !important; font-weight: 500 !important; opacity: 1 !important;
}
[data-testid="stCheckbox"] { background: #FFFFFF; border: 1px solid var(--border-color); border-radius: 12px; padding: 14px 18px; box-shadow: 0 1px 3px rgba(0,0,0,0.02); transition: all 0.2s; }
[data-testid="stCheckbox"]:hover { border-color: #94A3B8; }

label[data-testid="stWidgetLabel"] p {
    font-size: 11.5px !important; font-weight: 700 !important; color: var(--text-muted) !important;
    text-transform: uppercase !important; letter-spacing: 0.1em !important; margin-bottom: 8px !important;
}
[data-testid="stAlert"] { border-radius: 12px !important; font-size: 14.5px !important; border: 1px solid var(--border-color) !important; }
[data-testid="stAlertContentSuccess"], [data-testid="stAlertContentSuccess"] * { color: #065F46 !important; -webkit-text-fill-color: #065F46 !important; }
[data-testid="stAlertContentError"],   [data-testid="stAlertContentError"] *   { color: #991B1B !important; -webkit-text-fill-color: #991B1B !important; }
[data-testid="stAlertContentInfo"],    [data-testid="stAlertContentInfo"] *    { color: var(--info-text) !important; -webkit-text-fill-color: var(--info-text) !important; }
div[data-testid="stAlertContainer"]:has([data-testid="stAlertContentSuccess"]) { background: var(--success-bg) !important; border-color: rgba(16, 185, 129, 0.2) !important; }
div[data-testid="stAlertContainer"]:has([data-testid="stAlertContentError"])   { background: var(--danger-bg) !important; border-color: rgba(239, 68, 68, 0.2) !important; }
div[data-testid="stAlertContainer"]:has([data-testid="stAlertContentInfo"])    { background: var(--info-bg) !important; border-color: rgba(37, 99, 235, 0.2) !important; }
[data-testid="stExpander"] { border: 1px solid var(--border-color) !important; border-radius: 12px !important; background: var(--bg-surface) !important; box-shadow: 0 1px 3px rgba(0,0,0,0.02) !important; }
[data-testid="stExpander"] summary, [data-testid="stExpander"] summary span {
    color: var(--text-main) !important; font-weight: 600 !important; font-size: 14.5px !important;
}
</style>
""", unsafe_allow_html=True)

# ── Logo SVG (reused) ──
LOGO_SVG = """
<svg width="22" height="22" viewBox="0 0 22 22" fill="none">
  <rect x="3" y="3" width="12" height="12" rx="2.5" fill="white" opacity="0.3"/>
  <rect x="7" y="7" width="12" height="12" rx="2.5" fill="white"/>
</svg>"""

LOGO_SVG_LG = """
<svg width="30" height="30" viewBox="0 0 30 30" fill="none">
  <rect x="4" y="4" width="15" height="15" rx="3" fill="white" opacity="0.3"/>
  <rect x="11" y="11" width="15" height="15" rx="3" fill="white"/>
</svg>"""

# ── TOPBAR ──
st.markdown(f"""
<div class="topbar">
  <div class="tb-brand">
    <div class="tb-logo">{LOGO_SVG}</div>
    <div>
      <div class="tb-name">SupportFlow AI</div>
      <div class="tb-sub">AI-Powered Customer Support</div>
    </div>
  </div>
  <span class="tb-online">System online</span>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["  Customer portal  ", "  Supervisor review  "])


# ══════════════════════════════════════════
#  CUSTOMER PORTAL
# ══════════════════════════════════════════

with tab1:

    if "customer_view"        not in st.session_state: st.session_state["customer_view"]        = "landing"
    if "ticket_id"            not in st.session_state: st.session_state["ticket_id"]            = None
    if "thread_id"            not in st.session_state: st.session_state["thread_id"]            = None
    if "conversation_history" not in st.session_state: st.session_state["conversation_history"] = []
    if "query_box_gen"        not in st.session_state: st.session_state["query_box_gen"]        = 0
    if "is_submitted"         not in st.session_state: st.session_state["is_submitted"]         = False
    if "msg_submitted"        not in st.session_state: st.session_state["msg_submitted"]        = False
    if "customer_name"        not in st.session_state: st.session_state["customer_name"]        = ""

    view = st.session_state["customer_view"]

    # ── LANDING ──
    if view == "landing":
        st.markdown(f"""
        <div class="land-hero">
          <div class="land-logo-wrap">{LOGO_SVG_LG}</div>
          <div class="land-h">How can we help you?</div>
          <div class="land-sub">Submit a new request or continue an existing conversation.</div>
        </div>
        """, unsafe_allow_html=True)

        _, c_new, c_cont, _ = st.columns([1,2,2,1], gap="medium")

        with c_new:
            st.markdown("""
            <div class="choice-card">
              <div class="choice-card-icon">✉️</div>
              <div class="choice-card-title">New ticket</div>
              <div class="choice-card-desc">Describe your issue and a support agent will respond.</div>
            </div>""", unsafe_allow_html=True)
            if st.button("Start new ticket", type="primary", use_container_width=True, key="btn_new"):
                st.session_state["customer_view"] = "create"
                st.rerun()

        with c_cont:
            st.markdown("""
            <div class="choice-card">
              <div class="choice-card-icon">🔍</div>
              <div class="choice-card-title">Continue existing</div>
              <div class="choice-card-desc">Have a ticket ID? Resume the conversation.</div>
            </div>""", unsafe_allow_html=True)
            if st.button("Continue ticket", type="secondary", use_container_width=True, key="btn_cont"):
                st.session_state["customer_view"] = "continue"
                st.rerun()

    # ── CREATE TICKET ──
    elif view == "create":
        if st.button("← Back", key="back_create"):
            st.session_state["customer_view"] = "landing"; st.rerun()

        st.markdown('<span class="slabel">New support ticket</span>', unsafe_allow_html=True)

        c1, c2 = st.columns(2, gap="medium")
        with c1:
            name_input  = st.text_input("Customer Name",  placeholder="e.g. Alice Johnson",      key="create_name")
        with c2:
            email_input = st.text_input("Email",          placeholder="e.g. alice@example.com",  key="create_email")

        issue_input = st.text_area("Issue Description", height=148,
            placeholder="e.g. I was charged twice for invoice INV-404. My customer ID is CUST-101.",
            key="create_issue")

        if st.button("Create Ticket", type="primary", use_container_width=True, key="btn_create"):
            if not name_input.strip():   st.error("Enter your name.")
            elif not email_input.strip(): st.error("Enter your email.")
            elif not issue_input.strip(): st.error("Describe your issue.")
            else:
                try:
                    r = requests.post(f"{API_URL}/ticket/create", json={
                        "customer_name": name_input.strip(), "customer_email": email_input.strip(),
                        "query": issue_input.strip(), "thread_id": None })
                    if r.status_code == 200:
                        d = r.json()
                        st.session_state["ticket_id"]            = d["ticket_id"]
                        st.session_state["thread_id"]            = d["thread_id"]
                        st.session_state["customer_name"]        = name_input.strip()
                        st.session_state["conversation_history"] = d.get("data",{}).get("conversation_history",[])
                        st.session_state["customer_view"]        = "chat"
                        st.session_state["is_submitted"]         = True
                        st.rerun()
                    else: st.error("Could not create ticket. Please try again.")
                except requests.exceptions.RequestException:
                    st.error("Could not reach the support system. Please try again.")

    # ── CONTINUE ──
    elif view == "continue":
        if st.button("← Back", key="back_continue"):
            st.session_state["customer_view"] = "landing"; st.rerun()

        st.markdown('<span class="slabel">Resume a ticket</span>', unsafe_allow_html=True)

        lookup_id = st.text_input("Support Ticket ID", placeholder="e.g. TKT-8A91F3D2", key="continue_tid")

        if st.button("Load Ticket", type="primary", use_container_width=True, key="btn_load"):
            if not lookup_id.strip(): st.error("Enter your ticket ID.")
            else:
                raw_id = lookup_id.strip().upper().replace("TKT-","")
                try:
                    r = requests.get(f"{API_URL}/ticket/state/{raw_id}")
                    if r.status_code == 200:
                        d    = r.json()
                        info = d.get("ticket",{})
                        state= d.get("state",{})
                        st.session_state["ticket_id"]            = info.get("ticket_id", lookup_id.strip().upper())
                        st.session_state["thread_id"]            = raw_id
                        st.session_state["customer_name"]        = info.get("customer_name","")
                        st.session_state["conversation_history"] = state.get("conversation_history",[])
                        st.session_state["customer_view"]        = "chat"
                        st.session_state["is_submitted"]         = False
                        st.rerun()
                    else: st.error("Ticket not found. Check your ID and try again.")
                except requests.exceptions.RequestException:
                    st.error("Could not reach the support system. Please try again.")

    # ── CHAT ──
    elif view == "chat":
        ticket_id = st.session_state.get("ticket_id","")
        thread_id = st.session_state.get("thread_id","")

        if st.session_state.get("is_submitted"):
            st.markdown(f"""
            <div class="banner-created">
              <div class="check-ring">✓</div>
              <div>
                <div class="banner-created-title">✅ Ticket created successfully</div>
                <div class="banner-created-sub">Your request is in the queue. Save your ticket ID to follow up.</div>
              </div>
            </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="tkt-block">
          <span class="slabel">Support ticket ID</span>
          <div class="tkt-chip"><span class="tkt-dot"></span>{ticket_id}</div>
        </div>""", unsafe_allow_html=True)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        conversation = st.session_state.get("conversation_history",[])
        if conversation:
            st.markdown('<span class="slabel">Conversation</span>', unsafe_allow_html=True)
            st.markdown('<div class="conv-wrap">', unsafe_allow_html=True)
            for i, msg in enumerate(conversation):
                role = msg.get("role","customer")
                if role == "customer":
                    lbl,bcls,rcls = "You","bubble-customer","bubble-role-c"
                else:
                    lbl,bcls,rcls = "SupportFlow AI","bubble-support","bubble-role-s"
                st.markdown(f"""
                <div class="bubble {bcls}">
                  <div class="bubble-role {rcls}">{lbl}</div>
                  <div class="bubble-text">{msg.get("text","")}</div>
                  <div class="bubble-time">{msg.get("submitted_at","")}</div>
                </div>""", unsafe_allow_html=True)
                if i < len(conversation)-1:
                    st.markdown('<hr class="conv-sep">', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('<hr class="divider">', unsafe_allow_html=True)

        if st.session_state.get("msg_submitted"):
            st.markdown("""
            <div class="banner-submit">
              <div class="check-ring-sm">✓</div>
              <div>
                <div class="banner-submit-text">✅ Your message has been submitted successfully.</div>
                <div class="banner-submit-sub">Our support team will review it.</div>
              </div>
            </div>""", unsafe_allow_html=True)
            tick = st_autorefresh(interval=1000, limit=6, key="msg_timer")
            if tick is not None and tick >= 5:
                st.session_state["msg_submitted"] = False; st.rerun()

        st.markdown('<span class="slabel">Send a message</span>', unsafe_allow_html=True)
        new_msg = st.text_area("Message", height=120, placeholder="Add more details or ask a follow-up question...",
            label_visibility="collapsed", key=f"chat_msg_{st.session_state['query_box_gen']}")

        if new_msg.strip() and st.session_state.get("msg_submitted"):
            st.session_state["msg_submitted"] = False

        sc, bc = st.columns([3,1], gap="small")
        with sc: send_btn = st.button("Send Message", type="primary", use_container_width=True, key="btn_send")
        with bc:
            if st.button("New ticket", type="secondary", use_container_width=True, key="btn_new_chat"):
                st.session_state["customer_view"] = "landing"
                st.session_state["is_submitted"]  = False
                st.session_state["msg_submitted"] = False
                st.rerun()

        if send_btn:
            if not new_msg.strip(): st.error("Type a message before sending.")
            else:
                try:
                    r = requests.post(f"{API_URL}/ticket/create", json={
                        "customer_name": st.session_state.get("customer_name",""),
                        "customer_email": "", "query": new_msg.strip(), "thread_id": thread_id })
                    if r.status_code == 200:
                        d = r.json()
                        st.session_state["conversation_history"] = d.get("data",{}).get("conversation_history",[])
                        st.session_state["is_submitted"]         = False
                        st.session_state["msg_submitted"]        = True
                        st.session_state["query_box_gen"]        += 1
                        st.rerun()
                    else: st.error("Could not send message. Please try again.")
                except requests.exceptions.RequestException:
                    st.error("Could not reach the support system. Please try again.")


# ══════════════════════════════════════════
#  SUPERVISOR REVIEW
# ══════════════════════════════════════════

with tab2:

    if "review_outcome" in st.session_state:
        kind, msg = st.session_state.pop("review_outcome")
        if kind == "approved":
            st.balloons()
            st.markdown(f"""
            <div class="res-banner res-ok">
              <span class="res-icon">✓</span>
              <div><div class="res-title">Approved</div><div class="res-detail">{msg}</div></div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="res-banner res-bad">
              <span class="res-icon">✕</span>
              <div><div class="res-title">Rejected</div><div class="res-detail">{msg}</div></div>
            </div>""", unsafe_allow_html=True)

    try:
        cr = requests.get(f"{API_URL}/ticket/queue/counts", timeout=3)
        qc = cr.json() if cr.status_code == 200 else {}
    except: qc = {}

    p = qc.get("pending_review",0)
    a = qc.get("approved",0)
    rj= qc.get("rejected",0)

    st.markdown(f"""
    <div class="stats-row">
      <div class="stat-box"><div class="stat-label">Awaiting review</div><div class="stat-val">{p}</div></div>
      <div class="stat-box"><div class="stat-label">Approved</div><div class="stat-val">{a}</div></div>
      <div class="stat-box"><div class="stat-label">Rejected</div><div class="stat-val">{rj}</div></div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<span class="slabel">Pending queue</span>', unsafe_allow_html=True)

    if "response_version" not in st.session_state:
        st.session_state["response_version"] = 0

    _, btn_col = st.columns([5,1], gap="small")
    with btn_col:
        load_btn = st.button("Load next", type="primary", use_container_width=True, key="sup_load")

    if load_btn:
        try:
            r = requests.get(f"{API_URL}/ticket/next")
            if r.status_code == 200:
                result = r.json()
                if result.get("status") == "empty":
                    st.info("No tickets are waiting for review right now.")
                    for k in ["review_thread","loaded_response","loaded_conversation","loaded_ticket_info","sup_feedback","sup_confirm"]:
                        st.session_state.pop(k,None)
                else:
                    ti = result.get("ticket",{})
                    sd = result.get("data",{})
                    st.session_state["review_thread"]       = ti.get("thread_id", result.get("thread_id"))
                    st.session_state["loaded_ticket_info"]  = ti
                    st.session_state["loaded_response"]     = sd.get("draft_response","")
                    st.session_state["loaded_conversation"] = sd.get("conversation_history",[])
                    st.session_state["response_version"]   += 1
            else: st.error("Couldn't reach the queue. Please try again.")
        except requests.exceptions.RequestException as e:
            st.error(f"Backend error: {e}")

    review_thread = st.session_state.get("review_thread","")

    if not review_thread:
        st.markdown('<div class="banner-info">📋 Click "Load next" to pull the oldest pending ticket from the queue.</div>', unsafe_allow_html=True)
    else:
        ti          = st.session_state.get("loaded_ticket_info",{})
        display_tid = ti.get("ticket_id", f"TKT-{review_thread}")
        cust_name   = ti.get("customer_name","—")
        cust_email  = ti.get("customer_email","—")

        st.markdown(f"""
        <div class="cust-info">
          <div><div class="cf-label">Ticket ID</div><div class="cf-val cf-mono">{display_tid}</div></div>
          <div><div class="cf-label">Name</div><div class="cf-val">{cust_name}</div></div>
          <div><div class="cf-label">Email</div><div class="cf-val">{cust_email}</div></div>
        </div>""", unsafe_allow_html=True)

        conversation = st.session_state.get("loaded_conversation",[])
        if conversation:
            st.markdown('<span class="slabel">Conversation</span>', unsafe_allow_html=True)
            st.markdown('<div class="conv-wrap">', unsafe_allow_html=True)
            for i, msg in enumerate(conversation):
                role = msg.get("role","customer")
                if role == "customer":
                    lbl,bcls,rcls = "Customer","bubble-customer","bubble-role-c"
                else:
                    lbl,bcls,rcls = "SupportFlow AI","bubble-support","bubble-role-s"
                st.markdown(f"""
                <div class="bubble {bcls}">
                  <div class="bubble-role {rcls}">{lbl}</div>
                  <div class="bubble-text">{msg.get("text","")}</div>
                  <div class="bubble-time">{msg.get("submitted_at","")}</div>
                </div>""", unsafe_allow_html=True)
                if i < len(conversation)-1:
                    st.markdown('<hr class="conv-sep">', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<div class="banner-warn">⚠️ Review carefully before approving — response sends directly to the customer and cannot be undone.</div>', unsafe_allow_html=True)

        lp, rp = st.columns([3,2], gap="medium")

        with lp:
            st.markdown('<span class="slabel">AI suggested response — edit before deciding</span>', unsafe_allow_html=True)
            edited_response = st.text_area("AI response",
                value=st.session_state.get("loaded_response",""),
                height=280, label_visibility="collapsed",
                key=f"sup_response_box_{st.session_state.get('response_version', 0)}")

        with rp:
            st.markdown('<span class="slabel">Decision</span>', unsafe_allow_html=True)
            feedback = st.text_area("Rejection reason (only if rejecting)", height=100,
                placeholder="e.g. Incorrect balance, tone too informal...", key="sup_feedback")
            st.checkbox("Confirm: I authorize this response to be sent", key="sup_confirm")

            ac, rc = st.columns(2, gap="small")
            with ac:
                with st.container(key="approve-action"):
                    approve_btn = st.button("Approve", type="primary", use_container_width=True)
            with rc:
                with st.container(key="reject-action"):
                    reject_btn = st.button("Reject & Regenerate", type="secondary", use_container_width=True)

        decision = True if approve_btn else (False if reject_btn else None)

        if decision is not None:
            try:
                r = requests.post(f"{API_URL}/ticket/review", json={
                    "thread_id": review_thread, "approved": decision,
                    "feedback": st.session_state.get("sup_feedback",""),
                    "edited_response": edited_response })
                result = r.json()
                if r.status_code == 200:
                    rd = result.get("data",{})
                    if decision:
                        st.session_state["review_outcome"] = ("approved","The response has been sent to the customer.")
                        for k in ["review_thread","loaded_response","loaded_conversation","loaded_ticket_info","sup_feedback","sup_confirm"]:
                            st.session_state.pop(k,None)
                    else:
                        st.session_state["loaded_response"]     = rd.get("draft_response","")
                        st.session_state["loaded_conversation"] = rd.get("conversation_history",[])
                        st.session_state["response_version"]   += 1
                        st.session_state["review_outcome"]      = ("rejected","A new draft has been generated for your review.")
                    st.rerun()
                else: st.error(f"Review API error: {result}")
            except requests.exceptions.RequestException as e:
                st.error(f"Review submission failed: {e}")