# example/urls.py
from django.urls import path

from example.views import index
from example.views import save_audio
from example.views import admin


urlpatterns = [
    path('save_transcription/', save_audio, name='save_audio1'),
    path('', index, name='save_audio2'),
    path('admin_lydec', admin, name='admin_lydec'),
]