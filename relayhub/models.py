from django.db import models
from django.contrib.auth.models import User

class OrgUnit(models.Model):
    label = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.label

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='categories')
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    is_department_admin = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}'s profile"

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('in_progress', 'In Progress'),
        ('responded', 'Responded'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    citizen = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    subject = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    
    def __str__(self):
        return f"{self.subject} - {self.get_status_display()}"

class TicketResponse(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='responses')
    responder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ticket_responses')
    response_note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Response to {self.ticket.subject} by {self.responder.username}"

class Submission(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Review'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    ]
    category = models.CharField(max_length=100)
    description = models.TextField()
    citizen = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(OrgUnit, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    response_note = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"#{self.id} - {self.category}"

