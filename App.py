import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="Sales Data Import",
    page_icon="",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #D6D2D2;
}

.main .block-container {
    padding-top: 4rem;
    padding-bottom: 3rem;
    max-width: 640px;
}

.main-title {
    font-size: 1.6rem;
    font-weight: 700;
    color: #000000;
    margin-bottom: 0.3rem;
    letter-spacing: -0.01em;
}

.subtitle {
    color: #000000;
    opacity: 0.55;
    font-size: 0.9rem;
    font-weight: 400;
    margin-bottom: 2rem;
}

.card {
    background: #FFFFFF;
    border: 1px solid #00000022;
    border-radius: 4px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
}

.card-label {
    color: #000000;
    opacity: 0.5;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}

.card-value {
    color: #000000;
    font-size: 0.95rem;
    font-weight: 600;
}

.meta-row {
    display: flex;
    gap: 1.6rem;
    margin-top: 0.6rem;
}

.meta-item {
    font-size: 0.8rem;
    color: #000000;
    opacity: 0.6;
}

.meta-item b {
    opacity: 1;
    font-weight: 600;
}

.status-bar {
    border-left: 3px solid #00A972;
    background: #FFFFFF;
    padding: 0.7rem 1rem;
    border-radius: 0 4px 4px 0;
    color: #000000;
    font-size: 0.85rem;
    margin-bottom: 0.6rem;
}

.status-bar.error {
    border-left-color: #C0392B;
}

div[data-testid="stFileUploader"] {
    background: #FFFFFF;
    border: 1.5px dashed #00000033;
    border-radius: 4px;
}

div[data-testid="stFileUploader"] label,
div[data-testid="stFileUploaderDropzoneInstructions"] span,
div[data-testid="stFileUploaderDropzoneInstructions"] small {
    color: #000000 !important;
}

div[data-testid="stFileUploader"] section {
    background: #FFFFFF;
}

.stButton > button {
    background: #00A972;
    color: #FFFFFF;
    border: none;
    border-radius: 4px;
    padding: 0.6rem 1.5rem;
    font-weight: 600;
    font-size: 0.88rem;
    width: 100%;
    transition: opacity 0.15s;
}

.stButton > button:hover {
    opacity: 0.88;
    color: #FFFFFF !important;
}

.stButton > button:hover p,
.stButton > button:hover span,
.stButton > button:hover div {
    color: #FFFFFF !important;
}

div[data-testid="stExpander"] {
    background: #FFFFFF;
    border: 1px solid #00000022;
    border-radius: 4px;
}

div[data-testid="stExpander"] summary,
div[data-testid="stExpander"] summary:hover,
div[data-testid="stExpander"] summary:active,
div[data-testid="stExpander"] summary span,
div[data-testid="stExpander"] summary p {
    color: #000000 !important;
    font-size: 0.85rem;
    font-weight: 500;
    background: #FFFFFF !important;
}

div[data-testid="stExpander"] summary:hover {
    background: #F5F5F5 !important;
}

div[data-testid="stExpander"] svg {
    fill: #000000 !important;
}

/* Dataframe overlay editor (cell click popup) - keep light theme */
.gdg-search-bar {
    background: #FFFFFF !important;
    color: #000000 !important;
}

div[data-testid="stDataFrame"] {
    background: #FFFFFF;
}

.stProgress > div > div {
    background: #00A972;
}

hr {
    border-color: #00000022 !important;
    margin: 1.2rem 0 !important;
}

footer { display: none; }
#MainMenu { display: none; }
header { background: transparent !important; }
.stAppDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)


from azure.storage.blob import BlobServiceClient

AZURE_STORAGE_ACCOUNT = st.secrets["AZURE_STORAGE_ACCOUNT"]
AZURE_STORAGE_KEY     = st.secrets["AZURE_STORAGE_KEY"]
AZURE_CONTAINER       = st.secrets["AZURE_CONTAINER"]


def upload_file(file_bytes, filename):
    connection_string = (
        f"DefaultEndpointsProtocol=https;"
        f"AccountName={AZURE_STORAGE_ACCOUNT};"
        f"AccountKey={AZURE_STORAGE_KEY};"
        f"EndpointSuffix=core.windows.net"
    )
    blob_service = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service.get_blob_client(container=AZURE_CONTAINER, blob=filename)
    blob_client.upload_blob(file_bytes, overwrite=True)
    return f"https://{AZURE_STORAGE_ACCOUNT}.blob.core.windows.net/{AZURE_CONTAINER}/{filename}"


# ── Header ──────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">Sales Data Import</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Upload a monthly file to add it to the sales pipeline.</div>',
    unsafe_allow_html=True
)

# ── File uploader ────────────────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Select a monthly file",
    type=["csv"],
    label_visibility="collapsed"
)

if uploaded_file:
    try:
        df_preview = pd.read_csv(uploaded_file, sep=";")
    except Exception as e:
        st.error(f"Could not read file: {str(e)}")
        st.stop()
    uploaded_file.seek(0)

    st.markdown(f"""
    <div class="card">
      <div class="card-label">File ready</div>
      <div class="card-value">{uploaded_file.name}</div>
      <div class="meta-row">
        <div class="meta-item">Rows <b>{len(df_preview):,}</b></div>
        <div class="meta-item">Columns <b>{len(df_preview.columns)}</b></div>
        <div class="meta-item">Size <b>{uploaded_file.size / 1024:.1f} KB</b></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("Preview data"):
        st.dataframe(df_preview.head(10), use_container_width=True)

    if st.button("Upload file", type="primary"):
        try:
            with st.spinner("Uploading..."):
                volume_path = upload_file(uploaded_file.read(), uploaded_file.name)

            st.markdown(
                f'<div class="status-bar">File uploaded to Azure Blob Storage. Run the ETL job in Databricks to process it.</div>',
                unsafe_allow_html=True
            )

        except requests.exceptions.HTTPError as e:
            st.markdown(
                f'<div class="status-bar error">Upload failed: {e.response.status_code}</div>',
                unsafe_allow_html=True
            )
        except Exception as e:
            st.markdown(
                f'<div class="status-bar error">Unexpected error: {str(e)}</div>',
                unsafe_allow_html=True
            )

# w celu uruchomienia aplikacji - z poziomu consoli  .venv\Scripts\streamlit.exe run App