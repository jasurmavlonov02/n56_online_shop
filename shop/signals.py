import os
import json
from config.settings import BASE_DIR
from django.core.mail import send_mail, EmailMessage
from django.db.models.signals import post_save, pre_delete
from shop.models import Product
from django.dispatch import receiver

from user.models import User


# def product_saved(sender, instance, created=False, *args, **kwargs):
#     if created:
#         print(f'{instance.name} successfully saved')
#
#
# post_save.connect(product_saved, sender=Product)


# def product_saved(sender, instance, created=False, *args, **kwargs):
#     if created:
#         print(f'{instance.name} successfully saved')
#
#
# post_save.connect(product_saved, sender=Product)

@receiver(post_save, sender=Product)
def product_saved(sender, instance, created, **kwargs):
    if created:
        users = User.objects.all()
        email_of_users = [user.email for user in users]
        email = EmailMessage(
            f'Product saved',
            f'{instance.name.title()} successfully saved',
            to=email_of_users
        )
        email.send()
        print('Email sent')


@receiver(pre_delete, sender=Product)
def product_saved_before_delete(sender, instance, **kwargs):
    product_data = {
        instance.id: {
            'id': instance.id,
            'name': instance.name,
            'description': instance.description,
            'image': str(instance.image.url),
            'price': float(instance.price),
            'discount': instance.discount,
            'quantity': instance.quantity,
            'category': instance.category,
            'rating': instance.rating,
            'created_at': str(instance.created_at),
            'updated_at': str(instance.updated_at)
        }
    }
    file_path = os.path.join(BASE_DIR, 'product_data', f'product_{instance.id}_data.json')
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(product_data, f, indent=3)

    print('Product data saved')
