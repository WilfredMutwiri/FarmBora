from django.db import models
from django.contrib.auth.models import AbstractUser
from shared.basemodel import BaseModel
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username

class FarmerProfile(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='farmer_profile')
    farm_name = models.CharField(max_length=255)
    farm_location = models.CharField(max_length=255)
    farm_size = models.DecimalField(max_digits=10, decimal_places=2)
    farm_image=models.URLField(blank=True,null=True)
    farm_description=models.TextField(blank=True,null=True)
    is_farmer = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.farm_name} - {self.user.username}"

class BuyerProfile(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='buyer_profile')
    company_name = models.CharField(max_length=255)
    company_address = models.CharField(max_length=255)
    company_description = models.TextField(blank=True, null=True)
    company_image=models.URLField(blank=True,null=True)
    is_buyer = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.company_name} - {self.user.username}"

class ProductListing(BaseModel):
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name='product_listings')
    product_name = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    product_image=models.URLField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product_name} by {self.farmer.user.username}"