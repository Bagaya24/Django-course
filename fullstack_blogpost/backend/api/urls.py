from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('users/register/', views.UserCreateView.as_view(), name='user-create'),
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('notes/', views.NoteListCreateView.as_view(), name='note-list-create'),
    path('notes/delete/<uuid:pk>/', views.NoteDestroyView.as_view(), name='delete-note'),
]