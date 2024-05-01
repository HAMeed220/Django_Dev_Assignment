from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from app.models import Vendor, PurchaseOrder, HistoricalPerformance
from app.Serializers import VendorSerializer, PurchaseOrderSerializer
from rest_framework.response import Response
# Backend Logic for Performance Metrics   
from django.db.models import Count, Avg, Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from app.models import PurchaseOrder, Vendor
from app.models import *


# 1. Vendor Profile Management:
class VendorListCreateAPIView(generics.ListCreateAPIView):# Define a class-based view that allows for creating and listing vendors
    queryset = Vendor.objects.all()  # Specify the queryset that this view will operate on, which is all vendors in the database
    serializer_class = VendorSerializer # Define the serializer class that will be used to convert vendor objects to JSON data

class VendorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView): # Define a class-based view that allows for retrieving, updating, and deleting individual vendors
    queryset = Vendor.objects.all() # Specify the queryset that this view will operate on, which is all vendors in the database
    serializer_class = VendorSerializer # Define the serializer class that will be used to convert vendor objects to JSON data

# 2. Purchase Order Tracking:
    # This class is a ListCreateAPIView, which is a type of Django Rest Framework view that allows 
    # for both listing and creating objects in a single view.
class PurchaseOrderListCreateAPIView(generics.ListCreateAPIView):
    # This queryset specifies the objects that this view will operate on. 
    # In this case, it will operate on all PurchaseOrder objects.
    queryset = PurchaseOrder.objects.all()
    
    # This serializer_class specifies the serializer that will be used to convert 
    # PurchaseOrder objects to and from JSON data.
    serializer_class = PurchaseOrderSerializer

    # This class is a RetrieveUpdateDestroyAPIView, which is a type of Django Rest Framework view 
    # that allows for retrieving, updating, and deleting individual objects.
class PurchaseOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    # This queryset specifies the objects that this view will operate on. 
    # In this case, it will operate on all PurchaseOrder objects.
    queryset = PurchaseOrder.objects.all()
    
    # This serializer_class specifies the serializer that will be used to convert 
    # PurchaseOrder objects to and from JSON data.
    serializer_class = PurchaseOrderSerializer

# Vendor Performance Evaluation:/API Endpoint Implementation
class VendorPerformanceAPIView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all() # Define the queryset for this API view, which retrieves all Vendor objects
    serializer_class = VendorSerializer # Specify the serializer class to use for serializing Vendor objects

    def retrieve(self, request, *args, **kwargs): # Get the Vendor object instance from the queryset
        instance = self.get_object() # Create a dictionary to store the vendor performance metrics
        data = {
            "on_time_delivery_rate": instance.on_time_delivery_rate, # Calculate the on-time delivery rate for the vendor
            "quality_rating_avg ": instance.quality_rating_avg, # Calculate the average quality rating for the vendor
            "average_response_time": instance.average_response_time, # Calculate the average response time for the vendor
            "fulfillment_rate": instance.fulfillment_rate # Calculate the fulfillment rate for the vendor
        }
        # Return a Response object with the vendor performance metrics
        return Response(data)
    
# Backend Logic for Performance Metrics   
@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance(sender, instance, created, **kwargs):
    # This function is a signal receiver that listens for the post_save signal sent by the PurchaseOrder model.
    # It updates the vendor's performance metrics whenever a PurchaseOrder is saved or created.

    if created or instance.status_changed:  # Check if the PurchaseOrder is newly created or if its status has changed.
        vendor = instance.vendor # Get the vendor associated with the PurchaseOrder.
        # On-Time Delivery Rate Calculation
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed') # Get all completed PurchaseOrders for the vendor.
        on_time_deliveries = completed_pos.filter(delivery_date__lte=models.F('delivery_date')).count() # Count the number of PurchaseOrders that were delivered on or before the scheduled delivery date.
        total_completed_pos = completed_pos.count() # Get the total number of completed PurchaseOrders for the vendor.
        vendor.on_time_delivery_rate = (on_time_deliveries / total_completed_pos) * 100 if total_completed_pos > 0 else 0
        # Calculate the on-time delivery rate as a percentage. If there are no completed PurchaseOrders, set the rate to 0.

        # Quality Rating Average Calculation
        quality_ratings = completed_pos.exclude(quality_rating__isnull=True).aggregate(avg_quality=Avg('quality_rating'))
        # Get the average quality rating for all completed PurchaseOrders that have a quality rating.
        vendor.quality_rating_avg = quality_ratings['avg_quality'] if quality_ratings['avg_quality'] else 0
        # Set the vendor's average quality rating. If there are no quality ratings, set it to 0.

        # Average Response Time Calculation
        response_times = completed_pos.exclude(acknowledgment_date__isnull=True).aggregate(avg_response_time=Avg(models.F('acknowledgment_date') - models.F('issue_date')))
        # Calculate the average response time for all completed PurchaseOrders that have an acknowledgment date.
        vendor.average_response_time = response_times['avg_response_time'].total_seconds() if response_times['avg_response_time'] else 0
        # Set the vendor's average response time in seconds. If there are no response times, set it to 0.

        # Fulfilment Rate Calculation
        fulfilment_rate = completed_pos.filter(status='completed').count() / PurchaseOrder.objects.filter(vendor=vendor).count() * 100
        # Calculate the fulfilment rate as a percentage of completed PurchaseOrders out of all PurchaseOrders for the vendor.
        vendor.fulfilment_rate = fulfilment_rate if total_completed_pos > 0 else 0
        # Set the vendor's fulfilment rate. If there are no completed PurchaseOrders, set it to 0.

        vendor.save()
        # Save the updated vendor performance metrics.

# Update Acknowledgment Endpoint

class AcknowledgePurchaseOrderAPIView(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all() # Define the queryset for this API view, which includes all PurchaseOrder objects
    serializer_class = PurchaseOrderSerializer  # Specify the serializer class to use for this API view

    def perform_update(self, serializer):# Override the perform_update method to perform additional actions after updating a PurchaseOrder instance
        instance = serializer.save() # Save the updated PurchaseOrder instance using the serializer
        instance.vendor.update_average_response_time() # After updating the PurchaseOrder, update the average response time for the associated vendor
        