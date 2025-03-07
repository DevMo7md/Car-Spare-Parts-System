from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(SparePart)
admin.site.register(Bill)
admin.site.register(BillItem)
admin.site.register(VerivcationToken)
admin.site.register(IncomeBill)
admin.site.register(IncomeBillItem)
