FROM python:3.12

WORKDIR /IoT

COPY Pipfile Pipfile.lock /IoT/

RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

COPY . /IoT/

EXPOSE 5000

CMD ["pipenv", "run", "python", "app.py"]
