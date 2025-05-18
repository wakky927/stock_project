import os
import pandas as pd
import yfinance as yf
from google.cloud import bigquery
import streamlit as st

client = bigquery.Client()
TABLE_ID = os.getenv("TABLE_ID", "your_project_id.your_dataset.ohlcv_daily")

st.set_page_config(page_title="OHLCV Fetcher", layout="centered")

@st.cache_data(show_spinner=False)
def load_ticker_list() -> list:
    url = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
    df = pd.read_excel(url, dtype={"コード": str})
    return (df["コード"].str.zfill(4) + ".T").tolist()


def fetch_ohlcv(ticker: str):
    df = yf.download(ticker, period="2d", interval="1d")
    if df.empty:
        return None
    df = df[["Open", "High", "Low", "Close", "Volume"]]
    df["symbol"] = ticker
    df["date"] = df.index.date
    df.reset_index(drop=True, inplace=True)
    return df


def save_to_bigquery(df: pd.DataFrame):
    job = client.load_table_from_dataframe(df, TABLE_ID, job_config=bigquery.LoadJobConfig(write_disposition="WRITE_APPEND"))
    job.result()


def run_batch():
    tickers = load_ticker_list()
    progress = st.progress(0)
    for idx, tkr in enumerate(tickers, 1):
        try:
            _df = fetch_ohlcv(tkr)
            if _df is not None:
                save_to_bigquery(_df)
        except Exception as exc:
            st.warning(f"{tkr} error: {exc}")
        progress.progress(idx / len(tickers))
    st.success("Fetch Completed")

st.title("JPX OHLCV Fetcher (Streamlit)")
if st.button("Run Fetch Now"):
    run_batch()
else:
    st.info("Auto-run executed on container start or click button.")
    run_batch()

