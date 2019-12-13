from django.urls import path

from . import views

app_name = 'puppies'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/v1/puppies/<int:pk>', views.get_delete_update_puppy, name='get_delete_update_puppy'),
    path('api/v1/puppies/', views.get_post_puppies, name='get_post_puppies'),

    path('add/', views.add, name='add_post_puppies'),
    # path('add/', views.Puppy.as_view(), name='add_post_puppies'),

    # path('about_us/', views.about, name='about_us'),
    # # path('', views.IndexView.as_view(), name='index'),
    # path('<int:pk>', views.DeatailView.as_view(), name='detail'),
    # path('<int:question_id>/vote', views.vote, name='vote'),
    # path('<int:pk>/result', views.ResultView.as_view(), name='result'),
]
