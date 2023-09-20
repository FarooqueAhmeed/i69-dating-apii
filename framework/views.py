from user.models import User
from django.contrib import admin
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import reverse_lazy
from user.models import ChatsQue
from django.http import JsonResponse
from .forms import CustomPasswordChangeForm, CustomPasswordResetForm


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = "admin/password_reset.html"
    success_url = reverse_lazy("custom_password_reset_done")

    email_template_name = "registration/password_reset_email.html"
    html_email_template_name = "registration/password_reset_email.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "registration/password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy("custom_password_reset_complete")


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "registration/password_reset_complete.html"


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "registration/password_change_form.html"
    title = "Change Password Custom"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(admin.site.each_context(self.request))
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        try:
            form.save()
        except ValueError as e:
            form.add_error(None, e.message)
            return self.form_invalid(form)
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


def users_in_queue(request):
    queues = ChatsQue.objects.all()
    data = []
    for queue in queues:
        context = {
            "roomid": queue.room_id,
            "moderator": {
                "id": queue.moderator.id,
                "display_name": queue.moderator.username,
                "full_name": queue.moderator.fullName,
                "email": queue.moderator.email,
                "city": queue.moderator.city,
                "age": queue.moderator.age.age,
                "joined": queue.moderator.created_at
            }
        }
        data.append(context)

    return JsonResponse(data, safe=False)


def fake_users_in_queue(request, id):
    queues = ChatsQue.objects.all()
    worker = User.objects.get(id=id)
    data = []
    for queue in queues:
        if queue.isAssigned == True:
            if queue.worker == worker:
                context = {
                    "roomid": queue.room_id,
                    "fake_user": {
                        "id": queue.moderator.id,
                        "display_name": queue.moderator.username,
                        "full_name": queue.moderator.fullName,
                        "email": queue.moderator.email,
                        "city": queue.moderator.city,
                        "age": queue.moderator.age.age,
                        "joined": queue.moderator.created_at
                    }
                }
                data.append(context)

    return JsonResponse(data, safe=False)
