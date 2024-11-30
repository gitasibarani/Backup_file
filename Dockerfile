FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Salin semua file ke dalam container
COPY . /app

# Install pip dan virtualenv
RUN pip install --upgrade pip
RUN pip install virtualenv

# Buat virtual environment
RUN python -m venv /venv

# Aktifkan virtual environment saat container dijalankan
CMD ["/venv/bin/python", "main.py"]

