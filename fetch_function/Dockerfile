FROM python:3.10-slim

WORKDIR /app

# 先に全体をコピー（uvが依存するモジュールを含めるため）
COPY . .

# uvインストール & 依存パッケージ解決（extrasも含む）
RUN pip install uv && uv pip install --all-extras .

# 環境変数やポート、起動コマンド
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/service-account.json
EXPOSE 8080
CMD ["streamlit", "run", "main.py", "--server.port", "8080", "--server.address", "0.0.0.0"]
