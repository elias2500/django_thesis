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
    model = Project
    form_class = ProjectForm
    template_name = 'rooms/project_form.html'
    #success_url = reverse_lazy('rooms:project_list username=')

    def get_success_url(self):
        return reverse('rooms:project_list', kwargs= {'username': self.request.user})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    #def get_context_data(self, **kwargs):
     #   context = super().get_context_data(**kwargs)
      #  context['riddle_form'] = RiddleForm()
       # return context

    #def form_valid(self, form):
        #project = form.save()
     #   project_id = self.kwargs.get('pk')
      #  project = Project.objects.get(id=project_id)
       # riddle_form = RiddleForm(self.request.POST)
        #if riddle_form.is_valid():
         #   riddle = riddle_form.save(commit=False)
          #  riddle.project = project
           # riddle.save()
        #return super().form_valid(form)

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

    #def form_valid(self, form):
        #project = form.save()
     #   project_id = self.kwargs.get('pk')
      #  project = Project.objects.get(id=project_id)
       # riddle_form = RiddleForm(self.request.POST)
        #if riddle_form.is_valid():
         #   riddle = riddle_form.save(commit=False)
          #  riddle.project = project
           # riddle.save()
        #return super().form_valid(form)

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

class RiddleAddView(CreateView):
    model = Riddle
    form_class = RiddleForm
    template_name = 'rooms/riddle_form.html'

    def form_valid(self, form):
        project = form.cleaned_data.get('project')
        project_title = project.title
        try:
            project = Project.objects.get(title=project_title)
        except Project.DoesNotExist:
            messages.error(self.request, "No project with the title '{}' was found.".format(project_title))
            return super().form_invalid(form)
        form.instance.project = project
        return super().form_valid(form)

    def get_success_url(self):
       return reverse_lazy('rooms:project_detail', kwargs={'username': self.object.project.user.username, 'pk': self.object.project.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['riddle_form'] = RiddleForm()
        #context['project_id'] = self.kwargs['project_id']
        return context