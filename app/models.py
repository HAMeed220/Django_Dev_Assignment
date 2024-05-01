from django.db import models

# Create your models here.

# Data Models 1. Vendor Model
class Vendor(models.Model):
    name = models.CharField(max_length=100) # The vendor's name, limited to 100 characters
    contact_details = models.TextField() # A text field to store the vendor's contact details, such as phone number, fax, etc.
    email = models.EmailField() # The vendor's email address
    address = models.TextField() # The vendor's physical address
    vendor_code = models.CharField(max_length=50, unique=True) # A unique code assigned to each vendor, used for identification purposes
    on_time_delivery_rate = models.FloatField(default=0) # The vendor's on-time delivery rate, a float value between 0 and 1
    quality_rating_avg = models.FloatField(default=0) # The average quality rating given to the vendor by customers, a float value between 0 and 1
    average_response_time = models.FloatField(default=0)  # The average time taken by the vendor to respond to customer inquiries, in minutes or hours
    fulfillment_rate = models.FloatField(default=0) # The percentage of orders fulfilled by the vendor, a float value between 0 and 1
    
    # Returns a string representation of the vendor, which is the vendor's name
    def __str__(self):
        return self.name

# Data Models 2. Purchase Order (PO) Model
class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100, unique=True) # Unique identifier for the purchase order
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE) # Foreign key referencing the vendor who the purchase order is with
    order_date = models.DateTimeField() # Date and time the purchase order was created
    delivery_date = models.DateTimeField(null=True, blank=True) # Date and time the items are expected to be delivered (optional)
    items = models.JSONField() # JSON field to store a list of items in the purchase order
    quantity = models.IntegerField() # Total quantity of items in the purchase order
    status = models.CharField(max_length=50) # Status of the purchase order (e.g. "pending", "shipped", "delivered", etc.)
    quality_rating = models.FloatField(null=True, blank=True) # Quality rating of the purchase order (optional)
    issue_date = models.DateTimeField()# Date and time the purchase order was issued
    acknowledgment_date = models.DateTimeField(null=True, blank=True) # Date and time the purchase order was acknowledged (optional)

    # Returns a string representation of the purchase order, which is the PO number
    def __str__(self):
        return self.po_number


#  Data Models 3. Historical Performance Model

class HistoricalPerformance(models.Model):
   # Define a foreign key field to establish a relationship with the Vendor model
   # This field will store the ID of the associated vendor
   # The on_delete=models.CASCADE parameter specifies that if the associated vendor is deleted, 
   # this object will also be deleted to maintain data integrity
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)

    # Define a date and time field to store the date of the record
    # This field will store a datetime object, which can be used to track when the record was created or updated
    date = models.DateTimeField()
    
    on_time_delivery_rate = models.FloatField() # The vendor's on-time delivery rate, a float value between 0 and 1
    quality_rating_avg = models.FloatField() # The average quality rating given to the vendor by customers, a float value between 0 and 1
    average_response_time = models.FloatField() # The average time taken by the vendor to respond to customer inquiries, in minutes or hours
    fulfillment_rate = models.FloatField() # The percentage of orders fulfilled by the vendor, a float value between 0 and 1

    def __str__(self):
        return f"{self.vendor} - {self.date}"
