#FROM python:3.13-slim

#WORKDIR /app

#COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt

#COPY . .

#EXPOSE 8000

#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Stage 1: build the frontend
FROM node:24-slim AS frontend-build
WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Stage 2: the actual runtime image
FROM python:3.13-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY --from=frontend-build /frontend/dist ./frontend/dist

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

