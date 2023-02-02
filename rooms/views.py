from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View, generic
from django.views.generic import CreateView, DetailView, UpdateView
from .models import Project, Riddle
from .forms import ProjectForm, RiddleForm
from django.contrib.auth import get_user_model
from django.http import Http404
from braces.views import SelectRelatedMixin
from django.contrib import messages

User = get_user_model()

class ProjectCreateView(CreateView):
    form_class = ProjectForm
    template_name = 'rooms/project_form.html'
    #success_url = reverse_lazy('rooms:project_list username=')

    def get_success_url(self):
        return reverse('rooms:project_list', kwargs= {'username': self.request.user})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['riddle_form'] = RiddleForm()
        return context

    def form_valid(self, form):
        #project = form.save()
        riddle_form = RiddleForm(self.request.POST)
        if riddle_form.is_valid():
            riddle = riddle_form.save(commit=False)
            riddle.project = project
            riddle.save()
        return super().form_valid(form)

class ProjectDetailView(DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs.get('pk')
        project = Project.objects.get(id=project_id)
        context['project'] = project
        return context


class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'rooms/project_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['riddle_form'] = RiddleForm()
        return context

    def form_valid(self, form):
        #project = form.save()
        riddle_form = RiddleForm(self.request.POST)
        if riddle_form.is_valid():
            riddle = riddle_form.save(commit=False)
            riddle.project = project
            riddle.save()
        return super().form_valid(form)

    #def form_valid(self, form):
     #   form.save()
      #  return redirect('rooms:project_list')

class ProjectListView(generic.ListView):
    model = Project
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


class ProjectDeleteView(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = Project
    select_related = ('user',)
    #success_url = reverse_lazy('home')

    def get_success_url(self):
        return reverse('rooms:project_list', kwargs= {'username': self.request.user})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)


#class ProjectDeleteView(LoginRequiredMixin, View):
 #   def post(self, request, project_id, *args, **kwargs):
  #      project = Project.objects.get(id=project_id)
   #     project.delete()
    #    return redirect('project_list')