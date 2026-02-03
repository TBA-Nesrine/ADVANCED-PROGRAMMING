from django.contrib.auth.models import User

def set_admin_permissions(strategy, details, user=None, *args, **kwargs):
    """Set admin permissions if user email matches admin emails."""
    if user:
        email = user.email
        
        # List of admin emails
        admin_emails = [
            'your_admin_email@gmail.com',  # Add your admin email here
            'admin@example.com',
        ]
        
        # Also check existing admin users
        existing_admin = User.objects.filter(
            email=email, 
            is_staff=True
        ).first()
        
        if email in admin_emails or existing_admin:
            user.is_staff = True
            user.is_superuser = True
            user.save()
            print(f"DEBUG: Set admin permissions for {user.email}")
    
    return {'user': user}