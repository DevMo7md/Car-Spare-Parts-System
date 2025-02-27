from django.db import models
from django.contrib.auth.models import User
import qrcode
from reportlab.lib.pagesizes import landscape
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from reportlab.lib.units import inch
from django.db.models.signals import post_save
from django.dispatch import receiver
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class SparePart(models.Model):
    name = models.CharField(max_length=100)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)
    qr_pdf = models.FileField(upload_to='qr_pdfs', blank=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='spare_parts')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='supplier')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
    # احفظ الكائن أولاً للحصول على المعرف (id) المطلوب لتوليد كود QR
        if not self.id:  # لا تقم بتوليد QR للأشياء التي ليس لها معرف
            super().save(*args, **kwargs)
        
        if not self.qr_code:
            # توليد كود QR
            qrcode_img = qrcode.make(self.id)  # استبدل self.id بمحتوى فريد إذا لزم الأمر
            canvas = Image.new('RGB', (290, 290), 'white')
            qrcode_img = qrcode_img.resize((290, 290))  # ضبط الحجم ليتطابق مع الـ canvas
            
            # لصق كود QR على الـ canvas
            canvas.paste(qrcode_img)

            # حفظ الصورة في ذاكرة مؤقتة
            fname = f"qr_code_{self.name}_id_{self.id}.png"
            buffer = BytesIO()
            canvas.save(buffer, 'PNG')
            
            # حفظ الصورة في حقل ImageField
            self.qr_code.save(fname, File(buffer), save=False)
            buffer.close()

        if self.qr_code and not self.qr_pdf:
            self.create_pdf()

        super().save(*args, **kwargs)
    def create_pdf(self):
        # مسار الملف المؤقت
        pdf_name = f"qr_code_{self.name}_id_{self.id}.pdf"
        buffer = BytesIO()

        # إنشاء كائن PDF
        small_page_size = (4 * inch, 2 * inch)  # أبعاد الورقة الصغيرة
        pdf_canvas = canvas.Canvas(buffer, pagesize=landscape(small_page_size))

        # إضافة النصوص مع تنسيق مناسب
        pdf_canvas.setFont("Helvetica", 10)
        pdf_canvas.drawString(10, 50, f"Product: {self.name}")
        pdf_canvas.drawString(10, 35, f"ID: {self.id}")
        pdf_canvas.drawString(10, 20, f"Price: {self.price} EGP")

        # تحميل وإضافة صورة QR Code مع ضبط حجمها
        qr_code_path = self.qr_code.path
        if os.path.exists(qr_code_path):
            pdf_canvas.drawImage(
                qr_code_path, 
                x=150, y=10,  # الموقع (معدّل)
                width=1.5 * inch, height=1.5 * inch  # حجم الصورة
            )

        # إنهاء وإنشاء PDF
        pdf_canvas.save()

        # حفظ الملف في الحقل
        buffer.seek(0)
        self.qr_pdf.save(pdf_name, File(buffer), save=False)
        buffer.close()

class Bill(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return f"Invoice #{self.id} - {self.created_at.strftime('%Y-%m-%d')}"

class BillItem(models.Model):
    invoice = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='items')
    spare_part = models.ForeignKey(SparePart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.spare_part.name} (x{self.quantity})"        
    

class VerivcationToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_password_token = models.CharField(max_length=40, unique=True, null=True, blank=True)
    reset_password_expires = models.DateTimeField(null=True, blank=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"Token for {self.user.username} - {self.reset_password_token}"