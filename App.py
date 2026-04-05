import streamlit as st
import requests
import time
import pandas as pd
import base64

st.set_page_config(
    page_title="Sales Data Import",
    page_icon="",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #1a1a4e 40%, #24243e 100%);
    min-height: 100vh;
}

.main .block-container {
    padding-top: 3rem;
    padding-bottom: 3rem;
    max-width: 720px;
}

.header-badge {
    display: inline-block;
    background: rgba(99, 102, 241, 0.15);
    border: 1px solid rgba(99, 102, 241, 0.4);
    color: #a5b4fc;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 20px;
    margin-bottom: 1rem;
}

.main-title {
    font-size: 2.4rem;
    font-weight: 600;
    background: linear-gradient(90deg, #ffffff 0%, #a5b4fc 60%, #818cf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.2;
    margin-bottom: 0.5rem;
}

.subtitle {
    color: #94a3b8;
    font-size: 0.95rem;
    font-weight: 300;
    margin-bottom: 2.5rem;
    line-height: 1.6;
}

.card {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 1.8rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(10px);
}

.card-title {
    color: #e2e8f0;
    font-size: 0.78rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 1rem;
    opacity: 0.6;
}

.step-row {
    display: flex;
    gap: 0.8rem;
    margin-bottom: 0.8rem;
    align-items: flex-start;
}

.step-num {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    font-weight: 500;
    width: 22px;
    height: 22px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 1px;
}

.step-text {
    color: #cbd5e1;
    font-size: 0.88rem;
    line-height: 1.5;
}

.step-text strong {
    color: #e2e8f0;
    font-weight: 500;
}

.meta-row {
    display: flex;
    gap: 1.5rem;
    padding-top: 0.8rem;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin-top: 0.8rem;
}

.meta-item {
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    color: #64748b;
}

.meta-item span {
    color: #a5b4fc;
    font-weight: 500;
}

.status-success {
    background: rgba(16, 185, 129, 0.08);
    border: 1px solid rgba(16, 185, 129, 0.25);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    color: #6ee7b7;
    font-size: 0.9rem;
}

.status-error {
    background: rgba(239, 68, 68, 0.08);
    border: 1px solid rgba(239, 68, 68, 0.25);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    color: #fca5a5;
    font-size: 0.9rem;
}

.status-info {
    background: rgba(99, 102, 241, 0.08);
    border: 1px solid rgba(99, 102, 241, 0.25);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    color: #a5b4fc;
    font-size: 0.9rem;
    font-family: 'DM Mono', monospace;
    font-size: 12px;
}

div[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.03);
    border: 1.5px dashed rgba(99, 102, 241, 0.35);
    border-radius: 12px;
    padding: 0.5rem;
    transition: border-color 0.2s;
}

div[data-testid="stFileUploader"]:hover {
    border-color: rgba(99, 102, 241, 0.6);
}

div[data-testid="stFileUploader"] label {
    color: #94a3b8 !important;
}

.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.65rem 2rem;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    font-size: 0.9rem;
    letter-spacing: 0.02em;
    width: 100%;
    transition: opacity 0.2s, transform 0.1s;
    cursor: pointer;
}

.stButton > button:hover {
    opacity: 0.9;
    transform: translateY(-1px);
}

.stButton > button:active {
    transform: translateY(0);
}

div[data-testid="stExpander"] {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
}

div[data-testid="stExpander"] summary {
    color: #94a3b8;
    font-size: 0.85rem;
}

.stProgress > div > div {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    border-radius: 4px;
}

.stDataFrame {
    border-radius: 8px;
    overflow: hidden;
}

hr {
    border-color: rgba(255,255,255,0.06) !important;
    margin: 1.5rem 0 !important;
}

.stAlert {
    border-radius: 12px;
}

