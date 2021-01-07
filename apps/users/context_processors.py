from .models import CustomUser


def experts(request):
    experts = len(CustomUser.objects.filter(is_expert=True, is_active=False))
    return {"experts_len": experts}
