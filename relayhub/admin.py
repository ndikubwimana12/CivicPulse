from django.contrib import admin
from .models import Category, Department, Ticket, TicketResponse, UserProfile

# Register your models
admin.site.register(Category)
admin.site.register(Department)
admin.site.register(Ticket)
admin.site.register(TicketResponse)
admin.site.register(UserProfile)
