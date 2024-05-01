"""
URL configuration for project_DDA project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
#1. Vendor Profile Management:
from app.views import  VendorListCreateAPIView, VendorRetrieveUpdateDestroyAPIView

#2. Purchase Order Tracking:/URL Routing (purchase_orders/urls.py):
from app.views import PurchaseOrderListCreateAPIView, PurchaseOrderRetrieveUpdateDestroyAPIView
from app.views import VendorPerformanceAPIView

# Update Acknowledgment Endpoint
from app.views import AcknowledgePurchaseOrderAPIView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/vendors/', VendorListCreateAPIView.as_view(), name='vendor-list-create'),
    path('api/vendors/<int:pk>/', VendorRetrieveUpdateDestroyAPIView.as_view(), name='vendor-retrieve-update-destroy'),
    
    #2. Purchase Order Tracking:/URL Routing (purchase_orders/urls.py):

    path('api/purchase_orders/', PurchaseOrderListCreateAPIView.as_view(), name='purchase-order-list-create'),
    path('api/purchase_orders/<int:pk>/', PurchaseOrderRetrieveUpdateDestroyAPIView.as_view(), name='purchase-order-retrieve-update-destroy'),

    #URL Routing (vendors/urls.py):Vendor Model Enhancement (vendors/models.py):/ Vendor Performance Evaluation:/ #API Endpoint Implementation
    path('api/vendors/<int:pk>/performance/', VendorPerformanceAPIView.as_view(), name='vendor-performance'),
   
    # Update Acknowledgment Endpoint
    path('api/purchase_orders/<int:pk>/acknowledge/', AcknowledgePurchaseOrderAPIView.as_view(), name='acknowledge-purchase-order'),

]





    
