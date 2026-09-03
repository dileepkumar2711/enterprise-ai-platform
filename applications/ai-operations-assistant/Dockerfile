FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

#RUN python -m pip install --no-cache-dir -r requirements.txt
RUN python -m pip install --no-cache-dir \
    torch==2.14.0 \
    --index-url https://download.pytorch.org/whl/cpu

RUN python -m pip install --no-cache-dir -r requirements.txt

COPY src ./src

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]