FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install uv && uv pip install --system .

ENV GOOGLE_APPLICATION_CREDENTIALS=/app/service-account.json
EXPOSE 8080
CMD ["streamlit", "run", "fetch_function/main.py", "--server.port=8080", "--server.address=0.0.0.0"]
