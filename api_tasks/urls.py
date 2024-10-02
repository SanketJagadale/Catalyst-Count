from django.urls import path
from .views import FileUploadView, QueryBuilderView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file_upload'),
    path('query_builder/', QueryBuilderView.as_view(), name='get_count_match_filter'),
]