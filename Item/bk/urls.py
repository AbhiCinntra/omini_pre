from django.urls import path,include
from .views import *
from .viewPriceList import *

urlpatterns = [
    # Item
    path('create', create),
    path('update', update),
    path('all', all),
	path('one', one),
    path('delete', delete),
    path('all_filter_pagination', all_filter_pagination),
    
    # Tex
    path('tax_all', tax_all),
    path('tax_create', tax_create),
    path('tax_update', tax_update),
	path('tax_one', tax_one),
    
    # Category
    path('category_create', category_create),
    path('category_all', category_all),
    path('category_update', category_update),
	path('category_one', category_one),
	path('itemcategoryupdate', itemcategoryupdate),
    
    # PriceList
	path('price_list_all', price_list_all),
    
    # UoMList
	path('all_uom', all_uom),
	path('all_filter_uom', all_filter_uom),

    # sync items api
	path('searchinitems', searchInItems),
	path('sync_inventroy', syncInventroy),

    # filter apis
	path('filter_item_dashboard', filter_item_dashboard),
	path('sub_category_items_dashboard', sub_category_items_dashboard),
	path('sold_items_dashboard', sold_items_dashboard),
	path('item_overview', item_overview),
	path('item_invoices', item_invoices),
	path('bp_item_invoices', bp_item_invoices),
]
