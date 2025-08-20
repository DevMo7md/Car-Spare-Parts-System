# نبدأ من صورة Python الرسمية
FROM python:3.11-slim

# نحدد مكان المشروع داخل الكونتينر
WORKDIR /app

# ننسخ ملف المتطلبات
COPY requirements.txt /app/

# نثبت المكتبات
RUN pip install --no-cache-dir -r requirements.txt

# ننسخ باقي المشروع
COPY . /app/

# نفتح البورت الافتراضي بتاع Django
EXPOSE 8000

# نشغل السيرفر
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
