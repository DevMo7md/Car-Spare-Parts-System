# نظام إدارة قطع غيار السيارات

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.x-red?logo=django&logoColor=white)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![AI](https://img.shields.io/badge/AI-Enabled-purple?logo=openai&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue?logo=docker&logoColor=white)


نظام إدارة قطع غيار السيارات هو مشروع بسيط يهدف إلى تسهيل إدارة قطع الغيار في ورشة أو متجر سيارات. يتيح النظام للمستخدمين إضافة قطع غيار جديدة، تعديلها، حذفها، وعرضها بطريقة منظمة وسهلة.

## الميزات الرئيسية

- **إدارة قطع الغيار**:
  - إضافة قطع غيار جديدة مع انشاء صورة و ملف pdf خاص بالباركود الخاص بالمنتج بالحجم المناسب لطباعته على المنتج.
  - تعديل معلومات القطع الموجودة.
  - حذف قطع الغيار.
  - عرض قائمة بجميع قطع الغيار المتاحة.
  - إضافة موردين و تفاصيلهم كالعنوان و ارقامهم.
  - عمل فواتير مع ميزة انشاء الفاتورة عبر قراءة الباركود من كاميرا الحاسوب.
- **واجهة مستخدم بسيطة**:
  - واجهة تحكم سهلة الاستخدام تعتمد على الأوامر النصية (CLI).
- **التخزين المحلي**:
  - يتم حفظ بيانات قطع الغيار في ملف محلي (`db.sqlite3`) لتخزين البيانات بين الجلسات حيث يمكن اتاحة استرجاع البيانات من النسخ الإحطياتية في اي وقت.
- **التكامل مع الذكاء الاصطناعي**:
  - تم استخدام الذكاء الاصطناعي (`gemini 2.0 flash`) لقراءة الفواتير و المنتجات من الصور و ملفات ال PDF و حفظها بجانب امكانية ادخال الفواتير و المنتجات يدويا 

## المتطلبات

- Python 3.x
- نظام تشغيل يدعم Python (Windows, macOS, Linux)
- Docker

## كيفية التشغيل

1. قم بتنزيل أو استنساخ المستودع:
   ```bash
   git clone https://github.com/DevMo7md/Car-Spare-Parts-System.git
   cd Car-Spare-Parts-System
   docker-compose build
   docker-compose up
   docker-compose logs -f
   ```
   - (`docker-compose build`) in first run only

   - then you can open : http://localhost:8000 