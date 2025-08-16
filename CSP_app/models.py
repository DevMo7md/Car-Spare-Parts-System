from django.db import models
from django.contrib.auth.models import User
import qrcode
from reportlab.lib.pagesizes import landscape
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from reportlab.lib.units import inch, cm
from django.db.models.signals import post_save
from django.dispatch import receiver
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont 
import arabic_reshaper
from bidi.algorithm import get_display
from django.conf import settings
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
    
    def unavailable_parts_count(self):
        return self.spare_parts.filter(is_available=False).count()



class IncomeBill(models.Model):
    title = models.CharField(max_length=100)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='income_bills')
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class SparePart(models.Model):
    name = models.CharField(max_length=100)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)
    qr_pdf = models.FileField(upload_to='qr_pdfs', blank=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    income_bill = models.ForeignKey(IncomeBill, on_delete=models.SET_NULL , related_name='spare_parts', null=True, blank=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='spare_parts')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='spare_parts')
    is_available = models.BooleanField(default=True)
    date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

# تعديل مطلوب --> [supplier, category, price, description, name] *add
class IncomeBillItem(models.Model):
    income_bill = models.ForeignKey(IncomeBill, on_delete=models.CASCADE, related_name='items')
    spare_part = models.ForeignKey(SparePart, on_delete=models.CASCADE, related_name='income_bill_items')
    name = models.CharField(max_length=100 , blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2 , default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='income_bill_items', null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2 , default=0)

    def __str__(self):
        return f"{self.spare_part.name} (x{self.quantity}) - {self.income_bill.title}"


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