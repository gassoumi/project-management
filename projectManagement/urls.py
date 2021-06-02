from rest_framework import routers
from .api import ProjectViewSet, SprintViewSet, TaskViewSet, \
    ActiveSprintList, DocumentViewSet, CommentViewSet, DiscussionViewSet, \
    NoteViewSet, TopDiscussionList, ProblemViewSet, TaskCacheViewSet, UserTaskList
from django.urls import path, include

# https://www.django-rest-framework.org/api-guide/routers/
router = routers.DefaultRouter()
router.register('projects', ProjectViewSet, 'projects')
router.register('sprints', SprintViewSet, 'sprints')
router.register('tasks', TaskViewSet, 'tasks')
#router.register('documents', DocumentViewSet, 'documents')
router.register('discussions', DiscussionViewSet, 'discussions')
router.register('comments', CommentViewSet, 'comments')
router.register('notes', NoteViewSet, 'notes')
router.register('problems', ProblemViewSet, 'problems')

urlpatterns = [
    path('activeSprints/', ActiveSprintList.as_view()),
    path('topDiscussion/', TopDiscussionList.as_view()),
    path('userTasks/', UserTaskList.as_view()),
    # path('cacheTask/', TaskCacheViewSet.as_view({'get': 'list'})),
]

urlpatterns += router.urls
