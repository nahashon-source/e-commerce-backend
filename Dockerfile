FROM python:3.11-slim-bookworm

WORKDIR /app

# Install system updates and dependencies
RUN apt-get update && apt-get upgrade -y && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
