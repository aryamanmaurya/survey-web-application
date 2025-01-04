FROM python:3.12-slim

WORKDIR /usr/src/app

COPY . /usr/src/app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=run.py FLASK_RUN_HOST=0.0.0.0 FLASK_ENV=production

CMD ["flask", "run"]