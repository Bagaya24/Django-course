from django.urls import path
from . import views

urlpatterns = [
    path('blogpost/', views.BlogPostList.as_view(), name='blogpost-create-view'),
    path('blogpost/<int:pk>/', views.BlogPostRetrieveUpdateDestroy.as_view(), name='blogpost-detail-view'),
    path("", views.BlogPostList.as_view(), name='blogpost-list-view')
]