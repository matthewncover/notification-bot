FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 \
    TZ=America/Los_Angeles \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"
WORKDIR /app
RUN python -m venv "$VIRTUAL_ENV"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY bot.py .
CMD ["python", "bot.py"]
