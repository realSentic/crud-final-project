from .models import Admins

def admin_context(request):
    admin = None
    if request.session.get('admin_id'):
        try:
            admin = Admins.objects.get(admin_id=request.session['admin_id'])
        except Admins.DoesNotExist:
            pass
    return {'admin': admin}