footer { display: none; }
#MainMenu { display: none; }
</style>
""", unsafe_allow_html=True)


DATABRICKS_HOST  = st.secrets["DATABRICKS_HOST"]
DATABRICKS_TOKEN = st.secrets["DATABRICKS_TOKEN"]
JOB_ID           = int(st.secrets["JOB_ID"])
GITHUB_TOKEN     = st.secrets["GITHUB_TOKEN"]
HEADERS          = {"Authorization": f"Bearer {DATABRICKS_TOKEN}"}

GITHUB_REPO      = "dawidsado/file_upload_app"
GITHUB_FOLDER    = "data"
GITHUB_HEADERS   = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}


def upload_file(file_bytes, filename):
    content = base64.b64encode(file_bytes).decode("utf-8")
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FOLDER}/{filename}"

    # sprawdź czy plik już istnieje (potrzebny SHA do update)
    check = requests.get(url, headers=GITHUB_HEADERS)
    sha = check.json().get("sha") if check.status_code == 200 else None

    payload = {
        "message": f"Upload {filename} via Streamlit app",
        "content": content,
    }
    if sha:
        payload["sha"] = sha

    resp = requests.put(url, headers=GITHUB_HEADERS, json=payload)
    resp.raise_for_status()
    return f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/{GITHUB_FOLDER}/{filename}"


def trigger_job(input_path, filename):
    resp = requests.post(
        f"{DATABRICKS_HOST}/api/2.1/jobs/run-now",
        headers=HEADERS,
        json={
            "job_id": JOB_ID,
            "job_parameters": {
                "input_path": input_path,
                "source_file": filename
            }
        }
    )
    resp.raise_for_status()
    return resp.json()["run_id"]


def get_status(run_id):
    resp = requests.get(
        f"{DATABRICKS_HOST}/api/2.1/jobs/runs/get?run_id={run_id}",
        headers=HEADERS
    )
    resp.raise_for_status()
    state = resp.json()["state"]
    return state["life_cycle_state"], state.get("result_state")


# ── Header ──────────────────────────────────────────────────────────────
st.markdown('<div class="header-badge">Datasphere / Sales Pipeline</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">Sales Data Import</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Upload a monthly sales file to trigger the full ETL pipeline — '
    'Bronze ingestion, Silver cleansing, and Gold aggregation run automatically.</div>',
    unsafe_allow_html=True
)

# ── How it works card ───────────────────────────────────────────────────
st.markdown("""
<div class="card">
  <div class="card-title">How it works</div>
  <div class="step-row">
    <div class="step-num">1</div>
    <div class="step-text"><strong>Upload</strong> — select a monthly XLSX or CSV file. A preview loads instantly.</div>
  </div>
  <div class="step-row">
    <div class="step-num">2</div>
    <div class="step-text"><strong>Process</strong> — the file is sent to Databricks and the ETL job starts automatically.</div>
  </div>
  <div class="step-row">
    <div class="step-num">3</div>
    <div class="step-text"><strong>Done</strong> — you receive a confirmation once data has been updated in the warehouse.</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── File uploader ────────────────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Select a monthly file",
    type=["xlsx", "csv"],
    help="One file at a time — e.g. January, February, etc.",
    label_visibility="collapsed"
)

if uploaded_file:
    # File loaded confirmation
    try:
        if uploaded_file.name.lower().endswith(".csv"):
            df_preview = pd.read_csv(uploaded_file)
        elif uploaded_file.name.lower().endswith(".xlsx"):
            df_preview = pd.read_excel(uploaded_file, engine="openpyxl")
        else:
            df_preview = pd.read_excel(uploaded_file, engine="openpyxl")
    except Exception as e:
        st.error(f"Could not read file preview: {str(e)}")
        st.stop()
    uploaded_file.seek(0)

    st.markdown(f"""
    <div class="card">
      <div class="card-title">File loaded</div>
      <div class="step-text"><strong>{uploaded_file.name}</strong> is ready to be processed.</div>
      <div class="meta-row">
        <div class="meta-item">Rows <span>{len(df_preview):,}</span></div>
        <div class="meta-item">Columns <span>{len(df_preview.columns)}</span></div>
        <div class="meta-item">Size <span>{uploaded_file.size / 1024:.1f} KB</span></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("Preview data (first 10 rows)"):
        st.dataframe(df_preview.head(10), use_container_width=True)

    st.divider()

    if st.button("Run import to data warehouse", type="primary"):
        try:
            with st.spinner("Uploading file to Databricks..."):
                volume_path = upload_file(uploaded_file.read(), uploaded_file.name)

            st.markdown(
                f'<div class="status-info">File uploaded to GitHub: {volume_path}</div>',
                unsafe_allow_html=True
            )
            st.write("")

            with st.spinner("Starting ETL job..."):
                run_id = trigger_job(volume_path, uploaded_file.name)

            st.markdown(
                f'<div class="status-info">ETL job started &nbsp;|&nbsp; Run ID: {run_id}</div>',
                unsafe_allow_html=True
            )
            st.write("")

            progress   = st.progress(0, text="Processing data...")
            status_box = st.empty()

            for i in range(120):
                time.sleep(5)
                lifecycle, result = get_status(run_id)
                progress.progress(
                    min((i + 1) / 120, 0.95),
                    text=f"Pipeline status: {lifecycle}"
                )

                if lifecycle == "TERMINATED":
                    progress.progress(1.0)
                    if result == "SUCCESS":
                        status_box.markdown(
                            '<div class="status-success">'
                            'Pipeline complete. Data has been updated across Bronze, Silver, and Gold layers.'
                            '</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        status_box.markdown(
                            f'<div class="status-error">Pipeline failed with status: {result}. '
                            f'Check the Databricks job logs for details.</div>',
                            unsafe_allow_html=True
                        )
                    break
            else:
                status_box.markdown(
                    '<div class="status-error">Timeout reached. The job may still be running — '
                    'check the status directly in Databricks.</div>',
                    unsafe_allow_html=True
                )

        except requests.exceptions.HTTPError as e:
            st.markdown(
                f'<div class="status-error">Databricks connection error: '
                f'{e.response.status_code} — {e.response.text}</div>',
                unsafe_allow_html=True
            )
        except Exception as e:
            st.markdown(
                f'<div class="status-error">Unexpected error: {str(e)}</div>',
                unsafe_allow_html=True
            )