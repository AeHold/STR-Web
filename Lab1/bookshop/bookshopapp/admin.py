from django.contrib import admin
import bookshopapp.models as models

admin.site.register(models.Genre)
admin.site.register(models.Type)
admin.site.register(models.Profile)
admin.site.register(models.Order)
admin.site.register(models.Product)
admin.site.register(models.Post)
