from django.shortcuts import redirect

class RoleBasedAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        print("🚨 Middleware executed for:", request.path)  # Debug line
        
        user = request.user
        path = request.path
        if not user.is_authenticated:
            print("🚨 not authenticated")  # Debug line
            # Allow access to login and register pages
            print(path)
            if path != '/':
                if not path.startswith('/auth') and not path.startswith('/admin'):
                    return redirect('home')

        else:
            # Example: block access based on role
            print("🚨 not authenticated") # debug line
            if path.startswith('/produits') and user.role != 'AGRI':
                return redirect('home')
            if path.startswith('/agriculteur_dashboard') and user.role != 'ACHETEUR':
                return redirect('home')

        return self.get_response(request)
