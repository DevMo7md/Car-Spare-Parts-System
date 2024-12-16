from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('spare-part-details/<int:pk>', views.spare_part_detail, name='spare_part_detail'),
    path('make-bill/', views.mkbill, name='mkbill'),
    path('archived-bills/', views.archived_bills, name='archived_bills'),
    path('non-archived-bills/', views.non_archived_bills, name='non_archived_bills'),
    path('suppliers/', views.suppliers, name='suppliers'),
    path('add-product/', views.add_product, name='add_product'),
    path('add-supplier/', views.add_supplier, name='add_supplier'),
    path('delete-supplier/<int:pk>/', views.delete_supplier, name='delete_supplier'),
    path('edit-supplier/<int:pk>/', views.edit_supplier, name='edit_supplier'),
    path('edit-invoice-page/<int:invoice_id>', views.edit_invoice_page, name='edit_invoice_page'),
    path('archive-invoice/<int:invoice_id>', views.archive_invoice, name='archive_invoice'),
    path('archived-bills-items/<int:pk>', views.archived_bills_items, name='archived_bills_items'),
    path('supplier-details/<int:pk>', views.supplier_details, name='supplier_details'),
    path('edit-product/<int:pk>', views.edit_product, name='edit_product'),
    path('delete-product/<int:pk>', views.delete_product, name='delete_product'),
    path('backup/', views.backup, name='backup'),
    path('restore-backup/', views.restore_backup_view, name='restore_backup'),
    path('add-category/', views.add_category, name='add_category'),
    path('add-supplier/', views.add_supplier, name='add_supplier'),
    path('create-category/', views.create_category, name='create_category'),
    path('categories/', views.categories, name='categories'),
    path('category-details/<int:pk>/', views.category_details, name='category_details'),
    path('edit-category/<int:pk>/', views.edit_category, name='edit_category'),
    path('delete-categoty/<int:pk>', views.delete_category, name='delete_category'),

]
