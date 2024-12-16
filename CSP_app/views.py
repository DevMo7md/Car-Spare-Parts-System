from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib import messages
import os
from django.db.models import Q
import shutil
from django.conf import settings
from django.urls import reverse
import datetime


# Create your views here.
def home(request):
    return render(request, 'home.html')


def products(request):

    category_id = request.GET.get('category')
    if category_id:
        parts = SparePart.objects.filter(category_id=category_id)
    else:
        parts = SparePart.objects.all()
    if 'search-bar' in request.GET:
        search = request.GET['search-bar']
        parts = SparePart.objects.filter(Q(name__icontains=search)|Q(category__name__icontains=search)|Q(supplier__name__icontains=search))

    categories = Category.objects.all()
    context = {
        'parts': parts,
        'categories': categories,
        'selected_category': category_id,
    }
    return render(request, 'products.html', context)


# عرض تفاصيل قطعة معينة
def spare_part_detail(request, pk):
    part = get_object_or_404(SparePart, id=pk)
    return render(request, 'spare_part_detail.html', {'part': part})


# إضافة قطعة جديدة
def add_spare_part(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock_quantity = request.POST.get('stock_quantity')
        category_id = request.POST.get('category')
        supplier_id = request.POST.get('supplier')

        category = get_object_or_404(Category, id=category_id)
        supplier = get_object_or_404(Supplier, id=supplier_id)

        spare_part = SparePart.objects.create(
            name=name,
            description=description,
            price=price,
            stock_quantity=stock_quantity,
            category=category,
            supplier=supplier
        )

        # توجيه المستخدم بعد الإضافة
        messages.success(request, f"تم إضافة القطعة {spare_part.name} بنجاح!")
        return redirect(reverse('spare_parts_list'))
    
    categories = Category.objects.all()
    suppliers = Supplier.objects.all()

    return render(request, 'add_spare_part.html', {
        'categories': categories,
        'suppliers': suppliers,
    })


# البحث عن قطعة بناءً على الباركود
@csrf_exempt
def get_spare_part_by_barcode(request):
    if request.method == "POST":
        barcode_id = request.POST.get('barcode_id')
        try:
            spare_part = SparePart.objects.get(id=barcode_id)
            response_data = {
                'name': spare_part.name,
                'description': spare_part.description,
                'price': float(spare_part.price),
                'stock_quantity': spare_part.stock_quantity,
                'category': spare_part.category.name,
                'supplier': spare_part.supplier.name,
            }
            return JsonResponse({'status': 'success', 'data': response_data})
        except SparePart.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'القطعة غير موجودة.'})

    return JsonResponse({'status': 'error', 'message': 'طريقة الطلب غير مدعومة.'})


def mkbill(request):

    invoice, created = Bill.objects.get_or_create(archived=False)
    if request.method == 'POST':
        barcode = request.POST.get('barcode_id')
        try:
            spare_part = SparePart.objects.get(id=barcode)
        except SparePart.DoesNotExist:
            messages.error(request, "Product not found!")
            return redirect('mkbill')

        # إضافة المنتج إلى الفاتورة
        if not spare_part.stock_quantity <= 0:
            invoice_item, item_created = BillItem.objects.get_or_create(
                invoice=invoice,
                spare_part=spare_part,
                defaults={'price': spare_part.price}
            )
            if not item_created:
                invoice_item.quantity += 1
                invoice_item.save()
            # تحديث الإجمالي
            invoice.total_price += spare_part.price
            invoice.save()
        else:
            messages.error(request, "المنتج لم يعد موجود")       

        print(invoice.total_price)
    return render(request, 'mkbill.html', {'invoice': invoice})


