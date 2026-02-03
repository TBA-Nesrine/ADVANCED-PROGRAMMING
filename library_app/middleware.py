from django.shortcuts import redirect
from django.urls import reverse

class RoleBasedRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process request BEFORE view is called
        response = self.get_response(request)
        
        # Check if user is authenticated and just logged in
        if request.user.is_authenticated:
            current_path = request.path
            
            # Check if we're on a login redirect page
            login_redirect_paths = [
                '/',  # LOGIN_REDIRECT_URL
                '/user/home/',  # Default redirect
                '/oauth/complete/google-oauth2/',  # Google callback
                '/accounts/google/login/callback/',  # Allauth Google callback
            ]
            
            # Check if current path is a login redirect path
            if current_path in login_redirect_paths:
                # Check user role
                if request.user.is_staff or request.user.is_superuser:
                    # Don't redirect if already going to admin page
                    if not current_path.startswith('/dashboard/'):
                        return redirect('admin_home')
                else:
                    # Don't redirect if already going to user page
                    if not current_path.startswith('/user/'):
                        return redirect('user_home')
        
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        """Alternative approach - intercept before view is called"""
        if request.user.is_authenticated:
            # Check specific paths that indicate login completion
            if request.path == '/' or request.path == '/user/home/':
                if request.user.is_staff or request.user.is_superuser:
                    return redirect('admin_home')
        
        return None