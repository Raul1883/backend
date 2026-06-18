FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV CLIENT_URL=http://localhost:5173
ENV SECRET_KEY=cbbba88a10fca62f5af6a6d04b235b632cb2fece35
ENV REG_KEY=af5bb51c27f201e5dfb6e67e2590772786bb8ea82d87

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]