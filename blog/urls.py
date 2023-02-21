from . import views
from django.urls import path

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('detail/<str:id>', views.detail_post, name='detail_post'),
    path('post-by-category/<str:category_id>',
         views.get_post_by_category,
         name='get_post_by_category'),
    path('categories', views.categories, name='categories'),
    path('create-category', views.create_category, name='create_category'),
    path('edit-post/<str:id>', views.edit_post, name='edit_post'),
    path('create-post', views.create_post, name='create_post'),
]