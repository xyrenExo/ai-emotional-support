FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Download models at build time
RUN python -c "from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModelForCausalLM; \
    AutoTokenizer.from_pretrained('SamLowe/roberta-base-go_emotions'); \
    AutoModelForSequenceClassification.from_pretrained('SamLowe/roberta-base-go_emotions'); \
    AutoTokenizer.from_pretrained('AliiaR/DialoGPT-medium-empathetic-dialogues'); \
    AutoModelForCausalLM.from_pretrained('AliiaR/DialoGPT-medium-empathetic-dialogues')"

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--threads", "2", "wsgi:app"]