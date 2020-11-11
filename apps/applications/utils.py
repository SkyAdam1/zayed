from django.shortcuts import render, get_object_or_404


class ObjectDetailMixin:
    model = None
    template_name = None

    def get(self, request, id):
        obj = get_object_or_404(self.model, id=id)
        return render(request, self.template_name, context={self.model.__name__.lower(): obj})
