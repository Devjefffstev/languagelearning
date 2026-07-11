# to build locally | docker build -t my-fastapi-app .
# to run locally | docker run -it -p 8000:8000 my-fastapi-app
# / 
# /greet/{yourname} | returns a greeting message

FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
