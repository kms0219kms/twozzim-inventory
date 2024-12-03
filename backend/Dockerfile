FROM python:3.13-slim
LABEL org.opencontainers.image.source https://github.com/kms0219kms/twozzim-inventory

# Initial Setup
WORKDIR /usr/app
RUN apt update && apt install curl tar xz-utils git -y
RUN ln -snf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

# Install required dependencies
COPY requirements.txt .
RUN python3 -m pip install -r /usr/app/requirements.txt

COPY . .

CMD ["python3", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "6"]
