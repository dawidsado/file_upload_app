FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY App.py .
COPY .streamlit/secrets.toml .streamlit/secrets.toml
EXPOSE 8501
CMD ["streamlit", "run", "App.py", "--server.port=8501", "--server.address=0.0.0.0"]