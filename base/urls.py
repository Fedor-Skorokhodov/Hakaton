from django.urls import path
from rest_framework.authtoken import views as views_token
from . import views


urlpatterns = [
    path('auth_get_token', views_token.obtain_auth_token),

    path('get_question/<int:key>', views.get_question),
    path('get_meeting/<int:key>', views.get_meeting),
    path('user/get_meetings', views.get_user_meetings),  # return meetings in which user takes place
    path('user/get_questions', views.get_user_questions),  # return questions in which user can vote
    path('meeting/<int:key>/get_questions', views.get_meeting_questions),
    path('question/<int:key>/get_votes', views.get_question_votes),
    path('get_topics/', views.get_topics),

    path('vote/<int:question_key>', views.make_vote),
    path('ready/<int:key>', views.set_ready),
    path('finish/<int:key>', views.set_finished),

    path('create_meeting', views.create_meeting),
    path('create_material', views.create_material),
    path('create_question', views.create_question),
]
