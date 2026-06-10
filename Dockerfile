FROM python:3.11.9-slim

WORKDIR /app

COPY Chatbot/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY Chatbot/ .

EXPOSE 10000

CMD ["gunicorn", "Chatbot.wsgi", "--bind", "0.0.0.0:10000"]