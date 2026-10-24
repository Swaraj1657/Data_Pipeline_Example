FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV OUTPUT_DIR=/opt/spark-data/output

EXPOSE 5200

CMD ["python", "app.py"]
