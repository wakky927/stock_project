FROM python:3.10-slim

WORKDIR /app

# pyproject.toml + 全体構造を一緒にコピー
COPY . .

# カレントディレクトリをモジュールパスとしてインストール対象にする
WORKDIR /app/notify_function

# uv で依存を解決（extras も）
RUN pip install uv && uv pip install --all-extras .

ENV GOOGLE_APPLICATION_CREDENTIALS=/app/service-account.json
EXPOSE 8080

CMD ["streamlit", "run", "main.py", "--server.port", "8080", "--server.address", "0.0.0.0"]
