FROM python:3.11-slim
 
# Non-root user for security
RUN useradd -m -u 1000 appuser
 
WORKDIR /app
 
# Layer-cache deps separately from code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
 
# Copy application
COPY . .
 
# Streamlit config
RUN mkdir -p /app/.streamlit
COPY .streamlit/config.toml /app/.streamlit/config.toml
 
# Ownership
RUN chown -R appuser:appuser /app
USER appuser
 
EXPOSE 8501
 
CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]
 