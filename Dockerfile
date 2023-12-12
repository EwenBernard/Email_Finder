FROM python:latest

COPY requirements.txt .

COPY views/templates/index.html .

COPY db/pythonsqlite.db .

COPY models/backend_file.py .

COPY models/retrieve_domain.py .

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED 1

COPY . .

EXPOSE 8001

# Commande pour exécuter l'application Flask
CMD ["gunicorn", "-w", "4", "-b", ":8001", "backend_file:app"]
