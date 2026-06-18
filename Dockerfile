FROM python:3.14

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN playwright install --with-deps chromium

COPY . .

EXPOSE 8000

ENV PYTHONPATH=/app

CMD ["pytest","tests/test_l3.py", "-v"]