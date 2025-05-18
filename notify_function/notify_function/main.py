import os
import pandas as pd
from google.cloud import bigquery
from linebot import LineBotApi
from linebot.models import TextSendMessage
import streamlit as st

client = bigquery.Client()
TABLE_ID = os.getenv("TABLE_ID", "your_project_id.your_dataset.ohlcv_daily")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "")
TARGET_USER_ID = os.getenv("LINE_USER_ID", "")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN) if LINE_CHANNEL_ACCESS_TOKEN else None

st.set_page_config(page_title="Stock Notifier", layout="centered")


def get_top_movers():
    query = f"""
        SELECT * FROM `{TABLE_ID}`
        WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 32 DAY)
    """
    df = client.query(query).to_dataframe()
    result = []
    for symbol, group in df.groupby("symbol"):
        group = group.sort_values("date")
        try:
            week = (group.iloc[-1]["Close"] - group.iloc[-6]["Close"]) / group.iloc[-6]["Close"] * 100
            month = (group.iloc[-1]["Close"] - group.iloc[0]["Close"]) / group.iloc[0]["Close"] * 100
            result.append({"symbol": symbol, "week": week, "month": month})
        except Exception:
            continue
    movers = pd.DataFrame(result)
    return movers.sort_values("week", ascending=False).head(3), movers.sort_values("month", ascending=False).head(3)


def send_message(message: str):
    if not line_bot_api or not TARGET_USER_ID:
        st.error("LINE Messaging API credentials not set; skipping")
        return
    line_bot_api.push_message(TARGET_USER_ID, TextSendMessage(text=message))
    st.write("Message sent via LINE Messaging API")


def run_notify():
    top_week, top_month = get_top_movers()
    msg = "【おすすめ株式通知】\n■週間伸び率TOP3:\n" + top_week.to_string(index=False)
    msg += "\n\n■月間伸び率TOP3:\n" + top_month.to_string(index=False)
    send_message(msg)
    st.success("Notification Process Completed")

st.title("Stock Notifier (Streaming API)")
if st.button("Send Notification Now"):
    run_notify()
else:
    st.info("Auto-run executed on container start or click button.")
    run_notify()
