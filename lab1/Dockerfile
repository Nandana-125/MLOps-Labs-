FROM python:3.10-slim

WORKDIR /app

# Copy only requirements first (better docker caching)
COPY src/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY src/ /app/

CMD ["python", "main.py"]

