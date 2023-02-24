from . import views
from django.urls import path

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('signin/', views.signin, name='signin'),
    path('profile/<int:id>', views.userprofile, name='profile'),
    path('editprofile/<int:id>', views.editprofile, name='editprofile'),
    path('detail/<str:id>', views.detail_post, name='detail_post'),
    path('post-by-category/<str:category_id>',
         views.get_post_by_category,
         name='get_post_by_category'),
    path('delete-post/<int:id>', views.delete_post, name='delete_post'),
    path('delete-category/<int:id>',
         views.delete_category,
         name="delete_category"),
    path('delete-comment/<int:id>',
         views.delete_comment,
         name='delete_comment'),
    path('categories', views.categories, name='categories'),
    path('create-category', views.create_category, name='create_category'),
    path('edit-post/<str:id>', views.edit_post, name='edit_post'),
    path('create-post', views.create_post, name='create_post'),
]