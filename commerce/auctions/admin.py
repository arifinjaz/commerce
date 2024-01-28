from django.contrib import admin
from .models import listing,category,User, bids, winner
# Register your models here.

admin.site.register(listing)
admin.site.register(category)
admin.site.register(User)
admin.site.register(bids)
admin.site.register(winner)


