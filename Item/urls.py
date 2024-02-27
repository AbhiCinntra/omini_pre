from django.urls import path,include
from .views import *
from .viewPriceList import *
from .viewPurchase import *

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

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    #                   Sales Item 
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # filter apis
	path('filter_item_dashboard', filter_item_dashboard),
    path('filter_bpgroup_item', filter_bpgroup_item),    
	path('filter_bpsubgroup_item', filter_bpsubgroup_item),
    path('filter_bpitem', filter_bpitem),    
	path('sub_category_items_dashboard', sub_category_items_dashboard),
	path('sold_items_dashboard', sold_items_dashboard),
	path('item_overview', item_overview),
	path('bp_item_invoices', bp_item_invoices),
	path('item_invoices', item_invoices),

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    #                   Sales Item 
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # filter apis
	path('ap_filter_item_dashboard', ap_filter_item_dashboard),
	path('ap_filter_bpgroup_item', ap_filter_bpgroup_item),
	path('ap_filter_bpsubgroup_item', ap_filter_bpsubgroup_item),
    path('ap_filter_bpitem', ap_filter_bpitem),
	path('ap_sub_category_items_dashboard', ap_sub_category_items_dashboard),
    path('ap_sold_items_dashboard', ap_sold_items_dashboard),
	# path('ap_item_overview', ap_item_overview),
	path('ap_bp_item_invoices', ap_bp_item_invoices),
	path('ap_item_invoices', ap_item_invoices),
	# path('item_overview', ap_item_overview),
]


# http://103.107.67.160:8003/item/filter_item_dashboard
# http://103.107.67.160:8003/item/filter_bpgroup_item
# http://103.107.67.160:8003/item/filter_bpsubgroup_item
# http://103.107.67.160:8003/item/filter_bpitem
# http://103.107.67.160:8003/item/sub_category_items_dashboard
# http://103.107.67.160:8003/item/sold_items_dashboard
# http://103.107.67.160:8003/item/item_overview
# http://103.107.67.160:8003/item/bp_item_invoices
# http://103.107.67.160:8003/item/item_invoices

# http://103.107.67.160:8003/item/ap_filter_item_dashboard
# http://103.107.67.160:8003/item/ap_filter_bpgroup_item
# http://103.107.67.160:8003/item/ap_filter_bpsubgroup_item
# http://103.107.67.160:8003/item/ap_filter_bpitem
# http://103.107.67.160:8003/item/ap_sub_category_items_dashboard
# http://103.107.67.160:8003/item/ap_sold_items_dashboard
# http://103.107.67.160:8003/item/ap_bp_item_invoices
# http://103.107.67.160:8003/item/ap_item_invoices
