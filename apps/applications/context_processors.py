from .models import Application, ApplicationRemark


def notifications(request):
    rems = []
    if request.user.is_authenticated:
        apps = Application.objects.filter(user=request.user)
        for app in apps:
            rems = ApplicationRemark.objects.filter(application__app=app.id)
    return {'notifications_len': len(rems)}
