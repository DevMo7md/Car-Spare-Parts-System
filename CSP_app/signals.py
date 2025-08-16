# signals.py
import qrcode
import arabic_reshaper
from bidi.algorithm import get_display
from io import BytesIO
from django.core.files import File
from PIL import Image
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.conf import settings
import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SparePart

@receiver(post_save, sender=SparePart)
def create_qr_code_and_pdf(sender, instance, created, **kwargs):
    """
    هذه الدالة تستجيب لإشارة post_save لنموذج SparePart.
    تقوم بإنشاء كود QR وملف PDF عندما يتم إنشاء كائن جديد لأول مرة.
    """
    # الكود سيعمل فقط عندما يكون الكائن جديدًا (created=True)
    if created:
        # 1. توليد وحفظ كود QR
        qrcode_img = qrcode.make(str(instance.id))
        canvas_img = Image.new('RGB', (200, 200), 'white')
        qrcode_img = qrcode_img.resize((200, 200))
        canvas_img.paste(qrcode_img)

        # حفظ الصورة في الذاكرة المؤقتة
        fname = f"qr_code_{instance.name}_id_{instance.id}.png"
        buffer = BytesIO()
        canvas_img.save(buffer, 'PNG')

        # حفظ الصورة في حقل ImageField
        instance.qr_code.save(fname, File(buffer), save=False)
        buffer.close()
        
        # 2. توليد وحفظ ملف PDF
        pdf_name = f"qr_code_{instance.name}_id_{instance.id}.pdf"
        pdf_buffer = BytesIO()

        # إنشاء كائن PDF
        small_page_size = (6 * cm, 3 * cm)
        pdf_canvas = canvas.Canvas(pdf_buffer, pagesize=landscape(small_page_size))

        # مسار الخط
        path_font = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'ARIAL.TTF')
        
        # تسجيل الخط
        pdfmetrics.registerFont(TTFont('ArabicFont', path_font))
        
        def arabic_text(text):
            reshaped_text = arabic_reshaper.reshape(text)
            return get_display(reshaped_text)
            
        pdf_canvas.setFont("ArabicFont", 6)
        pdf_canvas.drawString(5, 55, f"Product: {arabic_text(instance.name)}")
        pdf_canvas.drawString(5, 42, f"Category: {arabic_text(instance.category.name)}")
        pdf_canvas.drawString(5, 29, f"ID: {instance.id}")
        pdf_canvas.drawString(5, 16, f"Price: {instance.price} EGP")

        # تحميل وإضافة صورة QR Code
        qr_code_path = instance.qr_code.path
        if os.path.exists(qr_code_path):
            pdf_canvas.drawImage(
                qr_code_path, 
                x=3*cm, y=0.2*cm, 
                width=2.5 * cm, height=2.5 * cm
            )

        # إنهاء وإنشاء PDF
        pdf_canvas.save()

        # حفظ ملف PDF في حقل FileField
        pdf_buffer.seek(0)
        instance.qr_pdf.save(pdf_name, File(pdf_buffer), save=False)
        pdf_buffer.close()

        # 3. حفظ الكائن مرة أخيرة لتأكيد مسارات الملفات
        instance.save()