def edit_invoice_page(request, invoice_id):
    invoice = get_object_or_404(Bill, id=invoice_id, archived=False)
    if request.method == 'POST':
        for item in invoice.items.all():
            quantity = request.POST.get(f'quantity_{item.id}')
            if quantity:
                quantity = int(quantity)
                if quantity == 0:
                    item.delete()
                else:
                    if not quantity > item.spare_part.stock_quantity : 
                        invoice.total_price -= item.quantity * item.price
                        item.quantity = quantity
                        invoice.total_price += item.quantity * item.price
                        item.save()
                    else:
                        messages.error(request,f"المنتج لا يوجد منه عدد كافي لا يوجد سوى {item.spare_part.stock_quantity} قطع")
                        redirect('edit_invoice_page', item.id)    

        invoice.save()
        messages.success(request, "Invoice updated successfully!")
        return redirect('edit_invoice_page', invoice_id=invoice.id)

    return render(request, 'edit_invoice_page.html', {'invoice': invoice})


def archive_invoice(request, invoice_id):

    invoice = get_object_or_404(Bill, id=invoice_id, archived=False)
    for item in invoice.items.all():
        # تحديث مخزون المنتجات
        item.spare_part.stock_quantity -= item.quantity
        item.spare_part.save()

    invoice.archived = True
    invoice.save()
    messages.success(request, "تم الأرشفة بنجاح")
    return redirect('mkbill')

def archived_bills(request):

    bills = Bill.objects.filter(archived=True).order_by('-created_at')
    
    return render(request, 'archived_bills.html', {'bills':bills})


def non_archived_bills(request):

    bills = Bill.objects.filter(archived=False).order_by('-created_at')
    
    return render(request, 'non_archived_bills.html', {'bills':bills})


def suppliers(request):

    suppliers = Supplier.objects.all()
    if 'search-bar' in request.GET:
        search = request.GET['search-bar']
        suppliers = suppliers.filter(name__icontains=search)
    
    return render(request, 'suppliers.html', {'suppliers':suppliers})


