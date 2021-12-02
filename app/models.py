from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db.models import Q

# Create your models here.

class Product_with_quantity(models.Model):
    product_id=models.IntegerField()
    quantity=models.IntegerField()

class Product (models.Model):
    product_name=models.CharField(max_length=255)
    price=models.IntegerField()
    supermarket=models.CharField(max_length=255)
    image_name=models.CharField(max_length=255)

    class Meta:
        db_table = "product"

    def __str__(self):
        return (self.product_name + " " + str(self.price) + " " + self.supermarket+ " "+ self.image_name)


    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Product.objects.filter(
            Q(product_name__icontains=query) 
        )
        return object_list


class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    cart=models.ManyToManyField(Product_with_quantity)

    class Meta:
        db_table = "profile"

    def __str__(self):
        return self.user.username

    def get_cart(self):
        return list(self.cart.all())

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()