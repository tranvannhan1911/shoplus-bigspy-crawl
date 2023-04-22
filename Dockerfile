# Sử dụng Python 3.8
FROM python:3.8

RUN apt update -y

# RUN apt install -y libglib2.0-0=2.50.3-2 libnss3=2:3.26.2-1.1+deb9u1 libgconf-2-4=3.2.6-4+b1 libfontconfig1=2.11.0-6.7+b1
RUN apt install chromium -y

# Thêm các biến môi trường
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Thiết lập thư mục làm việc trong Docker container
WORKDIR /app

# Sao chép file requirements.txt vào thư mục làm việc
COPY requirements.txt .

# Cài đặt các thư viện cần thiết
RUN pip install --upgrade pip && pip install -r requirements.txt

# Sao chép toàn bộ source code của ứng dụng vào thư mục làm việc
COPY . .

# migrate
RUN python manage.py makemigrations
RUN python manage.py makemigrations crawler
RUN python manage.py loaddata init_data.json --app auth.user

# Thiết lập port để truy cập ứng dụng
EXPOSE 8000

# Chạy ứng dụng
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]