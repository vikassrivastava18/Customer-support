FROM python:3.12-slim

WORKDIR /app

COPY ./backend/support/requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install gunicorn

COPY ./backend/support /app

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "support.wsgi:application"]