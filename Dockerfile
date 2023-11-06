FROM python:3.11.4

WORKDIR /app

COPY requirements.txt .
# Install any necessary dependencies
RUN pip install -r requirements.txt

COPY . .

EXPOSE 80
# Command to run the FastAPI server when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]