from django.core.mail import send_mail, EmailMessage
from django.db.models.signals import post_save
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
