FROM python:3.12

WORKDIR /var/www

COPY /FinalProjec/sql_app/requirements.txt .

RUN pip install -r requirements.txt

COPY sql_app .

CMD ["fastapi", "run", "main.py"]