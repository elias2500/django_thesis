from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views import generic
from braces.views import SelectRelatedMixin
from . import models
from . import forms
from django.contrib.auth import get_user_model
from django.http import Http404
from django.contrib import messages

# Create your views here.

User = get_user_model()

class RoomList(SelectRelatedMixin,generic.ListView):
    model = models.Room
    select_related = ('user',)

class UserRooms(generic.ListView):
    model = models.Room
    template_name = "rooms/room_list.html"

    def get_queryset(self):
        try:
            self.room_user = User.objects.prefetch_related('rooms').get(
                username__iexact=self.kwargs.get('username')
                )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.room_user.rooms.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["room_user"] = self.room_user
        return context

class RoomDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Room
    select_related = ('user',)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )

class CreateRoom(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    fields = ('title','noOfPlayers','difficulty','hasActor','theme','scenario','riddles')
    model = models.Room

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class UpdateRoom(LoginRequiredMixin, generic.UpdateView):
    fields = ('title','noOfPlayers','difficulty','hasActor','theme','scenario','riddles')
    model = models.Room

class DeleteRoom(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Room
    select_related = ('user',)
    #success_url = reverse_lazy('home')

    def get_success_url(self):
        return reverse('rooms:roomlist', kwargs= {'username': self.request.user})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)