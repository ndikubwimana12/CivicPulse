from django import forms
from .models import Submission,Ticket,Ticket,Department, Category


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['category', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }


from django import forms
from .models import Ticket, TicketResponse

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['subject', 'description', 'category']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief subject of your complaint'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe your issue in detail'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

class TicketResponseForm(forms.ModelForm):
    class Meta:
        model = TicketResponse
        fields = ['response_note']
        widgets = {
            'response_note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter your response here...',
                'style': 'width: 100%;'
            })
        }


class TicketStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width: 100%;'
            })
        }



class UserCreationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    
    



class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'department']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
        }


