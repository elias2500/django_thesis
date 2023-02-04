from django.urls import path
from .views import ProjectListView, ProjectDetailView, ProjectCreateView, ProjectUpdateView, ProjectDeleteView, RiddleAddView

app_name = 'rooms'

urlpatterns = [
    path('projects/madeby/<slug:username>', ProjectListView.as_view(), name='project_list'),
    path('projects/<slug:username>/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('projects/create/', ProjectCreateView.as_view(), name='project_create'),
    path('projects/update/<int:pk>', ProjectUpdateView.as_view(), name='project_update'),
    path('projects/delete/<int:pk>/', ProjectDeleteView.as_view(), name='project_delete'),
    path('projects/addriddle/', RiddleAddView.as_view(), name='riddle_add'),
]
