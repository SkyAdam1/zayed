from .models import Application, ApplicationRemark


def notifications(request):
    rems = 0
    if request.user.is_authenticated:
        apps = Application.objects.filter(user=request.user)
        for app in apps:
            rems += len(
                ApplicationRemark.objects.filter(application__app=app.id, status=False)
            )
    return {"notifications_len": rems}
