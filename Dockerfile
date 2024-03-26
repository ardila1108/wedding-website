FROM python:3.10

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN apt-get update && apt-get install -y \
    software-properties-common \
    npm

COPY . /app

ENTRYPOINT ["streamlit", "run", "🏠_Home.py", "--theme.secondaryBackgroundColor=#FFDFDF"]