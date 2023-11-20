from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('', home_view, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('upload/', upload_file, name='upload_file'),
    path('anomaly_detection/', anomaly, name='anomaly'),
    path('get_threat_solution/', get_threat_solution, name='nlp'),
    path('llama/', llama, name='llama'),
    path('other_models', other_models, name='other_models'),
    
]