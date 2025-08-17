from django.urls import path
from .views import upvote_view, downvote_view, delete_tip_view
urlpatterns = [
    path('<int:pk>/upvote/', upvote_view, name='upvote_view'),
    path('<int:pk>/downvote/', downvote_view, name='downvote_view'),
    path('<int:pk>/delete/', delete_tip_view, name='delete_tip_view'),
]