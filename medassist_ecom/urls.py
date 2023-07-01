"""medassist_ecom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import category_controller
from . import sub_category_controller
from . import brand_controller
from . import product_controller
from . import Login_controller
from . import User_Interface

urlpatterns = [
    path('admin/', admin.site.urls),
    path('categoryinterface/',category_controller.category_interface),
    path('submitcategory',category_controller.submit_category),
    path('displaycategories/',category_controller.displayyAll_categories),
    path('editcategory/', category_controller.edit_category),
    path('deletecategory/', category_controller.delete_category),
    path('editcategoryicon', category_controller.edit_categoryicon),
    path('fetch_all_category_json', category_controller.Fetch_All_Categories_JSON),


    path('subinterface/', sub_category_controller.subcategory_interface),
    path('sub_category_interface', sub_category_controller.submit_subcategory),
    path('displaysubcategory/',sub_category_controller.displayySub_categories),
    path('edit_subcategory/',sub_category_controller.edit_subcategory),
    path('delete_subcategory/', sub_category_controller.delete_subcategory),
    path('editsubcategoryicon', sub_category_controller.edit_subcategoryicon),
    path('fetch_all_json/', sub_category_controller.fetch_all_subcategories_json),



    path('brand_interface/',brand_controller.main),
    path('brand_submit',brand_controller.submit_brand),
    path('display_brand/',brand_controller.displaybrand),
    path('editbrand/',brand_controller.update_brand),
    path('deletebrand/',brand_controller.brand_delete),
    path('editbrandicon',brand_controller.edit_brandicon),
    path('fetch_all_brand/',brand_controller.fetch_all_brand_json),

    path('product_interface/',product_controller.product_interface),
    path('product_submit', product_controller.product_submit),
    path('displayproduct/', product_controller.product_display),
    path('editproduct/', product_controller.edit_product),
    path('deleteproduct/',product_controller.delete_product),
    path('product_image',product_controller.edit_producticon),
    path('fetchallproductsjson/',product_controller.fetch_all_product_json),
    path('imagesinterface',product_controller.images_interface),
    path('submitimage',product_controller.Add_picture),


    path('login_interface/',Login_controller.Login_interface),
    path('Submit_login',Login_controller.Login_success),
    path('dashboard/',Login_controller.dashboard),
    path('admin_logout/',Login_controller.Admin_logout),


    path('User_interface/',User_Interface.Index),
    path('fetch_all_category_user/',User_Interface.Fetch_All_Categories_JSON_user),
    path('fetch_all_Product_user/',User_Interface.Fetch_All_Product_JSON),
    path('fetch_all_Subcategory_user/',User_Interface.Fetch_All_SubCategories_JSON_user),

    path('Buy_product/',User_Interface.Buy_product),
    path('add_to_cart/',User_Interface.AddToCart),
    path('Fetch_cart/',User_Interface.FetchCart),
    path('remove_from_cart/',User_Interface.Remove_Cart),
    path('Shopping_cart/',User_Interface.ShoppingCart),
    path('check_usermobileno/',User_Interface.User_check_mobileno),
    path('insertuser/',User_Interface.UserData),
    path('check_useraddress/',User_Interface.User_check_mobilenoforaddress),
    path('insertaddress/',User_Interface.UseraddressData),







]