def add_supplier(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
    
        supplier = Supplier(name=name, phone=phone, address=address)
        supplier.save()
        messages.success(request, "تم اضافة المورد بنجاح")
        return redirect('add_supplier')
    
    return render(request, 'add_supplier.html')


def edit_supplier(request, pk):

    supplier = get_object_or_404(Supplier, id=pk)

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
    
        supplier.name = name
        supplier.phone = phone
        supplier.address = address
        supplier.save()

        messages.success(request, "تم تحديث المورد بنجاح")
        return redirect('supplier_details', supplier.id)
    
    return render(request, 'edit_supplier.html', {'supplier': supplier})


def supplier_details(request, pk):

    supplier = Supplier.objects.get(id=pk)
    
    return render(request, 'supplier_details.html', {'supplier':supplier})


def delete_supplier(request, pk):

    supplier = get_object_or_404(Supplier, id=pk)
    supplier.delete()
    messages.success(request, "تم حذف المورد بنجاح")
    return redirect('suppliers')


def archived_bills_items(request, pk):

    bill = get_object_or_404(Bill, id=pk)
    
    return render(request, 'archived_bills_items.html', {'bill':bill})


def add_product(request):
    suppliers = Supplier.objects.all()
    categories = Category.objects.all()

    if request.method == 'POST':
        product_name = request.POST.get('name')
        product_price = request.POST.get('price')
        product_description = request.POST.get('description')
        product_quantity = request.POST.get('quantity')
        product_category_id = request.POST.get('category')
        product_supplier_id = request.POST.get('supplier')
        try :
            product_category = get_object_or_404(Category, id=product_category_id)
            product_supplier = get_object_or_404(Supplier, id=product_supplier_id)
        except:
            messages.error(request, "عفوا الفئة او المورد غير موجود")
            return redirect('add_product')
        product = SparePart(name=product_name, price=product_price, description=product_description, stock_quantity=product_quantity, category=product_category, supplier=product_supplier)
        product.save()

    context = {
        'categories': categories,
        'suppliers': suppliers,
            }

    return render(request, 'add_product.html', context)

def delete_product(request,pk):
    product = get_object_or_404(SparePart, id=pk)
    product.delete()

    return redirect('products')


def edit_product(request,pk):

    product = get_object_or_404(SparePart, id=pk)
    categories = Category.objects.all()
    suppliers = Supplier.objects.all()
    if request.method == 'POST':
        product_name = request.POST.get('name')
        product_price = request.POST.get('price')
        product_description = request.POST.get('description')
        product_quantity = request.POST.get('quantity')
        product_category_id = request.POST.get('category')
        product_supplier_id = request.POST.get('supplier')
        try :
            product_category = get_object_or_404(Category, id=product_category_id)
            product_supplier = get_object_or_404(Supplier, id=product_supplier_id)
        except:
            messages.error(request, "عفوا الفئة او المورد غير موجود")
            return redirect('add_product')
        product.name = product_name
        product.price = product_price
        product.description = product_description
        product.stock_quantity = product_quantity
        product.supplier = product_supplier
        product.category = product_category
        product.save()
        return redirect('spare_part_detail', product.id)
    context = {
        'product': product,
        'categories': categories,
        'suppliers': suppliers,
    }
    return render(request, 'edit_product.html', context)


def backup (request):
    date = datetime.datetime.now()
    str_date = date.strftime('%Y%m%d_%H%M')
    if request.method == 'POST':
        db_path = settings.DATABASES['default']['NAME']
        backups_dir = os.path.join(settings.BASE_DIR, 'db_backups')
        os.makedirs(backups_dir, exist_ok=True)
        
        backup_file = os.path.join(backups_dir, f'backup_{str_date}.sqlite3')
        shutil.copy(db_path, backup_file)
        messages.success(request, f"تم نسخ قاعدة البيانات: {os.path.basename(backup_file)}")
        return redirect('backup')
    return render(request, 'backup.html')
    

def restore_backup_view(request):
    if request.method == 'POST' and request.FILES['backup_file']:
        backup_file = request.FILES['backup_file']
        db_path = settings.DATABASES['default']['NAME']
        
        # كتابة النسخة الاحتياطية في قاعدة البيانات الأصلية
        with open(db_path, 'wb') as db:
            for chunk in backup_file.chunks():
                db.write(chunk)

        messages.success(request, "تم استعادة قاعدة البيانات بنجاح.")
        return redirect('restore_backup')  # إعادة التوجيه إلى نفس الصفحة
    
    return redirect('home')


def add_category(request):
    if request.method == 'POST':
        category_name = request.POST['category_name']
        category = Category(name=category_name)
        category.save()
        messages.success(request, 'تم اضافة الفئة بنجاح')
        return JsonResponse({'message': 'تم اضافة الفئة بنجاح' , 'id': category.id}, status=200)


def add_supplier(request):
    if request.method == 'POST':
        name = request.POST['name']
        address = request.POST['address']
        phone = request.POST['phone']
        supplier = Supplier(name=name, address=address, phone=phone)
        supplier.save()
        messages.success(request, 'تم اضافة المورد بنجاح')
        return JsonResponse({'message': 'تم اضافة المورد بنجاح', 'id': supplier.id}, status=200)


def categories(request):
    categories = Category.objects.all()
    if 'search-bar' in request.GET:
        search = request.GET['search-bar']
        categories = categories.filter(name__icontains=search) 
    return render(request, 'categories.html', {'categories': categories})

def create_category(request):
    if request.method == 'POST':
        category_name = request.POST['name']
        category = Category(name=category_name)
        category.save()
        messages.success(request, 'تم اضافة الفئة بنجاح')
        return redirect('categories')
    return render(request, 'create_category.html')



def category_details(request, pk):
    category = Category.objects.get(id=pk)
    return render(request, 'category_details.html', {'category': category})


def edit_category(request, pk):
    category = Category.objects.get(id=pk)
    if request.method == 'POST':
        category.name = request.POST['name']
        category.save()
        messages.success(request, 'تم تعديل الفئة بنجاح')
        return redirect('categories')
    return render(request, 'edit_category.html', {'category': category})
    


def delete_category(request, pk):
    category = Category.objects.get(id=pk)
    category.delete()
    messages.success(request, 'تم حذف الفئة بنجاح')
    return redirect('categories')