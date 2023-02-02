from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Project, Riddle

class ProjectCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        title = request.POST['title']
        project = Project.objects.create(title=title, user=request.user)
        return redirect('project_detail', project_id=project.id)

    def get(self, request, *args, **kwargs):
        return render(request, 'project_form.html')

class ProjectDetailView(LoginRequiredMixin, View):
    def get(self, request, project_id, *args, **kwargs):
        project = Project.objects.get(id=project_id)
        riddles = Riddle.objects.filter(project=project)
        return render(request, 'project_detail.html', {'project': project, 'riddles': riddles})

class ProjectUpdateView(LoginRequiredMixin, View):
    def post(self, request, project_id, *args, **kwargs):
        project = Project.objects.get(id=project_id)
        project.title = request.POST['title']
        project.max_players = request.POST['max_players']
        project.has_actor = request.POST['has_actor']
        project.scenario = request.POST['scenario']
        project.number_of_riddles = request.POST['number_of_riddles']
        project.save()
        return redirect('project_detail', project_id=project.id)

    def get(self, request, project_id, *args, **kwargs):
        project = Project.objects.get(id=project_id)
        return render(request, 'project_form.html', {'project': project})

class ProjectDeleteView(LoginRequiredMixin, View):
    def post(self, request, project_id, *args, **kwargs):
        project = Project.objects.get(id=project_id)
        project.delete()
        return redirect('project_list')

class ProjectListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        projects = Project.objects.filter(user=request.user)
        return render(request, 'project_list.html', {'projects': projects})
