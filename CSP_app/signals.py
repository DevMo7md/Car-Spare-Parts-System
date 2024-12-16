# import time
# import sys
# import os
# from io import BytesIO
# from django.core.files import File
# from PIL import Image
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from CSP_app.models import SparePart

# def save_qr_code_as_pdf(product_id, qr_image_path, save_path):
#     try:
#         pdf_path = os.path.join(save_path, f"barcode_{product_id}.pdf")
#         c = canvas.Canvas(pdf_path, pagesize=letter)
#         c.drawImage(qr_image_path, x=100, y=700, width=200, height=200)
#         c.drawString(100, 680, f"QR Code for Product ID: {product_id}")
#         c.save()
#         return pdf_path
#     except Exception as e:
#         print(f"Error generating barcode PDF: {e}", file=sys.stderr)
#         return None

# @receiver(post_save, sender=SparePart)
# def create_qr_pdf(sender, instance, created, **kwargs):
#     """
#     Signal to create a QR code PDF when a SparePart object is created.
#     """
#     if created:
#         save_path = os.path.join(os.path.dirname(instance.qr_code.path), 'pdfs/')
        
#         if not os.path.exists(save_path):
#             os.makedirs(save_path)
        
#         pdf_path = save_qr_code_as_pdf(instance.id, instance.qr_code.path, save_path)
#         if pdf_path:
#             print(f"QR Code PDF created at: {pdf_path}")
#         else:
#             print("Failed to create QR Code PDF.")
