FROM python:3.10

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY src /app/src
COPY views /app/views

ENTRYPOINT ["streamlit", "run", "views/streamlit/🏠_Home.py"]