from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Q
from django.contrib.auth.models import User
from .models import Ticket, Category,Department, TicketResponse
from .forms import TicketForm, TicketResponseForm,TicketStatusUpdateForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from datetime import datetime, timedelta
from django.contrib.auth import logout as auth_logout
from django.contrib.sessions.models import Session
from django.utils import timezone
from .forms import DepartmentForm, CategoryForm




# Home page view
def home(request):    
    return render(request, 'relayhub/home.html')

# Authentication views
def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'There was an error with your registration.')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    form = AuthenticationForm()
    return render(request, 'registration/login.html',{'form': form})


def logout_user(request):
    if request.user.is_authenticated:
        # Get the current user
        user = request.user
        
        # Delete all sessions for user
        all_sessions = Session.objects.filter(expire_date__gte=timezone.now())
        for session in all_sessions:
            session_data = session.get_decoded()
            if session_data.get('_auth_user_id') == str(user.id):
                session.delete()
        
        # Standard logout procedure
        auth_logout(request)
        
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')


# Dashboard view based on user role
@login_required
def dashboard(request):
    if request.user.is_superuser:
        recent_activity = []
        upcoming_events = []
        notifications = []
        
        context = {
            'recent_activity': recent_activity,
            'upcoming_events': upcoming_events,
            'notifications': notifications,
        }
        
        return render(request, 'relayhub/dashboard.html', context)
    
    else:
        from .models import Ticket
        recent_tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')[:5]
        
        announcements = [
            {
                'title': 'System Maintenance',
                'content': 'The system will be undergoing maintenance on Saturday from 2-4 AM.',
                'date': datetime.now() - timedelta(days=2)
            },
            {
                'title': 'New Features Added',
                'content': 'We\'ve added new features to help you track your requests more efficiently.',
                'date': datetime.now() - timedelta(days=5)
            }
        ]
        
        context = {
            'recent_tickets': recent_tickets,
            'announcements': announcements,
        }
        
        return render(request, 'relayhub/user_dashboard.html', context)


# Ticket management views
@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.citizen = request.user
            ticket.status = 'submitted'
            
            ticket.save()
            
            try:
                if ticket.category:
                    if hasattr(ticket.category, 'department'):
                        department = ticket.category.department
                        
                        department_staff = User.objects.filter(
                            profile__department=department,
                            is_staff=True
                        ).first()
                        
                        if department_staff:
                            ticket.assigned_to = department_staff
                            ticket.save()
                        else:
                            admin = User.objects.filter(is_superuser=True).first()
                            if admin:
                                ticket.assigned_to = admin
                                ticket.save()
                    else:
                        admin = User.objects.filter(is_superuser=True).first()
                        if admin:
                            ticket.assigned_to = admin
                            ticket.save()
            except Exception as e:
                print(f"Error assigning ticket: {e}")
            
            messages.success(request, 'Your complaint has been submitted successfully!')
            return redirect('my_tickets')
        else:
            messages.error(request, 'There was an error with your submission. Please check the form.')
    else:
        form = TicketForm()
    
    return render(request, 'relayhub/create_ticket.html', {'form': form})


def my_tickets(request):
    tickets = Ticket.objects.filter(citizen=request.user).order_by('-submitted_at')
    
    tickets = tickets.prefetch_related('responses')
    
    return render(request, 'relayhub/my_tickets.html', {
        'tickets': tickets,
    })


@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    if not (request.user == ticket.citizen or 
            request.user.is_superuser or 
            ticket.assigned_to == request.user or 
            (hasattr(request.user, 'profile') and 
             hasattr(ticket.category, 'department') and 
             request.user.profile.department == ticket.category.department)):
        messages.error(request, "You don't have permission to view this ticket.")
        return redirect('dashboard')
    
    responses = TicketResponse.objects.filter(ticket=ticket).order_by('-created_at')
    
    return render(request, 'relayhub/ticket_detail.html', {
        'ticket': ticket,
        'responses': responses
    })

@login_required
def view_progress_pathway(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, citizen=request.user)
    status_steps = [
        {'key': 'submitted', 'label': 'Submitted', 'active': True},
        {'key': 'in_progress', 'label': 'In Progress', 'active': ticket.status in ['in_progress', 'responded', 'resolved']},
        {'key': 'responded', 'label': 'Responded', 'active': ticket.status in ['responded', 'resolved']},
        {'key': 'resolved', 'label': 'Resolved', 'active': ticket.status == 'resolved'},
    ]
    
    return render(request, 'relayhub/ticket_timeline.html', {
        'ticket': ticket,
        'steps': status_steps,
    })

@login_required
def progress_info(request):
    tickets = Ticket.objects.filter(citizen=request.user).order_by('-submitted_at')
    return render(request, 'relayhub/progress_info.html', {'tickets': tickets})

