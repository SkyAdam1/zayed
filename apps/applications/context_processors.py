from .models import Application, ApplicationRemark, ApplicationReport


def notifications(request):
    rems = []
    apps = Application.objects.filter(user=request.user)
    for app in apps:
        rems = ApplicationRemark.objects.filter(application__app=app.id)
    return {'notifications_len': len(rems)}
