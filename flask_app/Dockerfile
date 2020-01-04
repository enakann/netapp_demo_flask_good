FROM python:3-alpine
WORKDIR /usr/src/
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
COPY . .
CMD ["python","./app/app.py"]