# Staff/Admin views
def is_staff_user(user):
    return user.is_staff or user.is_superuser

@login_required
def dashboard(request):
    is_superuser = request.user.is_superuser
    is_staff = request.user.is_staff
    is_regular_user = not is_superuser and not is_staff
    
    context = {
        'is_superuser': is_superuser,
        'is_staff': is_staff,
        'is_regular_user': is_regular_user,
    }
    
    if is_regular_user:
        # For regular users (citizens), show their submitted tickets
        tickets = Ticket.objects.filter(citizen=request.user).order_by('-submitted_at')
        context.update({
            'tickets': tickets,
            'ticket_count': tickets.count()
        })
    elif is_staff and not is_superuser:
        # For department staff, show only tickets assigned to them or their department
        try:
            user_department = request.user.profile.department
            if user_department:
                # Get tickets for this user's department
                department_categories = Category.objects.filter(department=user_department)
                tickets = Ticket.objects.filter(
                    Q(assigned_to=request.user) | 
                    Q(category__in=department_categories)
                ).order_by('-submitted_at')
            else:
                # If user has no department, show only directly assigned tickets
                tickets = Ticket.objects.filter(assigned_to=request.user).order_by('-submitted_at')
        except:
            # Fallback if profile doesn't exist
            tickets = Ticket.objects.filter(assigned_to=request.user).order_by('-submitted_at')
            
        context.update({
            'tickets': tickets,
            'ticket_count': tickets.count()
        })
    elif is_superuser:
        # For admins, show all tickets with filtering options
        tickets = Ticket.objects.all().order_by('-submitted_at')
        departments = Department.objects.all()
        
        # Filter by department if requested
        department_id = request.GET.get('department')
        if department_id:
            department_categories = Category.objects.filter(department_id=department_id)
            tickets = tickets.filter(category__in=department_categories)
        
        context.update({
            'tickets': tickets,
            'ticket_count': tickets.count(),
            'departments': departments,
            'selected_department': department_id
        })
    
    return render(request, 'relayhub/dashboard.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff)
def respond_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # Check if the user has permission to respond to this ticket
    user_department = None
    try:
        user_department = request.user.profile.department
    except:
        pass
    
    # Only allow response if user is superuser, assigned to the ticket, or in the same department
    if not (request.user.is_superuser or 
            ticket.assigned_to == request.user or 
            (user_department and ticket.category and ticket.category.department == user_department)):
        messages.error(request, "You don't have permission to respond to this ticket.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        response_form = TicketResponseForm(request.POST)
        status_form = TicketStatusUpdateForm(request.POST, instance=ticket)
        
        if response_form.is_valid() and status_form.is_valid():
        # This line should be indented
            response = response_form.save(commit=False)
            response.ticket = ticket
            response.responder = request.user
            response.save()
    
        # Update ticket status
        status_form.save()
        
        messages.success(request, 'Response submitted successfully!')
        return redirect('assigned_tickets')

    else:
        response_form = TicketResponseForm()
        status_form = TicketStatusUpdateForm(instance=ticket)
    
    # Get previous responses
    previous_responses = TicketResponse.objects.filter(ticket=ticket).order_by('-created_at')
    
    return render(request, 'relayhub/respond_ticket.html', {
        'ticket': ticket,
        'response_form': response_form,
        'status_form': status_form,
        'previous_responses': previous_responses
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_insightboard(request):
    is_superuser = request.user.is_superuser
    
    if is_superuser:
        # Admins see insights for all departments
        tickets = Ticket.objects.all()
    else:
        # Department staff see insights only for their department
        try:
            user_department = request.user.profile.department
            if user_department:
                department_categories = Category.objects.filter(department=user_department)
                tickets = Ticket.objects.filter(category__in=department_categories)
            else:
                tickets = Ticket.objects.filter(assigned_to=request.user)
        except:
            tickets = Ticket.objects.filter(assigned_to=request.user)
    
    total_tickets = tickets.count()
    
    tickets_by_category = (
        tickets.values('category__name')
        .annotate(total=Count('id'))
        .order_by('-total')
    )
    
    tickets_by_status = (
        tickets.values('status')
        .annotate(total=Count('id'))
        .order_by('-total')
    )
    
    # For admins, show by department; for staff, show by assigned user
    if is_superuser:
        tickets_by_agency = (
            tickets.values('category__department__name')
            .annotate(total=Count('id'))
            .order_by('-total')
        )
    else:
        tickets_by_agency = (
            tickets.values('assigned_to__username')
            .annotate(total=Count('id'))
            .order_by('-total')
        )
    
    return render(request, 'relayhub/admin_insightboard.html', {
        'total_tickets': total_tickets,
        'tickets_by_category': tickets_by_category,
        'tickets_by_status': tickets_by_status,
        'tickets_by_agency': tickets_by_agency,
    })

def home(request):
    """
    Home page view - entry point for the application
    """
    # If user is already logged in, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    # Otherwise show the home page with links to register/login
    return render(request, 'relayhub/home.html')



@login_required
@user_passes_test(lambda u: u.is_staff)
def assigned_tickets(request):
    """View for staff users to see tickets assigned to them."""
    is_superuser = request.user.is_superuser
    
    if is_superuser:
        # Admins can see all tickets
        tickets = Ticket.objects.all().order_by('-submitted_at')
    else:
        # Department staff see only their assigned tickets
        tickets = Ticket.objects.filter(assigned_to=request.user).order_by('-submitted_at')
    
    # Filter by status if requested
    status = request.GET.get('status')
    if status:
        tickets = tickets.filter(status=status)
    
    return render(request, 'relayhub/assigned_tickets.html', {
        'tickets': tickets,
        'status_choices': Ticket.STATUS_CHOICES
    })


def is_staff_user(user):
    return user.is_staff


# Check if user is admin
def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_departments(request):
    departments = Department.objects.all()
    return render(request, 'relayhub/admin/departments.html', {'departments': departments})

@login_required
@user_passes_test(is_admin)
def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department added successfully.')
            return redirect('admin_departments')
    else:
        form = DepartmentForm()
    
    return render(request, 'relayhub/admin/department_form.html', {
        'form': form,
        'title': 'Add Department'
    })

@login_required
@user_passes_test(is_admin)
def edit_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department updated successfully.')
            return redirect('admin_departments')
    else:
        form = DepartmentForm(instance=department)
    
    return render(request, 'relayhub/admin/department_form.html', {
        'form': form,
        'title': 'Edit Department'
    })

@login_required
@user_passes_test(is_admin)
def delete_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    
    if request.method == 'POST':
        department.delete()
        messages.success(request, 'Department deleted successfully.')
        return redirect('admin_departments')
    
    return render(request, 'relayhub/admin/department_confirm_delete.html', {
        'department': department
    })

@login_required
@user_passes_test(is_admin)
def admin_categories(request):
    categories = Category.objects.all()
    return render(request, 'relayhub/admin/categories.html', {'categories': categories})

@login_required
@user_passes_test(is_admin)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully.')
            return redirect('admin_categories')
    else:
        form = CategoryForm()
    
    return render(request, 'relayhub/admin/category_form.html', {
        'form': form,
        'title': 'Add Category'
    })

@login_required
@user_passes_test(is_admin)
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('admin_categories')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'relayhub/admin/category_form.html', {
        'form': form,
        'title': 'Edit Category'
    })

@login_required
@user_passes_test(is_admin)
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect('admin_categories')
    
    return render(request, 'relayhub/admin/category_confirm_delete.html', {
        'category': category
    })


class AdminUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']

@login_required
def admin_users(request):
    """View to list and manage users"""
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard')
        
    search_query = request.GET.get('search', '')
    
    if search_query:
        users = User.objects.filter(
            Q(username__icontains=search_query) | 
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        ).order_by('username')
    else:
        users = User.objects.all().order_by('username')
    
    context = {
        'users': users,
        'search_query': search_query
    }
    return render(request, 'relayhub/admin_users.html', context)

@login_required
def admin_add_user(request):
    """View to add a new user"""
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = AdminUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.username} has been created successfully.')
            return redirect('admin_users')
    else:
        form = AdminUserForm()
    
    return render(request, 'relayhub/admin_add_user.html', {'form': form})

@login_required
def admin_edit_user(request, user_id):
    """View to edit an existing user"""
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard')
        
    user_obj = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        # Handle user editing without password change
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        is_staff = request.POST.get('is_staff') == 'on'
        is_active = request.POST.get('is_active') == 'on'
        
        # Update user fields
        user_obj.username = username
        user_obj.email = email
        user_obj.first_name = first_name
        user_obj.last_name = last_name
        user_obj.is_staff = is_staff
        user_obj.is_active = is_active
        user_obj.save()
        
        messages.success(request, f'User {user_obj.username} has been updated successfully.')
        return redirect('admin_users')
    
    context = {
        'user_obj': user_obj
    }
    return render(request, 'relayhub/admin_edit_user.html', context)

@login_required
def admin_delete_user(request, user_id):
    """View to delete a user"""
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard')
        
    user_obj = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        username = user_obj.username
        user_obj.delete()
        messages.success(request, f'User {username} has been deleted successfully.')
        return redirect('admin_users')
    
    context = {
        'user_obj': user_obj
    }
    return render(request, 'relayhub/admin_delete_user.html', context)
