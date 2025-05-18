FROM python:3.10-slim

WORKDIR /app

COPY . .

WORKDIR /app/fetch_function

RUN pip install uv && uv pip install --all-extras .

ENV GOOGLE_APPLICATION_CREDENTIALS=/app/service-account.json
EXPOSE 8080

CMD ["streamlit", "run", "main.py", "--server.port", "8080", "--server.address", "0.0.0.0"]
